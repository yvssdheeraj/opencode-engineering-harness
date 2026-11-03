---
name: react-typescript
description: Use when modifying a frontend that actually uses React and TypeScript, including components, hooks, routing, state, forms, and client-side tests.
---

# React and TypeScript Skill — Starter Guidance

## Supported scope

- Technology and version range: React 18/19+ with TypeScript 5+ (inspect `package.json` and `tsconfig.json` for exact versions, strictness flags, and bundler/framework setup).
- Last reviewed: 2026-11
- Runtime/build tooling: Vite, Next.js, Remix/React Router, or custom Webpack/Rspack toolchains via `npm`, `pnpm`, `yarn`, or `bun`.
- Framework modules covered: components, hooks, client/server state management, forms, routing, accessibility semantics, and client/component testing.
- Out-of-scope / unsupported versions: Legacy class-component-only React (< 16.8), non-React frontend frameworks (Vue, Angular, Svelte), and backend-only Node.js services.

## When to load

Load when modifying a frontend application or UI library that uses React and TypeScript, including components, hooks, routing, state, forms, styling, and client-side tests. Do not load for backend-only or infrastructure tasks.

## Before implementation

- Detect React, TypeScript, router, bundler, state/data-fetching library (TanStack Query, Redux Toolkit, Zustand, SWR), form library, styling system, and test runner from `package.json` and lockfiles.
- Inspect existing component organization, design-system primitives, error boundaries, and accessibility conventions before creating new components.
- Check `package.json` scripts (`typecheck`, `lint`, `test`, `build`) before running verification commands.

## Implementation standards

- Keep components focused on a clear responsibility; compute derived values during render rather than synchronizing duplicate state in `useEffect`.
- Model asynchronous and UI flows with strict TypeScript types and discriminated unions; avoid `any`, unsafe `as` casts, and non-null assertions (`!`) on untrusted data.
- Handle complete user-facing states where relevant: initial loading, empty data, validation errors, server/network failure, unauthorized state, retry, and in-flight submission disabling.
- Use semantic HTML elements (`<button>`, `<form>`, `<label>`, `<dialog>`, `<nav>`, landmarks), explicit accessible names, keyboard navigation, and visible focus management.
- Prevent XSS by avoiding `dangerouslySetInnerHTML` with unsanitized content; never embed secrets in client bundles or treat client-side checks as authoritative authorization.

## Testing and verification

- Test user-visible behavior and accessibility roles (`getByRole`, `getByLabelText`, `userEvent`) using the repository's configured runner (Vitest, Jest, React Testing Library, Playwright) rather than asserting internal hook or state implementation details.
- Verify keyboard submission, validation error messages, loading/error states, and TypeScript compilation (`tsc --noEmit` or project `typecheck` script).

## Completion checklist

- [ ] Implementation follows the installed React/TypeScript versions and existing project conventions.
- [ ] Typecheck, lint, and component/E2E tests executed and passing.
- [ ] Semantic markup, keyboard interaction, and UI error/loading states verified.
- [ ] No unapproved UI/state dependencies or client-side secret exposures introduced.

## References

- React official documentation: https://react.dev/reference/react
- TypeScript handbook: https://www.typescriptlang.org/docs/
- WAI-ARIA Authoring Practices Guide (APG): https://www.w3.org/WAI/ARIA/apg/
