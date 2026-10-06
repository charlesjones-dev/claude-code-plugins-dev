# ai-aeo

> Audits how ready a site's pages are to be the direct answer in featured snippets, voice assistants and answer boxes, and fixes what's in the way.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Checks that each page answers its question in the first sentence, in HTML an engine can lift, with nothing blocking the snippet.**

---

## What is AEO?

**Answer Engine Optimization (AEO)** structures content so a search or answer engine can lift one passage as the direct answer to a question: a featured snippet, a voice assistant reply, a direct answer box, a "People also ask" entry, or a question-and-answer pair an assistant quotes word for word. The goal is to be *the* concise answer to a specific question.

The usual tactics are FAQ sections, clean schema markup, concise definitions, answer-first paragraphs and clear question headings.

What the engines themselves say:

- **Google** picks featured snippets itself; no markup makes a page one. It says its AI features need nothing beyond normal SEO, and that you don't need to write in a special way for them.
- **Microsoft** (Bing and Copilot) is more specific: direct questions with clear answers, one- to two-sentence responses, lists and tables, and important answers that aren't hidden in tabs or expandable menus.

This plugin checks for those things and treats them as clear writing for people that also happens to be easy to lift. Heuristics without a documented source are marked 🧪.

---

## AEO, GEO and SEO

| | SEO | AEO | GEO |
|---|-----|-----|-----|
| **Goal** | Rank in the organic results | Be the single direct answer | Be cited or mentioned inside multi-source AI answers |
| **Surfaces** | Search results pages | Featured snippets, voice replies, answer boxes, "People also ask" | ChatGPT, Perplexity, Claude, Gemini, Copilot, AI Overviews |
| **Main tactics** | Crawlability, meta tags, performance, links | FAQ sections, clean schema, concise definitions, answer-first paragraphs, question headings | Topical authority, original research, expert perspectives, third-party validation |
| **Plugin** | [ai-seo](../ai-seo/) | ai-aeo | [ai-geo](../ai-geo/) |

---

## Installation

```bash
/plugin install ai-aeo@claude-code-plugins-dev
```

Or add the marketplace first if you haven't:

```bash
/plugin marketplace add charlesjones-dev/claude-code-plugins-dev
/plugin install ai-aeo@claude-code-plugins-dev
```

---

## Commands

| Command | Purpose |
|---------|---------|
| `/aeo-audit` | Audit the site for AEO and write a timestamped report to `docs/aeo-audit/`. Optional live URL check. |
| `/aeo-fix` | Apply fixes from the latest audit with a diff for each change. Supports `--dry-run`. |
| `/aeo-questions` | Map the questions the site should answer to the page that answers each one, and find gaps and competing pages. |
| `/aeo-faq` | Build, update or validate visible FAQ sections and, if you want it, their FAQPage or QAPage markup. Supports `--dry-run`. |

All skills are interactive. `/aeo-audit` and `/aeo-questions` take no arguments; `/aeo-fix` and `/aeo-faq` accept only `--dry-run`.

---

## Usage

### Run an audit

```
/aeo-audit
```

You'll be asked for the audit scope, whether to commit reports, and whether to check the live site. The skill then:

1. Detects your framework (Next.js, Nuxt, TanStack Start, Astro, SvelteKit, Remix / React Router, or vanilla HTML).
2. Checks whether Context7 MCP is available for current documentation.
3. Reads the latest question map from `/aeo-questions`, if there is one.
4. Lists the pages whose job is to answer questions and runs the nine checks under [What gets audited](#what-gets-audited).
5. With a live URL, fetches up to ten pages to confirm the answers are in the served HTML and to read the robots directives actually sent.
6. Writes a timestamped report, an index with trend indicators and `latest.md` to `docs/aeo-audit/` (see [Report output](#report-output)).

### Map questions to pages

```
/aeo-questions
```

Starts from the questions your site already asks in its headings and FAQs. You can add questions by typing them, from a query export (Search Console, Bing Webmaster Tools, or the grounding queries in Bing's AI Performance report), or from web search suggestions, each linked to where it was found. It merges duplicates, gives each question one owner page, and marks it answered first, buried, partial, missing or competing. `/aeo-audit` scores question coverage against the latest map.

### Apply fixes

```
/aeo-fix             # apply fixes interactively
/aeo-fix --dry-run   # preview diffs without writing
```

`/aeo-fix` reads `docs/aeo-audit/latest.md` and sorts findings into:

- **Safe fixes**, confirmed once as a batch: div lists to `<ol>`/`<ul>`, JSON-LD validity fixes, microdata to JSON-LD, removing markup for questions that aren't on the page.
- **Fixes that need your intent**: every `noindex`, `nosnippet`, `max-snippet`, `data-nosnippet`, `nocache` or `noarchive` on answer pages (keep, remove or narrow), repeated FAQ markup, and whether to add FAQPage markup at all.
- **Fixes that need your content**, confirmed one by one: answer-first rewrites drawn from the page's own text, question headings, definitional openings, summaries, "last updated" dates and local business details. It never invents an answer.
- **Larger refactors**: accordions that load answers on click, CSS-grid "tables", client-only answer pages, glossaries, and pages that compete for the same question.

### Build FAQ sections

```
/aeo-faq             # build, update or validate interactively
/aeo-faq --dry-run   # print the would-be files without writing
```

Drafts questions and answers from the page's own content, the question map, or answers you supply, and shows the source for each draft. It renders the visible FAQ and any markup from one data source so they can't drift apart, keeps answers in the HTML with the main ones open, and can validate every FAQ on the site.

---

## What gets audited

| Category | Weight | What it checks |
|----------|--------|----------------|
| Answer-First Formatting | 20% | The first sentence under each question answers it; no preambles; summaries on long pages; answers that stand alone |
| Question Coverage & Headings | 15% | Natural question headings, clean hierarchy, follow-up questions, coverage of the question map |
| Concise Definitions | 10% | "X is a Y that Z" openings on concept pages, glossaries, consistent definitions |
| Snippet-Ready Structure | 15% | Real `<ol>`, `<ul>` and `<table>`; answers as text, not images or PDFs; answers in the initial HTML and main answers visible |
| Snippet Eligibility & Indexing Controls | 15% | `noindex`, `nosnippet`, `max-snippet`, `data-nosnippet`, Bing `nocache` / `noarchive`, `X-Robots-Tag` in config and middleware, canonicals |
| FAQ Sections & Structured Data | 10% | Visible FAQ sections, markup that matches them, QAPage vs FAQPage, JSON-LD validity |
| Voice & Assistant Readiness | 5% | Answers that read well aloud, `LocalBusiness` data, assistant crawlers not blocked |
| Answer Trust Signals | 5% | Dates on answers that change, sources on health, finance and legal answers, no contradictions between pages |
| Technical Answer Accessibility | 5% | Server rendering, status codes, mobile viewport |

Findings are rated Critical, High, Medium or Low, with 🧪 on heuristics. Each one has a file and line (or a live-check URL), the current code and a specific fix.

---

## What LLMs often get wrong about AEO

| What LLMs often do | What this plugin does |
|--------------------|-----------------------|
| Promise FAQ rich results from FAQPage markup | Google stopped showing FAQ rich results on May 7, 2026; markup is optional |
| Recommend HowTo markup for step lists | Uses a real `<ol>`; HowTo results ended in 2023 |
| Suggest "featured snippet schema" | No such markup exists; Google chooses snippets itself |
| Recommend `speakable` for voice search | Mentions it only for news publishers, as a legacy beta |
| Treat a word count (often "40–60 words") as a Google rule | Treats length as a heuristic; Google sets no minimum |
| Put answers in accordions that load on click | Flags answers missing from the initial HTML |
| Mark up FAQ entries that aren't on the page | Marks up only visible questions, from the same data |
| Miss a `nosnippet` set in a layout or header | Searches meta tags, framework APIs, header config, middleware and `data-nosnippet` |
| Write FAQ answers from thin air | Drafts only from your site or your answers |
| Rewrite pages just for engines | Recommends changes that also help readers |

---

## Report output

Reports go to `docs/aeo-audit/`. If the project already uses `documentation/` or `.docs/`, the skills write there instead.

```
docs/aeo-audit/
├── README.md                              # Index: audits with trend indicators, and question maps
├── latest.md                              # Copy of the most recent audit
├── aeo-audit-2026-10-06-143022.md         # Timestamped audits
├── question-map-latest.md                 # Copy of the most recent question map
├── question-map-2026-10-06-150110.md      # Timestamped question maps
└── faq-validation-2026-10-06-152245.md    # Optional /aeo-faq validation reports
```

Timestamped files are never overwritten. `latest.md` and `question-map-latest.md` are file copies, not symlinks, so they work on every platform.

---

## Live check

`/aeo-audit` can fetch your production site (up to ten pages) with a normal browser user agent. It reports the robots directives actually served, whether each answer is in the HTML before any script runs, whether the main answers are visible, and whether FAQ markup matches the page. A host or CDN can change what's served, so the live result can differ from the repo. Run it only against sites you own or are authorized to test.

---

## Context7 MCP integration

When [Context7 MCP](https://github.com/upstash/context7) is installed, the skills use it for current Google Search Central documentation, Schema.org types and your framework's head APIs.

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Without Context7, the skills fall back to training-data knowledge and mark more items with 🧪.

---

## Related plugins

- `/geo-audit` ([ai-geo](../ai-geo/)) covers being cited and mentioned in AI answers: crawler rules, topical authority, original research, authorship and third-party validation.
- `/seo-audit` ([ai-seo](../ai-seo/)) covers traditional rankings: meta tags, deprecated markup, performance and security headers.

To check all three:

```
/seo-audit
/aeo-audit
/geo-audit
```

---

## Limits

- The audit estimates readiness from your code. It can't see which queries show a featured snippet today or who holds it.
- Engines choose answers themselves and change how they do it often. Third-party tracking shows featured snippets on fewer results as AI Overviews spread.
- Voice assistants now run on large models with their own sources, which can't be tested from code.
- It doesn't measure traffic or zero-click effects. Use Search Console and Bing Webmaster Tools for that.

---

## Plugin Details

- **Name:** `ai-aeo`
- **Version:** 1.0.0
- **Author:** [Charles Jones](https://charlesjones.dev)
- **License:** MIT
- **Repository:** https://github.com/charlesjones-dev/claude-code-plugins-dev

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT. See [LICENSE](LICENSE).
