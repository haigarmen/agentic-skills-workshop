# Agents

Each agent is defined by an `AGENT.md` file in its own subdirectory. The file contains the agent's role, required inputs, and behavioral constraints.

## Agent Roster

| Agent | Directory | Purpose |
|-------|-----------|---------|
| Course Generator | `course-generator/` | Scaffold a new course from a topic, audience, and outline |
| Grader | `grader/` | Evaluate a learner's exercise submission against acceptance criteria |
| Q&A Tutor | `qa-tutor/` | Answer learner questions grounded in course content |

## Adding an Agent

1. Create a new directory under `agents/`: `agents/<agent-name>/`
2. Add an `AGENT.md` with: Role, Inputs, Allowed Skills, Output, and Notes sections
3. Register the agent in this README's roster table
