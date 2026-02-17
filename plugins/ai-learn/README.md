# AI-Learn Plugin

**Socratic learning mode for Claude Code.** Transform Claude into a patient coding mentor that guides you through problem-solving instead of just writing code for you.

---

## What This Plugin Does

Switches Claude from code-generation mode to teaching mode. Instead of giving you solutions, Claude asks probing questions, provides hints, and guides you toward discovering answers yourself. The result: you actually learn and retain the knowledge rather than passively consuming AI-generated code.

## Available Skills

### `/learn`

Activate Socratic teaching mode for your next coding problem.

**What it does:**

- Assesses your current knowledge before diving in
- Asks guiding questions instead of providing answers
- Offers hints when you're stuck rather than solutions
- Helps you trace through logic and discover bugs yourself
- Reinforces learning by having you explain solutions in your own words

**Usage:**

```
/learn
# Then describe what you want to learn:
"I want to understand how to implement a binary search tree"

# Claude will ask about your current knowledge
# Guide you through the implementation step by step
# Let you write the code yourself
# Help you debug through questions, not answers
```

### `/learn-review`

Get a Socratic code review - Claude asks questions to help you spot issues yourself.

**What it does:**

- Reviews your code through targeted questions
- Helps you discover bugs by tracing through edge cases
- Probes design decisions to deepen understanding
- Builds your self-review and debugging skills

**Usage:**

```
/learn-review
# Then paste your code

# Claude will ask you to explain what it does
# Guide you through edge cases with questions
# Help you discover issues yourself
# Build lasting debugging intuition
```

---

## Quick Start

### Installation

```
/plugin install ai-learn@claude-code-plugins-dev
```

### Usage

```
# Activate teaching mode
/learn

# Describe what you want to learn
"Help me understand async/await in JavaScript"

# Claude guides you through it with questions
# You write the code, Claude provides hints
# You actually learn instead of copy-pasting
```

---

## Why Use Teaching Mode?

### The Problem with Code Generation

When Claude writes code for you:
- You get a working solution immediately
- But you may not understand why it works
- You can't reproduce it without asking again
- Your fundamental skills may atrophy over time

### The Teaching Mode Approach

When Claude teaches you:
- You struggle productively with the problem
- You build mental models that stick
- You develop intuition for similar problems
- You retain knowledge for future use

### When to Use Each

**Use teaching mode (`/learn`) for:**
- Unfamiliar libraries or frameworks
- Complex patterns you want to deeply understand
- Skills you're rusty on and need to refresh
- Concepts you keep having to look up

**Use standard Claude for:**
- Boilerplate you understand but don't want to type
- Quick fixes in areas you're confident
- Time-sensitive tasks where speed matters
- Repetitive tasks that don't need deep understanding

---

## The Teaching Flow

### Phase 1: Assessment
Claude asks what you already know to meet you where you are.

### Phase 2: Foundation
Fills in prerequisite knowledge gaps before tackling the main problem.

### Phase 3: Guided Implementation
You write code while Claude asks questions and provides hints.

### Phase 4: Error Discovery
When bugs appear, Claude guides you to find them through questions.

### Phase 5: Reinforcement
You explain the solution in your own words to solidify understanding.

---

## Example Interaction

```
User: /learn
User: I want to implement debouncing in JavaScript

Claude: Before we dive in, what's your understanding of
        closures in JavaScript? Debouncing relies heavily
        on them.

User: I know closures let inner functions access outer
      variables even after the outer function returns.

Claude: Perfect. And what about setTimeout - how does
        that work with closures?

User: The callback can access variables from when
      setTimeout was called.

Claude: Exactly. So here's the core puzzle: if you want
        a function that only runs after the user stops
        typing for 300ms, what would you need to track?

User: The timer ID so I can cancel it?

Claude: Right! And where would you store that ID so it
        persists between calls but isn't global?

User: In a closure!

Claude: Now you're getting it. Try writing the skeleton
        of a debounce function. What parameters would it
        take?
```

---

## Escape Hatch

Teaching mode respects your autonomy. If you hit genuine frustration:

- Say "just show me" and Claude will provide the solution with explanation
- Say "I give up" and Claude will walk through the answer
- You can always return to teaching mode for the next problem

Learning requires agency. Forced struggle past the point of productivity isn't helpful.

---

## Plugin Details

- **Name:** AI-Learn Plugin
- **Type:** AI Instruction Plugin (Skills)
- **Skills:** `/learn`, `/learn-review`
- **Version:** 1.1.0
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built for developers who want to learn, not just ship.**
