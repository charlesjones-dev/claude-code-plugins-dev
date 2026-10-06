# AI-SEO Plugin

**Catches the deprecated patterns LLMs still generate** (like `<meta name="keywords">`), checks a web project against current SEO practice, and applies fixes through your framework's head API.

---

## Why This Plugin Exists

### The LLM Knowledge Gap Problem

LLMs still emit outdated SEO patterns from their training data. Examples:

| Topic | What LLMs Often Recommend | What This Plugin Enforces |
|-------|---------------------------|---------------------------|
| Keywords | `<meta name="keywords" content="...">` | **Remove.** Google deprecated it in 2009, and Bing uses it as a spam signal. |
| IE compatibility | `<meta http-equiv="X-UA-Compatible" content="IE=edge">` | **Remove.** IE was retired in 2022, and Edge has used Chromium since 2020. |
| IE legacy | `<!--[if IE]>...<![endif]-->` conditional comments | **Remove**, unless the project states IE11 support. |
| DOM libraries | "Add jQuery for DOM manipulation" | **Use native APIs.** |
| Layout | `float` columns | **Flexbox / Grid.** |
| Emphasis | `<b>Important!</b>` / `<i>aside</i>` | **`<strong>` / `<em>`** for semantic meaning. |
| Structured data | Microdata (`itemscope`/`itemprop`) or RDFa | **JSON-LD**, Google's preferred format. |
| Doctype | `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML...">` | **`<!DOCTYPE html>`**, the HTML5 doctype. |
| Core Web Vitals | "Optimize FID" | **Measure INP, LCP and CLS.** INP replaced FID in March 2024. |
| Mobile | "Create a mobile subdomain m.example.com" | **Responsive design.** Google has used mobile-first indexing since 2019. |
| Void elements | `<br />`, `<img />`, `<hr />` | **`<br>`, `<img>`, `<hr>`** in HTML5 contexts. |
| External links | `<a href="..." target="_blank">` | **Add `rel="noopener noreferrer"`** for security and performance. |
| Head management | Raw `<head>` edits in framework projects | **Framework head APIs** (Metadata API, `useSeoMeta`, route `head`, etc.). |

The skills carry current SEO rules in their prompts and can check them against current documentation through [Context7 MCP](#context7-mcp-integration).

## Limits

It's static analysis of HTML, JSX, Vue, Svelte and Astro files. It reads config files (`next.config.*`, `vercel.json`, `_headers`) but doesn't send HTTP requests, so it can't measure real LCP, CLS or INP (use PageSpeed Insights or Chrome DevTools) or check external links for 404s. Accessibility coverage is limited to the SEO overlap; for WCAG 2.1/2.2 compliance, use `/accessibility-audit` from `ai-accessibility`.

---

## Available Skills

### `/seo-audit`: Audit the project

Scans the project across 9 categories and writes a timestamped report to a `seo-audit` folder in your docs directory (see [Report Structure](#report-structure)). Each finding includes the file and line, the current code and a specific fix.

**Analyzes:**

| Category | Weight | What It Checks |
|----------|--------|----------------|
| Deprecated Patterns | 20% | Keywords meta, X-UA-Compatible, IE comments, XHTML style, `<b>`/`<i>` misuse, mobile subdomains, `target="_blank"` without `rel="noopener noreferrer"` |
| Modern Meta Tags | 15% | `<title>`, description, canonical, Open Graph, Twitter Card, viewport, charset, `lang`, favicon, robots.txt, sitemap.xml |
| Semantic HTML | 10% | `<header>`, `<nav>`, `<main>`, single `<h1>`, heading hierarchy |
| Structured Data | 15% | JSON-LD presence, valid `@context`, correct types, required properties |
| Performance Signals | 15% | Image dimensions, `loading="lazy"`, `decoding="async"`, WebP/AVIF, preconnect, preload, `async`/`defer` scripts, `font-display` |
| Accessibility (SEO overlap) | 10% | Alt text, generic link text, form labels, skip link |
| URL Structure | 5% | Clean URLs, trailing slash, HTTPS, redirect patterns |
| Security Headers | 5% | HSTS, CSP, X-Content-Type-Options, Referrer-Policy |
| Framework Best Practices | 5% | Next.js Metadata API, Nuxt `useSeoMeta`, TanStack Start `<HeadContent />`, Astro `<SEO>` (from the third-party `astro-seo` package), SvelteKit `<svelte:head>`, Remix `meta` export |

**Usage:**

```
/seo-audit
```

Interactive prompts:
1. **Scope:** entire solution or specific directory
2. **Version control:** commit audits (for PR-review trend tracking) or add to `.gitignore`

Framework is auto-detected from `package.json`, config files, and directory structure.

**Example terminal summary:**

```
SEO Audit Complete
==================
Project: my-portfolio
Framework: tanstack-start 1.2.0
Knowledge: Context7 MCP

Overall Score: 72/100 (C)
Trend: 📈 vs previous audit (64)

Critical: 2  High: 5  Medium: 8  Low: 3

Top 3 Critical Issues:
  1. Deprecated keywords meta tag  (src/routes/__root.tsx:23)
  2. Missing canonical URL          (src/routes/__root.tsx:N/A)
  3. X-UA-Compatible IE shim        (src/routes/__root.tsx:21)

Full report: docs/seo-audit/seo-audit-2026-04-17-143022.md
Index:       docs/seo-audit/README.md
Latest:      docs/seo-audit/latest.md
```

### `/seo-fix`: Apply safe remediations

Reads `docs/seo-audit/latest.md` and applies fixes categorized as safe-auto, content-requiring (confirm), or larger refactors (propose).

**Safe-auto (no content needed):** removes keywords meta, X-UA-Compatible and IE conditional comments; adds `rel="noopener noreferrer"`, image `loading`/`decoding`, `async`/`defer` on third-party scripts, and missing `lang`, charset and viewport; fixes XHTML void elements and `<b>`/`<i>` emphasis.

**Content-requiring (propose + confirm):**
- Meta descriptions (proposed from page content, user accepts/edits/skips)
- Page titles, Open Graph / Twitter copy, canonical URL

**Larger refactors (plan + confirm):**
- Div-soup → semantic HTML5
- Heading hierarchy corrections
- Structured data scaffolding (see `/seo-schema`)

**Usage:**

```
/seo-fix           # Interactive apply
/seo-fix --dry-run # Show all would-be diffs, write nothing
```

When a framework manages `<head>`, fixes go through its own API (see [Framework Support](#framework-support)).

### `/seo-schema`: Generate and validate JSON-LD

Produces Schema.org structured data for detected content types and validates existing JSON-LD blocks.

**Supports:**
- `Article` / `BlogPosting` (with `Person` author + `Organization` publisher)
- `Product` (with `Offer` + `AggregateRating`)
- `Organization` / `LocalBusiness`
- `FAQPage`, `BreadcrumbList`, `Event`, `HowTo`, `Recipe`, `VideoObject`, `Person`, `Course`, `JobPosting`
- Composite `@graph` structures (Organization + WebSite + SearchAction for homepages)

**Validates:**
- `@context` uses `https://` (not `http://`)
- `@type` is valid Schema.org
- Required properties present
- ISO 8601 dates
- Absolute URLs
- Properly typed nested entities

**Usage:**

```
/seo-schema                                     # Interactive target selection
/seo-schema src/routes/blog/$slug.tsx          # Target specific route
```

Output includes the JSON-LD and the code to inject it in your framework.

---

## Context7 MCP Integration

All three skills check for Context7 MCP and, when it's available, use it to fetch current docs for:

- Google Search Central guidelines
- Schema.org type definitions + required properties
- Framework SEO API syntax
- Core Web Vitals thresholds (values change periodically)
- Open Graph + Twitter Card specs
- W3C HTML Living Standard

Without Context7, the skills fall back to training-data knowledge and **state the fallback mode** in both the terminal output and the report header.

**Install Context7:**

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Restart Claude Code after install for the MCP to load.

---

## Quick Start

### Installation

```
/plugin install ai-seo@claude-code-plugins-dev
```

### Recommended Flow

```
# 1. Baseline audit
/seo-audit
  → Scope: Entire solution
  → Version control: Yes, commit audits

# 2. Review docs/seo-audit/latest.md

# 3. Apply safe fixes
/seo-fix --dry-run     # preview
/seo-fix               # apply

# 4. Generate structured data where missing
/seo-schema

# 5. Re-audit to verify
/seo-audit
  → Trend indicator should show 📈
```

---

## Framework Support

Each skill detects the framework from `package.json`, config files and directory structure, then uses that framework's own head API:

- **Next.js** (App Router + Pages Router): Metadata API, `generateMetadata`, `app/sitemap.ts`, `app/robots.ts`, `app/opengraph-image.tsx`
- **Nuxt:** `useSeoMeta`, `useHead`, `@nuxtjs/seo` module, `@nuxtjs/sitemap`
- **TanStack Start:** `createRootRoute`/`createFileRoute` with `head: () => ({ meta, links, scripts })`, `<HeadContent />` + `<Scripts />` in root
- **Astro:** layout `<head>`, `astro-seo`, `@astrojs/sitemap`, content collections schema
- **SvelteKit:** `<svelte:head>`, `$app/stores` for canonical, sitemap endpoint
- **Remix:** `meta` / `links` export functions
- **Vanilla HTML:** direct `<head>` inspection and recommendations

---

## Report Structure

Reports go in `docs/seo-audit/` by default. If the project already uses `documentation/` or `.docs/`, the skill writes there instead.

```
docs/seo-audit/
├── README.md                           # Reverse-chronological index with trend indicators
├── latest.md                           # Most recent audit (copy, not symlink)
└── seo-audit-YYYY-MM-DD-HHMMSS.md      # Timestamped reports (preserved)
```

The index has a table like:

| Date | Score | Grade | Critical | Trend | Report |
|------|-------|-------|----------|-------|--------|
| 2026-04-19 16:22:33 | 88/100 | B | 0 | 📈 | [view](./seo-audit-2026-04-19-162233.md) |
| 2026-04-18 09:15:44 | 78/100 | C | 1 | 📈 | [view](./seo-audit-2026-04-18-091544.md) |
| 2026-04-17 14:30:22 | 72/100 | C | 2 | — | [view](./seo-audit-2026-04-17-143022.md) |

**Trend indicators:** 📈 improved (score up ≥3), 📉 regressed (score down ≥3), ➡️ unchanged (±2).

Reports are never overwritten. Each run creates a new timestamped file, and `latest.md` is a copy of the most recent run.

---

## Resources

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [MDN: HTML `<meta>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta)
- [Core Web Vitals](https://web.dev/articles/vitals) (LCP, CLS, INP)
- [Context7 MCP](https://github.com/upstash/context7)

---

## Plugin Details

- **Name:** `ai-seo`
- **Version:** 1.0.1
- **License:** MIT
- **Author:** Charles Jones ([charlesjones.dev](https://charlesjones.dev) · [@charlesjones-dev](https://github.com/charlesjones-dev))

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

## License

MIT. See [LICENSE](./LICENSE).
