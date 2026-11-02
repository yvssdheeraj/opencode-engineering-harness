# Engineering Rule — Accessibility, UX, and Product Quality (UX)

Accessibility and user experience are product quality concerns, not visual polish to defer until the end. Apply the following to user-facing behavior as relevant.

| ID | Requirement | Agent must enforce |
|---|---|---|
| UX-01 | Requirement traceability | Ensure user-visible behavior maps to an explicit requirement, acceptance criterion, or approved product decision. |
| UX-02 | Consistent interaction | Follow established navigation, controls, terminology, confirmation, and interaction patterns. |
| UX-03 | Inclusive accessibility | Consider users with different abilities, assistive technologies, reduced motion, contrast needs, and alternative input methods. |
| UX-04 | Action feedback | Provide timely, understandable feedback for actions, validation, errors, progress, and completion. |
| UX-05 | Data validation | Prevent invalid or inconsistent input using clear constraints and actionable messages; validate again at trusted boundaries. |
| UX-06 | Destructive confirmation | Confirm destructive, irreversible, or high-impact actions when appropriate, and explain the consequence. Avoid needless confirmation for routine reversible actions. |
| UX-07 | Data preservation | Preserve user-entered data through recoverable failures where practical; prevent accidental data loss. |
| UX-08 | Localization correctness | Respect locale-specific language, date/time/time-zone, number, currency, unit, pluralization, and text-direction conventions where applicable. |
| UX-09 | Privacy-aware experience | Avoid collecting, showing, or retaining more user data than the feature needs. Explain sensitive data use where product requirements require it. |
| UX-10 | Product consistency | Prefer an existing suitable design pattern and component over introducing a competing interaction model. |

## Accessibility baseline

- Use WCAG 2.2 AA as a default target for applicable web content unless the project sets a stricter or different explicit standard.
- Validate semantic structure, accessible names, keyboard access, visible focus, contrast, zoom/reflow, error identification, and relevant dynamic announcements.
- Do not claim conformance based only on automated scans; manual keyboard and assistive-technology checks may be necessary.
