# Sandbox Architectures Book guidelines

## Communication

- Write book content in English and use the [glossary](docs/glossary.md) for shared terminology.
  - [UNREVIEWED] For translated copies of the English original, follow the [translation edition rules](README.md#translation-editions).
- Lead with the main point in plain language for readers with no prior knowledge, using one compact visual if it helps.
  - Keep caveats that change the takeaway in the introduction.
  - Define essential terms on first use, and use one concrete example or analogy when helpful; note any limit that could mislead.
  - Use a short numbered list for events readers must follow in order.
  - Put mechanisms, trade-offs, and other limitations under descriptive headings or link to a focused reference.

## Collaboration

- Use subagents freely for independent tasks and run them in parallel when possible.
- The main agent coordinates assignments, helps locate sources as needed, and combines and verifies the results.

## Research and Verification

- Proactively verify uncertain or consequential claims about APIs, tool behavior, and recommended practices before relying on them.
  - For project behavior, start with the repository’s code and configuration, then check `uv.lock` and consult the documentation or source for the pinned version.
  - For external claims, prefer primary sources: official documentation, specifications, standards, source code, and maintainer publications.
  - Use reputable secondary sources when primary evidence is insufficient, but cite primary sources for product-specific claims in the book.
  - Judge sources by accuracy, authority, relevance, and recency, not search rank; investigate conflicts before drawing a conclusion.
- Link directly to evidence for important claims and decisions, naming the release or revision when behavior varies by version.
- Separate verified facts from inferences and state what remains unknown or could not be verified.
- Never invent facts, citations, URLs, or evidence.

## Documentation

- Put published Markdown pages in `docs/` and add new chapters and reference indexes to `nav` in `zensical.toml`.
- On each book page, link technical terms and proper names on their first use in the body when a relevant reference exists.
  - Prefer the individual glossary entry for a technical term; otherwise, link to a relevant book page or a primary source, such as official documentation.
- Add technical terms used in the book to `docs/glossary.md`.
  - Give each glossary entry a short definition and link it to its own Markdown page under `docs/glossary/` that explains the term in detail.
  - Link individual term pages from the glossary rather than adding them to the main navigation.
- Use the isolation-boundaries chapter for concepts and the architecture survey for implementation details, and distinguish the execution boundary from the control plane.
- Use compact Mermaid diagrams in repository documentation when they explain a concept, relationship, or process more clearly than prose alone.
  - Put each diagram near the explanation it supports and state its main takeaway in prose.
  - In the published book, prefer the [diagram types styled by Zensical](https://zensical.org/docs/authoring/diagrams/): `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, and `erDiagram`.
  - Use `flowchart` for isolation boundaries, `sequenceDiagram` for interactions, and `stateDiagram-v2` for lifecycle changes.
- Edit source files rather than `site/`, which Zensical generates.

## Commands

- From the repository root, run `uv run --locked zensical build --strict` after changing book pages or site configuration.
- Run `prek run --files <changed-paths>` to check the files you intend to commit.

## Boundaries

- Push to a deployment branch only when the user requests it: `.github/workflows/docs.yml` deploys to GitHub Pages on pushes to `main` or `master`.

## Testing

- After adding or moving a page, check that the generated navigation and affected internal links lead to the intended pages.
- After adding or changing a Mermaid diagram, verify in a browser that it renders and remains readable on a narrow screen; a strict build does not validate Mermaid rendering.
