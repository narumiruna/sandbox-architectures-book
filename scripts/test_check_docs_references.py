import subprocess
from pathlib import Path

import pytest
from check_docs_references import (
    EXTENSIONS,
    LinkCollector,
    check_references,
    record_url,
    source_url,
)
from markdown import Markdown


def test_collects_links_but_not_code_or_comments():
    text = """
[Inline](https://example.com/with_(parentheses) "Title")
[Reference][page]
<https://example.com/autolink> and https://example.com/plain.
[Local](chapter.md) and [Section](#section)
![Image](//example.com/image.png)
<a href="https://example.com/html?a=1&amp;b=2">HTML</a>

[page]: https://example.com/reference#anchor
[unused]: https://example.com/unused

<!-- [Comment](https://example.com/comment) -->

`https://example.com/inline-code`

    https://example.com/indented-code

1. List item

   ```text
   [Example](https://example.com/fenced-code)
   ```
"""
    collector = LinkCollector()
    collector.feed(Markdown(extensions=EXTENSIONS).convert(text))
    collector.close()
    assert collector.urls == {
        "https://example.com/with_(parentheses)",
        "https://example.com/reference",
        "https://example.com/autolink",
        "https://example.com/plain",
        "https://example.com/image.png",
        "https://example.com/html?a=1&b=2",
    }


def test_collects_responsive_image_sources():
    html = """
<picture>
  <source srcset="https://example.com/small.png 320w,
                  https://example.com/large.png?size=640,480 640w">
  <img src="fallback.png" srcset="data:image/png;base64,AAAA 1x,
                                 //example.com/retina.png 2x">
</picture>
<img srcset="local.png, https://example.com/optional.png">
<video><source srcset="https://example.com/not-a-picture.png"></video>
"""
    collector = LinkCollector()
    collector.feed(Markdown(extensions=EXTENSIONS).convert(html))
    collector.close()
    assert collector.urls == {
        "https://example.com/small.png",
        "https://example.com/large.png?size=640,480",
        "https://example.com/retina.png",
        "https://example.com/optional.png",
    }


def test_matching_keeps_distinct_pages_and_queries():
    assert source_url("HTTPS://EXAMPLE.COM#fragment") == "https://example.com/"
    assert (
        source_url("https://example.com/doc?v=1#section")
        == "https://example.com/doc?v=1"
    )
    assert source_url("http://example.com/doc?v=1") == "http://example.com/doc?v=1"
    assert source_url("https://example.com/doc/") == "https://example.com/doc/"
    assert source_url("mailto:reader@example.com") is None


def test_invalid_record_url_reports_the_file():
    with pytest.raises(ValueError, match=r"docs/references/source\.md: .*HTTP\(S\)"):
        record_url(Path("docs/references/source.md"), 'url: "relative.md"')


def test_checks_repository_markdown_against_shared_source_records(tmp_path, capsys):
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)

    def write(path: str, content: str) -> None:
        file = tmp_path / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")

    write(".gitignore", "/site/\n")
    write("site/generated.md", "https://example.com/ignored\n")
    write(
        "docs/references/source.md",
        '---\nurl: "https://example.com/covered"\n---\n\n'
        "[See also](https://example.com/missing#section)\n",
    )
    write("docs/zh-TW/chapter.md", "[Covered](https://example.com/covered#section)\n")
    write(
        "README.MD",
        '<img src="fallback.png" srcset="https://example.com/missing 2x">\n',
    )
    write("docs/copy.md", '---\nurl: "https://example.com/missing"\n---\n')
    write("docs/references/index.md", '---\nurl: "https://example.com/missing"\n---\n')
    subprocess.run(["git", "-C", str(tmp_path), "add", "README.MD"], check=True)

    assert check_references(tmp_path) == 1
    assert capsys.readouterr().err.splitlines() == [
        "README.MD: missing reference for https://example.com/missing",
        "docs/references/source.md: missing reference for https://example.com/missing",
        (
            "Missing references: 1 distinct URLs in 2 Markdown files. "
            "Use templates/reference.template.md to add records under docs/references/."
        ),
    ]

    write(
        "docs/references/missing.md", '---\nurl: "https://example.com/missing"\n---\n'
    )
    assert check_references(tmp_path) == 0
    assert not capsys.readouterr().err
