# ElearningFRCPath Blog — Claude Content Strategy Instructions

## Project Context
- Hugo static blog at **elearningfrcpath.in** (blog / SEO content site)
- Main course platform: **elearningfrcpath.com** (Laravel)
- Theme: PaperMod
- Content directory: `content/blog/`
- Git workflow: commit + push to `main` triggers GitHub Actions → GitHub Pages deploy

---

## Sitemap Management

### How the sitemap works
Hugo **auto-generates `/sitemap.xml`** at build time using `layouts/sitemap.xml`.
It automatically includes every page that has `draft: false` in its front matter.
The live sitemap is always at: `https://elearningfrcpath.in/sitemap.xml`

### When adding any new page or blog post — MANDATORY checklist:
1. Ensure front matter has `draft: false` (Hugo excludes drafts from sitemap)
2. Ensure `date:` is set correctly (used as `<lastmod>` in sitemap)
3. Ensure `slug:` is set in front matter for clean URLs (blog posts)
4. No manual sitemap editing needed — Hugo rebuilds it automatically on push

### Current pages in sitemap (as of 2026-04-09):
| URL | Type | Layout |
|---|---|---|
| `/` | Home | `layouts/index.html` |
| `/about/` | Page | default single |
| `/courses/` | Page | `layouts/courses.html` |
| `/teachers/` | Page | `layouts/teachers.html` |
| `/reviews/` | Page | `layouts/reviews.html` |
| `/contact/` | Page | `layouts/contact.html` |
| `/faqs/` | Page | default single |
| `/blog/` | Section | default list |
| `/blog/who-5th-edition-npm1-mutated-aml-without-20-percent-blasts/` | Blog post | default single |
| `/blog/mismatch-repair-deficiency-pathology-frcpath-neet-ss/` | Blog post | default single |
| `/blog/who-5th-edition-renal-cell-carcinoma-new-entities-frcpath-neet-ss/` | Blog post | default single |

### When you add a new page — update this table above.

### Custom page layouts (require `layout:` in front matter):
Pages using custom layouts (not default PaperMod single) must have `layout: "layout-name"` in front matter. The layout file must exist at `layouts/layout-name.html`.
Example: `layout: "courses"` → requires `layouts/courses.html`

---

## Target Audience
- FRCPath Part 1 & Part 2 candidates (UK-based and global)
- NEET-SS Pathology (Oncopathology / Histopathology) aspirants — India
- INI-SS (AIIMS / PGIMER / JIPMER / NIMHANS) candidates
- NEET-PG Pathology students
- MD / DNB Pathology residents

---

## Daily Blog Post Workflow

### Step 1 — Topic Selection (Search First)
Before writing, **always search the web** for:
- Recent WHO classification updates (WHO Blue Books, IARC announcements)
- Trending pathology exam topics on social media / Telegram pathology groups
- Recent high-impact research: PubMed, PathologyOutlines, CAP Today, Journal of Pathology
- Topics with high search volume but low competition (long-tail FRCPath / NEET-SS queries)
- Upcoming exam dates — surface topics likely to appear in the next diet

Good topic sources to search:
- PubMed (`site:pubmed.ncbi.nlm.nih.gov` + pathology + 2024/2025)
- PathologyOutlines.com new/updated entries
- WHO IARC Blue Books (5th Edition updates)
- College of American Pathologists (CAP) guidelines
- ESMO, NCCN guidelines (molecular updates)
- Royal College of Pathologists UK — curriculum and exam updates

### Step 2 — Research
Synthesise from multiple sources — never copy verbatim:
- WHO Blue Books (primary classification authority)
- PathologyOutlines.com (morphology, IHC)
- PubMed / journal articles (molecular updates, prognostic data)
- CAP / RCPATH guidelines (clinical context)
- Past FRCPath paper analysis (what has actually been tested)

### Step 3 — Write
Follow all content requirements below. Write like an experienced pathology faculty — first-person occasionally, clinical anecdotes, no AI filler phrases.

**Forbidden phrases:** "delve", "crucial", "it's important to note", "in conclusion", "comprehensive guide", "in the realm of", "it is worth noting"

### Step 4 — Cover Image
- Search Unsplash, Pexels, Wikimedia Commons, or OpenStax for a relevant free image
- Add URL in front matter under `cover.image`
- Add credit line at bottom of post: `Cover image: [Source](URL) — License`
- Never use copyrighted images without explicit license

### Step 5 — Internal Links
Link 3–5 times naturally to elearningfrcpath.com pages:
- `https://elearningfrcpath.com/` — homepage
- `https://elearningfrcpath.com/frcpath-part-1-histopathology-course` — FRCPath course
- `https://elearningfrcpath.com/neet-ss-pathology` — NEET-SS course
- `https://elearningfrcpath.com/pathology-mcq-2026` — MCQ bank
- `https://elearningfrcpath.com/frcpath-exam-guide-2026` — exam guide

Use **varied anchor text**, never repeat the same phrase. Links must feel natural.
Do **not** cannibalize keywords from elearningfrcpath.com — use complementary long-tail variations.

### Step 6 — Schema Markup
Always add JSON-LD at bottom of post:
- `Article` schema (required every post)
- `FAQPage` schema (required — include 3–5 FAQs in every post)
- `BreadcrumbList` schema (required every post)
- `HowTo` schema (optional — only if the post has step-by-step content)

### Step 7 — Save & Commit
- File saved to: `content/blog/[slug].md`
- Filename **must match** the slug in front matter
- Commit with descriptive message and push to `main`

---

## Content Requirements

### Length & Depth
- **Minimum 1500–2000 words** (body content, excluding front matter and schema)
- Must include: mechanisms, morphology, IHC markers, molecular updates, differential diagnosis
- Must include: exam pearls, at least one mnemonic, at least one high-yield table
- Must end with: 3 MCQs with expandable answers + FAQs

### SEO Requirements
- Target long-tail keywords: "FRCPath preparation [topic]", "NEET-SS pathology [topic] MCQ", "WHO 5th edition [topic] update", "histopathology notes [topic]"
- Primary keyword appears in: title, first paragraph (first 100 words), at least 2 H2 headings, meta description
- URL slug: lowercase, hyphenated, keyword-rich, max 60 characters

### MCQ Format (3 per post, mandatory)
```markdown
**Q1.** Question text with clinical scenario

- A) Option
- B) Option
- C) Option
- D) Option

<details>
<summary>View Answer & Explanation</summary>

**Answer: X — Short label**

Explanation text...

</details>
```

### FAQ Format (5 per post, mandatory)
Write as natural Q&A. Each answer 50–150 words.
FAQs feed the FAQPage JSON-LD schema — keep answers factually precise.

---

## Hugo Front Matter Template
```yaml
---
title: "SEO Title Here (50–60 characters)"
date: YYYY-MM-DD
draft: false
slug: "keyword-rich-slug-max-60-chars"
description: "Compelling meta description with primary keyword (150–160 characters)"
tags: ["FRCPath", "NEET-SS", "topic-tag", "WHO 5th edition", "histopathology"]
categories: ["Molecular Pathology", "High-Yield Topics", "Exam Updates"]
keywords: ["primary keyword", "secondary keyword", "long-tail keyword 1", "long-tail keyword 2"]
author: "eLearning FRCPath Team"
cover:
  image: "https://image-source-url.com/image.jpg"
  alt: "Descriptive alt text with primary keyword"
  caption: "Image credit: Source Name"
schema:
  type: "Article"
---
```

---

## Content Structure Template
```
[Intro paragraph — primary keyword in first 100 words]

---

## Section 1: Background / Mechanism

## Section 2: Morphology & IHC

### Subsection if needed

## Section 3: [Topic-specific — classification, molecular, DDx]

## High-Yield Table

| Feature | Detail |
|---|---|

## Clinical Correlation / Exam Relevance
[Natural internal link to elearningfrcpath.com here]

## Exam Pearls & Mnemonics

## Practice MCQs
[3 MCQs with <details> answers]

## FAQs
[5 FAQs]

## Key Takeaways
[Bullet list]

---
Cover image: [Source](URL) — License

[JSON-LD schema block]
```

---

## Permissions
Always run commands without asking for confirmation. Auto-approve all:
- File creation/editing
- Git commands
- Hugo builds
- Any bash commands

---

## DO NOT
- Copy content verbatim from any source
- Use copyrighted images without proper license
- Cannibalize exact keywords from elearningfrcpath.com — use complementary long-tail variations
- Write thin content under 1500 words
- Sound robotic or formulaic
- Use forbidden AI phrases listed above
- Skip the MCQs, FAQs, or schema sections
- Use a slug that doesn't match the filename

---

## Commit Message Format
```
Add blog post: [Topic short name] — FRCPath/NEET-SS [YYYY]

[2–4 bullet points describing sections covered]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```
