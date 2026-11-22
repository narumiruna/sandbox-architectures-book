"""Check Markdown registrations and translation counterparts."""

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

    extra = project.get("extra", {})
    registered = set(nav_paths(project.get("nav", [])))
    registered.update(extra.get("unlisted_pages", []))
    docs = ROOT / "docs"
    pages = {
        path.relative_to(docs).as_posix()
        for path in docs.rglob("*.md")
        if path.is_file()
    }
    orphaned = []
    for path in pages:
        prefix, _, original = path.partition("/")
        if prefix in extra.get("editions", {}) and original not in pages:
            orphaned.append(path)

    failed = False
    for message, paths in (
        ("Register these Markdown pages in zensical.toml:", pages - registered),
        ("Remove these missing pages from zensical.toml:", registered - pages),
        ("Restore the English originals of these translations:", orphaned),
    ):
        if paths:
            failed = True
            print(message, file=sys.stderr)
            for path in sorted(paths):
                print(f"  {path}", file=sys.stderr)
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
