# Sandbox Architectures Book guidelines

## Communication

- Write the English original first.
  - [UNREVIEWED] For translated copies, follow the [translation edition rules](README.md#translation-editions).
- Lead with the main point in plain language for readers with no prior knowledge, and include caveats that change the takeaway in the introduction.
- Define essential terms on first use, and use a concrete example or analogy when helpful, noting any limit that could mislead.
- Use a short numbered list for events readers must follow in order.
- Put mechanisms, trade-offs, and other limitations under descriptive headings or link to a focused reference.

## Documentation

### Existing coverage and new chapters

For questions within the book's scope:

1. Start with the [book index](docs/index.md), search the English source pages in `docs/`, and check the [glossary](docs/glossary/index.md) for terminology questions.
2. If the book already answers the question correctly and no important detail is missing, cite the relevant section without editing.
3. Otherwise, unless the user asks for chat-only or read-only output, update the most relevant existing page with verified corrections or findings that explain an important limitation or help readers make a technical decision.
   - Use the [isolation-boundaries chapter](docs/sandbox-isolation-boundaries.md) for concepts and the [architecture survey](docs/agent-sandbox-architectures.md) for brief comparisons of implementations; distinguish the execution boundary from the control plane.
   - If a case study can stand alone and needs to explain how several mechanisms work together, such as isolation, scheduling, and persistence, keep the survey comparison brief and propose a separate chapter.
   - Ask before adding a chapter.
4. If you update the book, run the [strict build](#commands) and link to the changed section in the reply.

### Research and citations

- Verify uncertain or consequential claims about APIs, tool behavior, and recommended practices before relying on them.
  - For repository behavior, start with local code and configuration, then consult `uv.lock` and the documentation or source for the pinned version.
  - Prefer primary sources for external claims, and cite primary sources for product-specific claims; use reputable secondary sources when primary evidence is insufficient.
  - Judge sources by accuracy, authority, relevance, and recency rather than search rank, and investigate conflicting evidence.
- Separate verified facts from inferences, state what remains unverified, and do not invent facts, citations, URLs, or evidence.
- Link directly to the original evidence for important claims and decisions, naming the release or revision when behavior varies by version.
- Create or reuse a source record in `docs/references/` for each external source cited in the book, use the [reference template](templates/reference.template.md) for new records, and list each record in the [reference index](docs/references/index.md).

### Glossary and first-use links

- Use the [glossary](docs/glossary/index.md) for shared terminology, with one page per technical concept.
- Before adding a term, search the glossary index for the term, its abbreviations, and its alternate names, and reuse any entry for the same concept.
- For a newly introduced concept with no entry, create `docs/glossary/<term>.md` from the [glossary template](templates/glossary.template.md) and add a short definition and link to the glossary index.
- Link technical terms and proper names on first use in each page's body to an applicable glossary entry, a relevant book page, or a primary source.

### Diagrams

- Use a compact Mermaid diagram when it explains a concept, relationship, or process more clearly than prose alone, and put it near prose that states its main takeaway.
- Prefer the [diagram types styled by Zensical](https://zensical.org/docs/authoring/diagrams/): `flowchart` for isolation boundaries, `sequenceDiagram` for interactions, `stateDiagram-v2` for lifecycle changes, and `classDiagram` or `erDiagram` for structure or data relationships.

### Source files and site registration

- Put published Markdown under `docs/` and edit those sources rather than the generated `site/` directory.
- Add new chapters and reference indexes to `project.nav` in `zensical.toml`.
- Register new glossary pages and shared source records in `project.extra.unlisted_pages` in `zensical.toml` with paths relative to `docs/`, not in `project.nav`.

## Commands

- From the repository root, run `uv run --locked zensical build --strict` after changing book pages or site configuration.
- Run `prek run --files <changed-paths>` for files you intend to commit.

## Boundaries

- Commit or push only if the user requests it; pushes to `main` or `master` deploy the book to GitHub Pages through [`.github/workflows/docs.yml`](.github/workflows/docs.yml).

## Testing

- After adding or moving a page, check that the generated navigation and affected internal links lead to the intended pages.
- After adding or changing a Mermaid diagram, verify in a browser that it renders and stays readable on a narrow screen; a strict build does not check rendering.

## Collaboration

- Use subagents for independent tasks and run them in parallel when possible.
- The main agent coordinates assignments, helps locate sources as needed, and combines and verifies the results.
