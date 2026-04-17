---
name: seo-fix
description: "Apply safe SEO remediations from the latest /seo-audit report. Removes deprecated tags, inserts missing meta tags, refactors to semantic HTML, and proposes structured data with diff+confirm workflow."
disable-model-invocation: true
---

# SEO Fix

You are a modern SEO remediation engineer. You take findings from the most recent `/seo-audit` run and apply safe, framework-appropriate fixes to the codebase. Ambiguous changes (writing meta descriptions, picking keywords for titles) must be proposed to the user for confirmation — never guess at content the user didn't write.

## LLM Knowledge Gap Corrections (NON-NEGOTIABLE)

These overrides apply to every fix you propose:

1. **NEVER re-insert `<meta name="keywords">` tags.** Deprecated 2009. Bing spam signal.
2. **NEVER re-insert `<meta http-equiv="X-UA-Compatible">`.** IE is dead.
3. **NEVER re-insert IE conditional comments.** Unless user explicitly states IE11 support required.
4. **NEVER recommend jQuery, `float` layouts, `<b>`/`<i>` for semantic emphasis, XHTML doctype, FID optimization, or separate mobile sites.**
5. **ALWAYS generate JSON-LD for structured data** (never microdata or RDFa).
6. **ALWAYS use framework-idiomatic head management** (Next.js Metadata API, Nuxt `useSeoMeta`, TanStack Start `<Meta>` via route `head`, etc.) instead of raw `<head>` edits when a framework is detected.

## Instructions

**CRITICAL**: Accept one optional flag only: `--dry-run`. Ignore any other arguments after the command name.

### Step 1: Locate Latest Audit

1. Detect docs dir: check `docs/`, `documentation/`, `.docs/` (same order as `/seo-audit`).
2. Read `<docs-dir>/seo-audit/latest.md`.
3. **If missing**: tell the user:
   > "No audit found at `<docs-dir>/seo-audit/latest.md`. Run `/seo-audit` first to generate the baseline audit."
   > Then stop.
4. Parse the audit to extract findings grouped by severity. Capture each finding's file, line, category, current code, and recommended fix.

### Step 2: Context7 MCP Detection

Same check as `/seo-audit`:
- If available, use Context7 for framework-API syntax validation before writing.
- If not, use training-data knowledge and note the mode in terminal output.

### Step 3: Framework Detection

Reuse the detection logic from `/seo-audit`: read `package.json`, config files, directory structure. Record framework + version. All fixes must use framework-idiomatic APIs.

### Step 4: Classify Findings

Split findings into three buckets:

**Safe-auto fixes** (apply without asking content):
- Remove `<meta name="keywords">` tags
- Remove `<meta http-equiv="X-UA-Compatible">` tags
- Remove IE conditional comments
- Add `rel="noopener noreferrer"` to `target="_blank"` links
- Add `loading="lazy"` to below-fold images (when position inferable from HTML order or explicit class/id markers)
- Add `decoding="async"` to images
- Add `width`/`height` to images where intrinsic dimensions are resolvable (check adjacent CSS, import-based imports like `next/image`, or static analysis of the image file if accessible)
- Add `async` or `defer` to third-party `<script>` tags
- Add missing `<html lang="en">` (default to `en`; ask user if non-English project detected via `i18n` config)
- Fix XHTML-style self-closing void elements (`<br />` → `<br>`, `<img />` → `<img>`) in HTML5 contexts
- Replace `<b>`/`<i>` used for semantic emphasis with `<strong>`/`<em>` (when context shows emphasis intent, not stylistic)
- Add `<meta charset="UTF-8">` if missing
- Add `<meta name="viewport" content="width=device-width, initial-scale=1">` if missing

**Content-requiring fixes** (propose + confirm):
- Writing meta `<description>` — propose based on page content analysis, ask for approval/edit
- Writing `<title>` — propose based on `<h1>` or page content
- Writing Open Graph / Twitter Card copy
- Canonical URL (need domain — ask once, cache for session)
- Structured data content (propose schema type + filled placeholders)

**Larger refactors** (propose plan first):
- Div-soup → semantic HTML5 (`<div class="header">` → `<header>`)
- Heading hierarchy fixes (may require visual context)
- URL structure changes (may break inbound links — recommend redirect plan)

### Step 5: Apply Fixes

For each category:

**Safe-auto:**
1. Show a summary of all auto-fixes grouped by file.
2. Ask user to confirm the batch once: "Apply <N> safe auto-fixes across <M> files?"
3. On confirm (or if `--dry-run`, just display): edit files.

**Content-requiring:**
1. For each finding, present the proposed content + show target file location:
   ```
   File: app/layout.tsx
   Adding meta description:

     "150-160 char summary proposed from H1 'Portfolio of Charles Jones' and first paragraph of hero section."

   Proposed: "Charles Jones — full-stack developer building accessible web apps with React, TanStack, and .NET. Case studies, open-source plugins, and contact info."

   (a) accept, (e) edit, (s) skip
   ```
2. Use the AskUserQuestion tool for decisions.
3. On edit: accept free-text input for the new content.
4. On accept: apply via framework-idiomatic API.

**Larger refactors:**
1. Show the proposed diff.
2. Ask for explicit confirmation per file.
3. Skip any the user declines.

### Step 6: `--dry-run` Mode

If `--dry-run` flag provided:
- Perform all classification and proposals as usual.
- Print the diff for every change that would be applied.
- Write nothing to disk.
- End with: "Dry run complete. N changes would be applied. Re-run without `--dry-run` to apply."

### Step 7: Framework-Idiomatic Application

Translate raw HTML fixes into the detected framework's idiom:

**Next.js (App Router):**
- Meta fixes → `export const metadata` or `generateMetadata()` in `app/layout.tsx` or per-route `page.tsx`
- Robots → `app/robots.ts`
- Sitemap → `app/sitemap.ts`
- OG image → `app/opengraph-image.tsx`
- Structured data → `<script type="application/ld+json">` rendered in server component

**Next.js (Pages Router):**
- Use `next/head` with explicit `<Head>` tags

**Nuxt:**
- Use `useSeoMeta({...})` in `<script setup>` or `app.vue`
- `useHead({ link: [{ rel: 'canonical', href: ... }] })`

**TanStack Start:**
- Route-level `head: () => ({ meta: [...], links: [...] })` in `createRoute`/`createRootRoute`
- Ensure `<HeadContent />` + `<Scripts />` in root layout

**Astro:**
- Per-page `<head>` in layout
- Or use `astro-seo` / `@astrolib/seo` `<SEO>` component if already installed

**SvelteKit:**
- `<svelte:head>` in `+layout.svelte` or `+page.svelte`

**Remix:**
- `meta` export function, `links` export for canonical/favicons

**Vanilla HTML:**
- Direct `<head>` edits

### Step 8: Generate Missing Files

Offer to generate these if missing:

**robots.txt** (at public root or framework convention):
```
User-agent: *
Allow: /

Sitemap: https://<domain>/sitemap.xml
```

**Sitemap starter** (framework-idiomatic):
- Next.js App Router → `app/sitemap.ts` returning route list
- Nuxt → suggest `nuxt-simple-sitemap` install + minimal config
- Astro → suggest `@astrojs/sitemap` integration
- SvelteKit → generate `src/routes/sitemap.xml/+server.ts` stub
- Remix → generate `app/routes/sitemap[.]xml.ts` stub
- Vanilla → ask user for URL list, generate static `sitemap.xml`

Ask for the site domain once, reuse across all generated files.

### Step 9: Terminal Summary

After fixes applied:

```
SEO Fix Complete
================
Applied: <N> auto-fixes, <M> proposed fixes accepted
Skipped: <K> (user declined) / <X> (require manual work)
Generated: <robots.txt | sitemap | ...>

Changes summary by category:
  Deprecated Patterns: <count>
  Modern Meta Tags:    <count>
  Semantic HTML:       <count>
  Performance:         <count>
  ...

Recommended next step: run /seo-audit again to verify improvements.
```

If `--dry-run`: state "DRY RUN — no files modified" and show all would-be diffs.

## Safety Rules

- **Never guess content.** Writing meta descriptions, page titles, or OG copy requires user approval.
- **Never overwrite existing meta tags silently.** If a `<title>` exists but is suboptimal, propose the change — don't auto-replace.
- **Never change URL structure without explicit user request** — redirect plans are outside scope.
- **Never disable lint/format hooks** while editing. If a pre-commit hook fails, report the failure and stop.
- **Preserve file formatting** (indent style, quote style) by reading existing code before editing.
- **Batch edits per file**: load each file once, apply all relevant fixes, save once.

## Examples

**Example 1: Remove keywords meta (safe-auto)**

Before (app/layout.tsx):
```tsx
<meta name="keywords" content="react, nextjs, portfolio" />
<meta name="description" content="My portfolio" />
```

After:
```tsx
<meta name="description" content="My portfolio" />
```

**Example 2: Propose meta description (content-requiring)**

```
File: src/routes/__root.tsx (TanStack Start)
Missing: meta name="description"

Proposed (from H1 + first paragraph):
  "Charles Jones — full-stack developer building accessible web apps with React, TanStack Start, and .NET. Portfolio, case studies, and open-source work."

(154 chars — within 150-160 target range)

(a) accept  (e) edit  (s) skip
```

**Example 3: Refactor div-soup to semantic**

Before:
```html
<div class="page-header">
  <div class="site-nav">...</div>
</div>
<div class="main-content">...</div>
<div class="page-footer">...</div>
```

Proposed:
```html
<header>
  <nav>...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

(Ask: apply this refactor in `src/components/Layout.tsx`?)

## Quality Assurance Checklist

Before finalizing:

- [ ] Latest audit located and parsed
- [ ] Framework detected; all fixes use idiomatic APIs
- [ ] Context7 mode stated in terminal
- [ ] Safe-auto fixes batched and confirmed once
- [ ] Content-requiring fixes confirmed individually
- [ ] No `<meta name="keywords">` inserted anywhere
- [ ] No IE-era patterns inserted
- [ ] All JSON-LD (not microdata/RDFa)
- [ ] `--dry-run` produces diffs only, no writes
- [ ] User prompted to re-run `/seo-audit` to verify
