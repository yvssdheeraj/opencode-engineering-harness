---
name: technology-skill-name
description: State the exact language/framework/tool and task types that should trigger this skill. Be specific enough for the agent to select it only when relevant.
---

# Technology Skill: <Technology>

## Supported scope

- Technology and version range:
- Runtime/build tooling:
- Framework modules covered:
- Out-of-scope technologies:

## When to load

Describe concrete task triggers. Do not say "use for all development".

## Before implementation

- Inspect the repository's actual version and configuration.
- Read project conventions and existing examples.
- Check official documentation for version-sensitive APIs.
- Avoid assuming a new version or replacing established libraries.

## Implementation standards

- List concrete, testable patterns for this technology.
- Explain relevant project-architecture integration points.
- Identify common failure modes and anti-patterns.
- Include security, performance, reliability, and compatibility considerations relevant to the technology.

## Testing and verification

- Name the framework's relevant unit/integration/contract/E2E options.
- List project commands only after verifying actual package scripts/build tasks.
- Explain how to test failures and edge cases.

## Completion checklist

- [ ] Implementation follows the actual installed version.
- [ ] Tests and required checks executed.
- [ ] Documentation/configuration updated where needed.
- [ ] No unapproved dependency or breaking change.

## References

Prefer official documentation and project-approved sources. Record the documentation version/date when the guidance is version-sensitive.
