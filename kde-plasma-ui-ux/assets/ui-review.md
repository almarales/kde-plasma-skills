<!--
INSTRUCTIONS
Replace every <angle-bracketed> placeholder before sharing this review.
A review with no inspected evidence is inconclusive, not a pass.
Use the status vocabulary and severity definitions from references/review-checklist.md.
Delete this comment block before publishing.
-->

# UI review: <target>

## Scope

Use this template to record one UI review of a Plasma surface change: a widget, panel item, Kirigami screen, System Settings module, or Qt Widgets settings dialog. Record only what was inspected. A review without inspected evidence is `inconclusive`, never a pass. Do not use it as a general bug tracker or as a substitute for the engineering review of threading, lifetime, or performance.

## Target

| Field | Value |
| --- | --- |
| Component / screen | <name and repository-relative path> |
| Change under review | <merge request, commit, or diff range> |
| Branch / revision | `<branch>` at `<commit>` |
| Reviewer | <name or agent identifier> |
| Review date | `<YYYY-MM-DD>` |
| Checklist used | `references/review-checklist.md` |

## Versions

| Item | Value | How verified |
| --- | --- | --- |
| Plasma | `<version>` | `<command output>` |
| Qt | `<version>` | `<command output>` |
| KF6 modules | `<version>` | `<command output>` |
| Build type | `<release / debug>` | `<command or config>` |

## Environment

| Dimension | Value |
| --- | --- |
| Color scheme | <Breeze Light / Breeze Dark / other> |
| Scale factor | <100% / 200% / other> |
| Locale and layout direction | <locale, LTR/RTL> |
| Font size | <default / 14 pt / other> |
| Animations | <enabled / disabled> |
| Screen setup | <resolution, multi-screen arrangement> |
| Compositor | <Plasma/KWin state, if relevant> |

## Evidence captured

| Evidence | Path or URL | Captured in |
| --- | --- | --- |
| Baseline screenshot | <path> | <environment row> |
| Candidate screenshot | <path> | <environment row> |
| Interaction recording | <path> | <environment row> |
| Command output (`qmllint6` for Qt 6 QML, `kcmshell6`, version) | <path or inline block> | <environment row> |

## Findings

Severity: `Blocker | Major | Minor | Nit`. Status: `Fail | Unverified` (a finding is never a pass).

| ID | Status | Severity | Location (`file:line`) | Convention | Observed | Expected | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | `<Fail \| Unverified>` | <severity> | `<path:line>` | <rule or reference> | <what happens> | <what should happen> | <screenshot/command> |
| F2 | `<Fail \| Unverified>` | <severity> | `<path:line>` | <rule or reference> | <what happens> | <what should happen> | <screenshot/command> |

## Checks run

| Checklist ID | Status | Evidence |
| --- | --- | --- |
| A1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| A2 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| B1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| C2 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| D1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| E1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| F1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| G1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |

Add or remove rows to match the checklist groups actually reviewed (A through H).

## Checks not run

| Checklist ID or check | Reason | What evidence would close it |
| --- | --- | --- |
| <ID> | <missing environment, unavailable device, out of scope> | <specific evidence> |

## Deviation justification

| Deviation | Established pattern | Why the pattern is insufficient | Alternative considered | Accessibility impact |
| --- | --- | --- | --- | --- |
| <deviation> | <HIG page or component> | <evidence, not preference> | <alternative and cost> | <impact or "none verified"> |

Write `None` when the change does not deviate from an established pattern.

## Verdict

| Field | Value |
| --- | --- |
| Verdict | `<pass \| fail \| inconclusive>` |
| Open blockers | <count and IDs, or `none`> |
| Open major findings | <count and IDs, or `none`> |
| Unverified items | <count and IDs, or `none`> |
| Accepted risks | <risk and owner, or `none`> |

Verdict rules:

- `pass`: every applicable checklist item is `Pass`, with evidence, and no blocker or major finding is open.
- `fail`: at least one blocker or major finding is open.
- `inconclusive`: any required evidence is missing, or any applicable item is `Unverified`. A review without inspected evidence is always `inconclusive`.

## Sources

- KDE Human Interface Guidelines: https://develop.kde.org/hig/ (Accessed: 2026-10-20)
- KDE HIG, Accessibility and inclusiveness: https://develop.kde.org/hig/accessibility/ (Accessed: 2026-10-20)
- Porting Plasmoids to KF6 (root elements, configuration UI): https://develop.kde.org/docs/plasma/widget/porting_kf6/ (Accessed: 2026-10-20)
- Settings module (KCM) development: https://develop.kde.org/docs/features/configuration/kcm/ (Accessed: 2026-10-20)

## Version notes

- Template version 1.0, 2026-10-20. Authority for statuses, severities, and verdicts is `references/review-checklist.md`; this template only records the outcome.
- The severity definitions and verdict rules are this skill's proposed conventions (`[Recommendation]`), not official KDE policy.
