# Common Rule — Evidence, Progress, and Completion Reporting

| ID | Requirement | Agent behavior |
|---|---|---|
| EVID-01 | Inspected vs changed | Distinguish files and behavior inspected from files and resources actually changed. |
| EVID-02 | Executed vs verified | Distinguish commands/tests/scans executed from results that were successfully verified. |
| EVID-03 | Honest claims | Never fabricate file changes, line references, tests, builds, scans, reviews, deployment outcomes, or tool results. |
| EVID-04 | Actual command result | Report the relevant command/check and whether it passed, failed, was skipped, blocked, or was not applicable. |
| EVID-05 | Final status inspection | A command starting is not a pass. Inspect its final exit status and relevant failure output. |
| EVID-06 | Review scope | State the scope and limitations of a review. A review with no findings is not proof of overall security or correctness. |
| EVID-07 | Deployment evidence | A local build or deployment command is not proof that a deployed service is healthy. Verify the actual target where authorized. |
| EVID-08 | Traceable evidence | Link findings and verification to file paths, symbols, task IDs, acceptance criteria, commands, or logs where possible. |
| EVID-09 | Progress visibility | For long-running tasks, report meaningful milestones, decisions, blockers, and material changes in status; avoid action-by-action narration. |
| EVID-10 | Complete final report | Report summary, changed paths, verification evidence, skipped checks, limitations, outstanding issues, and material risks. |

## Final report template

```text
Status: COMPLETE | PARTIAL | BLOCKED
Summary:
Requirements/tasks addressed:
Files changed:
Verification:
  - command/check: result
Not run / not verified:
Review findings and disposition:
Outstanding issues / risks:
Spec Kit convergence status:
```

Do not mark a Spec Kit task complete until the corresponding implementation and applicable verification have been completed. Report the exact convergence status; do not infer it.
