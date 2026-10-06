# ai-geo

> Generative Engine Optimization (GEO) auditing and remediation for Claude Code.

[![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Audit how AI answer engines (ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews and Microsoft Copilot) can crawl and cite your site.**

---

## What is GEO?

**Generative Engine Optimization (GEO)** is the practice of structuring web content so AI engines are more likely to cite or quote it in their answers. SEO targets SERP position and organic traffic. GEO targets:

- **Citation probability** in AI-generated answers
- **Factual extraction quality** by retrieval-augmented models
- **Answer inclusion** across conversational AI surfaces
- **Entity disambiguation** in AI knowledge graphs
- **Markdown-first accessibility** for LLM consumption

GEO is an emerging discipline. This plugin flags experimental recommendations with 🧪 so you can apply judgment.

---

## GEO vs SEO

| Dimension | SEO | GEO |
|-----------|-----|-----|
| **Target** | Search engine rankings, SERP position | AI engine citations, answer inclusion |
| **Surface** | Google, Bing results pages | ChatGPT, Perplexity, Claude, Gemini, AI Overviews |
| **Metrics** | Impressions, CTR, backlinks, keywords | Citation frequency, quote accuracy, entity linking |
| **Key files** | `sitemap.xml`, `robots.txt` | `llms.txt`, `llms-full.txt`, `robots.txt` (AI bots) |
| **Content format** | HTML + metadata | Markdown-preferred, self-contained chunks |
| **Rendering** | Crawlable HTML (JS-tolerant) | Often JS-free; SSR/static critical |
| **Structured data** | Article, Product, LocalBusiness | FAQPage, HowTo, Person (with sameAs), DefinedTerm |
| **E-E-A-T** | Quality-rater concept, not itself a ranking factor | Citation-worthiness heuristic |
| **Tone** | Keyword-optimized | Conversational, question-anchored |

**Overlap:** technical fundamentals, structured data, HTTPS, semantic HTML, authoritativeness signals.
**Unique to GEO:** the `llms.txt` protocol, AI-bot policy (training vs citation), content chunking for embedding retrieval, markdown-accessible routes, and entity `sameAs` disambiguation.

---

## Installation

From the marketplace:

```bash
/plugin install ai-geo@claude-code-plugins-dev
```

Or add the marketplace first if you haven't:

```bash
/plugin marketplace add charlesjones-dev/claude-code-plugins-dev
/plugin install ai-geo@claude-code-plugins-dev
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/geo-audit` | Audit the site for GEO and write a timestamped report to `docs/geo-audit/`. |
| `/geo-fix` | Apply safe remediations from the latest audit. Diff+confirm workflow. Supports `--dry-run`. |
| `/geo-llms-txt` | Generate, update, or validate `llms.txt` and `llms-full.txt`. Supports `--dry-run`. |

All skills are interactive. `/geo-audit` takes no arguments; `/geo-fix` and `/geo-llms-txt` accept only `--dry-run`.

---

## Usage

### Run an audit

```
/geo-audit
```

You'll be asked for audit scope (full solution or a sub-directory) and whether to commit audit reports to version control. The skill then:

1. Detects your framework (Next.js, Nuxt, TanStack Start, Astro, SvelteKit, Remix, or vanilla HTML).
2. Checks Context7 MCP availability for current documentation (recommended for GEO).
3. Runs the ten categories listed under [What gets audited](#what-gets-audited).
4. Writes a timestamped report, an index with trend indicators and `latest.md` to `docs/geo-audit/` (see [Report output](#report-output)).
5. Prints a concise terminal summary with the top critical issues and AI crawler access summary.

### Apply fixes

```
/geo-fix             # apply fixes interactively
/geo-fix --dry-run   # preview diffs without writing
```

`/geo-fix` reads `docs/geo-audit/latest.md`, classifies findings, and guides you through:

- **Safe-auto fixes:** batch-confirmed once (add `dateModified`, migrate microdata to JSON-LD, add FAQPage wrapper to Q&A prose).
- **Intent-requiring fixes:** separate prompts for training-bot and citation-bot policies before modifying `robots.txt`.
- **Content-requiring fixes:** prompts for `sameAs` URLs, TL;DR copy, FAQ extraction (never fabricated).
- **Larger refactors:** proposed with per-file diffs (SSR migration, paragraph restructuring, heading rewording).

### Generate llms.txt

```
/geo-llms-txt             # generate, update or validate interactively
/geo-llms-txt --dry-run   # print the would-be files without writing
```

Interactive skill with four modes: generate, update, validate, or produce `llms-full.txt`. Detects your framework and places the file at the correct static-asset path (or emits a route handler for dynamic generation).

---

## What gets audited

### llms.txt Protocol Compliance
- Presence of `/llms.txt` and `/llms-full.txt`
- Spec compliance (H1 title, blockquote description, markdown throughout)
- Link reachability and `.md`-companion preference
- Staleness vs current content
- Discoverability hints 🧪: a `<link rel="alternate" type="text/markdown">` tag in `<head>`, a `/llms.txt` entry in the sitemap, and a `robots.txt` comment pointing to the file
- A manual reminder to submit the file to directories such as llmstxt.site and directory.llmstxt.cloud

### AI Crawler Access (Training vs Citation)
- Per-bot directives parsed from `robots.txt`
- Training bots flagged separately from citation bots
- Analysis commentary on whether the policy matches likely intent

### Content Structure for AI Extraction
- Q&A patterns with direct answers
- Definitional opening sentences
- Self-contained paragraphs (flags context-dependent phrasing)
- Lists, tables, and inline statistic attribution

### Citation-Worthiness Signals
- Visible author attribution + credentials
- E-E-A-T signals (About, Contact, Privacy, Terms)
- Publication and last-modified dates
- Outbound links to authoritative sources

### AI-Friendly Structured Data (JSON-LD)
- `FAQPage`, `HowTo`
- `Person` and `Organization` with `sameAs` for entity disambiguation
- `Article` with `speakable` specification 🧪
- `DefinedTerm`, `ClaimReview`, `Dataset` for specialized content 🧪

### Semantic Chunking Quality
- Heading hierarchy creates self-contained sections
- Paragraph length and topic sentences
- `<section>` / `<article>` landmarks

### Content Freshness Signals
- `article:modified_time` Open Graph tag
- `dateModified` in JSON-LD
- Visible "Last updated" indicators

### Entity Optimization
- `sameAs` links to Wikipedia/Wikidata, LinkedIn, GitHub, Crunchbase, ORCID
- Consistent entity naming
- Disambiguation for ambiguous terms

### Conversational Query Alignment
- Question-shaped H2/H3 headings
- Natural-language phrasing over keyword stuffing
- Long-tail conversational patterns

### Technical AI Accessibility
- Server-side rendered or static content (not client-only)
- Clean HTML (not deeply nested wrapper divs)
- Proper HTTP status codes, HTTPS, fast response times

---

## AI Crawler Reference

### Training Crawlers

| Bot | Operator | Purpose |
|-----|----------|---------|
| `GPTBot` | OpenAI | Model training |
| `ClaudeBot` | Anthropic | Model training |
| `Google-Extended` | Google | robots.txt control token, not a crawler: Gemini training and grounding |
| `Applebot-Extended` | Apple | Apple Intelligence training |
| `CCBot` | Common Crawl | Training corpus used by many |
| `Bytespider` | ByteDance | Training |
| `Amazonbot` | Amazon | Training + indexing |
| `FacebookBot` / `meta-externalagent` | Meta | Training |
| `Omgilibot` / `Omgili` | Webz.io | Training corpus |

### Answer / Citation Crawlers

| Bot | Operator | Purpose |
|-----|----------|---------|
| `ChatGPT-User` | OpenAI | ChatGPT browsing and citations |
| `OAI-SearchBot` | OpenAI | ChatGPT search index |
| `PerplexityBot` | Perplexity | Index |
| `Perplexity-User` | Perplexity | Live citation fetch |
| `Claude-User` | Anthropic | Fetches pages when a Claude user asks |
| `Claude-SearchBot` | Anthropic | Claude search results |

**A common pattern:** block training bots and allow citation bots, so AI answer engines can still cite the site while training crawlers are asked to stay out. `/geo-fix` asks about each group separately.

---

## llms.txt primer

`llms.txt` is a markdown index of a site's key pages, served from the web root (`/llms.txt`). Jeremy Howard proposed it at https://llmstxt.org/ in 2024. No major LLM provider has publicly committed to reading it 🧪.

**Minimal structure:**

```markdown
# Site Name

> One-sentence description of the site.

## Section

- [Page title](https://example.com/page.md): one-line summary.
- [Another page](https://example.com/another.md): one-line summary.

## Optional

- [Secondary resource](https://example.com/secondary.md): summary.
```

**Rules:**
- The H1 title is the only required section.
- A blockquote summary directly after the H1 is optional in the spec, but the audit checks for it.
- H2 section headers organize the index.
- Bulleted links with descriptive text and a one-line summary.
- The `## Optional` section (if present) holds links an agent can skip when it needs a shorter context.
- Prefer linking to `.md` companion URLs when the content is available in markdown.

`llms-full.txt` is a companion file with the full markdown content of the linked pages. Use it when licensing and bandwidth allow you to expose full text to AI engines.

---

## What LLMs often miss about GEO

| What LLMs often do | What this plugin does |
|---------------------|---------------------------|
| Treat GEO as a synonym for SEO | Keep GEO checks separate from SEO checks |
| Block all AI crawlers wholesale | Prompt separately for training vs citation intent |
| Dismiss `llms.txt` as "not a standard" | Proposed standard: generate and validate it |
| Suggest HTML-only content is fine for AI | Flag client-only rendering as critical; prefer markdown companions |
| Treat structured data as optional | `FAQPage`, `Person` `sameAs`, `dateModified` are core GEO signals |
| Skip content-freshness checks | Flag missing `dateModified` and `article:modified_time` on evergreen content |
| Fabricate `sameAs` URLs | Always prompt the user; never invent identity URLs |
| Ignore conversational phrasing | Flag keyword-stuffed H2/H3 in favor of question-shaped headings |
| Recommend cloaking for AI bots | Refuse, since showing bots different content than people see is cloaking |

---

## Report output

Reports go to `docs/geo-audit/`. If the project already uses `documentation/` or `.docs/`, the skill writes there instead.

```
docs/geo-audit/
├── README.md                                 # Index with trend indicators
├── latest.md                                 # Copy of most recent audit
├── geo-audit-2026-04-17-143022.md            # Timestamped reports
├── geo-audit-2026-04-10-091544.md
└── ...
```

Timestamped reports are never overwritten. `latest.md` always reflects the most recent run (file copy, not symlink, for cross-platform compatibility).

---

## Context7 MCP integration

When [Context7 MCP](https://github.com/upstash/context7) is installed, the plugin uses it for current documentation on:

- `llms.txt` specification updates
- AI bot documentation (OpenAI, Anthropic, Google, Perplexity)
- Schema.org types (FAQPage, HowTo, DefinedTerm, ClaimReview)
- Framework meta/head APIs

Install:

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Without Context7, the plugin falls back to training-data knowledge and marks more items with 🧪.

---

## Relationship to `ai-seo`

Use `/seo-audit` from [`ai-seo`](../ai-seo/) for traditional search engines (Google, Bing) and `/geo-audit` for AI answer engines (ChatGPT, Perplexity, Claude, Gemini, AI Overviews). For overlapping checks (structured data, semantic HTML, authoritativeness), the GEO report refers you to `/seo-audit`. To check both, run them in sequence:

```
/seo-audit
/geo-audit
```

---

## Plugin Details

- **Name:** `ai-geo`
- **Version:** 1.1.1
- **Author:** [Charles Jones](https://charlesjones.dev)
- **License:** MIT
- **Repository:** https://github.com/charlesjones-dev/claude-code-plugins-dev

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

If you have data on what gets pages cited, open an issue.

---

## License

MIT. See [LICENSE](LICENSE).
