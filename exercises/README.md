# Exercises

Exercises are stored here and referenced by path from `module.yml`. This keeps them reusable across courses.

## Conventions

- Each exercise lives in its own directory: `exercises/<exercise-id>/`
- The main file is always named `exercise.md`
- If the exercise requires runnable code, place it in `exercises/<exercise-id>/solution/`
- Exercise IDs are lowercase, hyphen-separated slugs

## Adding an Exercise

Run `/create-exercise` or copy `_template/` manually:

```
cp -r exercises/_template exercises/<your-exercise-id>
```

Then edit `exercises/<your-exercise-id>/exercise.md` and fill in every frontmatter field.

## Linking to a Lesson

Set `linked_lesson` in the exercise frontmatter, and add a reference to the exercise in the relevant `module.yml` under the `exercises` list.
