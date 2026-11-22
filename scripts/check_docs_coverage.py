"""Check that every Markdown page in docs/ is listed in zensical.toml."""

import sys
import tomllib
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def nav_paths(item: object) -> Iterator[str]:
    if isinstance(item, str):
        yield item
    elif isinstance(item, list):
        for child in item:
            yield from nav_paths(child)
    elif isinstance(item, dict):
        for child in item.values():
            yield from nav_paths(child)


def main() -> int:
    with (ROOT / "zensical.toml").open("rb") as config:
        project = tomllib.load(config)["project"]

    registered = set(nav_paths(project.get("nav", [])))
    registered.update(project.get("extra", {}).get("unlisted_pages", []))
    docs = ROOT / "docs"
    pages = {
        path.relative_to(docs).as_posix()
        for path in docs.rglob("*.md")
        if path.is_file()
    }
    missing = sorted(pages - registered)
    if missing:
        print(
            "Add these paths to project.nav or project.extra.unlisted_pages in zensical.toml:",
            file=sys.stderr,
        )
        for path in missing:
            print(f"  {path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
