---
name: implement-phases
description: "Use when implementing phases from a plan document, executing phased implementations, orchestrating sub-agents for phase work, or when /workflow-implement-phases command is invoked. Provides dependency analysis and parallel/sequential execution strategies."
---

# Phase Implementation Orchestration Skill

This skill provides the methodology for analyzing plan documents, determining optimal execution strategies, and coordinating phase implementation through sub-agents.

## Overview

When implementing phases from a plan document, the orchestrator must:
1. Extract and understand each phase's scope
2. Detect dependencies (explicit and implicit)
3. Choose optimal execution strategy
4. Coordinate sub-agents for implementation
5. Handle failures gracefully
6. Aggregate and report results

---

## CRITICAL: Mandatory Sub-Agent Requirement

**YOU MUST USE THE TASK TOOL TO SPAWN A SUB-AGENT FOR EVERY PHASE IMPLEMENTATION.**

This is a non-negotiable requirement. The orchestrator (main agent) is ONLY responsible for:
- Reading and parsing the plan document
- Analyzing dependencies
- Determining execution strategy
- Presenting the plan to the user
- Spawning Task() sub-agents for each phase
- Aggregating results after sub-agents complete

**The orchestrator MUST NOT:**
- Implement any phase directly in the main conversation
- Write code, create files, or make changes for any phase
- Skip sub-agent spawning for "simple" phases
- Combine multiple phases into a single implementation

**Why this matters:**
- Context isolation: Each sub-agent has fresh context, preventing saturation
- Parallelization: Independent phases can run in parallel via multiple Task() calls
- Failure isolation: A failed phase doesn't corrupt the main agent's state
- Results tracking: Sub-agents write structured results to coordination directory

**Correct pattern:**
```
# For each phase (or group of parallel phases), spawn Task() sub-agents
Task(
  subagent_type="general-purpose",
  prompt="[Phase implementation prompt with full spec and acceptance criteria]",
  description="Implement phase-1: [name]"
)
```

**WRONG pattern (never do this):**
```
# Never implement phases directly
Edit(file_path="src/feature.ts", ...)  # WRONG - orchestrator should not edit files
Write(file_path="src/new-file.ts", ...)  # WRONG - orchestrator should not create files
```

---

## Step 1: Parse the Plan Document

Extract from the plan file:

```
phases = [
  {
    id: "phase-1",
    name: "Human-readable name",
    spec: "Full specification text",
    acceptance_criteria: ["criterion 1", "criterion 2"],
    explicit_dependencies: ["phase-0"]  // if stated
  },
  ...
]
```

### Parsing Heuristics

Look for phase definitions in these formats:
- `## Phase 1:`, `### Phase 1 -`, `**Phase 1**`
- `# Step 1`, `## Step 1:`
- Numbered sections: `1.`, `1)`, `(1)`
- YAML frontmatter with phase definitions

Extract acceptance criteria from:
- Bullet points under "Acceptance Criteria", "Done when", "Requirements"
- Checkboxes: `- [ ] criterion`
- "Must have", "Should", "Will" statements

---

## Step 2: Dependency Analysis

### Explicit Dependencies (Highest Confidence)

Patterns that indicate explicit ordering:
- "Phase 2 requires Phase 1"
- "After completing X, proceed to Y"
- "Once X is done, Y can begin"
- "Depends on:", "Prerequisites:", "Requires:"
- "Do not start until X is complete"

### Implicit Dependencies (Analyze Code Paths)

**Data/Schema Dependencies**
```
DEPENDENT if Phase B:
- References database tables created in Phase A
- Uses migrations from Phase A
- Queries data that Phase A populates
```

**API/Interface Dependencies**
```
DEPENDENT if Phase B:
- Calls endpoints defined in Phase A
- Imports services/modules created in Phase A
- Uses types/interfaces exported by Phase A
```

**File Dependencies**
```
DEPENDENT if Phase B:
- Modifies files created in Phase A
- Extends classes defined in Phase A
- Imports from paths that Phase A creates
```

**Configuration Dependencies**
```
DEPENDENT if Phase B:
- Requires environment variables Phase A documents
- Uses config keys Phase A introduces
- Needs secrets/credentials Phase A sets up
```

**Build Dependencies**
```
DEPENDENT if Phase B:
- Requires compiled output from Phase A
- Uses generated code from Phase A
- Needs artifacts (bundles, images) from Phase A
```

### Independence Indicators (Safe to Parallelize)

High confidence parallel candidates:
- Phases operate on completely separate directories
- Phases add isolated features (no shared imports)
- Phases are orthogonal concerns (logging vs caching vs monitoring)
- Plan explicitly states "can be done in any order"
- Phases are different layers (frontend vs backend vs infra)

### Dependency Detection Algorithm

```
for each phase_b in phases:
  for each phase_a in phases where phase_a != phase_b:

    # Check explicit
    if phase_b.spec mentions phase_a.id as dependency:
      add_dependency(phase_b, phase_a, confidence=HIGH)

    # Check implicit - file paths
    files_created_by_a = extract_file_paths(phase_a.spec)
    files_referenced_by_b = extract_file_paths(phase_b.spec)
    if intersection(files_created_by_a, files_referenced_by_b):
      add_dependency(phase_b, phase_a, confidence=MEDIUM)

    # Check implicit - imports/types
    exports_from_a = extract_exports(phase_a.spec)
    imports_in_b = extract_imports(phase_b.spec)
    if intersection(exports_from_a, imports_in_b):
      add_dependency(phase_b, phase_a, confidence=MEDIUM)

    # Check implicit - keywords
    if phase_b.spec contains "after {phase_a.name}":
      add_dependency(phase_b, phase_a, confidence=HIGH)
    if phase_b.spec contains "using {artifact from phase_a}":
      add_dependency(phase_b, phase_a, confidence=MEDIUM)
```

---

## Step 3: Build Execution Graph

### Strategy Selection

**PARALLEL** - All phases run simultaneously:
```
Conditions:
- No dependencies between any phases
- Phases operate on isolated code paths
- No shared files being modified
- Low risk of merge conflicts

Benefits:
- Fastest total execution time
- Maximum context isolation

Risks:
- Potential merge conflicts if analysis missed shared files
```

**SEQUENTIAL** - Phases run one after another:
```
Conditions:
- Linear dependency chain exists
- Each phase depends on previous
- Shared state or files across phases
- High integration complexity

Benefits:
- Safest execution
- Each phase has full context from prior phases
- Easier debugging

Risks:
- Slowest execution
- Context may still accumulate if not managed
```

**MIXED** - Parallel groups with sequential ordering between groups:
```
Conditions:
- Some phases are independent (parallel within group)
- Some phases have dependencies (sequential between groups)

Algorithm:
1. Build dependency graph
2. Topologically sort into levels
3. Phases at same level (no dependencies on each other) run parallel
4. Wait for level to complete before starting next level

Example:
  Level 0: [phase-1, phase-3]     # No dependencies, run parallel
  Level 1: [phase-2]              # Depends on phase-1
  Level 2: [phase-4, phase-5]     # Both depend on phase-2
```

### Execution Plan Template

Present to user before executing:

```markdown
## Phase Execution Plan

### Phases Analyzed
| Phase | Description | Dependencies | Level |
|-------|-------------|--------------|-------|
| phase-1 | Create user model | None | 0 |
| phase-3 | Add logging | None | 0 |
| phase-2 | Authentication | phase-1 | 1 |
| phase-4 | User API | phase-2 | 2 |
| phase-5 | Admin API | phase-2 | 2 |

### Execution Strategy: **MIXED**

```
Level 0 (parallel):  phase-1 -+- phase-3
                              |
Level 1 (sequential): phase-2 <+
                              |
Level 2 (parallel):  phase-4 -+- phase-5
```

### Dependency Reasoning
- phase-1 <-> phase-3: Independent (separate directories)
- phase-2 -> phase-1: Uses User model (import dependency)
- phase-4 -> phase-2: Uses auth middleware (API dependency)
- phase-5 -> phase-2: Uses auth middleware (API dependency)
- phase-4 <-> phase-5: Independent (separate route files)

### Estimated Execution
- 3 sub-agent cycles (parallel reduces from 5 sequential)

Proceed? [Y/n/modify]
```

---

## Step 4: Execute Phases

**REMINDER: You MUST use Task() sub-agents for ALL phase implementations. Never implement directly.**

### Coordination Setup

```bash
mkdir -p .claude/phase-coordination/{artifacts,results}
```

### Sub-Agent Prompt Template

When spawning Task() for each phase (REQUIRED for every phase):

```markdown
## Phase Implementation Task

**Phase ID**: {phase_id}
**Phase Name**: {phase_name}

### Specification
{full_phase_spec}

### Acceptance Criteria
{acceptance_criteria_list}

### Context from Prior Phases
{if sequential or mixed, include summary from dependency phases}

Read artifacts from: `.claude/phase-coordination/artifacts/`
Write your artifacts to: `.claude/phase-coordination/artifacts/{phase_id}/`

### Required Outputs

1. **Implement the phase** according to specification

2. **Create results file** at `.claude/phase-coordination/results/{phase_id}.md`:

```markdown
# {phase_id} Results

## Summary
[2-3 sentences on what was implemented]

## Files Changed
- `path/to/file` - [description]

## Key Decisions
- [Decision]: [Rationale]

## Interfaces Exposed
[Types, functions, or contracts for downstream phases]

## Deviations
[Any deviations from spec with justification]

## Verification
[How to verify this phase works]
```

3. **Export any shared artifacts** (types, interfaces, schemas) to the artifacts directory

### Quality Standards
- No placeholder code or TODOs
- Match existing project conventions
- Handle errors appropriately
- Include inline documentation for complex logic
```

### Parallel Execution Pattern

**Use multiple Task() calls in a SINGLE message to execute phases in parallel:**

```
# Spawn all phases in current level simultaneously using multiple Task() calls in ONE message
# This is the ONLY way to achieve true parallelization

# In your response, include ALL of these Task() calls together:
Task(
  subagent_type="general-purpose",
  prompt=build_phase_prompt(phase_1),
  description="Implement phase-1: [name]"
)
Task(
  subagent_type="general-purpose",
  prompt=build_phase_prompt(phase_2),
  description="Implement phase-2: [name]"
)
Task(
  subagent_type="general-purpose",
  prompt=build_phase_prompt(phase_3),
  description="Implement phase-3: [name]"
)

# All tasks run in parallel when called in the same message
# Wait for all to complete
# Collect results from .claude/phase-coordination/results/
```

### Sequential Execution Pattern

**Each phase STILL requires its own Task() sub-agent, just called one at a time:**

```
for phase in topologically_sorted_phases:
  # Build context from dependencies
  dependency_context = ""
  for dep in phase.dependencies:
    dep_results = read(f".claude/phase-coordination/results/{dep.id}.md")
    dependency_context += f"\n### Context from {dep.id}\n{dep_results}"

  # Execute with dependency context - MUST use Task(), never implement directly
  Task(
    subagent_type="general-purpose",
    prompt=build_phase_prompt(phase, dependency_context),
    description="Implement {phase.id}: {phase.name}"
  )

  # Wait for sub-agent to complete
  # Verify results before proceeding to next phase
  verify_phase_results(phase)
```

---

## Step 5: Error Handling

### Phase Failure

```
If a phase fails:
1. Capture error output and partial results
2. Mark phase as FAILED in coordination directory
3. Check dependency graph:
   - SKIP all phases that depend on failed phase
   - CONTINUE with independent phases
4. Report failure clearly in final summary
```

### Dependency Conflict

```
If sub-agent reports unexpected dependency:
1. Pause execution
2. Present conflict to user
3. Options:
   a. Re-analyze with new information
   b. Force continue (user accepts risk)
   c. Abort and revise plan
```

### Uncertain Dependencies

```
When confidence is low:
1. Default to sequential (safer)
2. Flag uncertainty in execution plan
3. Ask user to confirm before proceeding
```

---

## Step 6: Results Aggregation

### Final Summary Template

```markdown
## Implementation Complete

### Execution Summary
| Phase | Status | Files | Duration |
|-------|--------|-------|----------|
| phase-1 | Done | 3 | ~1 cycle |
| phase-3 | Done | 1 | ~1 cycle |
| phase-2 | Done | 4 | ~1 cycle |
| phase-4 | Done | 2 | ~1 cycle |
| phase-5 | Partial | 1 | ~1 cycle |

### Strategy Used
Mixed parallel/sequential across 3 levels

### All Files Modified
- `src/models/user.ts` (phase-1)
- `src/middleware/logging.ts` (phase-3)
- `src/middleware/auth.ts` (phase-2)
- `src/routes/users.ts` (phase-4)
- `src/routes/admin.ts` (phase-5, incomplete)

### Key Decisions Across Phases
[Aggregated from phase results]

### Integration Points to Verify
- [ ] User model imports correctly in auth
- [ ] Auth middleware registered in app
- [ ] Logging captures auth events

### Issues Encountered
- phase-5: Admin role enum not defined, implemented basic version

### Recommended Next Steps
1. Run test suite: `npm test`
2. Manually verify integration points
3. Review phase-5 partial implementation
4. Address any flagged deviations

### Artifacts Location
Full details: `.claude/phase-coordination/results/`
Shared artifacts: `.claude/phase-coordination/artifacts/`
```

---

## Cleanup

After user confirms completion:

```bash
# Option to preserve for debugging
mv .claude/phase-coordination .claude/phase-coordination-{timestamp}

# Or clean up
rm -rf .claude/phase-coordination
```

Recommend user run `/compact` after completion since detailed context is persisted to files.
