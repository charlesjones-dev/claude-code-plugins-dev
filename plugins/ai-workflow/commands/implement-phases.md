---
name: implement-phases
description: "Orchestrates multi-phase implementation from a plan document using intelligent parallel/sequential execution strategy."
---

# Implement Phases

Analyzes phases from a plan document and orchestrates implementation using sub-agents with optimal execution strategy.

## Usage

```
/implement-phases @path/to/plan.md
/implement-phases @path/to/plan.md --phases=1,2,3
/implement-phases @path/to/plan.md --strategy=parallel|sequential|auto
```

## Arguments

- `plan_file` (required): Path to the plan document containing phase definitions
- `--phases`: Comma-separated list of specific phases to implement (default: all)
- `--strategy`: Force execution strategy. Default is `auto` (analyzed)

## Workflow

1. Parse plan document and extract phases
2. Analyze dependencies (explicit and implicit)
3. Determine optimal execution strategy (parallel/sequential/mixed)
4. Present execution plan to user for confirmation
5. Execute via Task() sub-agents with coordination directory
6. Aggregate results and report
