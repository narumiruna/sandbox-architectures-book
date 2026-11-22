"""Reject standalone CSS, HTML, and JavaScript files under docs/."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_SUFFIXES = {".css", ".htm", ".html", ".xhtml", ".js", ".mjs", ".cjs"}


def main() -> int:
    blocked = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").rglob("*")
        if path.suffix.lower() in WEB_SUFFIXES and path.is_file()
    )
    if not blocked:
        return 0

    print(
        "Keep CSS, HTML, and JavaScript files out of docs/. Move site assets "
        "to overrides/assets/ and HTML templates to overrides/:",
        file=sys.stderr,
    )
    for path in blocked:
        print(f"  {path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
