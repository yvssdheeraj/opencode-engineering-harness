# Common Rule — Context, Memory, and Token Efficiency

Applies to every agent. Token efficiency must never come at the expense of correctness, security, or required evidence.

| ID | Requirement | Agent behavior |
|---|---|---|
| CTX-01 | Relevant context only | Read the minimum set of files needed to understand the assigned task and its dependencies. |
| CTX-02 | Targeted exploration | Prefer symbol searches, filename searches, references, and bounded excerpts over dumping entire repositories or large files. |
| CTX-03 | Avoid repeated reads | Do not reread unchanged files or repeat completed investigations without a reason. Re-read after relevant changes or when verification requires it. |
| CTX-04 | Bounded outputs | Filter logs, test output, diffs, and command output to relevant errors, summaries, symbols, and changed ranges. Preserve enough context to diagnose the issue. |
| CTX-05 | Structured summaries | Summarize lengthy investigations and tool results into concise findings with paths, symbols, task IDs, evidence, and implications. |
| CTX-06 | Decision preservation | Preserve user intent, acceptance criteria, constraints, architectural decisions, rejected alternatives, and reasons that affect subsequent work. |
| CTX-07 | Progress preservation | For long tasks, maintain a compact checkpoint containing current task, completed work, files changed, verification, blockers, and next action. Use a task file only when it materially helps continuity. |
| CTX-08 | Efficient delegation | Delegate broad exploration or specialist review when a compact result is more useful than importing the full investigation into the primary context. |
| CTX-09 | No transcript dumping | Do not forward full subagent transcripts when a structured outcome and evidence summary are sufficient. |
| CTX-10 | On-demand rules and skills | Load detailed engineering rules and technology skills only when relevant to the current task. Do not load every available skill by default. |
| CTX-11 | Context handoff | When handing work to another agent or resuming after compaction, explicitly carry forward the relevant objective, constraints, decisions, paths, status, evidence, and unresolved questions. |
| CTX-12 | Correctness over compression | Never omit a relevant edge case, security constraint, test failure, or uncertainty merely to save tokens. |

## Suggested task checkpoint

```text
TASK: <ID and objective>
ACCEPTANCE: <key criteria>
CONSTRAINTS: <important boundaries>
STACK: <detected technologies and versions>
DECISIONS: <decisions and reasons>
PROGRESS: <done / in progress / blocked>
FILES: <relevant changed or inspected paths>
VERIFICATION: <commands and actual outcomes>
DELEGATION: <agent, scope, status, findings>
OPEN ISSUES: <risks and unresolved questions>
NEXT ACTION: <one concrete next step>
```
