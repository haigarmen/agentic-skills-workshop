# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.3.0] - 2026-04-16

### Changed
- `/write-content` skill enhanced with a session design principles step (step 5): learning objectives tied to course goals, minute-by-minute session structure, mandatory formative assessment activities, activity balance requirements (engaging/hands-on/instructional), later-phase variety guidelines, materials list output, and physical environment specification per session

## [0.2.0] - 2026-04-16

### Changed
- `course-generator` agent upgraded from a scaffold-only generator to a full 4-stage autonomous pipeline: research & curriculum sequencing → syllabus & detailed lessons → visual design aids → marketing campaign & online resource guide (parallel)
- `course-generator` inputs expanded: added `format`, `circuits`, `instructor_profile`, and `price_range`; agent now requires `format` as a required input alongside `topic` and `audience`
- `agents/README.md` updated to reflect the course-generator's new pipeline role and expanded `AGENT.md` section schema
- `skills/README.md` updated to register previously undocumented skills: `/create-visual`, `/web-research`, `/write-content`
- Root `README.md` Quickstart table updated to surface the full pipeline workflow and all available skills

## [0.1.0] - 2026-04-09

### Added
- Initial project setup with agents, courses, exercises, and skills structure
- Version field added to all skills
- Tags, repository, and compatibility metadata added to all skills
- MIT License

### Changed
- Repository renamed from `Agentic-Skills-Workshop` to `course-creator`
- Updated repository URLs to reflect rename
- Updated README title to match repository rename
