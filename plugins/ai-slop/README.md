# AI-Slop Plugin

**AI slop audits for Claude Code.** Find what a codebase shows its users that reads as machine-made, and what in it is wrong.

---

## What This Plugin Does

`/slop-audit` reads every surface a user sees: pages and shared layout, components and data files that carry copy, forms, emails, visible error text, legal pages, metadata, app strings and store listings, READMEs and `--help` output. It reports four kinds of problem:

- **Copy** that reads as AI-written: em dashes, "X, not Y" slogans, triplets, filler, inflated vocabulary, résumé voice
- **Layouts** that read as templates: the centered hero, icon grid and logo marquee stack, decorative badges, stock icon tiles, default AI palettes
- **Metadata** built from boilerplate: one tagline repeated across meta tags, JSON-LD, `llms.txt` and the manifest, or descriptions that promise content the site doesn't have
- **Errors**: a privacy policy that misses the fonts, analytics or pixels the code loads; prices, reply times or product lists that differ between pages; claims another page contradicts; links and components that lead nowhere

It changes nothing until you answer its questions.

## Available Skills

### `/slop-audit`

**How it works:**

1. Reads the project's own rules first (`CLAUDE.md`, `AGENTS.md`, a `docs/kb/` knowledge base, voice or style docs, `DESIGN.md`), so it doesn't flag documented house style or re-ask questions an earlier audit settled
2. Lists every user-facing surface before reading, and splits large repos across parallel read-only subagents
3. Counts habits that repeat across the site, and how many files each appears in
4. Checks legal pages against the code and, given a live URL, against the scripts the live page loads
5. Scores each area from 0 to 100, quotes each finding with `file:line`, and gives a concrete fix for every one
6. Ends with a fix plan, the defaults it will use, and numbered questions you can answer in one reply

After you answer, it applies the fixes, removes the old wording from every metadata surface, regenerates OG images and updates legal effective dates where needed, runs the project's checks, and records your answers as project rules so later sessions don't bring the old copy back.

The signal checklist is [`signals.md`](skills/slop-audit/signals.md). Rules in the project override it.

Claude also runs the skill when you ask whether a site, app or README reads as AI-written.

**Usage:**

```
/slop-audit
/slop-audit skip the blog
/slop-audit only /about https://example.com
```

### Related plugins

- `/writing-humanize` ([ai-writing](../ai-writing/)) rewrites text you point it at. `/slop-audit` covers every user-facing surface in a repo and checks facts too.
- `/modernize-audit` ([ai-modernize](../ai-modernize/)) covers slop in the code itself: anti-patterns and technical debt left by older AI-generated code.

---

## Quick Start

### Installation

```
/plugin install ai-slop@claude-code-plugins-dev
```

---

## Plugin Details

- **Name:** AI-Slop Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Skill:** `/slop-audit`
- **Version:** 1.0.0
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License. See [LICENSE](LICENSE).
