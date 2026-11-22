"""Require a source record for every external web link in repository Markdown."""

import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from markdown import Markdown

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = Path("docs/references")
FRONT_MATTER = re.compile(
    r"\A---[ \t]*\n(.*?)^---[ \t]*(?:\n|\Z)", re.MULTILINE | re.DOTALL
)
EXTENSIONS = ["extra", "pymdownx.superfences", "pymdownx.magiclink"]
LINK_ATTRIBUTES = {"a": "href", "area": "href", "img": "src"}


def markdown_paths(root: Path) -> list[Path]:
    listing = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            ":(icase,glob)**/*.md",
        ],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
    )
    paths = {Path(os.fsdecode(name)) for name in listing.stdout.split(b"\0") if name}
    return sorted(
        path
        for path in paths
        if (root / path).is_file() and not (root / path).is_symlink()
    )


def source_url(url: str) -> str | None:
    url = url.strip()
    try:
        parts = urlsplit(f"https:{url}" if url.startswith("//") else url)
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            return None
    except ValueError:
        return None
    userinfo, separator, host = parts.netloc.rpartition("@")
    return parts._replace(
        netloc=f"{userinfo}{separator}{host.lower()}",
        path=parts.path or "/",
        fragment="",
    ).geturl()


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.urls: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attribute = LINK_ATTRIBUTES.get(tag)
        target = dict(attrs).get(attribute) if attribute else None
        if target and (url := source_url(target)):
            self.urls.add(url)


def split_front_matter(text: str) -> tuple[str, str]:
    match = FRONT_MATTER.match(text)
    return (match[1], text[match.end() :]) if match else ("", text)


def record_url(path: Path, front_matter: str) -> str | None:
    try:
        metadata = yaml.safe_load(front_matter)
    except yaml.YAMLError as error:
        raise ValueError(
            f"{path.as_posix()}: invalid YAML front matter: {error}"
        ) from error
    if not isinstance(metadata, dict) or "url" not in metadata:
        return None
    value = metadata["url"]
    if isinstance(value, str) and (url := source_url(value)):
        return url
    raise ValueError(f"{path.as_posix()}: front matter `url` must be an HTTP(S) URL")


def check_references(root: Path) -> int:
    pages = {
        path: split_front_matter((root / path).read_text(encoding="utf-8-sig"))
        for path in markdown_paths(root)
    }
    covered = {
        url
        for path, (front_matter, _) in pages.items()
        if path.is_relative_to(REFERENCES)
        and path != REFERENCES / "index.md"
        and (url := record_url(path, front_matter))
    }
    parser = Markdown(extensions=EXTENSIONS)
    missing: set[str] = set()
    affected = 0
    for path, (_, body) in pages.items():
        collector = LinkCollector()
        collector.feed(parser.reset().convert(body))
        collector.close()
        uncovered = collector.urls - covered
        if uncovered:
            affected += 1
            missing.update(uncovered)
            for url in sorted(uncovered):
                print(
                    f"{path.as_posix()}: missing reference for {url}", file=sys.stderr
                )

    if missing:
        print(
            f"Missing references: {len(missing)} distinct URLs in {affected} Markdown files. "
            "Use templates/reference.template.md to add records under docs/references/.",
            file=sys.stderr,
        )
    return int(bool(missing))


def main() -> int:
    try:
        return check_references(ROOT)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
