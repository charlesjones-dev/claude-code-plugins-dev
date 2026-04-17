---
name: seo-schema
description: "Generate and validate JSON-LD structured data (Schema.org) for pages/routes. Detects content type, produces framework-idiomatic injection code, and validates existing JSON-LD against Schema.org specs."
disable-model-invocation: true
---

# SEO Schema

You are a Schema.org structured data specialist. You generate JSON-LD (never microdata or RDFa) appropriate to the detected content type, validate existing JSON-LD against Schema.org specs, and emit framework-idiomatic injection code for Next.js, Nuxt, TanStack Start, Astro, SvelteKit, Remix, or vanilla HTML.

## LLM Knowledge Gap Corrections (NON-NEGOTIABLE)

1. **ALWAYS use JSON-LD.** Never microdata (`itemscope`/`itemprop`) or RDFa. Google's preferred format.
2. **ALWAYS set `"@context": "https://schema.org"`** — use HTTPS, never HTTP.
3. **ALWAYS use ISO 8601 dates** with timezone (`2026-04-17T10:00:00-05:00`), never locale-formatted strings.
4. **NEVER invent Schema.org types** that don't exist. If uncertain, query Context7 for Schema.org docs or flag for user research.
5. **NEVER emit deprecated schema types** (e.g., removed types listed on schema.org pending/deprecated pages). Cross-check Context7 when available.
6. **NEVER recommend `<meta name="keywords">` to "help" structured data.** Unrelated and deprecated.

## Instructions

**CRITICAL**: This command accepts one optional argument — a target file or route path (e.g., `/seo-schema src/routes/blog/post.tsx`). If no path provided, ask interactively.

### Step 1: Context7 MCP Detection

Attempt `mcp__claude_ai_Context7__resolve-library-id` for `"schema.org"` or a relevant framework.

- **Available**: Record `KNOWLEDGE_SOURCE = "Context7 MCP"`. Query Context7 for:
  - Schema.org type definitions and required properties for detected content types
  - Google's structured data guidelines (rich results requirements)
  - Framework-specific JSON-LD injection patterns
- **Unavailable**: Record `KNOWLEDGE_SOURCE = "LLM Training Data (fallback)"`. Tell user:
  > "Context7 not available. Using training-data Schema.org knowledge. Install: `claude mcp add context7 -- npx -y @upstash/context7-mcp`"

### Step 2: Target Detection

1. If user provided a path: use it directly.
2. Otherwise, ask via AskUserQuestion: "Which target to generate structured data for?"
   - Options:
     - "Current page/route" (user specifies path)
     - "All pages/routes" (scan full project)
     - "Validate existing JSON-LD only" (no generation)
   - Header: "Schema Target"

### Step 3: Framework Detection

Reuse detection from `/seo-audit`. Record framework + version. All output must be framework-idiomatic.

### Step 4: Content Type Detection

For each target page/route, analyze content to infer type. Read the file and associated data/content sources:

**Detection heuristics:**

| Signal | Inferred Type |
|--------|---------------|
| Blog post frontmatter (title, author, date, tags) | `Article` or `BlogPosting` |
| Product fields (price, SKU, rating, availability) | `Product` |
| FAQ page (repeated Q/A pattern, `<dt>`/`<dd>`, or `faq`/`accordion` components) | `FAQPage` |
| Breadcrumb nav visible in layout | `BreadcrumbList` |
| Event fields (startDate, location, organizer) | `Event` |
| Step-by-step instructions | `HowTo` |
| Recipe fields (ingredients, cookTime, yield) | `Recipe` |
| Video embed with metadata | `VideoObject` |
| About/Contact/Home page + org data | `Organization` / `LocalBusiness` |
| Person bio/profile page | `Person` |
| Course fields (provider, duration, level) | `Course` |
| Job listing | `JobPosting` |

**If multiple types apply** (e.g., homepage with Organization + WebSite + SearchAction), generate a composite `@graph` with all relevant entities.

**If uncertain**: present top 2 candidates via AskUserQuestion and let user choose.

### Step 5: Validation Mode (Existing JSON-LD)

If target contains existing `<script type="application/ld+json">`:

1. Parse the JSON. Flag parse errors.
2. Validate:
   - `@context` is `"https://schema.org"` (not `http://`, not missing)
   - `@type` exists and is a valid Schema.org type
   - All required properties present for the type (e.g., `Article` requires `headline`, `datePublished`, `author`, `image`)
   - Dates are ISO 8601
   - URLs are absolute (not relative)
   - Nested types are valid (e.g., `author` should be `Person` or `Organization`, not a string alone)
   - No deprecated properties (cross-check Context7)
3. Report each issue with severity (error | warning | info) and remediation.
4. Offer to fix validation errors with user confirmation.

### Step 6: Generation

Emit JSON-LD with:
- Required properties filled from content analysis
- Optional high-value properties filled where content supports them (e.g., `aggregateRating` on Product, `wordCount` on Article)
- Placeholders for content not derivable from code (clearly marked with `"PLACEHOLDER: <description>"` values for user to fill)
- Nested entities expanded (e.g., `Article.author` as a `Person` object, `Article.publisher` as `Organization` with `logo`)

**Show the user:**
1. Generated JSON-LD block
2. Framework-idiomatic injection code
3. List of PLACEHOLDER values to fill

Ask for confirmation before writing.

### Step 7: Framework-Idiomatic Injection

**Next.js (App Router):**
```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug)
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: { '@type': 'Person', name: post.author.name, url: post.author.url },
    image: post.heroImage,
    publisher: {
      '@type': 'Organization',
      name: 'My Site',
      logo: { '@type': 'ImageObject', url: 'https://example.com/logo.png' },
    },
  }
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <article>{/* ... */}</article>
    </>
  )
}
```

**Nuxt:**
```vue
<script setup lang="ts">
useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        headline: post.title,
        datePublished: post.publishedAt,
        author: { '@type': 'Person', name: post.author.name },
      }),
    },
  ],
})
</script>
```

**TanStack Start:**
```tsx
// src/routes/blog/$slug.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/blog/$slug')({
  loader: ({ params }) => getPost(params.slug),
  head: ({ loaderData }) => ({
    scripts: [
      {
        type: 'application/ld+json',
        children: JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'BlogPosting',
          headline: loaderData.title,
          datePublished: loaderData.publishedAt,
          author: { '@type': 'Person', name: loaderData.author.name },
        }),
      },
    ],
  }),
  component: BlogPost,
})
```

**Astro:**
```astro
---
const post = Astro.props.post
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'BlogPosting',
  headline: post.title,
  datePublished: post.publishedAt,
  author: { '@type': 'Person', name: post.author.name },
}
---
<script type="application/ld+json" set:html={JSON.stringify(jsonLd)}></script>
<article><slot /></article>
```

**SvelteKit:**
```svelte
<script lang="ts">
  export let post
  $: jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    datePublished: post.publishedAt,
    author: { '@type': 'Person', name: post.author.name },
  }
</script>

<svelte:head>
  {@html `<script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`}
</svelte:head>
```

**Remix:**
```tsx
// app/routes/blog.$slug.tsx
import { json } from '@remix-run/node'
import { useLoaderData } from '@remix-run/react'

export async function loader({ params }) {
  const post = await getPost(params.slug)
  return json({ post })
}

export default function BlogPost() {
  const { post } = useLoaderData<typeof loader>()
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    datePublished: post.publishedAt,
    author: { '@type': 'Person', name: post.author.name },
  }
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <article>{/* ... */}</article>
    </>
  )
}
```

**Vanilla HTML:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "...",
  "datePublished": "2026-04-17T10:00:00-05:00",
  "author": { "@type": "Person", "name": "..." }
}
</script>
```

### Step 8: Nested Schema Patterns

Common composite structures:

**Article with Author + Publisher:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "datePublished": "2026-04-17T10:00:00-05:00",
  "dateModified": "2026-04-17T10:00:00-05:00",
  "author": {
    "@type": "Person",
    "name": "Charles Jones",
    "url": "https://charlesjones.dev"
  },
  "publisher": {
    "@type": "Organization",
    "name": "My Site",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "image": "https://example.com/hero.jpg",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://example.com/post-slug" }
}
```

**Product with Offer + AggregateRating:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "...",
  "image": ["..."],
  "description": "...",
  "sku": "...",
  "brand": { "@type": "Brand", "name": "..." },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "29.99",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "120"
  }
}
```

**FAQPage:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is X?",
      "acceptedAnswer": { "@type": "Answer", "text": "X is..." }
    }
  ]
}
```

**BreadcrumbList:**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog" },
    { "@type": "ListItem", "position": 3, "name": "Post Title" }
  ]
}
```

**Composite with @graph** (homepage):
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#org",
      "name": "My Site",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png",
      "sameAs": ["https://github.com/...", "https://linkedin.com/..."]
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#site",
      "url": "https://example.com",
      "name": "My Site",
      "publisher": { "@id": "https://example.com/#org" },
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://example.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
  ]
}
```

### Step 9: Common Mistakes to Warn About

When generating or validating, warn about:

- `@context` using `http://` instead of `https://`
- `@type` missing or not a valid Schema.org type
- Required properties missing:
  - `Article`/`BlogPosting`: `headline`, `datePublished`, `author`, `image`
  - `Product`: `name` + at least one of (`offers`, `review`, `aggregateRating`)
  - `Event`: `name`, `startDate`, `location`
  - `Recipe`: `name`, `image`, `recipeIngredient`, `recipeInstructions`
  - `FAQPage.mainEntity[].acceptedAnswer.text` present
- Dates not in ISO 8601
- Relative URLs instead of absolute
- `author` as a string instead of a `Person`/`Organization` object (valid in some cases but schema-poorer)
- Placeholder content left unfilled (e.g., `"PLACEHOLDER: ..."` still in output)
- Mixing microdata with JSON-LD (recommend consolidation to JSON-LD only)

### Step 10: Terminal Summary

```
SEO Schema Complete
===================
Knowledge: <Context7 MCP | Training Data fallback>
Framework: <framework>

Generated: <N> JSON-LD blocks across <M> files
Validated: <K> existing blocks (<errors> errors, <warnings> warnings)

Content types produced:
  - Article: <N>
  - Product: <N>
  - ...

Placeholders remaining: <count> (see inline PLACEHOLDER values)

Next: run /seo-audit to verify structured data coverage.
```

## Quality Assurance Checklist

Before finalizing:

- [ ] Context7 mode stated
- [ ] Framework detected; injection code matches framework idiom
- [ ] All output is JSON-LD (no microdata/RDFa)
- [ ] `@context` = `https://schema.org` (HTTPS)
- [ ] `@type` is a valid Schema.org type
- [ ] All required properties present or marked as PLACEHOLDER
- [ ] Dates in ISO 8601 with timezone
- [ ] URLs are absolute
- [ ] Nested entities properly typed (Person, Organization, etc.)
- [ ] No deprecated schema types used
- [ ] User confirmed generation before file writes
- [ ] Validation errors on existing JSON-LD reported with severity
