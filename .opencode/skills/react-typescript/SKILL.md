---
name: react-typescript
description: Use when modifying a frontend that actually uses React and TypeScript, including components, hooks, routing, state, forms, and client-side tests.
---

# React and TypeScript Skill — Starter Guidance

- Detect React, TypeScript, router, build tool, state library, and testing-library versions from manifests.
- Follow the existing component, hook, state ownership, data-fetching, and styling conventions.
- Keep components focused; extract shared abstractions only when behavior is genuinely shared.
- Prefer strict types and discriminated unions for meaningful state; avoid `any` and unsafe casts.
- Handle loading, success, empty, error, unauthorized, and retry states where relevant.
- Use semantic HTML, labels, keyboard interactions, visible focus, and accessible names.
- Do not put secrets or authoritative authorization decisions in the client.
- Test behavior with the repository's existing tools (for example component tests and browser-level tests where present).
- Verify package scripts before running lint, typecheck, test, or build.
