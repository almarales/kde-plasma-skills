---
name: kde-plasma-ui-ux
description: "Trigger: Plasma widget, KCM, panel, system tray, Breeze icons, Kirigami, QML UI, KDE design review. Design and review KDE Plasma interfaces."
license: Apache-2.0
metadata:
  author: "Javier Reinaldo Almarales"
  version: "1.0"
---

## Activation Contract

Load for Plasma shell, panels, widgets, system tray, System Settings KCMs, Breeze icons, Qt/QML/Kirigami/Plasma components, and KDE keyboard, theming, scaling, localization, design review, or refactoring work.

Do not load for generic web, SaaS, mobile, or marketing products unless explicitly requested.

## Hard Rules

1. **Native before novel.** Reuse established KDE patterns and platform components before custom UI.
2. **Simple by default, powerful when needed.** Keep the common workflow visible; make power optional and discoverable.
3. **Consistency with purpose.** Match KDE behavior, focus order, shortcuts, defaults, and state changes, not only pixels.
4. **Accessibility is foundational:** keyboard-only use, visible focus, screen-reader semantics, contrast, scaling, color-independent status, reduced motion, and localization.
5. **Adaptability and user control.** Respect color schemes, accent colors, scaling, input methods, and localization.
6. **Incremental, evidence-based evolution.** Prefer small validated changes to speculative redesigns.
7. **Explain deviations.** State pattern, reason, evidence, risk, and validation.
8. **Material follows the platform; identity lives in composition.** Never paint your own chrome; glass, glow, gradient, and custom shadows are not a style choice. See `references/official-applet-anatomy.md`.

- Qt Quick/Plasma surfaces: never hardcode colors, fonts, or pixel metrics; use `Kirigami.Theme` and `Kirigami.Units` roles verified in the target KF version.
- Qt Widgets surfaces: use the active `QPalette`, widget style, and KDE Frameworks integration; do not restyle standard dialogs to imitate Kirigami.
- Never invent KDE APIs, components, tokens, benchmarks, or roadmap decisions; never claim KDE endorsement.
- Label every substantive claim `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, or `[Unknown]`.

Evidence order, decision classes, and prohibited reasoning: `references/design-principles.md`. Never present Plasma 7 concepts as approved.

Target baseline: Plasma 6.8.0, Qt 6.11.1, KF6 (local, 2026-10-20). Verify against the target branch/version.

## Decision Gates

| Need | Read |
|---|---|
| Principles, evidence hierarchy, deviations | `references/design-principles.md` |
| Color, typography, icons, metrics, states, contrast | `references/visual-consistency.md` |
| Component order, plasmoid/KCM/tray/dialog structure | `references/plasma-components.md` |
| What official applets actually do, with metrics and source citations | `references/official-applet-anatomy.md` |
| Keyboard, focus, menus, drag/drop, feedback, RTL, accessibility | `references/interaction-patterns.md`, `references/accessibility.md` |
| QML/Kirigami implementation mechanics | `references/qt-qml-kirigami.md` |
| Future or Plasma 7 proposals | `references/plasma-future-proposals.md` |
| Pre-delivery review | `references/review-checklist.md` |
| Performance, lifetime, architecture | `../kde-plasma-best-practices/SKILL.md` |

## Execution Steps

1. Establish context: product, target versions, repository conventions, users, constraints.
2. Inspect before designing: components, theme usage, widget/KCM structure, tests, screenshots.
3. Classify each decision as Established, Proposed improvement, Experimental future, or Unknown.
4. Design or implement: choose components in order, use theme roles and units, define states, keyboard paths, and accessibility semantics.
5. Validate with repository build/tests/lint (`qmllint6` for Qt 6 QML); check contrast, scaling, RTL, keyboard-only use, and screen-reader output.
6. Explain deviations: pattern, reason, evidence, risk, validation.
7. Produce a reviewable result: minimal diff or proposal, open questions, next action.

## Output Contract

Return: outcome; an evidence label per claim; files changed; component and theme decisions; validation commands with observed results; deviations and rationale; `[Unknown]` items; next action. Never claim unrun validation.

## References

- `references/`: design-principles, visual-consistency, plasma-components, official-applet-anatomy, qt-qml-kirigami, interaction-patterns, accessibility, plasma-future-proposals, review-checklist
- `assets/design-proposal.md`, `assets/ui-review.md`
- `../kde-plasma-best-practices/SKILL.md` — engineering rules; do not duplicate them here.
