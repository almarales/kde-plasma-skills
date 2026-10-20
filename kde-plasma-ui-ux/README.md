# KDE Plasma UI/UX Skill

A community engineering skill for designing, implementing, and reviewing KDE Plasma interfaces with an AI agent.

## Purpose and audience

This skill gives an AI agent a KDE-specific runtime contract: when to load, which constraints are non-negotiable, where to route a question, and what a reviewable result must contain. It is written for KDE contributors, Plasma widget and KCM authors, designers working with QML/Kirigami, maintainers reviewing visual and interaction changes, and AI coding agents acting on their behalf.

It is not a style manifesto and not a replacement for the KDE Human Interface Guidelines. The HIG is the primary design reference; this skill turns that material into agent-executable rules, gates, and checks.

## Scope

In scope:

- Plasma shell surfaces: panels, widgets, launchers, popups, system tray, desktop interactions.
- System Settings modules (KCMs) and configuration experiences.
- Breeze visual conventions, theming, and icon usage.
- Qt Widgets, Qt Quick, QML, Kirigami, and Plasma-specific components.
- Accessibility, keyboard navigation, focus, input methods, display scaling, localization, and RTL.
- Design review, UI implementation, refactoring, and visual regression analysis.

Non-goals:

- Generic web dashboards, SaaS products, mobile applications, or marketing sites.
- Enforcing one aesthetic, one component, or one toolkit across KDE.
- Replacing repository requirements, maintainer judgment, or verified platform behavior.
- Duplicating the engineering rule catalog in `kde-plasma-best-practices`.

This skill is community material. It is not affiliated with or endorsed by KDE.

## Structure

| Path | Purpose |
|---|---|
| `SKILL.md` | Activation contract, hard rules, decision gates, workflow, output contract |
| `references/design-principles.md` | Principles, evidence hierarchy, decision classes, deviation protocol |
| `references/visual-consistency.md` | Color, typography, icons, metrics, states, contrast, schemes |
| `references/plasma-components.md` | Component selection, plasmoids, panels, popups, tray, KCMs, Qt Widgets |
| `references/official-applet-anatomy.md` | Observed anatomy of official Plasma applets: surfaces, typography ladder, numeric rows, states, motion, popup envelope, tray rules, and testable gates |
| `references/configurable-views.md` | User-selectable renderings: view ownership, capability negotiation, per-view configuration, editable layouts, shareable presets |
| `references/qt-qml-kirigami.md` | QML/Kirigami implementation mechanics |
| `references/interaction-patterns.md` | Keyboard, focus, menus, drag/drop, feedback, RTL, motion |
| `references/accessibility.md` | Accessibility requirements and verification |
| `references/plasma-future-proposals.md` | Evaluating speculative or future design directions |
| `references/review-checklist.md` | Pre-delivery review checklist |
| `assets/design-proposal.md` | Template for a design proposal |
| `assets/ui-review.md` | Template for a UI review |

## Install and activation

Install the whole bundle from its root. The installer replaces any previous copy, so an update never mixes two versions of a skill:

```bash
/path/to/kde-plasma-skills/install.sh           # user scope
/path/to/kde-plasma-skills/install.sh --scope project
```

To install only this skill, copy its directory into the root your agent scans (`~/.agents/skills` for Gentle AI agents), **replacing** the destination rather than merging into it, then refresh the registry:

```bash
mkdir -p ~/.agents/skills
rm -rf ~/.agents/skills/kde-plasma-ui-ux
cp -r /path/to/kde-plasma-ui-ux ~/.agents/skills/
gentle-ai skill-registry refresh
```

- Include the whole directory, including `references/` and `assets/`, because `SKILL.md` links to those files locally.
- Install into one root only. The registry keeps one entry per skill name, so a copy in two roots means one of them silently shadows the other; `install.sh check` reports it.
- If your agent scans a different skills root, copy the directory there instead and refresh the registry.
- Start a new agent session if the current one caches skill discovery at startup.
- The skill activates on Plasma widget, KCM, panel, tray, Breeze, Kirigami, QML UI, and KDE design-review tasks. It does not need a slash command.

## Relationship to `kde-plasma-best-practices`

The two skills are independent and complementary:

- `kde-plasma-ui-ux` sets interface goals, design constraints, interaction behavior, and accessibility expectations.
- `kde-plasma-best-practices` sets implementation quality: responsiveness, bindings, object lifetime, threading, architecture, build integration, and testing.
- Neither skill automatically overrides repository requirements or verified platform constraints.
- A performance change must not silently break accessibility or expected behavior.
- Visual consistency must not justify a technically incorrect implementation.
- When the two pull in different directions, document the alternatives, evidence, risks, and required validation.

Do not copy engineering rules into this skill. Link to `../kde-plasma-best-practices/SKILL.md` and its `../kde-plasma-best-practices/references/rules/` instead.

The design rules that are mechanically checkable are automated by `../kde-plasma-best-practices/scripts/lint_qml.py`: literal colors, custom material, numeric spacing, literal font sizes and literal durations (gates 1, 2, 4, 6 and 8 of `references/official-applet-anatomy.md`). The checker cites the rule each finding enforces, so a finding is always traceable to a rule and never to a tool's opinion.

## Version assumptions

The guidance was verified on 2026-10-20 against a local baseline of:

- KDE Plasma 6.8.0
- Qt 6.11.1
- KDE Frameworks 6
- `qmllint6` (Qt 6.11.1) available for QML checks; the unversioned `qmllint` on this machine is a Qt 5 wrapper

These are assumptions, not universal requirements. KDE documentation is a living target: before applying version-sensitive guidance, confirm the import, property, or behavior against the target branch and `https://api.kde.org/`. The skill labels claims `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, or `[Unknown]` so readers can see how strongly each statement is supported.

## Validation and maintenance

Structural validation for this skill:

1. Parse the YAML frontmatter; confirm `name`, quoted single-line `description`, `license`, `metadata.author`, and `metadata.version`.
2. Confirm the description is at most 250 characters and puts trigger words first.
3. Confirm section order: Activation Contract, Hard Rules, Decision Gates, Execution Steps, Output Contract, References.
4. Estimate body tokens; target 180–450, recommended maximum 700, hard maximum 1000.
5. Resolve every relative link in `SKILL.md`, the README, and each reference.
6. Confirm no file is empty and every reference has `## Scope`, numbered rules, `## Sources` with access dates, and version notes where applicable.
7. Run the `skill-improver` audit before publishing changes.

Maintenance:

- Re-verify all cited URLs when the HIG, Kirigami, Plasma, or Qt documentation changes, and at least once per Plasma major release.
- Re-check API names and imports against `api.kde.org` for the supported versions.
- Keep `SKILL.md` short. Move detail into references rather than growing the contract.
- Remove guidance that a newer release has made obsolete instead of accumulating contradictions.

## Proposing corrections

Open an issue or pull request in the repository that distributes this skill. Include:

- The exact file and section.
- The current text and the proposed text.
- The evidence: official URL, repository path with branch, observed output, or test result.
- The affected versions and platforms.
- Whether the change is a correction, a new recommendation, or an experiment.

Corrections that add a rule should also state its scope and how a reviewer can check it. Unsourced aesthetic preferences will be treated as proposals, not corrections.

## Reporting outdated or version-specific guidance

Report outdated guidance with the same evidence standard:

- Which Plasma, Qt, or KF version the guidance fails on.
- What the current documentation or implementation says instead, with a URL or repository reference.
- Whether the old guidance was wrong when written or became wrong after a release.
- A minimal reproduction for behavioral claims.

Do not silently edit version-specific guidance to cover a new release. State the supported versions explicitly and let the maintainers decide whether to widen, split, or replace the rule.

## License

The skill text is licensed under Apache-2.0. See `LICENSE` in the skill directory.

Apache-2.0 is used for portability with the agent-skill ecosystem. Application code in this repository remains under its own license (GPL-3.0 unless stated otherwise); the skill license does not relicense that code.

KDE, Plasma, Kirigami, and Breeze are trademarks or project names of their respective owners. This skill is an independent community resource and is not affiliated with or endorsed by KDE.
