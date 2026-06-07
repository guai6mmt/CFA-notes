from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = ROOT / ".mkdocs-docs"
SUBJECT_DIRS = (
    "数量",
    "经济学",
    "财务",
    "公金",
    "权益",
    "固收",
    "衍生品",
    "另类",
    "组合",
    "错题",
)


def copy_subject(subject: str) -> None:
    source = ROOT / subject
    target = STAGING_DIR / subject
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("html-preview"),
    )


def main() -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)

    STAGING_DIR.mkdir()
    shutil.copy2(ROOT / "index.md", STAGING_DIR / "index.md")
    shutil.copytree(ROOT / "assets", STAGING_DIR / "assets")

    for subject in SUBJECT_DIRS:
        copy_subject(subject)

    print(f"Prepared MkDocs content in {STAGING_DIR}")


if __name__ == "__main__":
    main()
