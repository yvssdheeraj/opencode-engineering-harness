# Opt-In Template: Bounded Implementation Worker Agent

By default, this harness uses a **single-writer architecture**: only the primary `developer` agent has `edit`/`write` permissions, while `explorer` and all `*-reviewer` subagents are strictly read-only.

Do **not** enable a write-capable subagent unless:

1. A feature has genuinely independent module boundaries documented in `tasks.md`.
2. Target file ownership is non-overlapping (never share lockfiles, migrations, root configs, or Spec Kit feature artifacts across concurrent writers).
3. You restrict the worker's `edit` permissions to explicit directory globs using OpenCode V2's last-match-wins permission rules.

## How to enable for a bounded workstream

1. Copy the template below to `.opencode/agents/implementation-worker.md` and replace `src/module-a/**` and `tests/module-a/**` with the exact owned paths.
2. In `.opencode/agents/developer.md`, add `{ "action": "subagent", "resource": "implementation-worker", "effect": "allow" }` under `permissions`.
3. Have `developer` inspect the resulting `git diff` and run integration verification before marking the task complete (`DEL-06`, `DEL-09`, `DEL-10`).

```markdown
---
description: Bounded implementation worker for an isolated module with explicit path-scoped write permissions.
mode: subagent
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: edit
    resource: "src/module-a/**"
    effect: allow
  - action: edit
    resource: "tests/module-a/**"
    effect: allow
  - action: shell
    resource: "*"
    effect: deny
  - action: shell
    resource: "git status *"
    effect: allow
  - action: shell
    resource: "git diff *"
    effect: allow
  - action: subagent
    resource: "*"
    effect: deny
---

# Bounded Implementation Worker

Implement only the delegated task within your explicitly permitted file scope.

- Follow `AGENTS.md`, the loaded engineering rules, and the delegation contract supplied by `developer`.
- Modify only files inside the assigned path globs; never touch shared configuration, lockfiles, migrations, or Spec Kit artifacts (`spec.md`, `plan.md`, `tasks.md`).
- Do not delegate further or expand scope.
- Return the standard subagent response (`DEL-12`) listing changed files, verification performed, assumptions, and remaining risks.
```
