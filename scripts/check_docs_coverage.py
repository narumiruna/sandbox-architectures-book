"""Check Markdown registrations and complete translation coverage."""

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
    editions = extra.get("editions", {})
    originals = {path for path in pages if path.partition("/")[0] not in editions}
    orphaned = {
        path for path in pages - originals if path.partition("/")[2] not in originals
    }
    shared_records = {
        path
        for path in originals
        if path.startswith("references/") and path != "references/index.md"
    }
    missing_translations = {
        f"{edition}/{path}"
        for path in originals - shared_records
        for edition in editions
    } - pages
    stale_registrations = registered - pages - missing_translations

    failed = False
    for message, paths in (
        ("Register these Markdown pages in zensical.toml:", pages - registered),
        ("Remove these missing pages from zensical.toml:", stale_registrations),
        ("Restore the English originals of these translations:", orphaned),
        ("Add these missing translations under docs/:", missing_translations),
    ):
        if paths:
            failed = True
            print(message, file=sys.stderr)
            for path in sorted(paths):
                print(f"  {path}", file=sys.stderr)
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
