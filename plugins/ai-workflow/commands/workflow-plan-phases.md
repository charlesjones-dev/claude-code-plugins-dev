---
name: workflow-plan-phases
description: "Creates a structured implementation plan document with properly sized phases for efficient sub-agent execution."
---

# Plan Phases

Creates a phased implementation plan from a feature description, optimized for context-efficient sub-agent execution.

## Usage

```bash
/workflow-plan-phases <description>
/workflow-plan-phases "Build a user authentication system with OAuth, MFA, and session management"
/workflow-plan-phases --output=docs/plans/auth-system.md "Build authentication system..."
```

## Arguments

- `description` (required): What the user wants to build
- `--output`: Custom output path (default: `docs/plans/{slugified-name}.md`)

## Instructions

1. **Read the user's description** from the command argument
2. **Ask clarifying questions** before creating the plan — never skip this step
3. **Wait for user responses** before proceeding
4. **Create the plan document** following the plan-phases skill methodology
5. **Save to `docs/plans/`** (create directory if needed) using a slugified filename
6. **Present the plan** and ask if changes are needed
7. **Stop** — do not implement

## Workflow

1. Ask clarifying questions (always — never skip)
2. Size phases for context efficiency (30-50k tokens each)
3. Use whole numbers only (no Phase 1.1 sub-phases)
4. Define clear acceptance criteria per phase
5. Map dependencies and recommend execution strategy
6. Output structured markdown to docs/plans/
7. **STOP** — do not implement the plan

## Important

**This command only creates the plan. Do NOT proceed to implement any phases.**

After the plan is written:
- Present the plan document to the user
- Ask if they want to make any changes
- Inform them they can use `/workflow-implement-phases` when ready to execute

**Never start writing code or implementing phases after creating the plan.**
