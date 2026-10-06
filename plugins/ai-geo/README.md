# ai-geo

> Audits how likely AI answer engines are to cite and mention your site, and fixes what's in the way.

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/charlesjones-dev/claude-code-plugins-dev)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Checks crawler rules, topical authority, original research, expert authorship, third-party validation and entity markup for ChatGPT, Perplexity, Claude, Gemini, Microsoft Copilot, and Google's AI Overviews and AI Mode.**

---

## What is GEO?

**Generative Engine Optimization (GEO)** makes a site worth citing, synthesizing and mentioning inside AI answers that draw on many sources. The goal is to earn brand mentions and trusted citations in those answers. The levers are deep topical authority, original research, expert perspectives and validation from other sites, on top of letting the right crawlers in.

The term comes from [Aggarwal et al. (KDD 2024)](https://arxiv.org/abs/2311.09735). In their benchmark, adding quotations, statistics and citations to sources raised a page's visibility in generative engine answers the most, and keyword stuffing did worse than nothing. Later academic work found AI search leans heavily on third-party coverage and favors newer content.

What the engines themselves say:

- **Google** says optimizing for its AI features "is still SEO": no special markup, files, Markdown or chunking, and inauthentic mentions don't help. Content people find unique and useful matters most.
- **Microsoft** (Bing and Copilot) recommends clear headings, self-contained sentences, lists and tables, and schema markup.

No AI provider publishes how it picks citations, so this plugin treats GEO checks as things that raise the odds and marks heuristics with 🧪.

---

## GEO, AEO and SEO

| | SEO | AEO | GEO |
|---|-----|-----|-----|
| **Goal** | Rank in the organic results | Be the single direct answer | Be cited or mentioned inside multi-source AI answers |
| **Surfaces** | Search results pages | Featured snippets, voice replies, answer boxes | ChatGPT, Perplexity, Claude, Gemini, Copilot, AI Overviews, AI Mode |
| **Main tactics** | Crawlability, meta tags, performance, links | FAQ sections, clean schema, concise definitions, answer-first paragraphs, question headings | Topical authority, original research, expert perspectives, third-party validation |
| **Plugin** | [ai-seo](../ai-seo/) | [ai-aeo](../ai-aeo/) | ai-geo |

Before v1.2.0 this plugin also checked FAQ markup, question headings and definitions. Those direct-answer checks now live in [ai-aeo](../ai-aeo/).

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
| `/geo-audit` | Audit the site for GEO and write a timestamped report to `docs/geo-audit/`. Optional live URL check and web search for brand mentions. |
| `/geo-fix` | Apply fixes from the latest audit with a diff for each change. Supports `--dry-run`. |
| `/geo-llms-txt` | Generate, update or validate `llms.txt` and `llms-full.txt`. Supports `--dry-run`. |

All skills are interactive. `/geo-audit` takes no arguments; `/geo-fix` and `/geo-llms-txt` accept only `--dry-run`.

---

## Usage

### Run an audit

```
/geo-audit
```

You'll be asked for the audit scope, whether to commit reports, and how far beyond the codebase to look: codebase only, plus a live URL, or plus a web search. The skill then:

1. Detects your framework (Next.js, Nuxt, TanStack Start, Astro, SvelteKit, Remix / React Router, or vanilla HTML) and hosting or edge config that can affect bots.
2. Checks whether Context7 MCP is available for current documentation.
3. Runs the ten checks under [What gets audited](#what-gets-audited).
4. With a live URL, compares the deployed robots.txt with the repo, checks that content is in the served HTML, and tests how the site responds to AI user agents.
5. With web search, takes a dated snapshot of third-party mentions and reviews of the brand and notes descriptions that don't match the site. The snapshot isn't scored, because results change from run to run.
6. Writes a timestamped report, an index with trend indicators and `latest.md` to `docs/geo-audit/` (see [Report output](#report-output)).

### Apply fixes

```
/geo-fix             # apply fixes interactively
/geo-fix --dry-run   # preview diffs without writing
```

`/geo-fix` reads `docs/geo-audit/latest.md` and sorts findings into:

- **Safe fixes**, confirmed once as a batch: `dateModified` from git history, JSON-LD validity, microdata to JSON-LD, and llms.txt discovery hints.
- **Fixes that need your intent**: three separate questions about AI training crawlers, AI search indexers and user-triggered fetchers before robots.txt changes, plus retired bot names, `Content-Signal` lines and user-agent logic in middleware. Snippet controls such as `nosnippet` and Bing's `nocache` are changed by `/aeo-fix`.
- **Fixes that need your content**: `Organization` and `Person` markup with the profile URLs you supply, author pages, sources for unsourced statistics, methodology notes, links to press coverage and review profiles. It never invents any of them.
- **Larger refactors**: server rendering for client-only pages, topic hub pages and internal links, merging thin pages, and paragraphs that only make sense in context.
- **Manual steps** it prints but doesn't automate: fixing third-party profiles, review platforms and directories, CDN bot settings, and tracking citations.

### Generate llms.txt

```
/geo-llms-txt             # generate, update or validate interactively
/geo-llms-txt --dry-run   # print the would-be files without writing
```

Generates, updates or validates `llms.txt` (and optionally `llms-full.txt`), places it where your framework serves static files, and offers discovery hints in the `<head>`, sitemap and robots.txt. Google Search ignores `llms.txt`. Some coding tools read it, and Chrome Lighthouse's agentic browsing audit checks for it. It's cheap to publish, but it isn't a citation lever.

---

## What gets audited

| Category | Weight | What it checks |
|----------|--------|----------------|
| AI Crawler Access | 15% | robots.txt rules for training crawlers, AI search indexers and user-triggered fetchers; Googlebot, Bingbot and Applebot; `Content-Signal` lines; retired bot names; middleware that treats bots differently |
| Technical AI Accessibility | 10% | Server-rendered or static content, content in the initial HTML, status codes, HTTPS, no cloaking |
| Topical Authority | 15% | Core topics, pages per topic, hub pages, internal links, orphan and thin pages |
| Original Research & Evidence | 15% | First-party data, methodology, statistics with linked sources, named quotations, primary sources, unsupported superlatives |
| Expert Perspectives & Authorship | 10% | Bylines, author pages, `Person` markup, reviewers on health, finance and legal topics, editorial pages |
| External Validation | 10% | Links to review profiles and press coverage, attributed testimonials, review markup that follows policy |
| Entity Clarity | 10% | `Organization` markup with `sameAs`, About page definition, consistent naming |
| Extractable Passages | 5% | Paragraphs that stand on their own, one idea per section, no walls of text |
| Content Freshness | 5% | Visible "last updated" dates, `dateModified`, stale time-sensitive pages |
| llms.txt & Markdown Access 🧪 | 5% | `llms.txt` format and discovery hints, Markdown copies matching the HTML |

Findings are rated Critical, High, Medium or Low, with 🧪 on heuristics and proposals. Each one has a file and line (or a live-check URL), the current code and a specific fix.

---

## AI crawler reference

### Training crawlers and tokens

| Bot | Operator | What it controls |
|-----|----------|------------------|
| `GPTBot` | OpenAI | Model training |
| `ClaudeBot` | Anthropic | Model training |
| `Google-Extended` | Google | A robots.txt token, not a crawler: Gemini training and grounding in Gemini Apps and Vertex AI. It doesn't affect Google Search, AI Overviews or AI Mode |
| `Applebot-Extended` | Apple | A token, not a crawler: Apple generative AI training |
| `meta-externalagent` | Meta | AI training and product improvement |
| `Amazonbot` | Amazon | Amazon products and services; may train Amazon AI models |
| `CCBot` | Common Crawl | Open web corpus many models train on |
| `MistralAI-Training` | Mistral | Model training |
| `Bytespider` | ByteDance | Reported as training; no vendor documentation |

### AI search indexers

| Bot | Operator | Feeds |
|-----|----------|-------|
| `OAI-SearchBot` | OpenAI | ChatGPT search |
| `Claude-SearchBot` | Anthropic | Claude search |
| `PerplexityBot` | Perplexity | Perplexity search (not training) |
| `Meta-WebIndexer` | Meta | Meta AI search |
| `Amzn-SearchBot` | Amazon | Alexa and Amazon search features (not training) |
| `MistralAI-Index` | Mistral | Mistral search (not training) |
| `DuckAssistBot` | DuckDuckGo | DuckAssist answers (not training) |
| `Googlebot` | Google | Google Search, including AI Overviews and AI Mode |
| `Bingbot` | Microsoft | Bing, which grounds Copilot |
| `Applebot` | Apple | Siri, Spotlight and Safari |

### User-triggered fetchers

| Bot | Operator | Follows robots.txt? |
|-----|----------|---------------------|
| `ChatGPT-User` | OpenAI | OpenAI says it "may not apply" |
| `Claude-User` | Anthropic | Yes |
| `Perplexity-User` | Perplexity | Perplexity says it "generally ignores" it |
| `meta-externalfetcher` | Meta | Meta says it "may bypass" it |
| `Amzn-User` | Amazon | Amazon says it may not follow all directives |
| `MistralAI-User` | Mistral | See Mistral's docs |
| `Google-Agent` | Google | Generally not; it acts on a user's request |

**A common setup** blocks training crawlers and allows AI search indexers and user-triggered fetchers, so the site can be cited without contributing training data. `/geo-fix` asks about each group separately. If a block has to hold, it needs CDN or firewall rules, because several fetchers say robots.txt may not apply.

**Google's AI features** are controlled by `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`, and the Search Console setting "Search generative AI" → Exclude, not by Google-Extended. **Copilot** respects Bing's `nocache` and `noarchive`.

**Your CDN may change the policy.** Since July 2025 Cloudflare has blocked AI crawlers by default on new domains, and its managed robots.txt can add rules. The live check compares the deployed file with the repo.

---

## Measuring citations

The audit measures readiness, not how often you're cited. To track that:

- **Bing Webmaster Tools → AI Performance** shows citations in Copilot and Bing AI summaries, with cited pages and grounding queries.
- **Google Search Console → Generative AI performance report** shows impressions in AI Overviews and AI Mode.
- **Server logs** show visits from the AI user agents above (check them against each operator's published IP ranges).
- **A fixed question list** asked of each assistant every month shows trends. `/aeo-questions` from [ai-aeo](../ai-aeo/) can build the list.

---

## What LLMs often get wrong about GEO

| What LLMs often do | What this plugin does |
|--------------------|-----------------------|
| Treat GEO as a synonym for SEO or AEO | Keeps citation checks here and direct-answer checks in ai-aeo |
| Split AI bots into "training" and "citation" only | Uses three groups: training, AI search and user-triggered |
| Block Google-Extended to leave AI Overviews | Explains it doesn't, and names the real controls |
| Assume robots.txt stops every AI bot | Notes which fetchers say it may not apply |
| Call llms.txt a ranking or citation signal | Rates it Low or Medium 🧪; Google Search ignores it |
| Recommend Markdown copies of pages for AI search | Treats them as optional and informational 🧪 |
| Suggest splitting content into small chunks for AI | Checks that paragraphs stand on their own, without fragmenting them |
| Invent statistics, quotes or sources to "add evidence" | Asks you for the source, your own data, or removal |
| Fabricate `sameAs` URLs, authors or reviews | Asks you; never invents identity or reviews |
| Recommend chasing mentions anywhere | Points to earned coverage and flags inauthentic tactics |
| Recommend cloaking for AI bots | Flags user-agent content changes as Critical |

---

## llms.txt primer

`llms.txt` is a Markdown index of a site's key pages, served at `/llms.txt`. Jeremy Howard proposed it at https://llmstxt.org/ in 2024. Google says Google Search ignores it, and no other major AI search provider has said it uses it. Some coding tools read it, and Chrome Lighthouse's agentic browsing audit checks for it, so it's most useful for developer documentation 🧪.

```markdown
# Site Name

> One-sentence description of the site.

## Section

- [Page title](https://example.com/page): one-line summary.
- [Another page](https://example.com/another): one-line summary.

## Optional

- [Secondary resource](https://example.com/secondary): summary.
```

- The H1 title is the only required part. A blockquote summary after it is optional in the spec, but the audit checks for it.
- H2 sections group bulleted links, each with a one-line summary.
- An `## Optional` section holds links a reader can skip when it needs a shorter context.

`llms-full.txt` is a companion with the full Markdown content of the linked pages.

---

## Report output

Reports go to `docs/geo-audit/`. If the project already uses `documentation/` or `.docs/`, the skill writes there instead.

```
docs/geo-audit/
├── README.md                                 # Index with trend indicators
├── latest.md                                 # Copy of the most recent audit
├── geo-audit-2026-10-06-143022.md            # Timestamped reports
├── geo-audit-2026-09-29-091544.md
└── ...
```

Timestamped reports are never overwritten. `latest.md` always reflects the most recent run (a file copy, not a symlink, so it works on every platform). Version 1.2.0 changed the categories, so the index marks the first 1.2.0 audit with 🔄 instead of comparing its score with older runs.

---

## Context7 MCP integration

When [Context7 MCP](https://github.com/upstash/context7) is installed, the plugin uses it for current documentation on the llms.txt proposal, AI crawler docs (OpenAI, Anthropic, Google, Perplexity, Apple, Meta, Amazon), Schema.org types and your framework's head APIs.

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Without Context7, the plugin falls back to training-data knowledge and marks more items with 🧪.

---

## Related plugins

- `/aeo-audit` ([ai-aeo](../ai-aeo/)) covers being the direct answer: answer-first paragraphs, question headings, definitions, FAQ sections and snippet controls.
- `/seo-audit` ([ai-seo](../ai-seo/)) covers traditional rankings. Google says its AI features rest on the same systems, so this one matters for AI Overviews too.

To check all three:

```
/seo-audit
/aeo-audit
/geo-audit
```

---

## Limits

- No AI provider publishes how it picks citations. The categories and weights are judgment informed by the GEO research and Google's and Microsoft's guidance.
- The off-site snapshot is a dated sample of web search results, not a full census of mentions.
- robots.txt states a policy; it doesn't prove enforcement. Live user-agent tests are indicative, because CDNs verify real crawlers by IP address.
- It doesn't measure citation frequency. See [Measuring citations](#measuring-citations).

---

## Plugin Details

- **Name:** `ai-geo`
- **Version:** 1.2.0
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
