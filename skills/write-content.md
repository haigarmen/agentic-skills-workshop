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

5. Apply session design principles when writing any lesson:

   **Learning objectives**
   - Open every session with explicit learning objectives tied directly to the overall course goal.
   - Each objective must be measurable — learners should be able to self-assess whether they met it.

   **Session structure**
   - Divide every session into clearly named sections; never plan a single undivided block.
   - Plan the session minute by minute so the sequence is explicit on paper, not just in the author's head.

   **Assessment activities**
   - Embed at least one formative assessment per session: a short task, quiz question, or structured discussion prompt that lets you gauge understanding before moving on.

   **Activity balance**
   - Each session must balance three elements: engaging activities, hands-on components, and instructional content. No single element should dominate.

   **Later-phase variety**
   - Once the course shifts into its practice-heavy phase (fewer lectures, more applied work), vary the session format deliberately: rotate between individual tasks, small-group discussions, peer feedback, and reflection exercises to prevent monotony.

   **Materials list**
   - Produce a materials section for the lesson listing everything needed — hardware, software, stationery, printed sheets, room booking, transportation, or additional assistance. Think broadly; omissions cause last-minute scrambles.

   **Physical environment**
   - Specify the ideal learning environment for each session. Examples: a clear open room for brainstorming or design thinking; a computer lab for individual and small-group work; an off-site venue (museum, studio, makerspace) for site visits; an exhibition or presentation area for showcases. State the environment type explicitly in the lesson plan.

6. Apply the `brand_profile`:
   - Match vocabulary level to the target audience
   - Mirror the tone (e.g. encouraging and practical vs. concise and technical)
   - Respect assumed knowledge — do not explain concepts covered in earlier lessons

7. Write the populated content to `target_path`. Do not modify any other file.

8. Return the path written and a one-line description of what was produced.
