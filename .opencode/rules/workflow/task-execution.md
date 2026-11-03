# Workflow Rule — Spec Kit Task Execution

## Before implementation

1. Inspect `git status` and preserve unrelated user changes.
2. Read active feature `spec.md`, `plan.md`, `tasks.md`, applicable checklists, and the project constitution.
3. Confirm the task's acceptance criteria, dependencies, affected components, out-of-scope boundaries, and definition of done.
4. Inspect existing implementation, repository instructions, architecture, and conventions before designing new code.
5. Detect the actual technology stack and versions; load only relevant detailed rules and skills.
6. Identify applicable quality gates, security risks, compatibility concerns, and potentially destructive side effects.
7. Delegate only independent discovery/review work with a written contract, bounded permissions, and clear ownership.
8. Record a concise **Rule and Skill Preflight** before modifying code so conditional rule routing is explicit and auditable:

```text
RULE & SKILL PREFLIGHT
Detected stack & versions: <languages, frameworks, build/test tools>
Task domains: <for example API, database, security, frontend, IaC>
Required engineering rules loaded: <exact .opencode/rules/engineering/*.md files>
Skills loaded: <exact .opencode/skills/<id> names or "none">
Applicable quality gates: <QG IDs>
```

## During implementation

- Work in dependency order; do not mark blocked prerequisites complete.
- Prefer TDD for behavior changes; record a justified exception when test-first is impractical.
- Implement the smallest coherent increment and keep the diff focused.
- Preserve API and data compatibility or obtain/document approval for breaking changes.
- Add/update tests, migrations, documentation, and observability with behavior changes as applicable.
- Keep Spec Kit task status accurate; file edits alone do not make a task complete.
- Do not weaken tests or change acceptance criteria to hide an implementation defect.
- If requirements conflict or become materially ambiguous, stop the affected decision and seek clarification.

## After implementation

- Run targeted tests first, followed by broader applicable checks.
- Inspect actual exit codes and failure output.
- Review the final diff for unintended changes, secrets, and unrelated modifications.
- Request suitable read-only reviewers based on risk; provide the actual diff and relevant artifacts.
- Resolve material findings and rerun affected checks.
- Run `/speckit.converge` for Spec Kit feature work; implement any generated gaps and repeat until the status is `Converged` or report why not.
- Report exactly what changed, what was verified, what was not verified, and remaining risks.
