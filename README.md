# CFA 二级笔记站点

这个仓库使用 MkDocs Material 构建 CFA Level II 笔记网站，并由 Docker 中的 Caddy 提供访问。默认地址为 `http://服务器IP:8889`。

## 服务器一键部署

服务器需要预先安装：

- Git
- curl
- Docker Engine
- Docker Compose 插件

首次部署和以后更新都可以执行同一条命令：

```bash
curl -fsSL https://raw.githubusercontent.com/guai6mmt/CFA-notes/main/scripts/install.sh | bash
```

脚本会自动完成以下操作：

1. 首次运行时，将仓库下载到 `~/CFA-notes`。
2. 已经部署过时，拉取 GitHub 上的最新代码。
3. 构建站点镜像并启动容器。
4. 等待健康检查通过，并输出访问地址。

部署成功后访问：

```text
http://服务器IP:8889
```

如果服务器启用了防火墙，需要放行 TCP 端口 `8889`。默认部署没有账号密码，能够访问该端口的人都可以查看笔记。

## HTTPS 和反向代理

如果服务器已经使用 Nginx、Caddy 等反向代理，建议只允许本机访问笔记容器。首次运行一键部署命令时增加两个环境变量：

```bash
curl -fsSL https://raw.githubusercontent.com/guai6mmt/CFA-notes/main/scripts/install.sh \
  | NOTES_BIND_ADDRESS=127.0.0.1 NOTES_PORT=8889 bash
```

配置会保存到 `~/CFA-notes/.env`，后续更新仍然只需执行普通的一键部署命令。`.env` 不会提交到 Git。

## 常用排查命令

查看容器状态：

```bash
cd ~/CFA-notes
docker compose ps
```

查看最近日志：

```bash
cd ~/CFA-notes
docker compose logs --tail=200 notes
```

查看首页是否正常响应：

```bash
curl --fail --show-error http://127.0.0.1:8889/
```

如果在 `.env` 中修改过 `NOTES_PORT`，将上面的 `8889` 替换为实际端口。

## 私有仓库部署

上面的一键命令适用于可以公开读取的 GitHub 仓库。如果以后将仓库改为私有仓库，需要先为服务器配置 GitHub SSH deploy key，然后首次执行：

```bash
git clone git@github.com:guai6mmt/CFA-notes.git ~/CFA-notes
bash ~/CFA-notes/scripts/deploy.sh
```

之后更新仍然只需执行：

```bash
bash ~/CFA-notes/scripts/deploy.sh
```

## 本地预览

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\stage_docs.py
.\.venv\Scripts\mkdocs serve
```

访问 <http://127.0.0.1:8000>。

Docker 构建时会自动整理笔记文件。本地新增图片或修改笔记后，如需再次预览，请重新运行 `scripts/stage_docs.py`。

## 日常修改后上传 GitHub

每次本地修改笔记或新增图片后，在当前仓库目录运行：

```powershell
git status
python scripts\stage_docs.py
git add -A
git commit -m "Update CFA notes"
git push origin main
```

如果只是少量文字修改，也可以跳过 `stage_docs.py`。提交前建议先看一眼 `git status`，确认本次改动都是要上传的内容。

## 听笔记（语音朗读）

文件名形如 `数量文字版.md` 的"文字版"笔记可以一键转成语音，像听播客一样复习。公式会先用 AI 改写成口语讲解，不会读出乱七八糟的符号。生成好的音频随网站一起发布，在手机或电脑打开对应页面，顶部就会出现播放器。

### 第一次使用（只需配置一次）

1. 到阿里云百炼（DashScope）控制台申请一个 API Key（`sk-` 开头）。语言模型和语音模型共用这一个 Key。
2. 复制 `scripts\audio_config.example.json`，改名为 `scripts\audio_config.json`。
3. 用记事本打开它，把 `api_key` 填进去，其它项可以先不动。

`audio_config.json` 已写入 `.gitignore`，不会上传 GitHub，可以放心填密钥。

### 日常使用

1. 照常写好或改好文字版笔记。
2. 双击运行 `scripts\生成音频.bat`。
   - 它会自动找出所有 `*文字版*.md`，只把**改动过的**转成语音；没改过的直接跳过、复用上次结果（省钱省时间）。
   - 公式会被 AI 先讲成人话再朗读。
3. 跑完后照常提交推送：

   ```powershell
   git add -A
   git commit -m "Update notes and audio"
   git push origin main
   ```

4. 服务器更新后，在手机或电脑打开任意"文字版（可听）"页面，顶部点 ▶️ 即可收听。

### 新增一个文字版页面时

不用改任何配置。只要文件名形如 `XX文字版.md`、放在对应科目文件夹里（例如 `固收/固收文字版.md`），构建时 `scripts/nav_hooks.py` 会**自动**在该科目下生成「文字版（可听）」入口。接着照常生成音频、提交推送即可。

### 换声音 / 换模型 / 调讲解风格

打开 `scripts\audio_config.json`：

- `tts_voice`：朗读音色（如 `Cherry`、`Ethan` 等，可选项见 DashScope 文档）。
- `tts_model`：语音模型，默认 `qwen-tts`。
- `rewrite_model`：负责把公式讲成人话的语言模型，默认 `qwen-plus`，想更细致可换成 `qwen-max`。
- `rewrite_prompt`：留空就用内置讲解风格；想改风格（更口语、更简短等）可以在这里写自己的要求。

改了音色或讲解风格后再运行，会把所有文字版重新生成一遍。

### 费用与本地缓存

- 只有内容改动过的文字版才会重新调用 API；没改的会跳过，直接复用已生成的音频。
- 生成记录存在 `scripts\.audio_cache\`（不上传）。删掉这个文件夹会触发全部重新生成。
- 想看 AI 把公式改写成了什么，可以打开 `scripts\.audio_cache\` 里对应的 `*.口语稿.txt`。

### 出问题时

`生成音频.bat` 窗口里会打印错误信息。常见原因：API Key 填错、模型名 / 音色名不被支持、连不上阿里云。如果是语音合成报错，把窗口里那段错误发我即可帮你调整。

## 其他说明

- 页面中的公式使用固定版本的 MathJax CDN。浏览器需要能够访问 `https://unpkg.com` 才能渲染公式。
- 一键部署脚本会先拉取代码、校验 Compose 配置、构建镜像，再等待站点通过健康检查。构建失败时不会替换当前正在运行的容器。
