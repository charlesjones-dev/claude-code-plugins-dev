# AI-SEO Plugin

**Modern SEO auditing and remediation for web projects.** Catches the deprecated patterns LLMs still generate (like `<meta name="keywords">`), validates current best practices (Core Web Vitals, structured data, semantic HTML), and produces framework-specific remediation guidance for Next.js, Nuxt, TanStack Start, Astro, SvelteKit, and Remix.

---

## 🎯 Why This Plugin Exists

### The LLM Knowledge Gap Problem

Current LLMs — including frontier models — still frequently emit **outdated SEO patterns** from their training data. Examples observed in the wild:

- `<meta name="keywords">` — **deprecated by Google since 2009**, used as a **spam signal by Bing**, still inserted by LLMs into new code
- `<meta http-equiv="X-UA-Compatible" content="IE=edge">` — **IE has been dead since 2022**; Edge has been Chromium since 2020
- IE conditional comments, XHTML doctypes, jQuery recommendations, `float`-based layouts, FID optimization advice (INP replaced FID in March 2024)
- Separate mobile subdomain (`m.example.com`) patterns — Google has been mobile-first since 2019
- Microdata / RDFa instead of JSON-LD (Google's preferred format)

**This plugin corrects that knowledge gap** by baking modern SEO rules directly into skill prompts and (optionally) querying [Context7 MCP](https://github.com/upstash/context7) for up-to-the-day documentation from Google Search Central, Schema.org, and framework SEO APIs.

### What This Plugin IS

- **Static code analysis** for SEO patterns in HTML, JSX, Vue, Svelte, Astro
- **Framework-aware** — TanStack Start, Next.js, Nuxt, Astro, SvelteKit, Remix, vanilla HTML
- **Modern** — enforces 2025/2026 best practices, flags 2009-era ones
- **Actionable** — every finding has file:line, current code, and specific remediation
- **Trackable** — timestamped reports in `/docs/seo-audit/` with trend indicators

### What This Plugin IS NOT

- **NOT a runtime Core Web Vitals tool** — use PageSpeed Insights or Chrome DevTools for real LCP/CLS/INP measurements
- **NOT a link crawler** — doesn't follow external links or check for 404s beyond project scope
- **NOT a server-header tester** — static analysis only; it reads config files (`next.config.*`, `vercel.json`, `_headers`) but doesn't send real HTTP requests
- **NOT a full a11y audit** — surface-level coverage only. Use the `/accessibility-audit` skill from `ai-accessibility` for WCAG 2.1/2.2 compliance

---

## 📋 Available Skills

### `/seo-audit` — Comprehensive SEO audit

Scans the project across 9 categories and writes a timestamped report to `/docs/seo-audit/`.

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
| Framework Best Practices | 5% | Next.js Metadata API, Nuxt `useSeoMeta`, TanStack Start `<Meta>`, Astro `<SEO>`, SvelteKit `<svelte:head>`, Remix `meta` export |

**Usage:**

```
/seo-audit
```

Interactive prompts:
1. **Scope** — entire solution or specific directory
2. **Version control** — commit audits (for PR-review trend tracking) or add to `.gitignore`

Framework is auto-detected from `package.json`, config files, and directory structure.

**Output:**

```
docs/seo-audit/
├── README.md                          # Index of all audits (trend indicators)
├── latest.md                          # Copy of most recent audit
├── seo-audit-2026-04-17-143022.md     # Timestamped reports
├── seo-audit-2026-04-18-091544.md
└── seo-audit-2026-04-19-162233.md
```

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

### `/seo-fix` — Apply safe remediations

Reads `docs/seo-audit/latest.md` and applies fixes categorized as safe-auto, content-requiring (confirm), or larger refactors (propose).

**Safe-auto (no content needed):**
- Remove `<meta name="keywords">`
- Remove `<meta http-equiv="X-UA-Compatible">`
- Remove IE conditional comments
- Add `rel="noopener noreferrer"` to `target="_blank"` links
- Add `loading="lazy"` / `decoding="async"` to images
- Add `async`/`defer` to third-party scripts
- Add missing `<html lang>`, `<meta charset>`, viewport
- Fix XHTML self-closing void elements
- Replace `<b>`/`<i>` used for emphasis with `<strong>`/`<em>`

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

All fixes are emitted using **framework-idiomatic APIs** (Next.js Metadata API, TanStack Start route `head`, Nuxt `useSeoMeta`, etc.) — not raw `<head>` edits when a framework manages head.

### `/seo-schema` — Generate and validate JSON-LD

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

Output includes JSON-LD + framework-specific injection code (Next.js `dangerouslySetInnerHTML`, Nuxt `useHead`, TanStack Start route `head.scripts`, Astro `set:html`, SvelteKit `<svelte:head>`, Remix route component).

---

## 🧠 Context7 MCP Integration

All three skills **check for Context7 MCP first** and use it to fetch current documentation when available:

- Google Search Central guidelines
- Schema.org type definitions + required properties
- Framework SEO API syntax (Next.js Metadata, Nuxt SEO module, TanStack Start head management)
- Core Web Vitals thresholds (values change periodically)
- Open Graph + Twitter Card specs
- W3C HTML Living Standard

**If Context7 is available:** real-time docs, never stale.

**If Context7 is NOT available:** skills fall back to training-data knowledge and **clearly state the fallback mode** in both terminal output and the generated report header. Nothing silent.

**Install Context7:**

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Restart Claude Code after install for the MCP to load.

---

## 🆚 LLM Default vs This Plugin

| Topic | What LLMs Often Recommend | What This Plugin Enforces |
|-------|---------------------------|---------------------------|
| Keywords | `<meta name="keywords" content="...">` | **Remove.** Deprecated 2009. Bing spam signal. |
| IE compatibility | `<meta http-equiv="X-UA-Compatible" content="IE=edge">` | **Remove.** IE is dead. Edge is Chromium. |
| IE legacy | `<!--[if IE]>...<![endif]-->` conditional comments | **Remove.** Unless explicit IE11 support stated. |
| DOM libraries | "Add jQuery for DOM manipulation" | **Use native APIs.** Modern browsers cover every jQuery use case. |
| Layout | `float` columns | **Flexbox / Grid.** |
| Emphasis | `<b>Important!</b>` / `<i>aside</i>` | **`<strong>` / `<em>`** for semantic meaning. |
| Structured data | Microdata (`itemscope`/`itemprop`) or RDFa | **JSON-LD.** Google's preferred format. |
| Doctype | `<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML...">` | **`<!DOCTYPE html>`.** HTML5 only. |
| Core Web Vitals | "Optimize FID" | **INP replaced FID in March 2024.** Measure INP, LCP, CLS. |
| Mobile | "Create a mobile subdomain m.example.com" | **Mobile-first responsive.** Google has been mobile-first since 2019. |
| Void elements | `<br />`, `<img />`, `<hr />` | **`<br>`, `<img>`, `<hr>`** in HTML5 contexts. |
| External links | `<a href="..." target="_blank">` | **Add `rel="noopener noreferrer"`.** Security + performance. |
| Head management | Raw `<head>` edits in framework projects | **Framework-idiomatic APIs** (Metadata API, `useSeoMeta`, route `head`, etc.). |

---

## 🚀 Quick Start

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

## 🏗️ Framework Support

Each skill auto-detects framework from `package.json` + config + directory structure, then emits framework-idiomatic recommendations:

- **Next.js** (App Router + Pages Router) — Metadata API, `generateMetadata`, `app/sitemap.ts`, `app/robots.ts`, `app/opengraph-image.tsx`
- **Nuxt 3** — `useSeoMeta`, `useHead`, `@nuxtjs/seo` module, `nuxt-simple-sitemap`
- **TanStack Start** — `createRootRoute`/`createFileRoute` with `head: () => ({ meta, links, scripts })`, `<HeadContent />` + `<Scripts />` in root
- **Astro** — layout `<head>`, `astro-seo`, `@astrojs/sitemap`, content collections schema
- **SvelteKit** — `<svelte:head>`, `$app/stores` for canonical, sitemap endpoint
- **Remix** — `meta` / `links` export functions
- **Vanilla HTML** — direct `<head>` inspection and recommendations

---

## 📁 Report Structure

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

Reports are **never overwritten** — each run creates a new timestamped file. `latest.md` is always a copy of the most recent run for easy reference.

---

## 📚 Resources

- [Google Search Central](https://developers.google.com/search) — official guidance
- [Schema.org](https://schema.org/) — structured data vocabulary
- [web.dev / Learn SEO](https://web.dev/learn/seo/) — modern SEO curriculum
- [MDN — HTML `<meta>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta)
- [Core Web Vitals](https://web.dev/articles/vitals) — LCP, CLS, INP
- [Context7 MCP](https://github.com/upstash/context7) — up-to-date library docs

---

## 🤝 Contributing

This plugin lives in the [`claude-code-plugins-dev`](https://github.com/charlesjones-dev/claude-code-plugins-dev) marketplace repo. Open issues or PRs there.

## 📄 License

MIT — see [LICENSE](./LICENSE).

## 👤 Author

**Charles Jones** — [charlesjones.dev](https://charlesjones.dev) · [@charlesjones-dev](https://github.com/charlesjones-dev)
