# Performance Audit

You are a comprehensive performance optimization expert with deep expertise in application performance, scalability, code optimization, and performance best practices.

## Instructions

Perform a thorough performance analysis of this codebase using the performance-optimizer subagent to identify performance bottlenecks, optimization opportunities, and scalability issues.

### Analysis Scope

1. **Code Pattern Analysis**: Scan for N+1 queries, inefficient loops, memory leaks, blocking operations
2. **Database Performance Review**: Analyze SQL queries, indexing strategies, and data access patterns
3. **Resource Utilization Assessment**: Review memory allocation patterns, CPU-intensive operations, I/O bottlenecks
4. **Architecture Performance Analysis**: Examine caching strategies, async/await patterns, connection pooling
5. **Scalability Assessment**: Identify thread pool issues, connection management, and load handling patterns

### Output Requirements

- Create a comprehensive performance audit report using the template provided below
- Save the report to: `/docs/performance/{timestamp}-performance-audit.md`
  - Format: `YYYY-MM-DD-HHMMSS-performance-audit.md`
  - Example: `2025-10-17-143022-performance-audit.md`
  - This ensures multiple scans on the same day don't overwrite each other
- Include actual findings from the codebase (not template examples)
- Provide exact file paths and line numbers for all findings
- Include before/after code examples for optimization guidance
- Prioritize findings by impact: Critical, High, Medium, Low

### Important Notes

- Focus on **code-level performance optimization** - identifying bottlenecks through static analysis
- Provide actionable optimization guidance with specific code examples
- Create a prioritized optimization roadmap based on performance impact
- Include expected performance improvement estimates for each recommendation

Use the performance-optimizer subagent to perform a comprehensive performance analysis of this codebase using the template below:

<template>
## Executive Summary

### Audit Overview

- **Target System**: [Application Name/System]
- **Analysis Date**: [Date Range]
- **Analysis Scope**: [Web Application/API/Database/Full Stack]
- **Technology Stack**: [e.g., .NET 8, Umbraco CMS, SQL Server, Elasticsearch, Azure]

### Performance Assessment Summary

| Performance Level | Count | Percentage |
|-------------------|-------|------------|
| Critical Issues   | X     | X%         |
| High Impact       | X     | X%         |
| Medium Impact     | X     | X%         |
| Low Impact        | X     | X%         |
| **Total**         | **X** | **100%**   |

### Key Analysis Results

- **Performance Anti-Patterns**: X critical patterns identified requiring immediate attention
- **Code Optimization Opportunities**: X high-impact optimizations discovered
- **Architecture Assessment**: X/10 performance best practices implemented
- **Overall Code Performance Score**: X/100 (based on static analysis and architectural patterns)

---

## Analysis Methodology

### Performance Analysis Approach

- **Static Code Analysis**: Comprehensive source code review for performance anti-patterns
- **Database Query Analysis**: Review of SQL queries, indexing strategies, and data access patterns
- **Resource Utilization Assessment**: Analysis of memory, CPU, and I/O usage patterns
- **Architecture Performance Review**: Examination of caching, scaling, and optimization strategies

### Analysis Coverage

- **Files Analyzed**: X source files across Y projects
- **Database Queries Reviewed**: X queries and stored procedures
- **API Endpoints Tested**: X endpoints across Y controllers
- **Performance Patterns Checked**: N+1 queries, memory leaks, CPU bottlenecks, I/O blocking

### Analysis Capabilities

- **Pattern Detection**: N+1 queries, inefficient loops, memory leaks, blocking operations
- **Database Analysis**: Missing indexes, expensive queries, deadlock potential
- **Resource Analysis**: Memory allocation patterns, CPU-intensive operations, I/O bottlenecks
- **Architecture Assessment**: Caching strategies, async/await patterns, connection pooling

---

## Performance Findings

### Critical Performance Issues

#### P-001: N+1 Query Problem

**Location**: `src/Website.Core/Services/VendorService.cs:78`
**Performance Impact**: 9.8 (Critical)
**Pattern Detected**: Loading related entities in a loop causing multiple database queries
**Code Context**:

```csharp
foreach (var vendor in vendors)
{
    vendor.Products = context.Products.Where(p => p.VendorId == vendor.Id).ToList();
}
```

**Impact**: Database query count increases linearly with result set size (1 + N queries instead of 1)
**Performance Cost**: 2000ms+ response time for 100 vendors
**Recommendation**: Use Include() for eager loading or projection for specific fields
**Fix Priority**: Immediate (within 24 hours)

#### P-002: Synchronous Database Operations

**Location**: `src/Website.Web/Controllers/ApiController.cs:45`
**Performance Impact**: 9.1 (Critical)
**Pattern Detected**: Synchronous database calls blocking request threads
**Code Context**: Missing async/await pattern in controller actions
**Impact**: Thread pool exhaustion under high load, poor scalability
**Performance Cost**: Thread starvation affecting overall application responsiveness
**Recommendation**: Convert all database operations to async/await pattern
**Fix Priority**: Immediate (within 48 hours)

### High Performance Impact Findings

#### P-003: Large Object Heap Pressure

**Location**: Multiple locations in data processing services
**Performance Impact**: 7.8 (High)
**Pattern Detected**: Large objects (>85KB) causing frequent Gen 2 garbage collection
**Affected Components**:

- `src/Website.AirtableData/Services/ImportService.cs:156`
- `src/Website.ElasticSearch/Services/IndexingService.cs:89`
**Impact**: GC pressure causing application pauses and increased memory usage
**Performance Cost**: 200-500ms GC pauses, 40% higher memory usage
**Recommendation**: Implement streaming for large data sets, use object pooling
**Fix Priority**: Within 1 week

#### P-004: Inefficient Elasticsearch Queries

**Location**: `src/Website.ElasticSearch/Services/SearchService.cs:123`
**Performance Impact**: 7.5 (High)
**Pattern Detected**: Full-text search without field targeting or filtering
**Code Context**: Broad queries without proper field restrictions or caching
**Impact**: High Elasticsearch cluster load, slow search response times
**Performance Cost**: 800ms+ search response time, high CPU usage on ES cluster
**Recommendation**: Implement targeted field searches, result caching, and query optimization
**Fix Priority**: Within 2 weeks

### Medium Performance Impact Findings

#### P-005: Missing Database Indexes

**Location**: Database schema analysis
**Performance Impact**: 6.3 (Medium)
**Pattern Detected**: Frequent WHERE clauses on non-indexed columns
**Affected Tables**:

- `Vendors` table: missing index on `OrganizationId, IsActive`
- `Products` table: missing composite index on `CategoryId, Status, CreatedDate`
**Impact**: Table scans causing slow query performance
**Performance Cost**: 500-1200ms query response time for filtered data
**Recommendation**: Add appropriate indexes based on query patterns
**Fix Priority**: Within 1 month

#### P-006: Inefficient LINQ Queries

**Location**: Multiple service classes
**Performance Impact**: 5.9 (Medium)
**Pattern Detected**: Multiple enumeration of IEnumerable, inefficient projections
**Affected Areas**: Vendor listing, product filtering, category navigation
**Impact**: Unnecessary CPU cycles, increased memory allocation
**Performance Cost**: 200-400ms additional processing time
**Recommendation**: Use ToList() strategically, optimize LINQ expressions
**Fix Priority**: Within 1 month

### Low Performance Impact Findings

#### P-007: Missing Output Caching

**Location**: Web application controllers and views
**Performance Impact**: 3.8 (Low)
**Pattern Detected**: Repeated computation of static or semi-static content
**Missing Caching**: Category lists, navigation menus, vendor counts
**Impact**: Unnecessary CPU usage for frequently accessed data
**Performance Cost**: 50-100ms additional processing per request
**Recommendation**: Implement response caching and memory caching strategies
**Fix Priority**: Within 2 months

---

## Code Pattern Performance Analysis

### Performance Anti-Pattern Detection

- **N+1 Query Patterns**: X instances detected across Y service classes
- **Synchronous Blocking Operations**: X async-convertible operations identified
- **Large Object Allocations**: X locations with >85KB object creation
- **Inefficient LINQ Usage**: X queries with multiple enumeration or suboptimal patterns

### Database Access Pattern Analysis

- **Entity Framework Usage**: X queries analyzed for efficiency patterns
- **Missing Async Patterns**: X database operations identified for async conversion
- **Query Complexity**: X complex queries requiring optimization review
- **Connection Management**: Connection pooling configuration assessment

### Resource Management Pattern Analysis

- **Memory Allocation Patterns**: Large object heap pressure points identified
- **Garbage Collection Pressure**: X locations with excessive object creation
- **Thread Pool Usage**: X blocking operations affecting scalability
- **Caching Opportunities**: X frequently computed operations without caching

---

## Architecture Performance Assessment

### Data Access Layer Analysis

- **Entity Framework Performance**: ⚠️ N+1 queries detected, lazy loading causing issues
- **Connection Pooling**: ✅ Properly configured with appropriate pool sizes
- **Query Optimization**: ❌ Missing indexes and inefficient LINQ expressions
- **Caching Strategy**: ❌ Insufficient caching at data layer

### Application Layer Analysis

- **Async/Await Usage**: ❌ Many synchronous operations blocking threads
- **Memory Management**: ⚠️ Some memory leaks in background services
- **CPU Utilization**: ⚠️ CPU-intensive operations not optimized
- **I/O Operations**: ❌ File operations and API calls not properly optimized

### Infrastructure Analysis

- **Load Balancing**: ✅ Properly configured with health checks
- **CDN Usage**: ⚠️ Static assets cached but optimization needed
- **Database Scaling**: ⚠️ Read replicas available but not fully utilized
- **Monitoring Coverage**: ❌ Limited application performance monitoring

---

## Performance Bottleneck Analysis

### Top 10 Performance Bottlenecks

| Rank | Component | Issue | Impact Score | Response Time Impact |
|------|-----------|-------|--------------|---------------------|
| 1 | VendorService | N+1 Query Problem | 9.8 | +2000ms |
| 2 | ApiController | Sync DB Operations | 9.1 | Thread exhaustion |
| 3 | ImportService | Large Object Heap | 7.8 | +500ms GC pauses |
| 4 | SearchService | Inefficient ES Queries | 7.5 | +800ms |
| 5 | Database | Missing Indexes | 6.3 | +600ms |
| 6 | LINQ Queries | Multiple Enumeration | 5.9 | +300ms |
| 7 | File Operations | Synchronous I/O | 5.2 | +400ms |
| 8 | Caching | Missing Cache Strategy | 4.8 | +200ms |
| 9 | Background Jobs | Memory Leaks | 4.5 | Resource exhaustion |
| 10 | API Serialization | Large Payloads | 3.9 | +150ms |

---

## Technical Recommendations

### Immediate Performance Fixes

1. **Fix N+1 query problems** using Include() or projection in Entity Framework
2. **Convert synchronous operations** to async/await pattern for scalability
3. **Add missing database indexes** for frequently queried columns
4. **Implement connection pooling** for external service calls

### Performance Enhancements

1. **Implement comprehensive caching strategy** using Redis or in-memory caching
2. **Optimize Elasticsearch queries** with proper field targeting and filtering
3. **Add response compression** for API endpoints and static content
4. **Implement lazy loading** for heavy components and data

### Architecture Improvements

1. **Add application performance monitoring** using Application Insights or similar
2. **Implement database read replicas** for read-heavy operations
3. **Add background job optimization** with proper queue management
4. **Implement API rate limiting** and request throttling

---

## Code Optimization Examples

### N+1 Query Fix

**Before (Inefficient)**:

```csharp
var vendors = context.Vendors.ToList();
foreach (var vendor in vendors)
{
    vendor.Products = context.Products.Where(p => p.VendorId == vendor.Id).ToList();
}
```

**After (Optimized)**:

```csharp
var vendors = context.Vendors
    .Include(v => v.Products)
    .ToList();
// OR for specific fields only
var vendorsWithProductCount = context.Vendors
    .Select(v => new VendorViewModel
    {
        Id = v.Id,
        Name = v.Name,
        ProductCount = v.Products.Count()
    })
    .ToList();
```

### Async/Await Implementation

**Before (Blocking)**:

```csharp
[HttpGet]
public IActionResult GetVendors()
{
    var vendors = vendorService.GetAll(); // Synchronous call
    return Ok(vendors);
}
```

**After (Non-blocking)**:

```csharp
[HttpGet]
public async Task<IActionResult> GetVendors()
{
    var vendors = await vendorService.GetAllAsync(); // Asynchronous call
    return Ok(vendors);
}
```

### Caching Implementation

**Before (No Caching)**:

```csharp
public List<Category> GetCategories()
{
    return context.Categories.OrderBy(c => c.Name).ToList();
}
```

**After (With Caching)**:

```csharp
public async Task<List<Category>> GetCategoriesAsync()
{
    const string cacheKey = "categories_all";
    var cached = await cache.GetAsync<List<Category>>(cacheKey);
    if (cached != null)
        return cached;

    var categories = await context.Categories
        .OrderBy(c => c.Name)
        .ToListAsync();
    
    await cache.SetAsync(cacheKey, categories, TimeSpan.FromMinutes(30));
    return categories;
}
```

---

## Performance Optimization Priorities

### Phase 1: Critical Performance Fixes (Week 1)

- [ ] Fix N+1 queries in `VendorService.cs:78`
- [ ] Convert synchronous database operations to async in `ApiController.cs:45`
- [ ] Add missing database indexes for Vendors and Products tables
- [ ] Implement connection pooling for Elasticsearch service

### Phase 2: High Impact Optimizations (Week 2-4)

- [ ] Optimize large object allocations in import services
- [ ] Implement caching strategy for frequently accessed data
- [ ] Optimize Elasticsearch queries with proper filtering
- [ ] Fix memory leaks in background job processing

### Phase 3: Medium Impact Improvements (Month 2)

- [ ] Optimize LINQ queries to avoid multiple enumeration
- [ ] Implement response compression and output caching
- [ ] Add database read replicas for read operations
- [ ] Optimize file I/O operations with async patterns

### Phase 4: Performance Monitoring and Fine-tuning (Month 3)

- [ ] Implement comprehensive APM solution
- [ ] Add custom performance counters and metrics
- [ ] Set up automated performance testing
- [ ] Document performance best practices

---

## Estimated Performance Improvement Impact

### Performance Gains by Priority

| Priority Level | Expected Improvement | Implementation Complexity |
|----------------|---------------------|--------------------------|
| Critical Fixes | 60-80% response time improvement | High - requires careful testing |
| High Impact | 30-50% overall performance gain | Medium - architectural changes |
| Medium Impact | 15-25% additional optimization | Medium - code and config changes |
| Low Impact | 5-10% fine-tuning benefits | Low - mostly configuration |

### Resource Utilization Improvements

- **Database Load**: Expected 40-60% reduction in query execution time
- **Memory Usage**: Expected 25-35% reduction in memory pressure
- **CPU Utilization**: Expected 20-30% reduction in CPU usage
- **Thread Pool**: Expected elimination of thread starvation issues

---

## Performance Monitoring Setup Recommendations

### Monitoring Infrastructure Setup

- **Application Performance Monitoring**: Azure Application Insights or New Relic integration
- **Database Monitoring**: SQL Server Extended Events and Performance Dashboard configuration
- **Infrastructure Monitoring**: Azure Monitor or Prometheus + Grafana setup
- **Code-Level Monitoring**: Custom performance counters for identified bottlenecks

### Recommended Performance Tracking

- **Database Query Monitoring**: Track queries identified in this analysis for execution time
- **Memory Allocation Tracking**: Monitor large object heap allocations in flagged components
- **Thread Pool Monitoring**: Track thread starvation in areas with synchronous operations
- **Cache Hit Rate Monitoring**: Measure effectiveness of recommended caching implementations

### Performance Testing Recommendations

- **Load Testing**: Focus on endpoints with identified N+1 query problems
- **Database Performance Testing**: Test queries with missing indexes under load  
- **Memory Pressure Testing**: Validate large object allocation fixes
- **Concurrency Testing**: Verify async/await implementations under concurrent load

---

## Summary

This performance analysis identified **X critical**, **Y high**, **Z medium**, and **W low** performance issues across the application stack. The analysis focused on code patterns, database queries, resource utilization, and architectural performance without requiring extensive load testing infrastructure.

**Key Strengths Identified**:

- Good modular architecture with clear separation of concerns
- Proper use of modern .NET 8 features and Umbraco CMS
- Well-structured database schema with appropriate relationships

**Critical Areas Requiring Immediate Attention**:

- N+1 query problems causing database performance issues
- Synchronous operations blocking thread pool resources
- Missing database indexes for frequently queried data
- Inefficient memory allocation patterns in data processing

**Expected Overall Performance Improvement**: 70-90% reduction in response times and 40-60% improvement in resource utilization after implementing all recommendations.
</template>
