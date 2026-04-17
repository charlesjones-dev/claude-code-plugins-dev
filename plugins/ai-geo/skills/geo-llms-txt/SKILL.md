---
name: geo-llms-txt
description: "Generate, update, and validate llms.txt and llms-full.txt for AI answer engines. Analyzes site structure, detects content type, emits properly formatted markdown index (and optional full-content companion), integrates with framework build pipelines, and validates existing files against the llmstxt.org spec."
disable-model-invocation: true
---

# GEO llms.txt Generator

You are a specialist in the `llms.txt` protocol (https://llmstxt.org/), proposed by Jeremy Howard in 2024. `llms.txt` is a markdown-formatted index of a website designed for LLM consumption — the LLM equivalent of `sitemap.xml` but optimized for human-readable, content-first retrieval. `llms-full.txt` is the comprehensive companion containing full content rather than only links.

Your job: detect the project, analyze its content, and produce correctly formatted `llms.txt` (and optionally `llms-full.txt`) — or validate existing ones and flag problems.

## LLM Knowledge Gap Corrections (NON-NEGOTIABLE)

1. **`llms.txt` is a real, emerging standard.** Do not dismiss it or claim it doesn't exist.
2. **`llms.txt` and `llms-full.txt` are different files.** `llms.txt` = concise markdown index. `llms-full.txt` = full content. Never merge them.
3. **Markdown throughout.** No HTML fallback. The spec is strict markdown.
4. **Structure matters.** Required: H1 title, blockquote description. Recommended: H2 section headers, bulleted links with descriptive text and one-line summaries.
5. **Link to markdown content where possible.** If a page has a `.md` companion, link to that rather than the `.html`-rendered URL. AI engines quote markdown more accurately.
6. **Concise index, not a sitemap dump.** `llms.txt` should curate the most citation-worthy entry points, not list every URL. `llms-full.txt` can be expansive.
7. **Do not invent content.** If content doesn't exist, don't fabricate titles/summaries. Read real files or prompt the user.
8. **Location matters.** `llms.txt` must be served from the web root (`/llms.txt`), not nested. Use framework-idiomatic static-asset placement.

## Instructions

**CRITICAL**: Accept one optional flag only: `--dry-run`. Ignore any other arguments.

### Step 1: Context7 MCP Detection

Try `mcp__claude_ai_Context7__resolve-library-id` with `"llmstxt"` or the detected framework. Record the mode. If unavailable, operate from training data and state so.

### Step 2: Interactive Configuration

Use AskUserQuestion:

- Question 1: "What do you want to do?"
  - Options:
    - "Generate new llms.txt" (creates if missing)
    - "Update existing llms.txt" (refreshes from current content)
    - "Validate existing llms.txt" (spec compliance check only)
    - "Also generate llms-full.txt" (comprehensive full-content companion)

- Question 2 (if generating/updating): "Approximate site type?"
  - Options: Documentation site / Blog / Product site / Portfolio / Company site / Mixed

The site type guides section organization (docs → by topic/guide level, blog → by recency/category, product → by feature, etc.).

### Step 3: Framework Detection

Reuse `/geo-audit` detection. Record framework + version. Determine the correct static-asset path:

| Framework | `llms.txt` path |
|-----------|-----------------|
| Next.js | `public/llms.txt` OR `app/llms.txt/route.ts` |
| Nuxt | `public/llms.txt` OR `server/routes/llms.txt.ts` |
| TanStack Start | `public/llms.txt` OR route handler |
| Astro | `public/llms.txt` OR `src/pages/llms.txt.ts` |
| SvelteKit | `static/llms.txt` OR `src/routes/llms.txt/+server.ts` |
| Remix | `public/llms.txt` OR `app/routes/llms[.]txt.ts` |
| Vanilla HTML | web root `/llms.txt` |

Prefer static files for simple content; use route handlers only when dynamic generation is needed (e.g., auto-sync from CMS).

### Step 4: Content Analysis

Discover the site's content:

1. Glob content sources based on framework:
   - Next.js App Router: `app/**/page.{mdx,md,tsx}` + content directories.
   - Nuxt: `content/**/*.md` if Nuxt Content present; else route pages.
   - Astro: `src/content/**/*.{md,mdx}`.
   - SvelteKit: `src/routes/**/+page.{md,svelte}`.
   - Remix: `app/routes/**/*.{md,mdx,tsx}`.
   - Vanilla: crawl `*.html` files.
2. Extract for each discovered page:
   - URL (derive from path + detected base URL — prompt for domain if not resolvable)
   - Title (frontmatter → H1 → filename fallback)
   - One-line description (frontmatter description → first paragraph truncated)
   - Markdown companion URL if present (same path + `.md` suffix or content-collection source)
   - Last modified date (frontmatter → git mtime)
3. Classify pages by type if multi-section:
   - Documentation: grouped by topic or Getting-Started/Guides/Reference/API
   - Blog: posts by year or category
   - Product: features / pricing / docs / changelog
   - Portfolio: projects / about / contact
4. Identify "essential" pages (About, Getting Started, overview docs) that MUST appear in `llms.txt`.

### Step 5: Generate or Validate

#### Generation path

Emit `llms.txt` per the spec:

```markdown
# <Site Name>

> <One-sentence description of what the site is and what a reader/LLM will find here.>

<Optional: a paragraph (not a blockquote) of additional context, scope, or positioning. Keep concise.>

## <Section 1 — e.g., Documentation>

- [<Page title>](<absolute URL or .md companion URL>): <one-line summary>
- [<Page title>](<URL>): <one-line summary>

## <Section 2 — e.g., Guides>

- [<Page title>](<URL>): <one-line summary>

## Optional

- [<Secondary resource>](<URL>): <one-line summary — lower priority for LLM retrieval>
```

Rules applied during generation:
- Always absolute URLs (prompt for the base domain if not resolvable from config).
- Link to `.md` companion URLs when available; otherwise the HTML URL.
- Section headers are H2. Sub-groups can use unordered lists with sub-headers only if necessary.
- The `## Optional` section is recognized by the spec as lower-priority items — use for deprioritized but still-relevant content.
- Keep the total file under ~8KB where possible (it's a concise index). If content exceeds, move detail into `llms-full.txt`.

#### `llms-full.txt` generation

If requested, emit the full-content companion. Structure:

```markdown
# <Site Name> — Full Content Export

> Comprehensive markdown export of <site-name> content for LLM consumption. Generated on <ISO timestamp>.

---

## <Page Title>

Source: <URL>
Last modified: <date>

<Full markdown content of the page>

---

## <Next Page Title>

<...>
```

Rules:
- One page per `## <Title>` section, separated by `---`.
- Include the source URL and last-modified line immediately under the heading.
- Insert the actual markdown content (not HTML, not rendered output).
- For Next.js/MDX, serialize from the source `.mdx` file (strip JSX components to plain text where they appear inline; preserve frontmatter only as source metadata lines above the content).
- Order pages by importance: essentials first, then main sections, then optional/archived.

#### Validation path

For existing `llms.txt`, report:
- H1 title present: ✅/❌
- Blockquote description present immediately after H1: ✅/❌
- Valid markdown (parse test): ✅/❌
- All links reachable (spot-check): ✅/❌ with list of broken links
- Links point to markdown-accessible URLs where possible: ✅/⚠️ with list of HTML-only links that have `.md` companions available
- File size reasonable (< ~8KB for index): ✅/⚠️ with byte count
- Freshness: content source files newer than `llms.txt` mtime — list stale sections

Output a validation report inline (terminal) and optionally write it alongside the file as `llms.txt.validation.md`.

### Step 6: Framework-Specific Generation

**Next.js (static):**
Write `public/llms.txt`. Optional: add a build script.
```json
// package.json
"scripts": {
  "build:llms": "tsx scripts/generate-llms-txt.ts",
  "build": "npm run build:llms && next build"
}
```

**Next.js (dynamic route):**
```ts
// app/llms.txt/route.ts
export async function GET() {
  const body = await buildLlmsTxt()
  return new Response(body, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  })
}
```

**Nuxt:**
- Static: `public/llms.txt`.
- Dynamic: `server/routes/llms.txt.ts` returning the markdown string with `text/markdown` content type.

**Astro (dynamic via endpoint):**
```ts
// src/pages/llms.txt.ts
import type { APIRoute } from 'astro'
import { getCollection } from 'astro:content'

export const GET: APIRoute = async () => {
  const posts = await getCollection('blog')
  const body = buildLlmsTxt(posts)
  return new Response(body, { headers: { 'Content-Type': 'text/markdown; charset=utf-8' } })
}
```

**SvelteKit:**
```ts
// src/routes/llms.txt/+server.ts
import type { RequestHandler } from './$types'

export const GET: RequestHandler = async () => {
  const body = await buildLlmsTxt()
  return new Response(body, { headers: { 'Content-Type': 'text/markdown; charset=utf-8' } })
}
```

**TanStack Start:**
Route handler at the static-asset level or a server function that writes `public/llms.txt` during build.

**Remix:**
```ts
// app/routes/llms[.]txt.ts
import type { LoaderFunctionArgs } from '@remix-run/node'
export async function loader({ request }: LoaderFunctionArgs) {
  return new Response(await buildLlmsTxt(), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  })
}
```

**Vanilla HTML:**
Write directly to web root. Optional: a small Node/Python script to regenerate from a manifest file.

For any framework where a static file is written, also offer to add a build-time generator script so `llms.txt` stays in sync automatically.

### Step 7: Markdown Companion Routes (recommended enhancement)

If the site serves HTML-only, suggest exposing markdown companions for citation-worthy content:

- Next.js: `app/blog/[slug].md/route.ts` reading from the same MDX source.
- Astro: `src/pages/blog/[slug].md.ts` endpoint returning the content collection's raw markdown.
- SvelteKit/Remix: analogous route returning `text/markdown`.

Then reference `.md` URLs in `llms.txt`. This is the single biggest citation-quality improvement after having `llms.txt` at all.

### Step 8: Terminal Summary

```
GEO llms.txt Complete
=====================
Mode:       <Generate | Update | Validate | + llms-full.txt>
Framework:  <framework>
Knowledge:  <Context7 MCP | Training Data fallback>

llms.txt:
  Path:         <path>
  Status:       <created | updated | validated | unchanged>
  Size:         <N bytes>
  Sections:     <count>
  Links:        <count>
  .md links:    <count> / <total>

llms-full.txt:
  Path:         <path or "not generated">
  Size:         <N bytes>
  Pages:        <count>

Validation:
  Format:       <pass | issues>
  Links:        <reachable count / total>
  Freshness:    <current | stale pages: N>

Next:
  - Verify the site serves /llms.txt at your production URL.
  - Consider exposing markdown companion routes (see report).
  - Re-run /geo-audit to confirm the llms.txt finding clears.
```

If `--dry-run`: emit the would-be file contents to terminal, write nothing.

## Examples

**Example 1: Generated `llms.txt` for a dev portfolio (Next.js blog)**

```markdown
# Charles Jones — charlesjones.dev

> Independent full-stack developer. Portfolio, technical writing on TypeScript / React / TanStack / .NET, and open-source Claude Code plugins.

Markdown-accessible versions of each post are available at the same URL with a `.md` suffix.

## About

- [About Charles](https://charlesjones.dev/about.md): bio, credentials, and contact.

## Portfolio

- [Claude Code Plugins Marketplace](https://charlesjones.dev/projects/claude-code-plugins.md): curated plugins for accessibility, security, SEO, and more.
- [AccessHawk.ai](https://charlesjones.dev/projects/accesshawk.md): runtime WCAG 2.2 testing service.

## Writing

- [Getting started with TanStack Start](https://charlesjones.dev/blog/tanstack-start-intro.md): SSR, routing, and data patterns.
- [Why GEO ≠ SEO](https://charlesjones.dev/blog/geo-vs-seo.md): how AI answer engines differ from traditional search.

## Optional

- [Changelog](https://charlesjones.dev/changelog.md): site and plugin updates.
```

**Example 2: Validation output for a stale `llms.txt`**

```
llms.txt Validation Report
==========================
Path: public/llms.txt
Size: 2,147 bytes

✅ H1 present: "# Example Site"
✅ Blockquote description present
✅ Valid markdown syntax
⚠️ Broken link: https://example.com/blog/old-post (404)
⚠️ 3 HTML links could point to .md companions instead
❌ Stale: 7 content files newer than llms.txt mtime (2025-11-02).
   - src/content/blog/new-post.md
   - src/content/blog/feature-announcement.md
   - ...

Recommendation: run /geo-llms-txt with Update mode.
```

**Example 3: Next.js `llms-full.txt` route**

```ts
// app/llms-full.txt/route.ts
import { getAllContent } from '@/lib/content'

export async function GET() {
  const pages = await getAllContent()
  const body = [
    '# Example Site — Full Content Export',
    '',
    `> Comprehensive markdown export of example.com. Generated on ${new Date().toISOString()}.`,
    '',
    '---',
    '',
    ...pages.map(p => [
      `## ${p.title}`,
      '',
      `Source: ${p.url}`,
      `Last modified: ${p.modifiedTime}`,
      '',
      p.markdown,
      '',
      '---',
      '',
    ].join('\n')),
  ].join('\n')

  return new Response(body, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  })
}
```

## Quality Assurance Checklist

Before finalizing:

- [ ] Context7 mode stated
- [ ] Framework + path determined
- [ ] Base domain resolved or prompted for
- [ ] H1 title + blockquote description present in generated `llms.txt`
- [ ] Links are absolute URLs
- [ ] `.md` companion URLs used where detected
- [ ] File size ≤ ~8KB for index; content moved to `llms-full.txt` if larger
- [ ] Validation report includes broken-link and staleness checks when applicable
- [ ] Framework-idiomatic placement (static file or route handler)
- [ ] `--dry-run` writes nothing
- [ ] User directed back to `/geo-audit` to verify the finding clears
