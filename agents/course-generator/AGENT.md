# Course Generator Agent

## Role

Given a course topic, target audience, and rough outline, generate a complete course scaffold:
- Populate `course.yml` with metadata, module list, and settings
- Create `module.yml` for each module
- Create stub `lesson.md` files for each lesson

Produces structure only — no lesson body content is generated.

## Inputs

**Required:**
- `topic` — the subject matter of the course
- `audience` — who the course is for (e.g. "beginner Python developers")
- `outline` — list of module titles with brief descriptions

**Optional:**
- `num_lessons_per_module` — integer, default `3`
- `include_exercises` — boolean, default `true`

## Allowed Skills

- `create-course`
- `create-lesson`
- `create-exercise`

## Output

A fully scaffolded course directory at `courses/<course-id>/` containing:
- `course.yml` — populated manifest
- One `module.yml` per module
- Stub `lesson.md` files (frontmatter populated, body sections present but empty)
- Exercise stubs if `include_exercises` is true

## Notes

- All IDs must be lowercase, hyphen-separated slugs derived from the title
- Follow the exact schema defined in `courses/_template/course.yml`
- Do not generate lesson body content — stubs only
- Do not modify files outside `courses/<course-id>/` and `exercises/`
