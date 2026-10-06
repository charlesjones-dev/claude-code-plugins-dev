# AI-Writing Plugin

**Writing tools for Claude Code.** `/writing-humanize` rewrites text to remove the patterns that make it read as AI-generated.

---

## What This Plugin Does

One skill, `/writing-humanize`, based on Wikipedia's "Signs of AI writing" guide, maintained by WikiProject AI Cleanup.

## Available Skills

### `/writing-humanize`

**What it does:**

- Scans text for 26 AI writing patterns in six groups, plus five developer-specific patterns for READMEs, docs, and PRs
- Rewrites at the intensity you pick: light, standard, or heavy
- Keeps the meaning and doesn't add facts
- Adds personality only where the content type allows it: none for technical docs or PR/commit/changelog text, light for READMEs, full for blog posts

**Patterns detected:**

- Inflated language ("pivotal", "stands as a testament", "vibrant", "nestled", "delve", "tapestry")
- Fake depth ("highlighting", "experts argue", negative parallelisms, rule of three)
- Unnatural grammar ("serves as" instead of "is", filler phrases, excessive hedging)
- Formatting tells (em dash overuse, mechanical boldface, title-case headings, emoji decoration)
- Chatbot artifacts ("I hope this helps", knowledge-cutoff disclaimers, sycophantic tone)
- Weak endings (generic positive conclusions, "the future looks bright")
- Developer-specific (README buzzword stacking, "Note:" prefixes, PR padding)

**Usage:**

```
/writing-humanize
# Asks what to humanize: a file, text you paste, or project docs it finds
# Asks the content type: technical docs, README, blog post, or PR/commit/changelog
# Asks the intensity: light, standard, or heavy
# Shows the rewrite and a summary of changes; for files, asks before applying them
```

---

## Quick Start

### Installation

```
/plugin install ai-writing@claude-code-plugins-dev
```

---

## Plugin Details

- **Name:** AI-Writing Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Skill:** `/writing-humanize`
- **Version:** 1.0.1
- **License:** [MIT](LICENSE)
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
