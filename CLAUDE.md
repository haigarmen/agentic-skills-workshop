# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A content-agnostic course creation system driven by markdown manifests, agent system prompts, and Claude Code skills. There is no build step, no runtime, and no test suite — the "code" is structured markdown and YAML. The system is operated entirely through Claude Code skills (`/skill-name`) and agents (`agents/<name>/AGENT.md`).

## Key Workflows

| Goal | How |
|---|---|
| Generate a complete course from scratch | Run the `course-generator` agent with `topic`, `audience`, and `format` |
| Scaffold a course directory manually | `/create-course` |
| Add a lesson to an existing module | `/create-lesson` |
| Add a standalone exercise | `/create-exercise` |
| Check a course for missing files or broken references | `/validate-course` |
| Write full lesson body content into stubs | `/write-content` |
| Produce a visual asset spec or diagram | `/create-visual` |
| Research a topic for course content | `/web-research` |
| Compile all lessons into a combined .docx or .html | `/export-course` |

## Architecture

### The Four Layers

```
skills/          ← Slash commands: atomic, user-invoked workflows
agents/          ← Agent system prompts: multi-step autonomous pipelines
courses/         ← Course content: manifests + lessons + exercises
exercises/       ← Standalone exercises (referenced by module.yml, not nested inside courses)
```

**Skills** (`skills/*.md`) are invoked directly by the user with `/skill-name`. Each skill is a numbered instruction list that Claude executes. Skills are atomic — they do one thing.

**Agents** (`agents/<name>/AGENT.md`) are autonomous multi-step pipelines. The `course-generator` agent is the primary entry point and runs a 4-stage sequential pipeline: research → syllabus & lessons → visual design → marketing campaign + resource guide (last two in parallel).

**Courses** (`courses/<id>/`) follow a strict directory and schema contract enforced by `/validate-course`. The hierarchy is: `course.yml` → `modules/<NN>-<slug>/module.yml` → `modules/<NN>-<slug>/lessons/<NN>-<slug>/lesson.md`.

**Exercises** live in `exercises/` (not inside course directories) and are referenced from `module.yml` by relative path (`../../../../exercises/<id>/exercise.md`). This keeps them reusable across courses.

### Schema Contract

Every file type has a mandatory schema — always copy from `_template/`, never create from scratch:

- `courses/_template/course.yml` — course manifest; `id` must be a lowercase hyphen-separated slug
- `courses/_template/modules/_template/module.yml` — module manifest; `order` must be set
- `courses/_template/modules/_template/lessons/_template/lesson.md` — lesson with required frontmatter: `id`, `title`, `module`, `order`, `type`, `estimated_minutes`
- `exercises/_template/exercise.md` — exercise with `Acceptance Criteria` section (used by the Grader agent)

### Agent Responsibilities

| Agent | When to use |
|---|---|
| `course-generator` | Full pipeline from topic to publication-ready package |
| `researcher` | Standalone topic research returning a structured brief |
| `writer` | Writing full lesson/exercise body content from stubs |
| `designer` | Producing visual asset specs and diagrams |
| `grader` | Evaluating a learner's exercise submission — reads `Acceptance Criteria`, never reveals `Solution` |
| `qa-tutor` | Answering learner questions grounded in course content |

### course-generator Pipeline (sequential)

1. **Research** — web research, pain points, curriculum sequencing
2. **Syllabus & Lessons** — `syllabus.md`, `course.yml`, `module.yml` files, `lesson.md` stubs
3. **Visuals** — `visuals.md` with asset specs and any directly producible diagrams
4. **Marketing + Resources** (parallel) — `marketing-campaign.md` and `online-resources.md`
5. **Lesson Content Authoring** — populate every `lesson.md` stub in sequence using `write-content` rules
6. **Export** — compile all content into `<course-id>-course-document.docx` (`.html` fallback if pandoc unavailable)

All output lands in `courses/<course-id>/`. Do not begin a later stage until the prior stage is complete.

## Conventions

- All IDs: lowercase, hyphen-separated slugs derived from the title (e.g. `intro-to-python`, `module-01`, `lesson-03`)
- Module directories: zero-padded numeric prefix — `modules/01-getting-started/`, `modules/02-core-concepts/`
- Lesson directories: same pattern — `lessons/01-overview/lesson.md`
- Never edit `_template/` files directly — they are the source of truth for schemas
- Skills frontmatter must include `name`, `description`, `version`, `tags`, `repository`, and `compatibility`
- When registering a new agent, update `agents/README.md` roster; when registering a new skill, update `skills/README.md` table and root `README.md` Quickstart
- All notable changes go in `CHANGELOG.md` under `[Unreleased]` until a version is cut
