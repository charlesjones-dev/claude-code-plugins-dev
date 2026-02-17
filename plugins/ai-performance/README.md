# AI-Performance Plugin

**Comprehensive AI-powered performance optimization toolkit for Claude Code.** Intelligent performance analysis, bottleneck detection, optimization opportunities, and scalability guidance.

---

## 🎯 What This Plugin Does

Provides a complete suite of AI-powered performance tools including commands, agents, and skills that help you build high-performance applications, detect bottlenecks, optimize resource usage, and maintain performance best practices throughout your development lifecycle.

### 🔍 Important: What This Plugin Is (and Isn't)

**This is a DEVELOPER-FOCUSED CODE ANALYSIS TOOL** designed to help developers with codebase access identify performance issues during development.

#### ✅ What This Plugin IS:
- **Static code analysis tool** for developers working with source code
- **Performance anti-pattern detection** for N+1 queries, inefficient loops, blocking operations
- **Developer education tool** with optimization guidance and code examples
- **Complementary tool** to augment your performance workflow
- **Early detection system** to catch performance issues before they reach production

#### ❌ What This Plugin IS NOT:
- **NOT a replacement for runtime performance monitoring** or Application Performance Monitoring (APM) platforms
- **NOT a load testing tool** (doesn't execute code or simulate traffic)
- **NOT a complete performance solution** (catches code-level issues, not infrastructure/runtime issues)
- **NOT a substitute for profiling tools** that measure actual execution time
- **NOT a replacement for real user monitoring (RUM)** or synthetic monitoring services
- **NOT a browser performance testing tool** (doesn't measure Core Web Vitals in browsers)

#### 🎯 How This Fits Into Your Performance Workflow:

```
┌─────────────────────────────────────────────────────────────┐
│           Comprehensive Performance Strategy                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Development Phase (Code-Level) ← THIS PLUGIN           │
│     • /performance-audit - Static code analysis            │
│     • N+1 query and anti-pattern detection                 │
│     • Early performance issue identification               │
│                                                             │
│  2. Profiling & Benchmarking                               │
│     • CPU and memory profilers                             │
│     • Database query analyzers                             │
│     • Performance benchmarking tools                       │
│                                                             │
│  3. Runtime Performance Testing                            │
│     • Load testing and stress testing                      │
│     • Application Performance Monitoring (APM)             │
│     • Real User Monitoring (RUM)                           │
│     • Browser performance testing (Lighthouse, WebPageTest)│
│                                                             │
│  4. Production Monitoring                                  │
│     • Continuous performance monitoring                    │
│     • Alerting and anomaly detection                       │
│     • Performance analytics and reporting                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Best Practice**: Use this plugin during development to catch code-level performance issues early, then validate with profiling tools, load testing, and production monitoring.

### Why Use This Plugin?

While you can manually review code for performance issues, this plugin provides structured, comprehensive performance analysis:

❌ **Manual performance review challenges:**
- No standardized analysis methodology
- Inconsistent performance documentation
- Difficult to track improvements over time
- Hard to prioritize optimization efforts

This plugin enhances performance analysis by providing:

✅ **Custom analysis templates** - Define exactly what your audit should cover
✅ **Controlled output location** - Reports saved to `/docs/performance/{timestamp}-performance-audit.md` (timestamp prevents overwrites)
✅ **Reproducible audits** - Same comprehensive format every time
✅ **Standardized documentation** - Consistent audit reports across all projects
✅ **Timestamped tracking** - Easy to compare audits and measure improvements over time
✅ **Enterprise-ready** - Professional audit documents suitable for performance reviews

**Use this plugin for:** Formal performance audits, optimization planning, and repeatable performance assessments

## 📋 Available Skills

### `/performance-audit`

Perform comprehensive performance analysis on your codebase and generate a detailed audit report with optimization opportunities and implementation guidance.

**Before (manual):**

```
# Manual performance review process
- Review code for N+1 query patterns
- Check for synchronous blocking operations
- Analyze memory allocation patterns
- Review database indexing strategy
- Check for missing caching opportunities
- Assess async/await usage
- Write detailed findings document
- Create optimization roadmap
```

**After (with ai-performance plugin):**

```
/performance-audit
# ✨ AI analyzes entire codebase for performance issues
# ✨ Identifies bottlenecks and optimization opportunities
# ✨ Generates comprehensive performance report
# ✨ Provides code examples and optimization steps
# ✅ Report saved to /docs/performance with timestamp
```

## 🤖 Available Agents

### `performance-auditor`

Specialized agent that performs deep performance analysis and generates comprehensive optimization reports. Automatically invoked by `/performance-audit` command.

---

---

> **Note:** The `/performance-audit` skill provides both the interactive audit workflow and comprehensive performance optimization expertise (bottleneck detection, scalability guidance, and code optimization patterns) in a single unified skill.

---

## 🚀 Quick Start

### Installation

```
/plugin install ai-performance@claude-code-plugins-dev
```

### Usage

```
# Run a performance audit
/performance-audit

# Review the generated report
# Located at: /docs/performance/{timestamp}-performance-audit.md
# Example: /docs/performance/2025-10-17-143022-performance-audit.md
```

---

## 💡 Features

### `/performance-audit` Command

#### Comprehensive Performance Pattern Detection

- **N+1 Query Problems**: Identifies loading related entities in loops
- **Synchronous/Blocking Operations**: Detects blocking database calls, I/O operations, and event loop blocking (Node.js)
- **Memory Issues**: Finds leaks from closures, uncleared listeners, large object allocations, and missing resource disposal
- **Concurrency Problems**: Detects race conditions, deadlocks, connection pool exhaustion, and thread/worker saturation
- **Inefficient Queries**: Detects suboptimal ORM usage, multiple enumeration, and missing projections
- **Missing Caching**: Locates frequently computed operations without caching
- **Database Optimization**: Identifies missing indexes and expensive queries
- **Frontend Performance**: Evaluates Core Web Vitals impact (LCP, INP, CLS), bundle size, and rendering performance
- **GraphQL Issues**: Detects missing query depth limiting, DataLoader opportunities, and over-fetching

#### Performance Best Practices Assessment

Automatically evaluates your codebase against performance best practices:

- Async/await pattern usage
- Connection pooling configuration
- Query optimization strategies
- Caching implementation
- Memory management and resource disposal
- Concurrency and thread safety
- Core Web Vitals optimization (LCP, INP, CLS)
- Bundle size and code splitting
- Streaming/SSR performance
- Observability (metrics, logs, distributed tracing)

#### Architecture Performance Assessment

- **Data Access Layer Analysis**: Reviews ORM usage, query patterns, and connection management
- **Application Layer Analysis**: Checks async patterns, memory management, concurrency safety, and CPU utilization
- **Frontend Analysis**: Evaluates Core Web Vitals, bundle size, code splitting, SSR/hydration cost
- **Infrastructure Analysis**: Examines caching layers, compression, CDN usage, and observability coverage

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

Reports include before/after code examples showing:

- Inefficient code patterns
- Optimized replacement code
- Explanation of the improvement
- Best practices applied

---

## ⚙️ How It Works

The `/performance-audit` command uses Claude Code's specialized **performance-auditor agent** to perform comprehensive performance analysis:

1. **Code Analysis**
   - Scans source files for performance anti-patterns
   - Analyzes database query patterns and data access strategies
   - Reviews async/await implementation
   - Checks memory allocation patterns

2. **Pattern Detection**
   - Identifies N+1 query problems
   - Detects synchronous/blocking operations and event loop blocking
   - Finds memory leaks and resource disposal issues
   - Detects concurrency problems (race conditions, deadlocks, pool exhaustion)
   - Locates missing caching opportunities
   - Checks for inefficient queries and data access patterns
   - Evaluates frontend Core Web Vitals impact

3. **Report Generation**
   - Categorizes findings by impact (Critical, High, Medium, Low)
   - Provides exact locations with file paths and line numbers
   - Includes code examples and optimization guidance
   - Creates prioritized optimization roadmap
   - Saves timestamped report to /docs/performance folder

The specialized agent brings deep performance expertise and pattern recognition capabilities to identify bottlenecks that might be missed by manual review.

---

## 🎓 Best Practices

### When to Run Performance Audits

- ✅ Before production deployments
- ✅ After implementing new features with database access
- ✅ When adding new API endpoints
- ✅ After integrating third-party services
- ✅ During performance reviews and optimization sprints
- ✅ As part of CI/CD pipeline (automated performance gates)

### How to Use Audit Results

1. **Prioritize Critical & High findings** - Address these immediately
2. **Review code context** - Understand why each finding impacts performance
3. **Apply optimization examples** - Use provided code fixes as templates
4. **Measure improvements** - Benchmark before and after optimizations
5. **Re-audit after fixes** - Verify improvements and track progress

---

## ⏱️ Time Savings

**Per performance audit:**

- Manual performance review: ~6-10 hours (for medium-sized codebase)
- With performance-audit: ~2-3 minutes (AI-powered analysis)

**Estimated savings:**

- Per comprehensive audit: Save ~6-10 hours
- Per month (2 audits): Save ~12-20 hours
- Per year: Save ~150+ hours

Plus improved application performance and reduced infrastructure costs.

---

## 🚀 Performance Expertise Built-In

This plugin embodies expert performance knowledge across multiple domains:

### Performance Analysis

- N+1 query detection and optimization
- Database indexing strategies
- Query optimization techniques (ORM-agnostic)
- Memory management across platforms (JS/Node.js, .NET, Java, Go)
- Async/await and concurrency patterns

### Frontend Performance

- Core Web Vitals optimization (LCP, INP, CLS)
- Bundle analysis and tree-shaking
- Framework-aware guidance (React, Vue, Svelte, Angular)
- Streaming SSR and hydration cost optimization
- Asset optimization (WebP/AVIF, responsive images, lazy loading)

### Scalability Assessment

- Thread pool and event loop management
- Connection pooling strategies
- Concurrency and thread safety analysis
- Caching architectures
- GraphQL performance (DataLoader, query depth limiting)

### Architecture Review

- Data access layer optimization
- Application layer performance
- Infrastructure and observability
- Distributed tracing and monitoring setup
- Performance testing strategies

---

## 🔧 Configuration

No configuration needed! The plugin works out of the box and generates comprehensive performance reports automatically.

Reports are saved to: `/docs/performance/{timestamp}-performance-audit.md`

**Naming Format:** `YYYY-MM-DD-HHMMSS-performance-audit.md` (e.g., `2025-10-17-143022-performance-audit.md`)

This timestamp-based naming ensures multiple audits on the same day don't overwrite each other.

---

## 📦 Plugin Details

- **Name:** AI-Performance
- **Version:** 1.2.0
- **Type:** Comprehensive Performance Optimization Toolkit
- **Features:**
  - Skills: `/performance-audit`
  - Agents: `performance-auditor`
- **License:** MIT
- **Author:** Charles Jones

---

## ⚠️ Important Notes

### What This Plugin Does

- ✅ Static code analysis for performance patterns
- ✅ Architecture and database performance review
- ✅ Resource utilization assessment
- ✅ Performance best practices validation
- ✅ Optimization opportunity identification
- ✅ Scalability analysis and planning
- ✅ Performance optimization guidance
- ✅ AI-assisted performance education

### What This Plugin Doesn't Do

- ❌ Runtime performance profiling
- ❌ Load testing or stress testing
- ❌ Network performance analysis
- ❌ Real-time monitoring
- ❌ Replace actual performance testing
- ❌ Guarantee specific performance improvements

### Performance Analysis Approach

This plugin focuses on **code-level performance optimization** through static analysis:

- Helps developers write performant code
- Identifies bottlenecks early in the development lifecycle
- Educates teams on performance best practices
- Supports optimization planning and prioritization
- Prevents performance issues before they reach production

**Complements but doesn't replace runtime profiling and load testing.**

---

## 🤝 Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) or submit a pull request!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Claude Code community**
