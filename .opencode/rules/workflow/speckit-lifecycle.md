# Workflow Rule — Spec Kit Lifecycle and OpenCode Agent Mapping

## Ownership model

- Spec Kit owns structured feature artifacts and specification-driven lifecycle commands.
- OpenCode provides the agent runtime, agent roles, permissions, shared instructions, and on-demand skills.
- The primary `developer` agent coordinates the feature and owns implementation, integration, verification, convergence, and reporting.
- Specialist subagents provide bounded exploration and reviews; they do not independently own feature artifacts by default.

## Standard production-feature workflow

| Stage | Spec Kit command | Primary agent | Specialist selection |
|---|---|---|---|
| Project principles | `/speckit.constitution` | `developer` works with user to establish durable principles | `architecture-reviewer` for major architectural constraints; `security-reviewer` for security baseline if useful |
| Feature behavior | `/speckit.specify` | `developer` | `explorer` only when existing behavior needs inspection; user resolves product decisions |
| Ambiguity | `/speckit.clarify` | `developer` | Specialist input may inform questions; user owns business decisions |
| Technical plan | `/speckit.plan` | `developer` | `explorer` for current-state discovery; `architecture-reviewer` for cross-cutting design; security/infra reviewers as relevant |
| Requirement checklist | `/speckit.checklist` | `developer` | `test-reviewer`, `security-reviewer`, `infra-reviewer` for applicable quality perspectives |
| Task breakdown | `/speckit.tasks` | `developer` | Usually no subagent; ask reviewer for task completeness on complex work |
| Consistency analysis | `/speckit.analyze` | `developer` | Specialists may investigate specific findings; developer resolves source artifacts |
| Implementation | `/speckit.implement` | `developer` | Load technology skills; delegate bounded independent discovery/review; write-enabled workers only after file ownership is clear |
| Convergence | `/speckit.converge` | `developer` | Specialists investigate unresolved implementation gaps as needed |
| Final review | After convergence | `developer` coordinates | `code-reviewer` plus risk-appropriate specialist reviewers |

## Standard sequence

1. `/speckit.constitution` — establish durable project principles when initializing or materially changing them.
2. `/speckit.specify` — define behavior, user/business value, and acceptance criteria.
3. `/speckit.clarify` — resolve material ambiguity before committing to design.
4. `/speckit.plan` — define technical approach; inspect the current codebase and relevant dependencies.
5. `/speckit.checklist` — create applicable requirement-quality checklist(s) based on risk.
6. `/speckit.tasks` — create actionable, dependency-ordered tasks with completion conditions.
7. `/speckit.analyze` — identify inconsistencies among specification, plan, and tasks; resolve at source.
8. `/speckit.implement` — implement tasks incrementally with relevant skills and tests.
9. `/speckit.converge` — compare codebase and artifacts, implement any generated gaps, and repeat until converged or explicitly report a blocker.
10. Run applicable independent reviews and quality gates; address findings and re-verify.

For small, low-risk changes, the user/team may choose a shorter path. Do not add ceremony where it offers no value, but preserve appropriate acceptance and verification evidence.

## Spec Kit and custom rules

- Keep the Spec Kit constitution concise, durable, testable, and project-specific. Do not paste every detailed framework rule into it.
- Put cross-project engineering detail in `.opencode/rules/engineering/` and language/framework detail in `.opencode/skills/`.
- Put feature behavior and acceptance criteria in feature artifacts, not in the constitution.
- Do not duplicate or shadow Spec Kit `/speckit.*` commands with custom commands.
- Preserve Spec Kit-generated `.opencode/commands/` and any integration event/plugin configuration.
- Invoke `/speckit.*` commands in OpenCode chat using the syntax installed by the current Spec Kit integration; do not assume they are shell commands.
- Avoid multiple agents editing the same Spec Kit artifacts concurrently. The primary developer owns the feature artifacts unless the user explicitly assigns otherwise.
