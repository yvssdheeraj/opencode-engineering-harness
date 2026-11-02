# Engineering Rule — Frontend and Client Application Engineering (FE)

Apply these practices to web, mobile, and desktop user interfaces as relevant to the platform.

| ID | Requirement | Agent must enforce |
|---|---|---|
| FE-01 | Component architecture | Build UI components with clear, cohesive responsibilities and predictable boundaries. |
| FE-02 | Component reuse | Reuse shared components when behavior and semantics genuinely match; avoid premature generic components. |
| FE-03 | Design system consistency | Follow established design tokens, component library, typography, spacing, and interaction patterns. |
| FE-04 | State management | Keep state ownership, lifecycle, synchronization, and side effects predictable; avoid duplicating derived state unnecessarily. |
| FE-05 | UI/business separation | Keep complex domain behavior out of presentation components; use appropriate services, hooks, view models, or domain layers. |
| FE-06 | Responsive behavior | Support required screen sizes, orientations, and input modes. Do not assume desktop-only layouts unless specified. |
| FE-07 | Accessibility | Implement semantic, keyboard-operable, assistive-technology-compatible interfaces and follow the project's WCAG target. |
| FE-08 | Semantic markup | Use semantic elements and correctly named controls rather than clickable generic containers when platform semantics exist. |
| FE-09 | Keyboard access | Ensure navigation, focus order, shortcuts, dialogs, menus, and forms work without a pointer. |
| FE-10 | Form validation | Provide useful client-side feedback while enforcing authoritative validation at the server/trusted boundary. |
| FE-11 | Complete UI states | Handle loading, success, empty, validation, error, unauthorized, offline, retry, and long-running states where applicable. |
| FE-12 | Rendering and asset performance | Avoid unnecessary rerenders, oversized bundles, unoptimized images, blocking resources, and expensive work on the main thread. |
| FE-13 | Browser/device support | Validate the browsers, devices, OS versions, and platform capabilities the product claims to support. |
| FE-14 | Client-side security | Prevent XSS and unsafe rendering; never treat client-side checks as authoritative authorization. Protect tokens and sensitive client state. |
| FE-15 | UI testing | Test meaningful components, user interactions, state transitions, accessibility behavior, and critical end-to-end journeys. |
| FE-16 | Visual consistency | Follow established spacing, typography, color, layout, and interaction conventions. Avoid one-off styles without reason. |
| FE-17 | Internationalization readiness | Localize user-facing strings and account for locale-sensitive dates, numbers, currencies, pluralization, and text direction when required. |
| FE-18 | Maintainable styling | Scope styles appropriately; avoid uncontrolled global selectors, brittle overrides, and unnecessary style duplication. |

## UI state checklist

For each changed interaction, consider initial/loading, success, empty, invalid input, server failure, unauthorized, network interruption, retry/recovery, and destructive confirmation states. Implement only those relevant to the actual feature.
