---
name: link-book-terms
description: Scan Sandbox Architectures Book pages for unlinked technical terms and proper names, and add links at their first use in the body. Use when asked to add, backfill, or audit glossary links or links to official references for named technologies in docs/. Do not use for general copyediting or a broken-link audit.
---

# Link book terms

1. Read the link rules in `AGENTS.md` and the term index in `docs/glossary/index.md` from the repository root.
   - Scan the requested files or directories; without a narrower scope, scan the book pages listed in `project.nav` and `project.extra.unlisted_pages` in `zensical.toml`.
   - If the user asks only to audit or report, do not edit files.
2. Read each page from the start and identify the first use of each technical term or proper name in the body, including in lists and tables.
   - Match the meaning, not just the spelling: check plurals and abbreviations such as `VM`, use the specific term when terms overlap, and skip ordinary uses of ambiguous words.
   - Skip headings, front matter, code, diagram source, URLs, and link syntax; count an existing link on the first use if it points to a suitable reference.
   - Prefer the individual glossary page, then a relevant book page or a primary source such as official documentation.
   - Do not link a page to itself or guess a destination; report terms that need a glossary entry or for which no suitable reference can be verified.
3. Wrap the existing words in a Markdown link without rewriting the sentence or changing its rendered formatting.
   - Use a relative `.md` path from the source page for internal links; for example, use `[control plane](../../glossary/control-plane.md)` in `docs/practice/operations/control-planes.md`.
   - If a later link to the same destination only defines the same term, move it to the first use rather than duplicating it; preserve later links that serve another purpose.
4. Review the diff to verify that only intended links changed and that each new or moved link points to the intended reference.
   - If any book page changed, run `uv run --locked zensical build --strict` from the repository root.
   - Report the pages scanned or changed, terms left unlinked and why, and the checks run.
