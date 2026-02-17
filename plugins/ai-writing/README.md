# AI-Writing Plugin

**Writing quality tools for Claude Code.** Detect and remove signs of AI-generated text to make writing sound natural and human-written.

---

## What This Plugin Does

Provides tools for improving writing quality, starting with the humanizer skill that identifies and removes common AI writing patterns. Based on Wikipedia's "Signs of AI writing" guide maintained by WikiProject AI Cleanup.

## Available Skills

### `/writing-humanize`

Remove AI writing patterns from text to make it sound natural and human-written.

**What it does:**

- Scans text for 24 documented AI writing patterns
- Rewrites problematic sections with natural alternatives
- Preserves meaning while improving voice and personality
- Handles content patterns, language/grammar patterns, style patterns, communication patterns, and filler/hedging

**Patterns detected:**

- Inflated significance ("pivotal moment", "stands as a testament")
- Promotional language ("vibrant", "nestled", "breathtaking")
- Superficial -ing analyses ("highlighting", "underscoring", "reflecting")
- Vague attributions ("experts argue", "industry reports")
- Overused AI vocabulary ("delve", "landscape", "tapestry", "crucial")
- Em dash overuse, rule of three, negative parallelisms
- Sycophantic tone, filler phrases, excessive hedging
- Generic positive conclusions, chatbot artifacts

**Usage:**

```
/writing-humanize
# Then provide the text you want to humanize

# Works with:
# - README files and documentation
# - Blog posts and articles
# - Commit messages and PR descriptions
# - Any text that sounds too "AI-generated"
```

---

## Quick Start

### Installation

```
/plugin install ai-writing@claude-code-plugins-dev
```

### Usage

```
# Humanize a piece of text
/writing-humanize

# Provide your text and Claude will:
# 1. Identify AI patterns
# 2. Rewrite problematic sections
# 3. Preserve meaning and add personality
# 4. Present the humanized version with a summary of changes
```

---

## Plugin Details

- **Name:** AI-Writing Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Skill:** `/writing-humanize`
- **Version:** 1.0.0
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built for developers who want their writing to sound like a human wrote it.**
