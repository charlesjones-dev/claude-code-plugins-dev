# AI-Performance Plugin

**Performance audits for Claude Code.** `/performance-audit` reads your codebase and saves a timestamped report with an impact score for each bottleneck it finds.

---

## What This Plugin Does

The plugin ships one skill and one agent. Run the audit during development to catch code-level performance problems before they reach production.

## Limits

`/performance-audit` reads code. It doesn't run your app, so it can't measure execution time or Core Web Vitals in a browser; pair it with profiling and load tests. Improvement figures in the report are estimates.

## Available Skills

### `/performance-audit`

Audits the whole codebase. It takes no arguments; anything typed after the slash command is ignored.

## Available Agents

### `performance-auditor`

Runs the audit in a fresh context and writes the report. `/performance-audit` invokes it, and you can also use it for unattended or scheduled reviews.

---

## Quick Start

### Installation

```
/plugin install ai-performance@claude-code-plugins-dev
```

### Usage

```
# Run a performance audit
/performance-audit

# Review the generated report in /docs/performance/
```

---

## Features

### `/performance-audit`

#### Performance Pattern Detection

- **N+1 Query Problems**: Identifies loading related entities in loops
- **Synchronous/Blocking Operations**: Detects blocking database calls, I/O operations, and event loop blocking (Node.js)
- **Memory Issues**: Finds leaks from closures, uncleared listeners, large object allocations, and missing resource disposal
- **Concurrency Problems**: Detects race conditions, deadlocks, connection pool exhaustion, and thread/worker saturation
- **Inefficient Queries**: Detects suboptimal ORM usage and missing projections
- **Missing Caching**: Locates frequently computed operations without caching
- **Database Optimization**: Identifies missing indexes and expensive queries
- **Frontend Performance**: Evaluates Core Web Vitals impact (LCP, INP, CLS), bundle size, and rendering performance
- **GraphQL Issues**: Detects missing query depth limiting, DataLoader opportunities, and over-fetching

#### Detailed Reporting

Each finding includes:

- **Location**: Exact file path and line number
- **Performance Impact**: Numerical impact score (1.0-10.0) with defined severity thresholds
- **Pattern Detected**: What performance issue was identified
- **Code Context**: The problematic code snippet
- **Impact**: Performance cost and scalability concerns
- **Recommendation**: How to optimize it
- **Fix Priority**: When it should be addressed

#### Code Optimization Examples

Reports include 2-4 before/after examples built from code in the findings, each with an expected improvement estimate.

---

## How It Works

`/performance-audit` hands the audit to this plugin's `performance-auditor` agent, which scans source files for the patterns above and tailors findings to the detected stack. Findings are grouped as Critical, High, Medium or Low, and the report ends with a phased optimization roadmap.

---

## Best Practices

### When to Run Performance Audits

- Before production deployments
- After implementing new features with database access
- When adding new API endpoints
- After integrating third-party services
- During performance reviews and optimization sprints

### How to Use Audit Results

1. **Prioritize Critical & High findings** - Address these immediately
2. **Review code context** - Understand why each finding impacts performance
3. **Apply optimization examples** - Use provided code fixes as templates
4. **Measure improvements** - Benchmark before and after optimizations
5. **Re-audit after fixes** - Verify improvements and track progress

---

## Configuration

There's nothing to configure.

Reports are saved to `/docs/performance/` as `YYYY-MM-DD-HHMMSS-performance-audit.md` (e.g., `2025-10-17-143022-performance-audit.md`). This timestamp-based naming ensures multiple audits on the same day don't overwrite each other.

---

## Plugin Details

- **Name:** AI-Performance
- **Version:** 1.2.2
- **Type:** Skill and agent
- **Features:**
  - Skills: `/performance-audit`
  - Agents: `performance-auditor`
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License - See [LICENSE](LICENSE) file for details.
