---
name: kb-query
description: "Query the knowledge base with a question. Synthesizes an answer from relevant KB files and optionally files the result back as a new KB article."
disable-model-invocation: true
---

# Knowledge Base Query

You are a knowledge base query engine. Your job is to answer questions by reading and synthesizing relevant KB files, then optionally filing valuable answers back into the wiki so explorations compound into the knowledge base.

## Frontmatter Schema

If filing an answer back as a KB page, use this frontmatter:

```yaml
---
tags: [topic-tag-1, topic-tag-2]       # Required: lowercase tags for discovery
related: [[source-kb-file]]            # Required: cross-references to KB files used in synthesis
created: YYYY-MM-DD                    # Required: date created
last-updated: YYYY-MM-DD              # Required: date last modified
pinned: false                          # Optional: default false
scope: "src/api/**"                    # Optional: glob pattern(s) for auto-matching. String or array.
type: synthesis                        # Required for filed queries: marks this as a synthesized answer
query: "the original question"         # Required for filed queries: the question that prompted this
sources: [[file1], [file2]]            # Required for filed queries: KB files consulted for the answer
---
```

**Resolving today's date (cross-platform, CRITICAL)**: Never guess, infer, or increment prior dates. When this skill writes `created` / `last-updated`, resolve today's date **once** at the start of the write phase, then reuse that single value for every write. Try these commands in order and use the first that returns a `YYYY-MM-DD` string:

- **macOS / Linux / WSL / Git Bash** (bash, zsh, sh): `date +%Y-%m-%d`
- **Windows PowerShell / pwsh**: `Get-Date -Format 'yyyy-MM-dd'`
- **Windows cmd.exe**: `powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd'"`
- **Portable fallback** (Node or Python available): `node -e "console.log(new Date().toISOString().slice(0,10))"` or `python -c "import datetime; print(datetime.date.today().isoformat())"`

Only update `last-updated` when the file's content actually changed. If an edit would leave the file byte-identical, do not rewrite it or bump the date.

## Obsidian-Compatible Related Links

When filing an answer with `related` entries in frontmatter, include a `## Related` section at the **end** of the file body with matching `[[wiki-links]]`. Keep frontmatter and body section in sync.

## Instructions

### Step 1: Get the Question

Check if the user provided a question after the command (e.g., `/kb-query How does the auth flow work?`).

- **If text was provided**: Use it as the query.
- **If no text was provided**: Use AskUserQuestion:
  - Question: "What would you like to know? I'll search the knowledge base and synthesize an answer."
  - Header: "KB Query"
  - Allow free-text input.

### Step 2: Prerequisite Check

1. **Check for `docs/kb/` directory**: If it doesn't exist, inform the user to run `/kb-init` first and stop.
2. **Check for KB files**: Glob for `.md` files under `docs/kb/` (excluding README.md, _index.md, _log.md). If none exist, inform the user: "No KB articles found. Add knowledge first with `/kb-learn`, `/kb-add`, or `/kb-discover`." and stop.

### Step 3: Find Relevant Pages

Use a multi-signal approach to find the most relevant KB files:

1. **Read `docs/kb/_index.md`** if it exists — this is the fastest way to understand what's in the KB. Scan the summaries and categories to identify potentially relevant pages.
2. **If `_index.md` doesn't exist**, read the CLAUDE.md Knowledge Base table for the page catalog.
3. **Keyword match**: Identify keywords in the question and match against file names, tags, and index summaries.
4. **Read candidate files**: Read the full content of the top candidate files (aim for 3-8 most relevant files, depending on the question scope).
5. **Follow cross-references**: If a relevant file has `related` references to files you haven't read yet that seem pertinent, read those too.
6. **Read `_global-learnings.md`** if it exists — check for any cross-cutting rules relevant to the question.

### Step 4: Synthesize Answer

Compose a comprehensive answer:

1. **Draw from multiple KB files** — the value of synthesis is connecting knowledge across pages.
2. **Cite sources** — reference which KB files contributed to each part of the answer using `[[wiki-links]]` (e.g., "According to [[server-tick-architecture]], the tick loop runs at 600ms...").
3. **Note contradictions** — if different KB files contain conflicting information, flag it explicitly.
4. **Note gaps** — if the question touches on topics not covered by the KB, say so. Suggest which `/kb-*` commands could fill the gap (e.g., "The KB doesn't cover deployment. You could run `/kb-discover src/deploy/` or `/kb-harvest` to add this knowledge.").
5. **Format appropriately** — use the format that best fits the answer:
   - Prose for explanatory answers
   - Bullet points for rules/conventions
   - Tables for comparisons
   - Code blocks for examples
   - Flowcharts or diagrams described in text for processes

Present the synthesized answer to the user.

### Step 5: Offer to File the Answer

After presenting the answer, offer to save it as a KB article. Use AskUserQuestion:

- Header: "File Answer to KB?"
- Question: "This synthesis drew from {count} KB files. Would you like to save it as a KB article so it's available in future sessions?"
- Options: "Save as KB article" | "Skip"

**When to encourage filing**: If the answer required synthesizing 3+ KB files, or if it produced a comparison, architectural overview, or decision rationale that would be valuable to reference later.

**When NOT to encourage filing**: If the answer was trivial, just quoted a single KB file, or is too specific to this moment to be reusable. In these cases, still offer but don't push.

If the user chooses "Skip", append a log entry (Step 7) and stop.

### Step 6: File the Answer

If the user chose to save:

#### 6a: Determine File Location

Suggest a path under `docs/kb/`. Prefer subfolder organization:
- Place synthesized answers in a logical category folder based on the topic (e.g., `docs/kb/architecture/`, `docs/kb/conventions/`, etc.)
- Use a descriptive filename based on the question topic (e.g., `docs/kb/architecture/auth-flow-overview.md`)

Use AskUserQuestion:
- Header: "KB File Location"
- Question: "Where should this be saved?"
- Options: Suggested path | "Different location" (free-text)

#### 6b: Write the KB File

1. **Reformat the answer** into KB style:
   - Concise, actionable, imperative voice where appropriate
   - Clear headings for scannability
   - Remove conversational phrasing ("As mentioned earlier...", "To answer your question...")
   - Keep citations as `[[wiki-links]]`

2. **Add frontmatter** with:
   - `type: synthesis` to mark this as a filed query result
   - `query: "the original question"` for context
   - `sources: [[file1], [file2]]` listing all KB files consulted
   - `related` pointing to the most relevant source KB files
   - Appropriate `tags` and `scope`
   - Today's date (resolved once via the cross-platform command in the Frontmatter Schema section) for `created` and `last-updated`

3. **Add `## Related` body section** mirroring the `related` frontmatter.

4. **Add reverse cross-references**: Update the `related` frontmatter and `## Related` body sections of the source KB files to point back to this new synthesis article. Update their `last-updated` to the resolved date (only for files that actually changed).

#### 6c: Register in CLAUDE.md

1. Add a row to the Knowledge Base table with appropriate Topic, File, and When to Load. Format the "When to Load" column using the structured format: `` `scope-glob1`, `scope-glob2` — tag1, tag2 ``. For synthesis articles, use the scope and tags of the source files that contributed most to the answer. For pinned files, use `Always (pinned)`.
2. Keep the table sorted alphabetically by Topic.

### Step 7: Update Index and Log

#### Update `docs/kb/_index.md`

If `_index.md` exists, add an entry for the new article in the appropriate category section with a one-line summary.

#### Append to `docs/kb/_log.md`

If `_log.md` exists, append:

```markdown
## [YYYY-MM-DD] query | {brief topic}
- Question: "{the original question}"
- Consulted: {list of KB files read}
- Result: {Filed as docs/kb/path/file.md | Not filed}
```

### Step 8: Confirm

Display:
- The synthesized answer (already shown in Step 4)
- If filed: the file path, tags, and cross-references added
- If not filed: a note that the answer is in chat history only
