# Sandbox Architectures Book

A book about software sandboxes: how they isolate programs and control what those programs can access. The book is written primarily in English.

Use the [book home page](docs/index.md) to choose a starting point. Begin with [Sandbox isolation boundaries](docs/sandbox-isolation-boundaries.md) if you are new to sandboxes, or follow the worked example in [From issue to patch](docs/practice/design/from-issue-to-patch.md) if you already know the basics.

## Preview locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run this command from the repository root:

```sh
uv run --locked zensical serve
```

Open [http://localhost:8000](http://localhost:8000). uv uses the dependencies in [`uv.lock`](uv.lock).

## Edit and build

Register every Markdown page in [`docs/`](docs/) in [`zensical.toml`](zensical.toml). Use paths relative to `docs/`: add pages shown in the site menu to `project.nav`, and add pages outside the menu (such as individual glossary terms) to `project.extra.unlisted_pages`.

```sh
uv run --locked zensical build --strict
```

The build writes the site to `site/` and stops if it finds warnings.

In light mode, the **Daytime paper** menu in the header offers Oat, Sage, Tea, Linen (the default), and Original (Zensical's built-in light palette). The browser remembers the selection. Zensical's separate theme toggle still controls light, dark, and system preference.

Theme CSS and JavaScript live in [`overrides/assets/`](overrides/assets/). Edit the paper colors in [`parchment.css`](overrides/assets/stylesheets/parchment.css) and the menu in [`paper.js`](overrides/assets/javascripts/paper.js).

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

Run `prek run --all-files` to run all hooks on demand. These two hooks use uv and scan `docs/`, including untracked files:

- `prek run check-docs-coverage --all-files` checks Markdown page registrations.
- `prek run check-docs-no-web-assets --all-files` rejects standalone CSS, HTML, and JavaScript files under `docs/`. Put styles and scripts in `overrides/assets/` and HTML templates in `overrides/`.

## Pi tools

[`.pi/mcp.json`](.pi/mcp.json) configures alphaXiv and Firecrawl for this project. Pi loads these servers after you trust the project. Set `FIRECRAWL_API_KEY` in the environment that starts Pi; do not put the key in the config file.

Run `/reload` in an open Pi session, then use `/mcp` to check the servers or sign in to alphaXiv if prompted.

## License

[MIT](LICENSE).
