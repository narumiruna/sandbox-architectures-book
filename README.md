# Sandbox Architectures Book

A book about software sandboxes: how they isolate programs and control what those programs can access. English is the source edition. The book is also available in [正體中文 (Traditional Chinese)](docs/zh-TW/index.md).

Use the [book home page](docs/index.md) to choose a starting point. Begin with [Sandbox isolation boundaries](docs/sandbox-isolation-boundaries.md) if you are new to sandboxes, or follow the worked example in [From issue to patch](docs/practice/design/from-issue-to-patch.md) if you already know the basics.

## Read a local copy with a coding agent

1. If you have [Git](https://git-scm.com/), clone the book and open the repository root:

   ```sh
   git clone https://github.com/narumiruna/sandbox-architectures-book.git
   cd sandbox-architectures-book
   ```

2. Start any coding agent that can read local files, with this directory as its workspace. Use read-only access if your agent supports it. Do not grant permission to run commands or write files for this exercise. You do not need to build the site, enable integrations, or run the examples.
3. Paste this prompt into the agent:

   > I am new to sandboxes. Read `docs/sandbox-isolation-boundaries.md` and explain how an isolation boundary differs from a policy in the file-open example. Cite the book file paths and section headings, and show me the two glossary entry paths. Label anything the book does not cover as extra context or unknown. Ask me one question that applies the distinction to file access, then wait for my answer. After I reply, check my answer against the book. Only read local files; do not modify files or run commands.

4. Open the cited sections and glossary entries, then answer the question. If you want a Git check, run `git status --short --untracked-files=all` yourself before and after reading. A clean checkout should show no changes in either check; Git status does not report ignored files. Keep any agent logs outside the checkout.

Use [`docs/index.md`](docs/index.md) as the chapter map and [`docs/glossary/index.md`](docs/glossary/index.md) to look up terms and abbreviations. For a separate hands-on session, find the [Lamp lab files](examples/lamp/) and follow the instructions for [checking access rules](docs/practice/verification/verifying-access-rules.md) or [measuring a sandbox](docs/practice/verification/measuring-a-sandbox.md). Before running an example, ask the agent to explain its prerequisites, what each command does, and what result to expect. Decide yourself whether to run it.

## Preview locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run `just serve` from the repository root if you have [Just](https://just.systems/) installed. Without Just, run the same command directly:

```sh
uv run --locked zensical serve
```

Open `http://localhost:8000` in your browser. uv uses the dependencies in [`uv.lock`](uv.lock).

## Edit and build

Register every Markdown page in [`docs/`](docs/) in [`zensical.toml`](zensical.toml). Use paths relative to `docs/`: add pages shown in the site menu to `project.nav`, and add pages outside the menu (such as individual glossary terms) to `project.extra.unlisted_pages`.

```sh
uv run --locked zensical build --strict
```

The build writes the site to `site/` and stops if it finds warnings.

In light mode, the **Daytime paper** menu in the header offers Oat, Sage, Tea, Linen (the default), and Original (Zensical's built-in light palette). The browser remembers the selection. Zensical's separate theme toggle still controls light, dark, and system preference.

Theme CSS and JavaScript live in [`overrides/assets/`](overrides/assets/). Edit the paper colors in [`parchment.css`](overrides/assets/stylesheets/parchment.css) and the menu in [`paper.js`](overrides/assets/javascripts/paper.js).

### Translation editions

Use the **Language** button next to Search to open the same page in another edition. If the same section exists in the target edition, the switch keeps your place. **English (original)** opens the source. If the button is unavailable, use the language links above the article instead.

The sidebar, previous and next links, and search show the current edition. Shared technical figures and some controls, including **Language** and **Daytime paper**, remain in English.

After a strict build, run `node --test scripts/check_edition_search.mjs` to verify that search finds terms in each language and returns results only from the current edition. The search adapter uses the message protocol of the Zensical UI worker pinned in `uv.lock`.

To add or maintain a translation:

1. For each new English page under `docs/`, except shared source records, add a Traditional Chinese translation at the same relative path under `docs/zh-TW/`. For example, `docs/glossary/policy.md` has a translation at `docs/zh-TW/glossary/policy.md`.
2. Preserve English technical terms, product names, abbreviations, glossary term headings, code, and citations. For cross-page references, keep the source heading IDs with explicit anchors such as `{#follow-a-request-to-open-a-file}`.
3. Link to chapters and glossary entries in the same edition.
4. Register the English page and its translations in `zensical.toml`. Run the strict build and check that the language links open the same page in each edition.

Source records in [`docs/references/`](docs/references/index.md) are shared by all editions; do not translate them. Register each record once in `project.extra.unlisted_pages`. Translate the index page, and link it to the shared index.

### Math in Markdown

Use `$E = mc^2$` for inline math. For a display equation, put `$$` on separate lines with a blank line before and after the block:

```markdown
$$
\frac{1}{2} + \frac{1}{2} = 1
$$
```

[KaTeX](https://katex.org/docs/supported.html) renders the formulas in the browser. It supports a subset of LaTeX commands and loads its assets from jsDelivr, so the preview needs network access to render math.

## Git checks

Install [prek](https://prek.j178.dev/), then run `prek install` to enable the checks in [`prek.toml`](prek.toml) before each commit. The checks clean up whitespace and line endings, flag large new files and private keys, and scan GitHub Actions workflows with zizmor.

Run `prek run --all-files` to run all hooks on demand. These documentation hooks use uv:

- `prek run check-docs-coverage --all-files` checks that all Markdown pages are registered, each English page except shared source records has a translation in every configured edition, and each translation has an English original.
- `prek run check-docs-no-web-assets --all-files` rejects standalone CSS, HTML, and JavaScript files under `docs/`. Put styles and scripts in `overrides/assets/` and HTML templates in `overrides/`.
- `prek run check-docs-references --all-files` scans all tracked and non-ignored untracked Markdown files, including translations and reference records. It requires every HTTP(S) hyperlink and remote image URL (including `srcset` candidates) to match the `url` in the YAML front matter of a source record under [`docs/references/`](docs/references/index.md). Use [`templates/reference.template.md`](templates/reference.template.md) to add a record. A single record covers all `#section` links to the same page, but different paths or queries need their own records. Code and comments are not links. The hook reports the Markdown file and URL for each missing record; it does not fetch URLs.

## Pi tools

With [Just](https://just.systems/) and Pi installed, run `just` from the repository root. It runs the default recipe, `just pi`. The recipe disables extension discovery and built-in extensions with `-ne`. It uses `-e` to load `diagram-design`, `@narumitw/pi-subagents`, and `@narumitw/pi-goal` for that run without adding them to Pi settings.

[`.pi/mcp.json`](.pi/mcp.json) configures alphaXiv and Firecrawl. To use these servers, start Pi with built-in MCP enabled (for example, run `pi -e builtin:mcp` instead of `just pi`) and trust the project. Set `FIRECRAWL_API_KEY` in the environment that starts Pi; do not put the key in the config file.

Run `/reload` in an open Pi session, then use `/mcp` to check the servers or sign in to alphaXiv if prompted.

Run `/skill:link-book-terms docs/sandbox-isolation-boundaries.md` to scan that page and add missing links on first use of technical terms and proper names. Omit the path to scan the whole book.

Run `/skill:audit-markdown-citations docs/sandbox-isolation-boundaries.md` to check whether sources support that page's definitions and factual claims. The audit adds reliable citations, corrects inaccurate claims, and removes claims that remain unsupported after a source search. It summarizes what changed in each file and reports unresolved claims when evidence is inaccessible or conflicts. Pass a Markdown file or directory to limit the scope; omit the path to scan all tracked and non-ignored Markdown in the repository, including translations. Add `report only` after the path to review findings without editing the articles.

## License

[MIT](LICENSE).
