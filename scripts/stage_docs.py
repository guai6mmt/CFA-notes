from __future__ import annotations

import shutil
import stat
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


def handle_remove_readonly(func, path, exc_info):
    Path(path).chmod(stat.S_IWRITE)
    func(path)


def copy2_force(source, target):
    target_path = Path(target)
    if target_path.exists():
        try:
            target_path.chmod(stat.S_IWRITE)
        except OSError:
            pass

    try:
        return shutil.copy2(source, target)
    except PermissionError as exc:
        print(f"Warning: could not update {target_path}: {exc}")
        return target


def copy_subject(subject: str) -> None:
    source = ROOT / subject
    target = STAGING_DIR / subject
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("html-preview"),
        copy_function=copy2_force,
        dirs_exist_ok=True,
    )


def main() -> None:
    if STAGING_DIR.exists():
        try:
            shutil.rmtree(STAGING_DIR, onerror=handle_remove_readonly)
        except PermissionError as exc:
            print(f"Warning: could not fully remove {STAGING_DIR}: {exc}")
            print("Reusing the existing staging directory.")

    STAGING_DIR.mkdir(exist_ok=True)
    copy2_force(ROOT / "index.md", STAGING_DIR / "index.md")
    shutil.copytree(
        ROOT / "assets",
        STAGING_DIR / "assets",
        copy_function=copy2_force,
        dirs_exist_ok=True,
    )

    for subject in SUBJECT_DIRS:
        copy_subject(subject)

    print(f"Prepared MkDocs content in {STAGING_DIR}")


if __name__ == "__main__":
    main()
