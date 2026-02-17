---
name: writing-humanize
description: "Remove signs of AI-generated writing from text. Detects and fixes 24 documented AI writing patterns to make text sound natural and human-written."
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanize Writing

Identify and remove signs of AI-generated text. Rewrite to sound natural, specific, and human. Based on patterns documented by Wikipedia's WikiProject AI Cleanup.

## Instructions

**CRITICAL**: This command MUST NOT accept any arguments. If the user provided any text, URLs, or paths after this command (e.g., `/writing-humanize README.md` or `/writing-humanize fix my blog post`), you MUST COMPLETELY IGNORE them. Do NOT use any arguments that appear in the user's message. You MUST ONLY gather input through the interactive workflow below.

### Step 1: Determine input source

Use the AskUserQuestion tool:

- Question: "What do you want to humanize?"
  - Header: "Input"
  - Options:
    - "A file in the project" (description: "Specify a file path or glob pattern to rewrite")
    - "Text I'll paste" (description: "Paste or type text directly in the chat")
    - "Scan project docs" (description: "Find markdown files in README, CHANGELOG, docs/, etc.")
  - multiSelect: false

If the user selects **"A file in the project"**: ask for the file path or glob pattern using AskUserQuestion with a text input prompt. Then read the file(s) with the Read tool.

If the user selects **"Text I'll paste"**: tell the user to paste their text in the next message, then wait for it.

If the user selects **"Scan project docs"**: use Glob to find markdown and text files (`**/*.md`, `**/*.txt`, `**/docs/**`). Present the list and let the user pick which file(s) to humanize using AskUserQuestion.

### Step 2: Detect content type

Use the AskUserQuestion tool:

- Question: "What type of content is this?"
  - Header: "Content type"
  - Options:
    - "Technical docs / API reference" (description: "Precision matters; no personality injection")
    - "README / project docs" (description: "Light personality OK; remove inflation")
    - "Blog post / article" (description: "Full personality; all patterns apply")
    - "PR description / commit / changelog" (description: "Brevity focus; strip filler")
  - multiSelect: false

The content type determines which rewriting rules apply. See the **Content-type rules** section below.

### Step 3: Choose intensity

Use the AskUserQuestion tool:

- Question: "How aggressive should the rewrite be?"
  - Header: "Intensity"
  - Options:
    - "Light pass (Recommended)" (description: "Fix obvious AI-isms only; preserve most of the original")
    - "Standard" (description: "Rewrite problematic sections; keep structure")
    - "Heavy" (description: "Full rewrite for natural voice; may restructure")
  - multiSelect: false

### Step 4: Analyze and rewrite

1. Read the input text
2. Scan for patterns from the **Pattern catalog** below
3. Apply the **Content-type rules** to determine which fixes are appropriate
4. Rewrite according to the selected intensity:
   - **Light**: only fix clear AI tells (filler phrases, hedging, chatbot artifacts, curly quotes, emoji headers)
   - **Standard**: fix all detected patterns; rewrite sentences where needed; preserve overall structure
   - **Heavy**: rewrite freely for natural voice; restructure paragraphs; vary rhythm; add specificity
5. Preserve meaning. Do not invent facts or add information that was not in the original.

### Step 5: Present results

1. Show the rewritten text
2. Below it, provide a brief summary of changes: which pattern categories were found and what was fixed
3. If the input was a file: ask the user if they want to apply the changes using the Edit tool

---

## Content-type rules

| Content type | Personality | Key focus | Skip these patterns |
|---|---|---|---|
| Technical docs / API reference | None. No first-person, no opinions, no humor. | Remove filler, hedging, promotional language. Preserve precision. | Voice/personality rules, first-person injection |
| README / project docs | Light. Brief asides OK. | Remove promotional inflation, buzzword stacking, vague claims. Keep specifics. | Heavy personality injection, humor |
| Blog post / article | Full. Opinions, humor, varied rhythm encouraged. | All patterns apply. Inject voice and specificity. | None |
| PR / commit / changelog | None. Brevity above all. | Strip filler, hedging, promotional language. Compress. | Voice/personality rules, formatting patterns (lists are fine) |

---

## Pattern catalog

Grouped from 24 documented patterns. Each group has a combined word list and one before/after example.

### 1. Inflated language

Patterns: significance/legacy inflation, notability claims, promotional tone, overused AI vocabulary.

**Words to watch:** stands/serves as, testament, pivotal, crucial, vital, key (adj.), underscores, highlights, reflects broader, enduring, lasting, setting the stage, evolving landscape, indelible mark, deeply rooted, vibrant, rich (figurative), profound, showcasing, exemplifies, commitment to, nestled, in the heart of, groundbreaking, renowned, breathtaking, stunning, delve, tapestry, interplay, intricate, garnered, valuable, Additionally, fostering, enhance

**Before:**
> Nestled in the heart of downtown, this groundbreaking startup serves as a testament to the vibrant innovation ecosystem, showcasing the intricate interplay between technology and community.

**After:**
> The startup is based downtown. It builds inventory tools for restaurants.

### 2. Fake depth

Patterns: superficial -ing analyses, vague attributions, formulaic "challenges and future prospects" sections, negative parallelisms ("not just X, it's Y"), rule-of-three overuse, false ranges ("from X to Y").

**Words to watch:** highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, showcasing, industry reports, experts argue, observers have cited, despite its... faces several challenges, not only... but also, it's not just about... it's about, from X to Y

**Before:**
> It's not just about code quality; it's about fostering a culture of excellence. Industry experts have highlighted how the tool encompasses everything from automated testing to seamless deployment, ensuring teams can overcome challenges while cultivating best practices.

**After:**
> The tool runs tests and deploys code. Teams at Stripe and Shopify reported fewer production incidents after adopting it, according to a 2024 case study by ThoughtWorks.

### 3. Unnatural grammar

Patterns: copula avoidance ("serves as" instead of "is"), synonym cycling, filler phrases, excessive hedging.

**Words to watch:** serves as, stands as, marks, represents, boasts, features, offers (as copula substitutes), it is important to note that, in order to, due to the fact that, at this point in time, has the ability to, in the event that, could potentially possibly, it could be argued that

**Common filler substitutions:**

| Filler | Replacement |
|---|---|
| In order to achieve this goal | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that you need help | If you need help |
| The system has the ability to | The system can |
| It is important to note that the data shows | The data shows |

**Before:**
> The platform serves as a comprehensive solution that boasts an array of features. It is important to note that the system has the ability to process requests. The tool offers integration. The solution provides monitoring. The framework features logging.

**After:**
> The platform processes requests, integrates with existing tools, and logs everything. It also includes monitoring.

### 4. Formatting tells

Patterns: em dash overuse, mechanical boldface, inline-header vertical lists ("**Header:** text"), title case in headings, emoji decoration, curly quotation marks.

**What to fix:**
- Replace em dashes with commas, periods, or parentheses
- Remove mechanical boldface emphasis (keep bold only where it serves a real purpose)
- Convert inline-header lists to prose or simpler lists
- Use sentence case for headings (capitalize only the first word and proper nouns)
- Remove decorative emojis from headings and bullet points
- Replace curly quotes (“” ‘’) with straight quotes (" " ' ')

**Before:**
> ## Key Features And Benefits
>
> - 🚀 **Performance:** The system delivers blazing-fast response times—even under heavy load.
> - 💡 **Insights:** Real-time analytics provide "actionable intelligence" for decision-makers.
> - ✅ **Reliability:** 99.9% uptime—guaranteed.

**After:**
> ## Key features and benefits
>
> The system responds quickly under load, provides real-time analytics, and maintains 99.9% uptime.

### 5. Chatbot artifacts

Patterns: collaborative communication leftovers, knowledge-cutoff disclaimers, sycophantic tone.

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like me to, let me know if, here is a, Great question!, That's an excellent point, as of [date], up to my last training update, while specific details are limited, based on available information

**Before:**
> Great question! Here is an overview of the authentication system. As of my last update, the library supports OAuth 2.0. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The authentication system uses OAuth 2.0. Tokens expire after 24 hours and refresh automatically.

### 6. Weak endings

Patterns: generic positive conclusions, vague optimism, section-ending summaries that repeat what was just said.

**Words to watch:** the future looks bright, exciting times lie ahead, continues to evolve, journey toward excellence, a step in the right direction, in conclusion, to summarize, as we have seen, remains to be seen

**Before:**
> The framework continues to evolve, and the future looks bright. Exciting times lie ahead as the community continues its journey toward building better software. This represents a major step in the right direction.

**After:**
> Version 4.0 ships in March with streaming support and a new plugin API.

---

## Developer-specific patterns

These appear frequently in READMEs, docs, and PR descriptions written or rewritten by AI.

**README inflation:**
- Buzzword stacking: "robust, scalable, maintainable, seamless, cutting-edge, state-of-the-art, battle-tested, enterprise-grade, developer-friendly"
- Replace with specifics. Instead of "a robust and scalable solution," say what it actually does and how big it can get.

**Documentation over-explanation:**
- "This function takes X and returns Y" when the signature already says that
- Only document non-obvious behavior, constraints, or gotchas

**Unnecessary prefixes:**
- "Note:", "Important:", "Please note that", "It's worth mentioning that"
- Usually the sentence works fine without the prefix

**PR/commit message padding:**
- "This PR addresses the issue where...", "This commit implements the functionality for..."
- Just say what changed: "Fix race condition in queue drain" not "This PR addresses a race condition that was occurring in the queue drain process"

**Buzzword stacking in project descriptions:**
- "A modern, lightweight, blazing-fast, developer-friendly CLI tool"
- Pick one or two real qualities and be specific about them

---

## Voice and personality guidelines

These rules scale with content type. Full application for blog posts, partial for READMEs, skip entirely for technical docs and commit messages.

**Vary your rhythm.** Short sentences. Then longer ones that take their time. Mix it up. Monotone sentence length is an AI tell even when the words are fine.

**Have opinions.** Don't just report facts neutrally. "I genuinely don't know how to feel about this" is more human than listing pros and cons with no reaction.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats a clean pro/con list.

**Use "I" when it fits.** First person is not unprofessional. "I keep coming back to..." or "Here's what bugs me..." signals a real person thinking.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

**Let some mess in.** Perfect parallel structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

**Content-type caveat:** these guidelines apply fully to blog posts and articles. For READMEs, use a lighter touch (brief asides, mild opinions). For technical docs and commit messages, skip personality entirely.

---

*Pattern catalog based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.*
