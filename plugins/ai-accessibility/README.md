# AI-Accessibility Plugin

**Accessibility audits for Claude Code.** `/accessibility-audit` checks your code or a live URL against WCAG 2.1, WCAG 2.2 or 508 / WCAG 2.0 AA and saves a report with before/after fixes. URL audits can use Playwright MCP for visual checks.

---

## What This Plugin Does

The plugin ships one skill and one agent. Run the audit during development to catch accessibility barriers in code or on a rendered page before they reach production.

## Limits

An audit doesn't certify WCAG or legal compliance. It also doesn't replace manual screen reader testing or testing with people with disabilities.

## Available Skills

### `/accessibility-audit`

**Interactive Configuration:**

The skill takes no arguments. Before starting the audit, it asks:

1. **WCAG Version**: Choose WCAG 2.1, WCAG 2.2, or 508 / WCAG 2.0 AA
2. **Conformance Level**: Choose A (minimum), AA (industry standard), or AAA (enhanced)
3. **Scope**: Choose entire codebase, specific directory, or a URL
4. **Visual Scanning** (if URL selected): Choose whether to use Playwright MCP tools for visual accessibility testing

**What it analyzes:** the areas listed under [Features](#features). URL audits with Playwright MCP also check:

- **Visual Color Contrast Testing** - Contrast measurements of rendered elements
- **Actual Focus Indicator Visibility** - Visual verification of focus states
- **Rendered DOM Structure** - Accessibility tree as perceived by assistive technologies
- **Interactive Element Testing** - Keyboard navigation testing on live page
- **Touch Target Size Verification** - Actual pixel measurements of interactive elements
- **Screenshot-based Analysis** - Visual accessibility assessment with evidence

## Available Agents

### `accessibility-auditor`

Runs the audit in a fresh context and writes the report. `/accessibility-audit` invokes it, and you can also use it for unattended or scheduled reviews.

---

## Quick Start

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
# - WCAG Version: 2.1, 2.2, or 508 / WCAG 2.0 AA
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
# - WCAG Version: 2.1, 2.2, or 508 / WCAG 2.0 AA
# - Conformance Level: A, AA, or AAA
# - Scope: a URL
# - Provide the URL to scan
# - Visual Scanning: Yes - Use Playwright for visual scans

# Step 3: If Playwright MCP is not installed, the skill will:
# - Offer to create .mcp.json configuration file
# - Ask you to restart Claude Code
# - After restart, run /accessibility-audit again

# Step 4: Review the generated report with visual evidence
# Located at: /docs/accessibility/{timestamp}-accessibility-audit.md

# Step 5: Implement recommended fixes
# Follow the prioritized remediation roadmap
```

---

## Features

### Configurable WCAG Assessment

**WCAG 2.1 vs 2.2:**
- **WCAG 2.1**: 78 success criteria across 13 guidelines (Level A 30, AA 20, AAA 28)
- **WCAG 2.2**: 86 success criteria (adds 9 and removes SC 4.1.1 Parsing; Level A 31, AA 24, AAA 31)
  - New criteria: Focus Not Obscured (AA/AAA), Focus Appearance (AAA), Dragging Movements (AA), Target Size Minimum (AA), Consistent Help (A), Redundant Entry (A), Accessible Authentication (AA/AAA)

**Conformance Levels** (WCAG 2.2, cumulative):
- **Level A** (31 criteria) - Minimum accessibility, critical barriers
- **Level AA** (55 criteria, A plus AA) - Industry standard
- **Level AAA** (86 criteria) - Enhanced accessibility, highest level

### Analysis Areas

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
- Visible focus indicators
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
- Touch target size: 24×24px minimum (AA, SC 2.5.8); 44×44px (AAA, SC 2.5.5)
- No horizontal scrolling at 320px width
- Text can be zoomed to 200%
- Orientation not locked
- Content reflows at 400% zoom
- WCAG 2.2: Dragging Movements (SC 2.5.7), Target Size Minimum (SC 2.5.8)

---

## Plugin Details

- **Name:** AI-Accessibility
- **Version:** 1.4.2
- **License:** MIT
- **Author:** Charles Jones

---

## Contributing

Bug reports and fixes are welcome. See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License. See [LICENSE](LICENSE).
