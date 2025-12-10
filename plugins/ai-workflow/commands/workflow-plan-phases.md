---
name: workflow-plan-phases
description: "Creates a structured implementation plan document with properly sized phases for efficient sub-agent execution."
---

# Plan Phases

Creates a phased implementation plan from a feature description, optimized for context-efficient sub-agent execution.

## Usage

```
/plan-phases <description>
/plan-phases "Build a user authentication system with OAuth, MFA, and session management"
/plan-phases --output=docs/plans/auth-system.md "Build authentication system..."
```

## Arguments

- `description` (required): What the user wants to build
- `--output`: Custom output path (default: `docs/plans/{slugified-name}.md`)

## Workflow

1. Ask clarifying questions (always — never skip)
2. Size phases for context efficiency (30-50k tokens each)
3. Use whole numbers only (no Phase 1.1 sub-phases)
4. Define clear acceptance criteria per phase
5. Map dependencies and recommend execution strategy
6. Output structured markdown to docs/plans/
