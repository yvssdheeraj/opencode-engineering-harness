# Workflow Rule — Task Execution

## Before implementation

1. Inspect `git status` and preserve unrelated user changes.
2. If feature artifacts (spec, plan, tasks, checklists, project principles) exist, read them; otherwise use the user requirements.
3. Confirm the task's acceptance criteria, dependencies, affected components, out-of-scope boundaries, and definition of done.
4. Inspect existing implementation, repository instructions, architecture, and conventions before designing new code.
5. Detect the actual technology stack and versions; load only relevant detailed rules and skills.
6. Identify applicable quality gates, security risks, compatibility concerns, and potentially destructive side effects.
7. Delegate only independent discovery/review work with a written contract, bounded permissions, and clear ownership.
8. Record a concise **Selected rules & skills** note before modifying code so conditional rule routing is explicit (because a file like `src/user_service.py` can still introduce `security`, `database`, or `performance` risks that filename alone cannot infer):

```text
Selected rules & skills
Stack & versions: <languages, frameworks, build/test tools>
Task domains: <for example API, database, security, frontend>
Engineering rules: <exact .opencode/rules/engineering/*.md files from AGENTS.md table>
Skills: <exact .opencode/skills/<id> names or "none">
Quality gates: <relevant QG IDs>
Reviewers: <reviewer agent IDs if delegation needed>
```

## During implementation

- Work in dependency order; do not mark blocked prerequisites complete.
- Prefer TDD for behavior changes; record a justified exception when test-first is impractical.
- Implement the smallest coherent increment and keep the diff focused.
- Preserve API and data compatibility or obtain/document approval for breaking changes.
- Add/update tests, migrations, documentation, and observability with behavior changes as applicable.
- Keep task status accurate; file edits alone do not make a task complete.
- Do not weaken tests or change acceptance criteria to hide an implementation defect.
- If requirements conflict or become materially ambiguous, stop the affected decision and seek clarification.

## Debugging and legacy protocol (bug fix or untested code only)

- Reproduce first with minimal case, commands, and logs before editing; do not guess.
- Isolate cause and record one hypothesis; disconfirm alternatives with evidence.
- For untested legacy code, pin current behavior with a characterization test before refactoring.
- Apply the minimal fix and add a regression test covering the reproduced failure.
- If reproduction is impossible, state the evidence gap; do not claim the defect is fixed.

## After implementation

- Run targeted tests first, followed by broader applicable checks.
- Inspect actual exit codes and failure output.
- Review the final diff for unintended changes, secrets, and unrelated modifications.
- Request suitable read-only reviewers based on risk; provide the actual diff and relevant artifacts.
- Resolve material findings and rerun affected checks.
- Report exactly what changed, what was verified, what was not verified, and remaining risks.

## Failure and recovery protocol

- **Subagent failure or timeout:** If a delegated `explorer` or `*-reviewer` times out or returns `BLOCKED`, narrow the scope and retry once or perform the bounded inspection directly in `developer` and disclose the fallback in the final report.
- **Reviewer disagreement:** Evaluate reviewer findings against feature acceptance criteria, project principles, and `.opencode/rules/`. If a finding is a false positive or out of scope, record the technical rationale under `Review findings and disposition` (`EVID-10`) rather than blindly applying harmful edits.
- **Unrunnable tests or missing tools:** Do not fake a pass (`EVID-03`, `TEST-18`). Diagnose whether the failure is environment-related, run the narrowest available static/syntax check, and explicitly list unverified checks under `Not run / not verified`.
- **Context compaction or interrupted session:** Maintain the compact task checkpoint (`CTX-07`) and re-read active task state and `git status` / `git diff` before resuming edits.
