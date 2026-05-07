# Commit Message Checklist

This checklist records the repository preference for clear, detailed git
commit messages.

Use it whenever preparing a commit for meaningful research, writing, code,
or repository-organization changes.

## Main Principle

Each commit message should explain the change as a small research or
engineering decision, not just label the files that moved.

The reader should be able to understand:

1. what changed
2. why it changed
3. what the practical consequence was

## Required Structure

### 1. Start with a typed subject line

Prefer a concise imperative summary beginning with a prefix such as:

**General (code / simulation / engineering):**
- `feat:` — new feature or capability
- `fix:` — bug or error correction
- `refactor:` — restructure without behavior change
- `docs:` — documentation only
- `chore:` — maintenance, tooling, dependencies

**Academic writing / research:**
- `write:` — new or revised LaTeX prose, equations, sections
- `lit:` — literature changes (register paper, add reading note, update bibliography)
- `struct:` — structural reorganization (folder layout, section splits, path updates)
- `build:` — LaTeX build setup (preamble, build.py, packages)
- `meta:` — repo metadata (CLAUDE.md, TIMELINE.md, memory files, .gitignore)
- `note:` — exploratory notes, reading reviews, draft scratch work

The subject line should identify the main action clearly.

Examples:

- `meta: retarget repo for PhD-wide research workspace`
- `fix: correct w00005 neutral-coordinate positivity claim`
- `lit: register b00026 BFL2020 NOD paper with arXiv TeX source`
- `write: add NOD citation graph and restructure Literature by theme`
- `struct: reorganize pdf_papers into age_structured and opinion_dynamics subfolders`

### 2. Leave one blank line after the subject

Do not run the body into the subject line.

### 3. Use a bullet-point body

The body must use flat bullet points.

Each bullet should describe:

- the concrete change
- the reason for the change
- the mathematical, writing, or workflow effect when relevant

Do not write a body that is only a file list.

## Preferred Content

### 1. Explain both edit and purpose

Prefer:

- `- rewrite the README so the repository is described as a private PhD research workspace rather than a single age-structured-control project`
- `- tighten the w00005 citation path so the semigroup discussion points to the exact Webb chapter results actually used`

Avoid:

- `- update README`
- `- edit citations`

### 2. Group by change area when useful

If a commit touches several coherent areas, group the bullets by topic in
the wording itself.

Examples:

- documentation updates
- theorem/proof corrections
- experiment or figure changes
- bibliography or catalog changes

### 3. Mention rebuilt outputs when applicable

If the commit updates tracked artifacts, say so explicitly.

Examples:

- `- rebuild the w00005 PDF after the citation cleanup`
- `- regenerate the figure outputs so the tracked artifacts match the new simulation layout`

## Style Rules

- Keep the subject line short but specific.
- Prefer imperative verbs: `add`, `fix`, `rewrite`, `tighten`, `rebuild`, `register`.
- Prefer informative bullets over generic summaries.
- Use flat bullets only; do not nest them.
- If the commit fixes a mathematical overstatement, say exactly what claim was weakened or corrected.
- If the commit changes repository organization, say what was reclassified, renamed, or retargeted.

## When to Split a Commit

If a session touches several distinct areas, split them into separate commits
rather than bundling everything into one. Each commit should do one coherent
thing. Typical split boundaries:

- literature changes (lit:) are separate from writing changes (write:)
- structural reorganization (struct:) is separate from content edits
- build/preamble fixes (build:) are separate from prose changes
- simulation or experiment updates are separate from paper edits

When splitting, stage and commit each group independently before moving to
the next.

## Final Self-Check

Before committing, ask:

- Does the subject line use a clear prefix such as `feat:` or `fix:`?
- Would someone understand the commit without opening the diff first?
- Does each bullet explain both the edit and its purpose?
- Did I mention rebuilt PDFs, regenerated figures, or synced outputs if they changed?
