# Sandbox Architectures Book

A book project about software sandboxes: how they isolate programs and control what those programs can access. The site currently contains only the [Zensical](https://zensical.org/) starter pages.

## Preview locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run this command from the repository root:

```sh
uv run --locked zensical serve
```

Open [http://localhost:8000](http://localhost:8000). uv uses the dependencies in [`uv.lock`](uv.lock).

## Edit and build

Write pages in [`docs/`](docs/). To show a new page in the site menu, add it to `nav` in [`zensical.toml`](zensical.toml).

```sh
uv run --locked zensical build --strict
```

The build writes the site to `site/` and stops if it finds warnings.

## Git checks

Install [prek](https://prek.j178.dev/), then run `prek install` to enable the checks in [`prek.toml`](prek.toml) before each commit. The checks clean up whitespace and line endings, flag large new files and private keys, and scan GitHub Actions workflows with zizmor.

Run `prek run --all-files` to check tracked files on demand.

## License

[MIT](LICENSE).
