---
name: audit-markdown-citations
description: Audit and fix Markdown citations and factual claims by checking existing evidence, finding better sources, correcting errors, and removing unsupported claims. Use for fact-checking documentation or finding authoritative references for definitions, architecture, and behavior. Do not use for a broken-link check, copyediting, or adding first-use term links alone.
---

# Audit Markdown citations

A link is not proof: check whether the cited material supports the specific claim in the article.
By default, audit the requested scope, apply evidence-backed fixes, and report what changed.
If the user explicitly asks for an audit, findings, or recommendations only, do not edit the articles.

## 1. Inventory the Markdown files

1. Read the applicable repository and directory instructions.
2. If the user supplies Markdown files or directories, scan only those inputs and recursively include all regular `.md` files under those directories, including hidden or ignored files, but not version-control metadata.
   - Resolve paths relative to the workspace unless given as absolute paths, and report invalid or unreadable inputs rather than expanding to the whole repository.
   - Follow links from an article to inspect evidence if needed, but do not add the linked files to the audit scope.
3. With no path, use the repository root and enumerate all tracked and non-ignored untracked `.md` files, including hidden Markdown and translations.
   - In Git, use `git ls-files --cached --others --exclude-standard -z -- ':(icase,glob)**/*.md'` from the root and keep the NUL-delimited paths intact.
   - In a workspace without Git, recursively enumerate Markdown from the workspace root, excluding identifiable dependency caches, generated output, and version-control metadata; report those exclusions.
4. Build a deduplicated file list before auditing; match `.md` case-insensitively and do not follow symlinks in the inventory.
   - Track each file as queued, inventoried, audited, or unreadable, and process large inventories in batches without silently dropping later files.

## 2. Read each article and record its claims

1. For each file in the inventory, read it from start to finish, including headings, tables, notes, captions, and diagrams.
2. Record each independently checkable claim as a separate item, even when several occur in one sentence.
   - Include first-use technical definitions and externally verifiable claims about architecture, component relationships, behavior, guarantees, defaults, versions, history, comparisons, and measurements.
   - Treat each meaningful diagram relationship or ordering as a claim; review code examples for what they assert about behavior, not every line of syntax.
   - Record author preferences and explicitly hypothetical examples as not needing external evidence unless they rely on a factual premise.
   - For a logical inference, record the premises and check that the conclusion follows; verify externally checkable premises separately and do not present an inference as a sourced fact.
3. Record the file and line range or heading, the exact claim or a faithful short paraphrase, relevant conditions, and any existing citation.
   - Resolve inline links, reference-style links, footnotes, and nearby figure credits by the claims they are attached to, not just by proximity.
   - An internal glossary or cross-reference can define a term, but trace its evidence before treating it as support for an external claim.
   - Record the earlier location of a possible repeat citation so you can verify it in the next pass.

## 3. Check citations and research gaps

1. After the inventory pass, open existing sources and read the exact passage or figure that is meant to support each claim.
   - Compare the product, version, platform, configuration, and other limits; a relevant title or a successful HTTP response is not evidence.
   - Distinguish a value set in this repository from a product default, an example from a guarantee, and a recommended setting from observed behavior.
   - Treat a later mention as `Cited earlier` only if the same article already cites adequate evidence for the same claim or meaning under the same conditions and the connection is clear.
   - A repeated term with a new claim, different meaning, or different scope needs its own check; citations in other articles or editions do not count as `Cited earlier`.
2. Group remaining gaps by equivalent claim and scope, then search for evidence once per group while retaining every affected article location.
   - For repository behavior, start with local code and configuration and check the locked version before using upstream documentation or source.
   - Prefer standards and specifications for standard behavior, versioned maintainer docs or source for product behavior, and original studies or reproducible results for measurements.
   - Use reliable secondary sources if primary evidence is insufficient; seek independent evidence for broad comparisons and do not generalize vendor claims to an entire category.
   - Open each candidate and record its direct URL or repository path, exact section or figure, applicable version or revision, and what it supports.
   - Treat search snippets as leads only, and do not send sensitive or unpublished text to external search services.
3. If evidence conflicts, compare its scope and dates, document the conflict, and identify any narrower wording the evidence supports.
   - If no adequate source is found after a targeted search of relevant primary sources and credible alternatives, record the sources or queries checked and the gap that remains.
   - If the appropriate evidence set was searchable but contains no supporting record, record `No adequate source found` and apply the removal rule; a record that might exist somewhere is not a search blocker.
   - Record `Research blocked` only when an applicable source or necessary search channel cannot be inspected, such as a known record that requires access you do not have.
   - Neither outcome proves the claim false.

### Labels

Use one **evidence** label per claim and assess each source's **authority** for that claim; preserve the original labels even when a better source is found.

| Evidence | Use when |
| --- | --- |
| `Supported` | The evidence directly supports the claim as written and in scope. |
| `Partial support` | The source supports only part of the claim or supports a narrower version of it. |
| `Wrong scope` | The source covers the topic, but for a different version, platform, or set of conditions. |
| `Unrelated` | The source does not address the claim. |
| `Contradicted` | In-scope evidence explicitly disagrees with the claim. |
| `Missing citation` | No citation is attached or clearly applicable from earlier in the article. |
| `Cited earlier` | An earlier citation in the same article adequately supports this repeat. |
| `Unverified` | The cited material could not be inspected or the available evidence did not resolve a conflict. |
| `No citation needed` | The item is not a factual assertion or is a clear inference from verified premises. |

| Authority | Use when |
| --- | --- |
| `Primary` | The source owns the specification or implementation, or reports the original evidence. |
| `Reliable secondary` | A credible independent source explains the subject and identifies its evidence. |
| `Insufficient authority` | The source is identifiable but lacks the expertise or evidence needed for this claim. |
| `Questionable source` | There is a specific reason to doubt the source, such as misattribution or evidence it misrepresents. |
| `Not assessed` | No source was cited or the source could not be inspected. |

`Supported` does not make a source authoritative, and `Primary` does not make it relevant or correct for the claim's scope.

### Diagrams

- Suggest a Mermaid diagram only if it explains a verified relationship, boundary, or sequence better than prose.
- For example, [Docker's container overview](https://www.docker.com/resources/what-container/) is a candidate for a basic definition and a figure about containers versus virtual machines; verify the relevant section before using it, and do not use it alone to support a security guarantee.
- Draw an original diagram from verified facts and cite the supporting sections or figures in a nearby caption.
  - If adapting a source's visual expression rather than illustrating the facts independently, verify reuse terms and provide the required attribution; if reuse is unclear, do not adapt it.

## 4. Apply fixes and verify them

1. Choose the smallest fix for each finding; recommend it without applying it in a report-only run.
   - **Cite**: Add or replace the reference only if the evidence supports all of the wording, including terms such as “default,” “always,” or “only.”
   - **Correct**: If reliable evidence supports only a narrower claim, replace the unsupported wording, cite the evidence, and preserve supported details.
   - **Remove**: For `No adequate source found`, remove only the unsupported claim or diagram element and preserve the meaning of the supported material around it.
   - **Keep**: Leave an adequately cited repeat alone; if research was blocked or credible sources still conflict, flag the unresolved claim instead of silently deleting it.
2. Edit only audited files within the authorized scope, and preserve unrelated changes.
   - Follow repository citation and translation rules; report any required updates outside the requested scope rather than silently expanding the edit.
   - Review the diff for broken references and inconsistencies in nearby text and figures, then run the repository's required checks.
   - After changing Mermaid, verify rendering and narrow-screen readability.

## 5. Report the outcome

1. Lead with a change summary: the scope, files inventoried, audited, and changed, and counts of citations added or replaced, claims corrected or removed, and unresolved claims.
   - For a report-only run, label these as proposed changes and state that the articles were not modified.
   - State any exclusions or unreadable files and the checks run.
2. Give a file-by-file findings list with the claim location, evidence label, original source and authority when applicable, and what changed and why.
   - For corrections, show the previous and corrected meaning; for citation changes, identify the added or replaced source.
   - Link directly to verified replacement evidence and state what it supports; for removals, name the unsupported claim and summarize the search.
   - For `Cited earlier`, point to the first citation and leave the repeat alone.
   - Count claims that need no change and list unresolved claims separately from completed fixes.
   - If the findings exceed one response, work in reported batches or save the full report at a user-authorized path; do not present a sample as an exhaustive audit.
3. Mark the audit complete only when every in-scope file has been read and every claim checked or explicitly reported as unresolved; identify any unread or pending work separately.
