"""把"文字版"笔记转成语音（mp3/wav）。

流程：
  1. 找出所有 *文字版*.md
  2. 用 Qwen 语言模型把笔记（含公式）改写成"口语讲解稿"
  3. 用 Qwen 语音模型把讲解稿合成为音频，存在同目录下
  4. 只处理内容改动过的文件；没改的直接跳过（本地缓存）

配置见 scripts/audio_config.json（从 audio_config.example.json 复制而来）。
依赖：requests（仓库 .venv 已自带）；可选 lameenc（装了就压成更小的 mp3）。
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import time
import wave
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CONFIG_PATH = SCRIPTS / "audio_config.json"
EXAMPLE_PATH = SCRIPTS / "audio_config.example.json"
CACHE_DIR = SCRIPTS / ".audio_cache"
MANIFEST_PATH = CACHE_DIR / "manifest.json"

SUBJECT_DIRS = (
    "数量", "经济学", "财务", "公金", "权益",
    "固收", "衍生品", "另类", "组合", "错题",
)

LLM_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
TTS_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

# 改了下面这个默认指令就把版本号 +1，强制全部重新生成
PROMPT_VERSION = "1"
CHUNK_CHARS = 350  # 每段送去合成的最大字数，避免超出单次长度限制

DEFAULT_REWRITE_PROMPT = (
    "你是一位 CFA 二级中文讲师，正在把书面学习笔记改写成可以用耳朵听的讲解稿。要求：\n"
    "1. 把所有公式、希腊字母、上下标、分数以及 LaTeX 写法（如 \\frac、R^2、b0/(1-b1)、"
    "SSE/(n-k-1) 等）翻译成自然的中文口语：先说它是什么、怎么算，必要时点一句含义或用途；"
    "绝对不要读出反斜杠、美元符号、下划线、尖括号等符号。\n"
    "2. 完整保留原意和全部知识点，不遗漏、不编造。\n"
    "3. 输出像老师讲课一样连贯的口语，可以用「首先」「接下来」「注意」这类衔接词，"
    "但不要任何 Markdown 标记（井号、星号、列表符号、表格等）。\n"
    "4. 合理断句，方便朗读。\n"
    "只输出讲解稿正文，不要前言和结尾客套。"
)


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print("找不到配置文件：", CONFIG_PATH)
        print(f"请先复制 {EXAMPLE_PATH.name} 为 {CONFIG_PATH.name}，并填入你的 API Key。")
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    api_key = (cfg.get("api_key") or "").strip()
    if not api_key or "填" in api_key:
        print("请在 scripts/audio_config.json 里填入有效的 api_key（DashScope / 阿里云百炼）。")
        sys.exit(1)
    cfg["api_key"] = api_key
    cfg.setdefault("rewrite_model", "qwen-plus")
    cfg.setdefault("tts_model", "qwen-tts")
    cfg.setdefault("tts_voice", "Cherry")
    if not (cfg.get("rewrite_prompt") or "").strip():
        cfg["rewrite_prompt"] = DEFAULT_REWRITE_PROMPT
    return cfg


def find_text_notes() -> list[Path]:
    notes: list[Path] = []
    for sub in SUBJECT_DIRS:
        d = ROOT / sub
        if d.exists():
            notes.extend(sorted(d.glob("*文字版*.md")))
    return notes


def content_hash(text: str, cfg: dict) -> str:
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    for key in ("rewrite_model", "tts_model", "tts_voice", "rewrite_prompt"):
        h.update(str(cfg.get(key)).encode("utf-8"))
    h.update(PROMPT_VERSION.encode("utf-8"))
    return h.hexdigest()


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _post(url: str, headers: dict, payload: dict, timeout: int = 180, retries: int = 2):
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return requests.post(url, headers=headers, json=payload, timeout=timeout)
        except requests.RequestException as exc:  # 网络抖动重试
            last_exc = exc
            time.sleep(1.5 * (attempt + 1))
    raise last_exc


def _get_bytes(url: str, timeout: int = 180, retries: int = 2) -> bytes:
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return requests.get(url, timeout=timeout).content
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(1.5 * (attempt + 1))
    raise last_exc


def rewrite_to_script(text: str, cfg: dict) -> str:
    headers = {"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"}
    payload = {
        "model": cfg["rewrite_model"],
        "messages": [
            {"role": "system", "content": cfg["rewrite_prompt"]},
            {"role": "user", "content": text},
        ],
        "temperature": 0.3,
    }
    resp = _post(LLM_URL, headers, payload)
    if resp.status_code != 200:
        raise RuntimeError(f"公式改写失败 HTTP {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise RuntimeError(f"改写返回看不懂：{json.dumps(data, ensure_ascii=False)[:500]}")


def split_text(text: str, limit: int = CHUNK_CHARS) -> list[str]:
    parts = re.split(r"(?<=[。！？；\n])", text)
    chunks: list[str] = []
    cur = ""
    for seg in parts:
        if not seg:
            continue
        if cur and len(cur) + len(seg) > limit:
            chunks.append(cur)
            cur = seg
        else:
            cur += seg
    if cur.strip():
        chunks.append(cur)
    # 兜底：极长无标点段落硬切
    result: list[str] = []
    for chunk in chunks:
        while len(chunk) > limit:
            result.append(chunk[:limit])
            chunk = chunk[limit:]
        if chunk.strip():
            result.append(chunk)
    return result


def tts_one(text: str, cfg: dict) -> bytes:
    """合成一段文字，返回音频字节。自动尝试两种请求格式以兼容不同接口版本。"""
    headers = {"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"}
    bodies = [
        {"model": cfg["tts_model"], "input": {"text": text, "voice": cfg["tts_voice"]}},
        {
            "model": cfg["tts_model"],
            "input": {"messages": [{"role": "user", "content": [{"text": text}]}]},
            "parameters": {"voice": cfg["tts_voice"]},
        },
    ]
    last_err = "未知错误"
    for body in bodies:
        resp = _post(TTS_URL, headers, body)
        if resp.status_code != 200:
            last_err = f"HTTP {resp.status_code}: {resp.text[:300]}"
            continue
        data = resp.json()
        try:
            url = data["output"]["audio"]["url"]
        except (KeyError, TypeError):
            last_err = f"返回里找不到音频地址：{json.dumps(data, ensure_ascii=False)[:300]}"
            continue
        return _get_bytes(url)
    raise RuntimeError(f"语音合成失败，请把这段信息发我以便修正：\n      {last_err}")


def _is_wav(data: bytes) -> bool:
    return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WAVE"


def concat_wav(parts: list[bytes]) -> bytes:
    if len(parts) == 1:
        return parts[0]
    out = io.BytesIO()
    writer = None
    for part in parts:
        with wave.open(io.BytesIO(part), "rb") as reader:
            params = reader.getparams()
            frames = reader.readframes(reader.getnframes())
        if writer is None:
            writer = wave.open(out, "wb")
            writer.setparams(params)
        writer.writeframes(frames)
    if writer is not None:
        writer.close()
    return out.getvalue()


def combine_audio(parts: list[bytes]) -> tuple[bytes, str]:
    if all(_is_wav(p) for p in parts):
        return concat_wav(parts), "wav"
    return b"".join(parts), "mp3"  # 非 wav（如 mp3）直接字节拼接


def maybe_to_mp3(wav_bytes: bytes) -> tuple[bytes, str]:
    """装了 lameenc 就把 wav 压成更小的 mp3，否则原样返回 wav。"""
    try:
        import lameenc
    except ImportError:
        return wav_bytes, "wav"
    with wave.open(io.BytesIO(wav_bytes), "rb") as reader:
        channels = reader.getnchannels()
        rate = reader.getframerate()
        pcm = reader.readframes(reader.getnframes())
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(64)
    encoder.set_in_sample_rate(rate)
    encoder.set_channels(channels)
    encoder.set_quality(2)
    mp3 = encoder.encode(pcm) + encoder.flush()
    return bytes(mp3), "mp3"


def process(note: Path, cfg: dict, manifest: dict) -> bool:
    rel = note.relative_to(ROOT).as_posix()
    text = note.read_text(encoding="utf-8").strip()
    if not text:
        print(f"  跳过（空文件）：{rel}")
        return False

    digest = content_hash(text, cfg)
    stub = note.with_suffix("")  # 去掉 .md
    out_mp3 = Path(f"{stub}.mp3")
    out_wav = Path(f"{stub}.wav")
    has_audio = out_mp3.exists() or out_wav.exists()
    if manifest.get(rel, {}).get("hash") == digest and has_audio:
        print(f"  未改动，跳过：{rel}")
        return False

    print(f"  生成中：{rel}")
    script = rewrite_to_script(text, cfg)
    CACHE_DIR.mkdir(exist_ok=True)
    (CACHE_DIR / (rel.replace("/", "__") + ".口语稿.txt")).write_text(script, encoding="utf-8")

    chunks = split_text(script)
    print(f"    讲解稿 {len(script)} 字，切成 {len(chunks)} 段合成…")
    audio_parts = []
    for i, chunk in enumerate(chunks, 1):
        audio_parts.append(tts_one(chunk, cfg))
        print(f"      第 {i}/{len(chunks)} 段完成")

    combined, ext = combine_audio(audio_parts)
    if ext == "wav":
        combined, ext = maybe_to_mp3(combined)

    out_path = Path(f"{stub}.{ext}")
    other = out_wav if ext == "mp3" else out_mp3
    if other.exists():
        other.unlink()
    out_path.write_bytes(combined)

    manifest[rel] = {"hash": digest, "audio": out_path.name}
    print(f"    完成 -> {out_path.relative_to(ROOT).as_posix()}  ({len(combined) // 1024} KB)")
    return True


def main() -> None:
    cfg = load_config()
    notes = find_text_notes()
    if not notes:
        print("没有找到任何 *文字版*.md 文件。")
        return

    print(f"改写模型：{cfg['rewrite_model']}   语音模型：{cfg['tts_model']}   音色：{cfg['tts_voice']}")
    print(f"发现 {len(notes)} 个文字版笔记。\n")

    manifest = load_manifest()
    changed = 0
    failed = 0
    for note in notes:
        try:
            if process(note, cfg, manifest):
                changed += 1
                save_manifest(manifest)  # 每成功一个就落盘，避免中途失败白干
        except Exception as exc:  # noqa: BLE001 单个文件失败不影响其它
            failed += 1
            print(f"  [X] 出错：{note.name}\n    {exc}\n")

    save_manifest(manifest)
    print(f"\n完成：新生成/更新 {changed} 个，失败 {failed} 个。")
    if changed:
        print('记得提交并推送：git add -A && git commit -m "Update audio" && git push')
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
