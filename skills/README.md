# Skills

Skills are Claude Code workflows invoked with a `/skill-name` command. Each skill is a markdown file describing a numbered sequence of steps.

## Available Skills

| Skill | File | Purpose |
|-------|------|---------|
| `/create-course` | `create-course.md` | Scaffold a new course directory from the template |
| `/create-lesson` | `create-lesson.md` | Add a lesson stub to an existing module |
| `/create-exercise` | `create-exercise.md` | Add a standalone exercise |
| `/validate-course` | `validate-course.md` | Check a course manifest for completeness |

## Adding a Skill

1. Create a `.md` file in `skills/` with a name matching the slash command
2. Add a frontmatter block with `name` and `description`
3. Write numbered steps describing what Claude should do when the skill is invoked
4. Register it in this README's table
