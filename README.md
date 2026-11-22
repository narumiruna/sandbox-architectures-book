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

The light palette is defined in [`docs/stylesheets/parchment.css`](docs/stylesheets/parchment.css). The stylesheet does not change the dark palette or the system preference option.

## Git checks

Install [prek](https://prek.j178.dev/), then run `prek install` to enable the checks in [`prek.toml`](prek.toml) before each commit. The checks clean up whitespace and line endings, flag large new files and private keys, and scan GitHub Actions workflows with zizmor.

Run `prek run --all-files` to run all hooks on demand. To check just the Markdown page registrations, run `prek run check-docs-coverage --all-files`. This hook uses uv and scans all Markdown files in `docs/`, including untracked files.

## Pi tools

[`.pi/mcp.json`](.pi/mcp.json) configures alphaXiv and Firecrawl for this project. Pi loads these servers after you trust the project. Set `FIRECRAWL_API_KEY` in the environment that starts Pi; do not put the key in the config file.

Run `/reload` in an open Pi session, then use `/mcp` to check the servers or sign in to alphaXiv if prompted.

## License

[MIT](LICENSE).
