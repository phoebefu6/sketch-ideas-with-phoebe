#!/usr/bin/env python3
"""Lightweight QA gate for scrollable, publishable gallery pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = sorted(
    path
    for path in ROOT.rglob("*.html")
    if ".git" not in path.parts and "node_modules" not in path.parts
)


def css_block_has(source: str, selector: str, declaration: str) -> bool:
    pattern = rf"{re.escape(selector)}\s*\{{[^}}]*{declaration}"
    return re.search(pattern, source, re.IGNORECASE | re.DOTALL) is not None


def has_screen_unlock(source: str) -> bool:
    screen_start = source.lower().find("@media screen")
    if screen_start == -1:
        return False
    screen_source = source[screen_start:]
    body_unlock = css_block_has(screen_source, "body", r"overflow\s*:\s*(?:visible|auto|scroll)")
    height_unlock = css_block_has(screen_source, "body", r"height\s*:\s*auto")
    return body_unlock and height_unlock


def qa_standalone_page(path: Path, source: str, errors: list[str]) -> None:
    body_locked = css_block_has(source, "body", r"overflow\s*:\s*hidden")
    fixed_body_height = css_block_has(source, "body", r"(?<!-)height\s*:\s*(?:\d|100)")
    locked_columns = css_block_has(source, "main.cols", r"overflow\s*:\s*hidden")

    if (body_locked or fixed_body_height) and not has_screen_unlock(source):
        errors.append(
            f"{path.relative_to(ROOT)} locks body height/overflow without a screen scroll override"
        )

    screen_start = source.lower().find("@media screen")
    screen_source = source[screen_start:] if screen_start != -1 else ""
    columns_unlock = css_block_has(
        screen_source,
        "main.cols",
        r"overflow\s*:\s*visible",
    )
    if locked_columns and not columns_unlock:
        errors.append(
            f"{path.relative_to(ROOT)} clips column content without a screen overflow override"
        )


def qa_gallery_css(errors: list[str]) -> None:
    style_path = ROOT / "site" / "style.css"
    if not style_path.exists():
        errors.append("site/style.css is missing")
        return
    source = style_path.read_text()
    if ".lightbox" in source and not css_block_has(source, ".lightbox", r"overflow-y\s*:\s*auto"):
        errors.append("site/style.css lightbox must scroll vertically for long detail content")
    if ".lb-body" in source and not css_block_has(source, ".lb-body", r"align-items\s*:\s*start"):
        errors.append("site/style.css detail body should align to the top for long content")


def main() -> int:
    errors: list[str] = []
    standalone_pages = [path for path in HTML_FILES if path.name == "sheet.html"]

    for path in standalone_pages:
        qa_standalone_page(path, path.read_text(), errors)

    qa_gallery_css(errors)

    if errors:
        print("Page QA failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Page QA passed: "
        f"{len(HTML_FILES)} HTML pages inspected, "
        f"{len(standalone_pages)} standalone visual subpages checked, "
        "gallery detail scrolling checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
