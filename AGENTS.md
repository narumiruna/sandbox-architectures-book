# Sandbox Architectures Book guidelines

## Communication

- Write book content in English and use the [glossary](docs/glossary.md) for shared terminology.

## Documentation

- Put published Markdown pages in `docs/` and add new chapters and reference indexes to `nav` in `zensical.toml`.
- Add technical terms used in the book to `docs/glossary.md`.
  - Give each glossary entry a short definition and link it to its own Markdown page under `docs/glossary/` that explains the term in detail.
  - Link individual term pages from the glossary rather than adding them to the main navigation.
- Use the isolation-boundaries chapter for concepts and the architecture survey for implementation details, and distinguish the execution boundary from the control plane.
- Use Mermaid for diagrams that help explain a concept, architecture, or flow.
  - Prefer the [diagram types styled by Zensical](https://zensical.org/docs/authoring/diagrams/): `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, and `erDiagram`.
  - Use `flowchart` for isolation boundaries, `sequenceDiagram` for interactions, and `stateDiagram-v2` for lifecycle changes.
- Cite primary sources for product-specific technical claims and identify the release or revision when behavior varies by version.
- Edit source files rather than `site/`, which Zensical generates.

## Commands

- From the repository root, run `uv run --locked zensical build --strict` after changing book pages or site configuration.
- Run `prek run --files <changed-paths>` to check the files you intend to commit.

## Boundaries

- Push to a deployment branch only when the user requests it: `.github/workflows/docs.yml` deploys to GitHub Pages on pushes to `main` or `master`.

## Testing

- After adding or moving a page, check that the generated navigation and affected internal links lead to the intended pages.
- After adding or changing a Mermaid diagram, verify in a browser that it renders and remains readable on a narrow screen; a strict build does not validate Mermaid rendering.
