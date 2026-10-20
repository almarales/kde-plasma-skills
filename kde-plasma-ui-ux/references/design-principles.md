# Design Principles and Evidence

## Scope

Use this reference to decide what KDE Plasma interface guidance applies, how strongly it applies, and how to justify a departure. It covers principles, the evidence hierarchy, decision classification, and the deviation protocol. It does not cover component APIs (`plasma-components.md`), visual tokens (`visual-consistency.md`), or accessibility verification (`accessibility.md`).

## Principles

### 1. Native before novel

- [Official] KDE recommends QtQuick with Kirigami for new applications and documents QtWidgets as the older toolkit for traditional desktop applications. KDE apps are expected to follow common interface patterns and platform conventions.
- [Recommendation] Before designing a custom control, name the established KDE/Qt component or pattern you rejected and why. If you cannot name one, you have not finished inspecting.
- [Recommendation] Custom chrome is a last resort. Custom content visualization is normal; custom window frames, focus rings, and menu behavior are not.

### 2. Simple by default, powerful when needed

- [Official] KDE's central principle is "Simple by default, powerful when needed". The HIG asks for the 80% common case to be simple and obvious, with guidance appropriate for non-experts, while still allowing experts to grow into powerful features.
- [Official] Primary actions and workflows must be visible by default. Keyboard shortcuts, context menus, hover controls, and gestures are accelerators, never the only path to important functionality.
- [Official] Settings should support diverse but valid workflows; a setting that merely enables or disables a feature is described by the HIG as a warning sign of sloppy design.
- [Recommendation] Apply this test: a first-time user completes the primary task without configuration; an expert can reach depth without the default UI becoming noisy.

### 3. Consistency with purpose

- [Official] The HIG treats design as targeted decisions and trade-offs toward a product's goals, not a universal checklist.
- [Recommendation] Review behavior before appearance: default focus, tab order, shortcut assignment, destructive-action confirmation, apply/cancel semantics, and state transitions. Two screens can look identical and still be inconsistent.
- [Recommendation] Match the surrounding product and platform. Importing a pattern from an unrelated ecosystem is a deviation that needs evidence, not a neutral choice.

### 4. Accessibility is foundational

- [Official] The HIG instructs authors to test keyboard-only use, pointing-device-only use, touch, alternate color schemes, increased text size, muted audio, a screen reader, and disabled animations.
- [Recommendation] Treat these as design inputs from the first draft. Retrofitting focus order, accessible names, and scalable layout after visual approval is usually a redesign, not a polish pass.
- [Recommendation] Pair this principle with `accessibility.md` for concrete requirements and verification steps.

### 5. Adaptability and user control

- [Official] The HIG asks apps to defer to platform visual styling and theming tools so system-level preferences apply consistently, and to apply saved settings immediately without requiring a restart.
- [Official] For touchpads and touchscreens, the HIG says to implement only two-finger gestures in apps.
- [Recommendation] Assume the user may change color scheme, accent color, icon theme, font, display scale, language, or input method. Any of these changing must not break layout or meaning.

### 6. Incremental, evidence-based evolution

- [Recommendation] Prefer the smallest change that resolves the observed problem. Preserve working conventions unless evidence shows they cause a concrete failure.
- [Recommendation] Base claims on inspected code, screenshots, tests, or documented behavior. Do not assert performance, usability, or accessibility gains without measurement; route performance questions to `../../kde-plasma-best-practices/SKILL.md`.
- [Recommendation] Separate a bug fix, a consistency improvement, and a redesign. Mixing them makes review and rollback harder.

### 7. Explain deviations

Every intentional departure from an established KDE pattern should record:

| Field | Content |
|---|---|
| Established pattern | What KDE/Qt normally does, with a source or repository example |
| Deviation | The exact behavior being changed |
| Reason | The user or technical problem it solves |
| Evidence | Observed behavior, test, measurement, or documented constraint |
| Risk | What becomes less predictable, accessible, or consistent |
| Validation | How the result was checked, and by whom |
| Revisit condition | Version, platform, or evidence that would justify reversing it |

- [Recommendation] A deviation without a validation entry is an unverified preference, not an engineering decision.

## Evidence hierarchy

When sources disagree, use the earlier item. Record the conflict instead of silently picking one.

1. **Repository implementation, APIs, and tests** — [Observed] The target branch is the strongest evidence of what the product actually does and what constraints apply.
2. **Current KDE Human Interface Guidelines** — [Official] KDE's design guidance for apps and Plasma integration.
3. **Current Plasma and Kirigami documentation** — [Official] Component behavior, imports, and documented conventions for the target release.
4. **Maintained KDE patterns** — [Observed] Repeated, reviewed practice in maintained KDE repositories. Useful where documentation is silent; weaker than explicit documentation.
5. **Qt documentation** — [Official] Authoritative for Qt APIs and behavior, not for KDE design policy.
6. **Community proposals and design discussions** — [Experimental] Input to evaluate, not an approved decision.
7. **General design knowledge** — [Recommendation] Transferable principles that still require KDE-specific validation.

Rules for applying the hierarchy:

- [Recommendation] A repository constraint outranks generic guidance. Document the constraint and the resulting trade-off.
- [Recommendation] Documentation for the installed target version outranks documentation for another major version.
- [Official] API reference pages at `https://api.kde.org/` are the place to confirm that a class, property, or import exists. Do not infer an API from a tutorial for a different release.
- [Observed] The KDE Visual Design Group wiki describes the group and its work; it is community material, not a normative standards body.

## Decision classification

| Class | Meaning | How to present it |
|---|---|---|
| Established | Documented in the HIG/docs or consistently implemented in maintained KDE code | State as the expected pattern; cite source or example |
| Proposed improvement | Evidence-based change not adopted by KDE | Label `[Recommendation]`; include trade-offs and validation |
| Experimental future | Unmerged, unverified, or speculative direction | Label `[Experimental]` or `[Unknown]`; never call it approved |
| Unknown | No reliable evidence | Say so; propose how to find out |

- [Official] Never present a Plasma 7 concept as an approved KDE decision. There is no basis in the consulted sources for treating any future design as settled.
- [Recommendation] When a task asks for a future-facing proposal, read `plasma-future-proposals.md` and keep the classification visible in the deliverable.

## Prohibited reasoning

- [Recommendation] "KDE does X" without a source, version, or observed example.
- [Recommendation] Inventing tokens, component names, properties, or benchmarks to make guidance feel concrete.
- [Recommendation] Treating the HIG as exhaustive; it explicitly notes topics it does not cover.
- [Recommendation] Using visual similarity as proof of behavioral consistency.
- [Recommendation] Presenting a personal aesthetic preference as an accessibility or platform requirement.

## Review questions

1. Which established KDE pattern or component does this reuse?
2. Which evidence class supports each non-obvious claim?
3. Does the default path work without configuration?
4. Is every primary action reachable without hover, gesture, or memorized shortcut?
5. What happens under a different color scheme, scale factor, language, and input method?
6. Is the deviation recorded with risk and validation?
7. Is any speculative direction labeled as such?
8. Would a reviewer be able to reproduce the validation?

## Sources

- KDE Human Interface Guidelines — https://develop.kde.org/hig/ — Accessed: 2026-10-20
- What makes a KDE app a KDE app? — https://develop.kde.org/hig/kde_app_design/ — Accessed: 2026-10-20
- Simple by default — https://develop.kde.org/hig/simple_by_default/ — Accessed: 2026-10-20
- Powerful when needed — https://develop.kde.org/hig/powerful_when_needed/ — Accessed: 2026-10-20
- Accessibility and inclusiveness — https://develop.kde.org/hig/accessibility/ — Accessed: 2026-10-20
- KDE Plasma Developer Guide — https://community.kde.org/Plasma/DeveloperGuide — Accessed: 2026-10-20
- KDE Visual Design Group — https://community.kde.org/KDE_Visual_Design_Group — Accessed: 2026-10-20
- KDE API reference — https://api.kde.org/ — Accessed: 2026-10-20

## Version notes

Verified against KDE HIG pages as published on 2026-10-20, with a local baseline of Plasma 6.8.0, Qt 6.11.1, and KF6. The HIG is a living document and KDE documentation can change without a version bump. Re-check principle wording and links when targeting a different Plasma major release or after a documentation migration.
