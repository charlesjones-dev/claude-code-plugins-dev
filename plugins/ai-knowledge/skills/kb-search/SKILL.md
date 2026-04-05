---
name: kb-search
description: "Search across all KB files in docs/kb/ for a keyword, topic, or tag. Returns matching files and relevant excerpts."
disable-model-invocation: true
---

# Knowledge Base Search

You are a knowledge base search assistant. Your job is to search across the project's KB files for relevant information using content, tags, and cross-references.

## Instructions

### Step 1: Get Search Query

Check if the user provided a search term after the command (e.g., `/kb-search authentication` or `/kb-search tag:security`).

- **If a term was provided**: Use it as the search query.
- **If no term was provided**: Use AskUserQuestion to ask:
  - Question: "What keyword or topic would you like to search for in the knowledge base?"
  - Header: "KB Search"
  - Allow free-text input.

### Step 2: Parse Query Type

Determine the search mode:
- **Tag search**: If the query starts with `tag:` (e.g., `tag:security`), search frontmatter `tags` arrays.
- **Content search**: Otherwise, search file content, names, and tags.

### Step 3: Search KB Files

1. **Glob** for all `.md` files under `docs/kb/` (excluding `docs/kb/README.md`).
2. If no KB files exist, inform the user: "No KB files found in `docs/kb/`. Run `/kb-init` to set up the knowledge base." and stop.
3. For each KB file, read its frontmatter and content.

**For tag search:**
- Match the query tag against each file's `tags` array (case-insensitive).
- Also check `related` references for files that link to matching files.

**For content search:**
- **Grep** across all found KB files for the search query (case-insensitive).
- Check file names and directory names for matches (e.g., searching "api" should match `docs/kb/api-conventions.md`).
- Check frontmatter `tags` for matches (a content search for "security" should also surface files tagged `security`).

### Step 4: Search Global Learnings

1. Read `docs/kb/_global-learnings.md` if it exists (this is the dedicated global learnings KB file).
2. Check if any global learning entries match the search query.
3. Also check CLAUDE.md for a legacy `### Global Learnings` inline section (older KB setups may still have this). If found, search it too.

### Step 5: Display Results

Present results grouped by source, including frontmatter metadata:

```
KB Search Results for: "{query}"
================================

KB Files with matches:

1. docs/kb/api-conventions.md
   Tags: [api, rest, conventions]
   Related: [[auth]], [[database]]
   Last updated: 2026-04-01 | Pinned: No
   > Matching excerpt line 1
   > Matching excerpt line 2

2. docs/kb/auth/tokens.md
   Tags: [auth, security, tokens]
   Related: [[api-conventions]]
   Last updated: 2026-03-28 | Pinned: Yes
   > Matching excerpt

Also related (via cross-references):
3. docs/kb/database.md — related to matched file api-conventions.md

Global Learnings:
   > Matching learning entry

Found {count} match(es) across {file_count} file(s).
```

If no results found:
> "No matches found for '{query}' in the knowledge base. The KB currently has {file_count} file(s) with tags: {unique tags list}."
