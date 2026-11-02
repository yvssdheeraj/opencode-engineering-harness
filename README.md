# Agentic Development Blueprint — OpenCode + Spec Kit

A stack-neutral, rule-ID-based engineering agent starter framework. This contains the detailed requirements for common agent behavior, engineering quality, technology skill selection, Spec Kit orchestration, and verification.

## What is included

1. **Common agent operating contract** — communication, context/token efficiency, delegation, tool discipline, autonomy/safety, collaboration, and evidence/reporting.
2. **Detailed engineering rules** — architecture, clean code, testing/TDD/BDD, security, performance, reliability, APIs, data, observability, frontend, accessibility/UX, infrastructure, CI/CD, documentation, Git/review, and cross-cutting practices.
3. **Rule catalogue** — `.opencode/rules/RULE-CATALOG.md` maps stable IDs and ranges to their authoritative files.
4. **OpenCode agents** — primary developer plus read-only explorer and specialist reviewers.
5. **On-demand skills** — stack-neutral and sample technology skills that can be expanded for your real project.
6. **Spec Kit lifecycle mapping** — which agent to use at specify, plan, tasks, analyze, implement, converge, and final review stages.
7. **Adoption guides and templates** — installation, agent selection, skill authoring, rule loading, and constitution input.

## Important interpretation

The catalogue is comprehensive, but **not every rule applies to every task**. Agents must load and apply the rules relevant to the changed behavior, technology, and risk. For example, a documentation-only task does not need database integration tests; a Terraform change does not need React skills. Conditional practices such as Cucumber, mutation testing, chaos testing, DDD, and advanced deployment strategies should be used when they add value—not mandated mechanically.

Prompt instructions are guidance, not executable enforcement. Use CI checks, tests, linters, formatters, scanners, policy-as-code, and protected deployment workflows to enforce critical controls.

## Suggested installation steps

1. Check your installed versions: `opencode --version` and `specify version`.
2. Back up or commit current project state.
3. For a new project, initialize Spec Kit for OpenCode using the current official integration instructions. For an existing Spec Kit project, install the OpenCode integration using the supported command for your installed Spec Kit version.
4. Merge this template into the repository. Do not overwrite existing `AGENTS.md`, OpenCode configuration, or `.opencode/` files blindly.
5. Merge `opencode.jsonc` instructions and permissions into the existing OpenCode config; avoid multiple conflicting config files.
6. Preserve Spec Kit-generated `.opencode/commands/` and integration event/plugin configuration.
7. Tailor `.opencode/agents/` permissions and project instructions to your actual risk model.
8. Run `/speckit.constitution` and create a concise project-specific constitution; use `docs/templates/constitution-input.md` as an input checklist.
9. Populate repository-specific facts and actual commands in `AGENTS.md`.
10. Tailor technology skills to actual languages/frameworks/versions.
11. Pilot one low-risk feature with one primary developer and read-only reviewers.
12. Adjust rules, automated checks, and delegation based on observed failure modes.

## Directory guide

- `AGENTS.md`: repository entry point, conditional detailed-rule routing, Spec Kit integration guidance.
- `opencode.jsonc`: example configuration that loads common rules for every agent. Merge rather than blindly overwrite.
- `.opencode/agents/`: agent roles and permission boundaries.
- `.opencode/rules/common/`: always-on shared agent operating rules.
- `.opencode/rules/engineering/`: detailed standards loaded conditionally by task domain.
- `.opencode/rules/workflow/`: Spec Kit lifecycle, task execution, skill selection, and quality gates.
- `.opencode/rules/RULE-CATALOG.md`: audit index for all numbered requirements.
- `.opencode/skills/`: reusable instructions loaded on demand by technology/domain relevance.
- `docs/`: selection, installation, rule loading, and reusable templates.

## Design defaults

- One primary `developer` agent owns implementation and integration.
- `explorer` and reviewers are read-only by default.
- The developer delegates only bounded, useful, non-overlapping tasks.
- Keep subagent depth bounded; do not introduce recursive delegation until there is a demonstrated need.
- Spec Kit remains the owner of feature artifacts and lifecycle commands.
- Use skills for technology-specific practices and actual tools/CI for enforcement.
- Keep the Spec Kit constitution concise; detailed reusable standards remain in rule files.

## Official references

- OpenCode rules: https://opencode.ai/docs/rules/
- OpenCode agents: https://opencode.ai/docs/agents/
- OpenCode skills: https://opencode.ai/docs/skills/
- OpenCode configuration: https://opencode.ai/docs/config/
- Spec Kit: https://github.com/github/spec-kit
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- WCAG: https://www.w3.org/TR/WCAG22/
- Cucumber BDD: https://cucumber.io/docs/bdd/
- DORA capabilities: https://dora.dev/capabilities/
