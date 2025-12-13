---
name: workflow-implement-phases
description: "Orchestrates multi-phase implementation from a plan document using intelligent parallel/sequential execution strategy."
---

# Implement Phases

Analyzes phases from a plan document and orchestrates implementation using sub-agents with optimal execution strategy.

## Usage

```bash
/workflow-implement-phases                    # Search docs/plans/ and pick one
/workflow-implement-phases @path/to/plan.md
/workflow-implement-phases @path/to/plan.md --phases=1,2,3
/workflow-implement-phases @path/to/plan.md --strategy=parallel|sequential|auto
```

## Arguments

- `plan_file` (optional): Path to the plan document. If omitted, searches `docs/plans/` for existing plans
- `--phases`: Comma-separated list of specific phases to implement (default: all)
- `--strategy`: Force execution strategy. Default is `auto` (analyzed)

## Instructions

### If a plan file is provided:
Read the plan file passed as an argument (e.g., `@docs/plans/my-plan.md`) and proceed with the workflow.

### If no plan file is provided:
1. Search for existing plan files in `docs/plans/` directory
2. If plans are found, present them to the user and ask which one to implement
3. If no plans are found, inform the user and suggest using `/workflow-plan-phases` to create one first

## Workflow

1. **Read the plan file** — Use the Read tool to load the plan document
2. Parse plan document and extract phases
3. Analyze dependencies (explicit and implicit)
4. Determine optimal execution strategy (parallel/sequential/mixed)
5. Present execution plan to user for confirmation
6. Execute via Task() sub-agents with coordination directory
7. Aggregate results and report
