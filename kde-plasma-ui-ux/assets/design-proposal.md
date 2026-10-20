<!--
INSTRUCTIONS
Replace every <angle-bracketed> placeholder before sharing this document.
A file that still contains <placeholders> is a draft, not a reviewable proposal.
Keep the status and decision-status values from the allowed lists; do not invent new ones.
Delete this comment block before publishing.
-->

# <Proposal title>

| Field | Value |
| --- | --- |
| Status | `<Established \| Proposed improvement \| Experimental future>` |
| Decision status | `<Draft \| Under discussion \| Prototype approved for evaluation \| Rejected \| Superseded \| Adopted>` |
| Owner | `<name or team>` |
| Date | `<YYYY-MM-DD>` |
| Target versions | `<Plasma version, Qt version, KF6 modules>` |
| Target components | `<repository paths or component names>` |
| Evidence label | `<Official / Observed / Recommendation / Experimental / Unknown>` |

> Experimental proposals only: keep this line visible on every artifact.
> **Experimental — not an official KDE decision** (as of `<YYYY-MM-DD>`, target `<version>`).

## Scope

Use this template for a design proposal that changes a Plasma surface: an established-pattern explanation, a scoped improvement, or an experimental future direction. Complete every section; write `none` where a section genuinely does not apply, and say why. Do not use it for an engineering-only refactor or for a change that is already merged.

## Problem

<One paragraph describing the user problem without naming the solution.>

## Users and tasks

| User group | Task | Frequency | Current pain |
| --- | --- | --- | --- |
| <group> | <task> | <daily / weekly / rarely> | <observed pain> |

## Current behavior and evidence

- Current behavior: <what happens today, in one or two sentences.>
- Implementation: `<path:line>` <what this code does.>
- Visual evidence: `<screenshot or recording path>` captured with <theme>, <scale>, <locale>.
- Documentation: <HIG or API URL and the relevant statement.>
- Measurement: <what was measured, with method and sample; write "none" if nothing was measured.>

## Affected workflows

| Workflow | Changes? | Must not regress | Input paths checked |
| --- | --- | --- | --- |
| <workflow> | `<yes / no>` | <behavior that must stay> | `<pointer / keyboard / screen reader / touch>` |

- Workflows not checked: <list, or "none".>
- Shared surfaces: <Plasma Mobile, touch-capable devices, or other consumers; or "none".>

## Constraints

- Platform: <Plasma/Qt/KF6 constraints, supported platforms.>
- Repository: <existing conventions, architecture, compatibility promises.>
- Accessibility: <requirements that cannot be traded away.>
- Localization: <locale, RTL, text expansion constraints.>
- Performance or resource: <budgets or known limits, with evidence.>
- Non-goals: <what this proposal deliberately does not change.>

## Options considered

| Option | Description | User benefit | Cost / risk | Reversible? |
| --- | --- | --- | --- | --- |
| A. Keep current behavior | <description> | <benefit> | <cost> | Yes |
| B. Smallest local fix | <description> | <benefit> | <cost> | <yes/no> |
| C. Proposed change | <description> | <benefit> | <cost> | <yes/no> |
| D. Do nothing and document the limitation | <description> | <benefit> | <cost> | Yes |

## Recommendation

<Which option, for which users, and why. State the evidence that decides it.>

- Confidence: `<high | medium | low>`
- What would change this recommendation: <evidence or constraint.>

## Accessibility impact

| Requirement | Impact | Status | Evidence |
| --- | --- | --- | --- |
| Keyboard-only operation and focus order | <impact> | `<verified / expected / unknown>` | <evidence> |
| Screen-reader name, role, and state | <impact> | `<verified / expected / unknown>` | <evidence> |
| Contrast in both color schemes | <impact> | `<verified / expected / unknown>` | <evidence> |
| Text scaling and reflow | <impact> | `<verified / expected / unknown>` | <evidence> |
| Color-independent status | <impact> | `<verified / expected / unknown>` | <evidence> |
| Reduced motion | <impact> | `<verified / expected / unknown>` | <evidence> |
| Localization and RTL | <impact> | `<verified / expected / unknown>` | <evidence> |

## Technical implications

- Components and files: <paths, QML/C++ boundary, Plasma/Kirigami components involved.>
- API and version constraints: <target Plasma, Qt, KF6 APIs; availability evidence.>
- Performance and resources: <expected cost, measurement plan, or "unknown".>
- Configuration and data: <new keys, migration, defaults, reversibility.>
- Packaging, translation, and release: <new dependencies, i18n impact, rollout.>
- Status: `<verified / expected / unknown>` per item.

## Implementation plan

1. <Smallest first change, with the file or component.>
2. <Next change.>
3. <Migration or fallback for existing configurations, themes, or third-party consumers.>
4. <Documentation and help-text updates.>

- Rollout: <off by default / behind a setting / enabled by default.>
- Reversibility: <how to remove it and what happens to user data and configuration.>

## Validation plan

| Check | Method | Pass criterion | Evidence to capture |
| --- | --- | --- | --- |
| <task completion> | <prototype task with N participants, or scripted UI run> | <criterion> | <recording, notes, counts> |
| <keyboard path> | <keyboard-only run> | <criterion> | <recording> |
| <screen reader> | <Orca walkthrough> | <criterion> | <transcript> |
| <themes and scaling> | <light/dark, 100%/200%> | <criterion> | <screenshots> |
| <localization> | <long locale and RTL> | <criterion> | <screenshots> |

## Risks

| Risk | Likelihood | Impact | Mitigation | Residual risk |
| --- | --- | --- | --- | --- |
| <risk> | `<low / medium / high>` | `<low / medium / high>` | <mitigation> | <accepted residual> |

## Open questions

- [ ] <question, owner, and what evidence would answer it.>
- [ ] <question, owner, and what evidence would answer it.>

## Sources

- <Title>: <full URL> (Accessed: `<YYYY-MM-DD>`)
- <Repository path or commit>: <URL or path>
- <Discussion or issue>: <full URL>

## Decision record

| Date | Status change | Decided by | Link |
| --- | --- | --- | --- |
| `<YYYY-MM-DD>` | `<Draft -> Under discussion>` | <person or group> | <URL> |

Do not mark `Adopted` without a merged change or a published decision URL.

## Version notes

- Template version 1.0, 2026-10-20. Pairs with `references/plasma-future-proposals.md` (levels, protocol, rubric) and `references/review-checklist.md` (evidence and severity vocabulary).
- Template structure follows the KDE HIG (https://develop.kde.org/hig/, Accessed: 2026-10-20) and the VDG proposal process (https://community.kde.org/KDE_Visual_Design_Group, Accessed: 2026-10-20).
- The status and decision-status vocabularies are this skill's proposed conventions (`[Recommendation]`), not KDE policy.
