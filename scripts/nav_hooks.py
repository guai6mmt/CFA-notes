"""MkDocs 构建钩子：自动把每个科目下的"文字版"笔记加入左侧导航。

这样新建 `XX文字版.md` 之后，无需再手动修改 mkdocs.yml 的 nav。
用的是 MkDocs 1.4+ 自带的 hooks 机制，不需要安装额外插件。

规则：
  - 扫描 docs_dir 下每个科目文件夹里的 `*文字版*.md`；
  - 找到导航里对应科目的条目，在它下面加一个"文字版（可听）"入口；
  - 如果该科目原本只是一个单页链接，就自动变成"图文版 + 文字版"小节；
  - 已经手动写进 nav 的文字版不会重复添加。
"""

from __future__ import annotations

from pathlib import Path


TEXT_LABEL = "文字版（可听）"
MAIN_LABEL = "图文版"


def _collect_paths(node) -> list[str]:
    """递归收集一个 nav 节点里出现的所有页面路径。"""
    paths: list[str] = []
    if isinstance(node, str):
        paths.append(node)
    elif isinstance(node, dict):
        for value in node.values():
            paths.extend(_collect_paths(value))
    elif isinstance(node, list):
        for item in node:
            paths.extend(_collect_paths(item))
    return paths


def on_config(config, **kwargs):
    nav = config.get("nav")
    if not nav:
        return config

    docs_dir = Path(config["docs_dir"])

    # 子目录名 -> 该目录下的文字版页面（相对 docs_dir 的 posix 路径）
    text_by_subject: dict[str, list[str]] = {}
    for md in sorted(docs_dir.glob("*/*文字版*.md")):
        rel = md.relative_to(docs_dir).as_posix()
        text_by_subject.setdefault(md.parent.name, []).append(rel)
    if not text_by_subject:
        return config

    already = set(_collect_paths(nav))

    for index, item in enumerate(nav):
        if not isinstance(item, dict) or len(item) != 1:
            continue
        title, value = next(iter(item.items()))

        # 这个导航条目涉及哪些子目录
        subjects = {p.split("/", 1)[0] for p in _collect_paths(value)}

        additions = []
        for subject in subjects:
            for rel in text_by_subject.get(subject, []):
                if rel not in already:
                    additions.append({TEXT_LABEL: rel})
                    already.add(rel)
        if not additions:
            continue

        if isinstance(value, str):
            # 单页条目 -> 变成"图文版 + 文字版"小节
            nav[index] = {title: [{MAIN_LABEL: value}, *additions]}
        elif isinstance(value, list):
            value.extend(additions)

    return config
