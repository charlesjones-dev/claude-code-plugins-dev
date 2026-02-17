# AI-Accessibility Plugin

**Comprehensive AI-powered accessibility toolkit for Claude Code.** Intelligent accessibility scanning, WCAG compliance detection, inclusive design guidance, and accessible development best practices.

---

## 🎯 What This Plugin Does

Provides AI-powered accessibility auditing tools including commands, agents, and skills that help you build inclusive applications, detect accessibility barriers, achieve WCAG compliance, and maintain accessibility best practices throughout your development lifecycle.

### 🔍 Important: What This Plugin Is (and Isn't)

**This is a DEVELOPER-FOCUSED ACCESSIBILITY TOOLKIT** designed to help developers identify accessibility issues through both static code analysis and visual testing (with optional Playwright MCP integration).

#### ✅ What This Plugin IS:
- **Static code analysis tool** for developers working with source code
- **Visual accessibility testing tool** (with optional Playwright MCP integration for URL scanning)
- **Pattern detection engine** that identifies accessibility anti-patterns in HTML, JSX, CSS
- **Developer education tool** with WCAG knowledge and code remediation examples
- **Complementary tool** to augment your accessibility workflow
- **Early detection system** to catch issues before they reach production

#### ❌ What This Plugin IS NOT:
- **NOT a replacement for runtime accessibility testing services** that monitor live websites
- **NOT a complete accessibility solution** (automated testing catches ~30-40% of issues)
- **NOT a substitute for manual screen reader testing** with assistive technologies
- **NOT a replacement for user testing** with people with disabilities
- **NOT a compliance certification tool** (doesn't provide legal compliance guarantees)

#### 🎯 How This Fits Into Your Accessibility Workflow:

```
┌─────────────────────────────────────────────────────────────┐
│           Comprehensive Accessibility Strategy              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Development Phase ← THIS PLUGIN                        │
│     • /accessibility-audit - Static code analysis          │
│     • /accessibility-audit - URL scanning (Playwright MCP) │
│     • WCAG pattern detection in source files               │
│     • Visual accessibility testing (contrast, focus)        │
│     • Early issue identification during development        │
│                                                             │
│  2. Runtime Testing Phase                                  │
│     • Automated browser testing tools                      │
│     • Continuous monitoring services for live sites        │
│     • Browser extensions for visual validation             │
│                                                             │
│  3. Manual Testing Phase                                   │
│     • Screen reader testing (NVDA, JAWS, VoiceOver)       │
│     • Keyboard-only navigation testing                     │
│     • Color contrast validation on rendered pages          │
│     • Touch target testing on actual devices               │
│                                                             │
│  4. User Testing Phase                                     │
│     • Testing with actual users with disabilities          │
│     • Usability validation                                 │
│     • Real-world accessibility verification                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Best Practice**: Use this plugin during development to catch accessibility issues early (both code-level and visual), then validate with runtime testing tools, manual testing, and user testing before deployment.

### Why Use This Plugin?

Manual accessibility reviews are time-consuming, inconsistent, and prone to missing critical issues. Automated tools like WAVE, axe, and Lighthouse catch only ~30-40% of accessibility issues and don't provide comprehensive remediation guidance.

❌ **Manual accessibility review challenges:**
- No standardized methodology across projects
- Time-consuming manual checks
- Inconsistent findings format
- Missing WCAG compliance matrix
- Limited remediation guidance
- No historical tracking of improvements

This plugin provides:

✅ **Comprehensive WCAG audits** - Configurable for WCAG 2.1/2.2, Levels A/AA/AAA
✅ **Intelligent pattern detection** - Identifies semantic HTML, ARIA, keyboard, contrast issues
✅ **Standardized reports** - Consistent format with severity-based findings
✅ **WCAG compliance matrix** - Detailed assessment of applicable criteria
✅ **Code remediation examples** - Before/after examples for every finding
✅ **Prioritized roadmap** - Phased approach to accessibility improvements
✅ **Timestamped tracking** - Reports saved to `/docs/accessibility/{timestamp}-accessibility-audit.md`

**Use accessibility testing tools (WAVE, axe, Lighthouse) for:** Quick automated checks during development

**Use `/accessibility-audit` for:** Comprehensive WCAG compliance audits, formal accessibility documentation, and accessibility improvement roadmaps

## 📋 Available Skills

### `/accessibility-audit`

Perform comprehensive accessibility analysis on your codebase or live website and generate a detailed WCAG compliance audit report with findings and remediation guidance.

**Interactive Configuration:**

Before starting the audit, the command will ask you:

1. **WCAG Version**: Choose between WCAG 2.1 or WCAG 2.2
2. **Conformance Level**: Choose A (minimum), AA (industry standard), or AAA (enhanced)
3. **Scope**: Choose entire codebase, specific directory, or a URL
4. **Visual Scanning** (if URL selected): Choose whether to use Playwright MCP tools for visual accessibility testing

**What it analyzes:**

**For Codebase Analysis:**
- ✅ **Semantic HTML & Document Structure** - Heading hierarchy, landmarks, semantic elements
- ✅ **ARIA Implementation** - Roles, states, properties, landmark regions
- ✅ **Keyboard Navigation** - Tab order patterns, focus management code, keyboard trap detection
- ✅ **Color Contrast** - CSS color values and contrast ratios
- ✅ **Forms** - Label associations, error handling, required field indication
- ✅ **Alternative Text** - Images, icons, multimedia text alternatives
- ✅ **Interactive Components** - Buttons, links, modals, custom widgets
- ✅ **Responsive & Mobile** - Touch target sizes, viewport scaling, orientation support

**Additional for URL Analysis with Playwright MCP:**
- ✅ **Visual Color Contrast Testing** - Real-time contrast measurements of rendered elements
- ✅ **Actual Focus Indicator Visibility** - Visual verification of focus states
- ✅ **Rendered DOM Structure** - Accessibility tree as perceived by assistive technologies
- ✅ **Interactive Element Testing** - Keyboard navigation testing on live page
- ✅ **Touch Target Size Verification** - Actual pixel measurements of interactive elements
- ✅ **Screenshot-based Analysis** - Visual accessibility assessment with evidence

**Before (manual):**

```
# Manual accessibility audit process
- Review each page for heading hierarchy
- Check ARIA roles and attributes manually
- Test keyboard navigation flow
- Calculate color contrast ratios
- Review form label associations
- Check alt text on all images
- Test with multiple screen readers
- Write detailed findings document
- Create compliance matrix
- Develop remediation plan
```

**After (with ai-accessibility plugin):**

```
/accessibility-audit
# ✅ Choose WCAG version (2.1/2.2) and level (A/AA/AAA)
# ✅ Select scope (entire codebase, specific directory, or URL)
# ✅ For URL: Choose whether to use Playwright MCP for visual testing
# ✨ AI analyzes codebase or website for accessibility barriers
# ✨ Identifies WCAG compliance issues with criterion references
# ✨ Performs visual testing with screenshots (if Playwright enabled)
# ✨ Generates comprehensive audit report with compliance matrix
# ✨ Provides code examples and remediation steps
# ✅ Report saved to /docs/accessibility with timestamp
```

## 🤖 Available Agents

### `accessibility-auditor`

Specialized agent that performs deep accessibility analysis on codebases and live websites (with Playwright MCP) and generates comprehensive WCAG compliance audit reports. Automatically invoked by `/accessibility-audit` command.

**Focus Areas:**
- Semantic HTML and document structure
- ARIA implementation validation
- Keyboard accessibility and focus management
- Color contrast and visual accessibility
- Form and input accessibility
- Alternative text validation
- Interactive components and custom widgets
- Responsive and mobile accessibility

---

---

> **Note:** The `/accessibility-audit` skill provides both the interactive audit workflow and comprehensive WCAG expertise (accessibility patterns, conformance criteria, remediation guidance, and Playwright MCP visual testing knowledge) in a single unified skill.

---

## 🚀 Quick Start

### Installation

```
/plugin install ai-accessibility@claude-code-plugins-dev
```

### Usage

**Codebase Analysis:**
```
# Step 1: Run an accessibility audit
/accessibility-audit

# Step 2: Answer configuration questions
# - WCAG Version: 2.1 or 2.2
# - Conformance Level: A, AA, or AAA
# - Scope: Entire solution or specific directory

# Step 3: Review the generated report
# Located at: /docs/accessibility/{timestamp}-accessibility-audit.md
# Example: /docs/accessibility/2025-10-29-143022-accessibility-audit.md

# Step 4: Implement recommended fixes
# Follow the prioritized remediation roadmap (Phase 1-4)
```

**URL Analysis with Playwright MCP:**
```
# Step 1: Run an accessibility audit
/accessibility-audit

# Step 2: Answer configuration questions
# - WCAG Version: 2.1 or 2.2
# - Conformance Level: A, AA, or AAA
# - Scope: a URL
# - Provide the URL to scan
# - Visual Scanning: Yes - Use Playwright for visual scans

# Step 3: If Playwright MCP is not installed, the command will:
# - Offer to create .mcp.json configuration file
# - Ask you to restart Claude Code
# - After restart, run /accessibility-audit again

# Step 4: Review the generated report with visual evidence
# Located at: /docs/accessibility/{timestamp}-accessibility-audit.md
# Screenshots: /docs/accessibility/screenshots/

# Step 5: Implement recommended fixes
# Follow the prioritized remediation roadmap
```

---

## 💡 Features

### Configurable WCAG Assessment

**WCAG 2.1 vs 2.2:**
- **WCAG 2.1**: 50 success criteria across 13 guidelines
- **WCAG 2.2**: 59 success criteria (adds 9 new criteria for mobile, cognitive accessibility, removes SC 4.1.1 Parsing)
  - New criteria: Focus Not Obscured (AA/AAA), Focus Appearance (AAA), Dragging Movements (AA), Target Size Minimum (AA), Consistent Help (A), Redundant Entry (A), Accessible Authentication (AA/AAA)

**Conformance Levels:**
- **Level A** (25 criteria) - Minimum accessibility, critical barriers
- **Level AA** (38 criteria) - Industry standard, often legally required
- **Level AAA** (61 criteria) - Enhanced accessibility, highest level

### Comprehensive Analysis Areas

#### Semantic HTML & Structure
- Heading hierarchy validation (h1-h6 without skipping levels)
- Semantic element usage (nav, main, footer, article, section)
- Landmark regions for screen reader navigation
- Logical reading order assessment

#### ARIA Implementation
- Valid ARIA roles, states, and properties
- Landmark roles (banner, navigation, main, complementary)
- Widget roles (button, checkbox, tab, dialog)
- Live regions for dynamic content
- ARIA labels and descriptions

#### Keyboard Accessibility
- Tab order follows logical flow
- All interactive elements keyboard accessible
- No keyboard traps detected
- Visible focus indicators (3:1 contrast minimum)
- Skip navigation links
- Focus management in modals/dialogs
- WCAG 2.2: Focus Not Obscured (SC 2.4.11), Focus Appearance (SC 2.4.13)

#### Color Contrast
- Normal text: 4.5:1 minimum (AA), 7:1 (AAA)
- Large text: 3:1 minimum (AA), 4.5:1 (AAA)
- UI components: 3:1 minimum
- Information not conveyed by color alone
- Color blindness considerations

#### Form Accessibility
- Label associations (explicit/implicit)
- Fieldset/legend for grouped controls
- Required field indication
- Error identification and suggestions
- Accessible error messages (aria-describedby, aria-invalid)
- Autocomplete attributes
- WCAG 2.2: Redundant Entry (SC 3.3.7), Accessible Authentication (SC 3.3.8/3.3.9)

#### Alternative Text
- Descriptive alt text for informative images
- Empty alt for decorative images
- Complex image descriptions
- Icon button accessible names
- SVG accessibility
- Video captions and audio transcripts

#### Interactive Components
- Accessible names for all interactive elements
- Proper button vs link semantics
- Modal/dialog accessibility (focus trap, ESC key, aria-modal)
- Tooltip accessibility
- Dropdown/select accessibility
- Custom widget ARIA patterns
- WCAG 2.2: Consistent Help (SC 3.2.6)

#### Mobile & Responsive
- Touch target size: 44×44px minimum (AA)
- No horizontal scrolling at 320px width
- Text can be zoomed to 200%
- Orientation not locked
- Content reflows at 400% zoom
- WCAG 2.2: Dragging Movements (SC 2.5.7), Target Size Minimum (SC 2.5.8)
