# Agents

Each agent is defined by an `AGENT.md` file in its own subdirectory. The file contains the agent's role, required inputs, and behavioral constraints.

## Agent Roster

| Agent | Directory | Purpose |
|-------|-----------|---------|
| Course Generator | `course-generator/` | Run the full course creation pipeline: research → syllabus & lessons → visual design → marketing campaign & resource guide |
| Grader | `grader/` | Evaluate a learner's exercise submission against acceptance criteria |
| Q&A Tutor | `qa-tutor/` | Answer learner questions grounded in course content |

## Adding an Agent

1. Create a new directory under `agents/`: `agents/<agent-name>/`
2. Add an `AGENT.md` with: Role, Pipeline, Inputs, Allowed Skills, Output, Execution Rules, and Notes sections
3. Register the agent in this README's roster table
