# Rule Loading Strategy

OpenCode combines repository instructions (`AGENTS.md`) and configured instruction files. This blueprint uses always-on rules for shared agent behavior and conditional detailed rule files for engineering domains.

## Always loaded for every agent

`opencode.jsonc` auto-loads the seven shared common rule files (communication, context-management, delegation, tool-use, autonomy-and-safety, collaboration, evidence-and-reporting). These govern how all agents communicate, manage context, delegate, use tools, make decisions, collaborate, and report evidence. See `opencode.jsonc` for the authoritative list.

## Loaded conditionally

Root `AGENTS.md` contains a routing matrix. The agent identifies affected domains and reads the corresponding detailed `.opencode/rules/engineering/*.md` files and workflow files before planning, implementation, or review.

Conditional loading is an explicit agent procedure. It is not an automatic rule engine that evaluates file paths. The agent must use its read tool to load each referenced document that applies.

## Selecting rules and skills

Root `AGENTS.md` contains the routing table. The agent identifies affected domains and reads the corresponding detailed `.opencode/rules/engineering/*.md` files and workflow files before planning, implementation, or review.

Conditional loading is an explicit agent procedure. It is not an automatic rule engine. The agent must use its read tool to load each referenced document that applies. Record the selected rules, skills, quality gates, and reviewers in a short `Selected rules & skills` note so omitted domains are visible during execution and review.

## Audit the full rule set

`.opencode/rules/RULE-CATALOG.md` is the authoritative index of stable rule IDs. It maps every numbered requirement to its file. The expanded catalogue includes:

- Architecture ARCH-01–ARCH-15
- Coding CODE-01–CODE-15
- Testing TEST-01–TEST-18
- Security SEC-01–SEC-17
- Performance PERF-01–PERF-12
- Reliability REL-01–REL-12
- APIs API-01–API-14
- Data DATA-01–DATA-13
- Observability OBS-01–OBS-10
- Frontend FE-01–FE-18
- UX/accessibility UX-01–UX-10
- Infrastructure INFRA-01–INFRA-20
- CI/CD CICD-01–CICD-20
- Documentation DOC-01–DOC-10
- Git/review GIT-01–GIT-10
- Cross-cutting practices XENG-01–XENG-15
- Common operating rules COM, CTX, DEL, TOOL, AUTO, COL, and EVID
- Quality gates QG-01–QG-17

The rule IDs are a traceability and review aid, not a requirement to apply everything to every task. Load the union of relevant files based on affected components and risk. Do not invent work to satisfy an irrelevant requirement.

## Skills

Skills under `.opencode/skills/<name>/SKILL.md` are discovered by OpenCode and loaded through its skill tool when relevant. Their frontmatter descriptions are trigger hints. Skill selection is model-guided and should be based on repository evidence, task scope, and actual versions; it is not a deterministic technology detector.

## Enforcement hierarchy

- Common rules define shared agent conduct.
- Engineering rules define reusable stack-neutral practices.
- Project principles define concise, durable, project-specific principles (if present).
- Feature requirements define required behavior and acceptance criteria.
- Technology skills define language/framework/platform implementation guidance.
- Agent prompt defines individual role and scope.
- Tool permissions define what an agent can actually do.
- CI, tests, linters, scanners, policy-as-code, and protected deployment workflows provide executable enforcement.

Rules and skills do not override explicit user requirements, applicable security constraints, or permission boundaries. When instructions conflict, surface the conflict and resolve it rather than silently blending incompatible requirements.
