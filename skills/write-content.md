---
name: write-content
description: Populate a lesson or exercise stub with fully-written content, adapting tone and activity format to the course brand and learning mode.
version: "1.0.0"
tags: [education, writing, content-authoring, lesson, exercise]
repository: https://github.com/haigarmen/course-creator
compatibility: [claude-code, claude]
---

1. Accept inputs:
   - `course_id` — id of the course
   - `target` — `lesson` or `exercise`
   - `target_path` — path to the file to populate
   - `brand_profile` — tone, vocabulary level, and assumed knowledge derived from `course.yml`
   - `research` (optional) — structured research findings to draw from

2. Read the target file to identify its `type` (for lessons) and which sections are empty.

3. Read any sibling lessons in the same module to maintain continuity of voice and avoid repeating content already covered.

4. Write content for each empty section according to the lesson type:

   **reading**
   - Prose with clear headings, short paragraphs, and at least one concrete example per key concept
   - Use callout blocks (tip, note, warning) where genuinely useful — not decoratively

   **video**
   - Structured script with `[TIMESTAMP]` markers, `[VISUAL:]` cues, and `[SPEAKER NOTE:]` asides
   - Each segment should be 60–120 seconds when read at a natural pace

   **interactive**
   - Numbered steps; each step is a single discrete action the learner completes
   - Include expected outcome after steps where the result might not be obvious

   **quiz**
   - Minimum 3 questions; mix formats (MCQ, short answer, scenario)
   - Each question includes: prompt, options (if MCQ), correct answer, and a one-sentence explanation

   **exercise**
   - Problem Statement: self-contained, no assumed context
   - Requirements: specific and testable checkboxes
   - Hints: two progressive hints — nudge then closer nudge
   - Acceptance Criteria: observable, unambiguous checkboxes
   - Solution: complete worked answer inside a `<details>` block

5. Apply the `brand_profile`:
   - Match vocabulary level to the target audience
   - Mirror the tone (e.g. encouraging and practical vs. concise and technical)
   - Respect assumed knowledge — do not explain concepts covered in earlier lessons

6. Write the populated content to `target_path`. Do not modify any other file.

7. Return the path written and a one-line description of what was produced.
