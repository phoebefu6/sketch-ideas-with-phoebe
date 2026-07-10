#!/usr/bin/env python3
"""Build the gallery: scan works/, generate thumbnails, data/works.js(.json), README grid.

One folder per work inside works/:
    works/2026-07-10-data-swamp-monster/
        full.png   (or .jpg / .jpeg / .webp)  - the original image
        meta.yml                              - title, date, tool, series, style, ...
        thumb.webp                            - generated here, never by hand

Run: python3 scripts/build.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
WORKS_DIR = ROOT / "works"
DATA_DIR = ROOT / "data"
THUMB_WIDTH = 720
THUMB_NAME = "thumb.webp"
FULL_NAMES = ("full.png", "full.jpg", "full.jpeg", "full.webp")

REQUIRED_META = ("title", "date", "tool")


def find_full(folder: Path) -> Path | None:
    for name in FULL_NAMES:
        candidate = folder / name
        if candidate.exists():
            return candidate
    return None


def make_thumb(src: Path, dest: Path) -> tuple[int, int]:
    """Generate (or refresh) the thumbnail. Returns full image (width, height)."""
    with Image.open(src) as img:
        width, height = img.size
        if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
            thumb = img.convert("RGB") if img.mode in ("P", "CMYK") else img.copy()
            if width > THUMB_WIDTH:
                ratio = THUMB_WIDTH / width
                thumb = thumb.resize((THUMB_WIDTH, round(height * ratio)), Image.LANCZOS)
            if thumb.mode == "RGBA":
                thumb = thumb.convert("RGB")
            thumb.save(dest, "WEBP", quality=84)
    return width, height


def load_taxonomy() -> dict:
    taxonomy_path = ROOT / "taxonomy.yml"
    if not taxonomy_path.exists():
        return {"formats": {}}
    return yaml.safe_load(taxonomy_path.read_text()) or {"formats": {}}


def scan_works() -> list[dict]:
    works = []
    problems = []
    for folder in sorted(WORKS_DIR.iterdir(), reverse=True):
        if not folder.is_dir() or folder.name.startswith("."):
            continue
        meta_path = folder / "meta.yml"
        full = find_full(folder)
        if not meta_path.exists():
            problems.append(f"{folder.name}: missing meta.yml, skipped")
            continue
        if full is None:
            problems.append(f"{folder.name}: missing full.png/.jpg/.webp, skipped")
            continue
        meta = yaml.safe_load(meta_path.read_text()) or {}
        missing = [key for key in REQUIRED_META if not meta.get(key)]
        if missing:
            problems.append(f"{folder.name}: meta.yml missing {', '.join(missing)}, skipped")
            continue
        width, height = make_thumb(full, folder / THUMB_NAME)
        works.append(
            {
                "id": folder.name,
                "title": str(meta["title"]),
                "date": str(meta["date"]),
                "tool": str(meta["tool"]),
                "format": str(meta.get("format") or "style-study"),
                "topic": [str(t) for t in (meta.get("topic") or [])],
                "style": str(meta.get("style") or ""),
                "inspired_by": str(meta.get("inspired_by") or ""),
                "prompt": str(meta.get("prompt") or ""),
                "takeaway": str(meta.get("takeaway") or ""),
                "featured": bool(meta.get("featured", False)),
                "full": f"works/{folder.name}/{full.name}",
                "thumb": f"works/{folder.name}/{THUMB_NAME}",
                "w": width,
                "h": height,
            }
        )
    for problem in problems:
        print(f"  warn: {problem}", file=sys.stderr)
    works.sort(key=lambda item: (item["date"], item["id"]), reverse=True)
    return works


def write_data(works: list[dict], taxonomy: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    payload = {"taxonomy": taxonomy, "works": works}
    (DATA_DIR / "works.json").write_text(json.dumps(payload, indent=2) + "\n")
    (DATA_DIR / "works.js").write_text(
        "const GALLERY = " + json.dumps(payload) + ";\n"
    )


def write_readme(works: list[dict], taxonomy: dict) -> None:
    styles = sorted({work["style"] for work in works if work["style"]})
    tools = sorted({work["tool"] for work in works})
    lines = [
        "# Worth a thousand words",
        "",
        "Data and AI, explained in pictures. I lead data teams by day and draw",
        "what's hard to say - complicated business, data, and data people,",
        "simplified into images anyone can act on. Every prompt published.",
        "",
        f"**{len(works)} works · {len(styles)} styles · {len(tools)} tools · every prompt is yours to copy**",
        "",
        "🖼️ **[Enter the gallery →](https://phoebefu6.github.io/phoebe-the-artist/)**",
        "",
        "## Latest",
        "",
    ]
    latest = works[:9]
    for row_start in range(0, len(latest), 3):
        row = latest[row_start : row_start + 3]
        cells_img = "".join(
            f'<td width="33%"><img src="{work["thumb"]}" alt="{work["title"]}" width="100%"></td>'
            for work in row
        )
        cells_caption = "".join(
            f'<td align="center"><sub><b>{work["title"]}</b> · {work["tool"]}</sub></td>'
            for work in row
        )
        lines += ["<table><tr>" + cells_img + "</tr><tr>" + cells_caption + "</tr></table>", ""]
    lines += [
        "## Formats",
        "",
    ]
    for key, info in taxonomy.get("formats", {}).items():
        count = sum(1 for work in works if work["format"] == key)
        lines.append(f"- **{info.get('label', key)}** ({count}) - {info.get('blurb', '')}")
    lines += [
        "",
        "## How this repo works",
        "",
        "- `works/` holds one folder per image: the original, a 7-line `meta.yml`, an auto thumbnail.",
        "- `scripts/build.py` regenerates thumbnails, `data/works.js`, and this README.",
        "- A GitHub Action rebuilds and redeploys the gallery on every push.",
        "- New work = drop one folder, push. Nothing else is ever edited by hand.",
        "",
        "Made with Midjourney, ChatGPT image, Nano Banana - and strong opinions about data.",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines))


def main() -> None:
    if not WORKS_DIR.exists():
        sys.exit("works/ directory not found")
    print("Scanning works/ ...")
    taxonomy = load_taxonomy()
    works = scan_works()
    write_data(works, taxonomy)
    write_readme(works, taxonomy)
    styles = {work["style"] for work in works if work["style"]}
    print(f"Built: {len(works)} works, {len(styles)} styles → data/works.js, README.md")


if __name__ == "__main__":
    main()
