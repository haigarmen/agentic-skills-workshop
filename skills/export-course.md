---
name: export-course
description: Compile all lesson content for a course into a single combined document (.docx or .html), with a generated table of contents and module dividers.
version: "1.0.0"
tags: [export, documentation, publishing, pandoc, docx, html]
repository: https://github.com/haigarmen/course-creator
compatibility: [claude-code, claude]
---

1. Accept inputs:
   - `course_id` — id of the course to export (e.g. `tumo2026`)
   - `output_format` — `docx` (default) or `html`
   - `course_path` — path to the course directory (default: `courses/<course_id>/`)

2. Read `course.yml` to extract the course title, subtitle, description, estimated hours, and tags.

3. Collect and sort all modules by scanning `course_path/modules/` for directories containing a `module.yml`. Read each `module.yml` to get the module title, description, and order. Sort by the `order` field.

4. For each module in order, collect and sort all lessons by scanning the module's `lessons/` subdirectory for directories containing a `lesson.md`. Read each `lesson.md` frontmatter to get the lesson title and order. Sort by the `order` field.

5. Build the combined document content in this order:

   **Cover section:**
   - Course title (H1)
   - Subtitle and date on separate lines
   - A horizontal rule
   - Course overview table: duration, disciplines, tools, format, final output — drawn from `course.yml` fields

   **For each module:**
   - A module divider (H2): `## Module N — <title>`
   - The module description paragraph
   - A horizontal rule

   **For each lesson in the module:**
   - The lesson heading (H1): `# <lesson title>`
   - The full lesson body content with one transformation: any fenced Mermaid code blocks (` ```mermaid ... ``` `) replaced with a readable text-based equivalent:
     - If the diagram is a flowchart, render it as a `>` blockquote signal flow description (e.g. `> **A** → **B** → **C**`)
     - If the diagram contains a table-like structure (families, comparisons), render it as a markdown table instead
     - Preserve all other content (code blocks in other languages, callouts, lists) verbatim

   **Closing line:**
   - `*End of course handbook. <course title>.*`

6. Write the combined content to `/tmp/<course_id>-combined.md`.

7. Attempt to export using pandoc:
   ```
   pandoc /tmp/<course_id>-combined.md --toc --toc-depth=2 -o <course_path>/<course_id>-course-document.docx
   ```
   - If pandoc succeeds, report the output path and file size.
   - If pandoc is not installed or returns a non-zero exit code, fall back to step 8.

8. HTML fallback (if pandoc unavailable or `output_format` is `html`):
   - Write a self-contained HTML file to `<course_path>/<course_id>-course-document.html`
   - Embed the following in the `<head>`: Inter and JetBrains Mono from Google Fonts; a print-friendly CSS block (max-width 800px, comfortable line-height, page-break-before on H1 headings, monospace code blocks); Mermaid.js from CDN (`https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js`) with `mermaid.initialize({ startOnLoad: true })`
   - In this HTML path, preserve Mermaid fenced blocks as `<pre class="mermaid">` tags so diagrams render in the browser
   - Include a cover page section and a generated table of contents as a `<nav>` block with anchor links to each H1/H2 heading

9. Return the output file path and a one-line summary of what was produced (format, number of modules, number of lessons).
