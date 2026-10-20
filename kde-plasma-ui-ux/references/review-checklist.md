# UI review checklist

A review is an evidence exercise, not an opinion exchange. Use this checklist to review a Plasma surface change, a Kirigami application screen, a KCM, or a plasmoid. Every item is written so it can pass, fail, or be marked not applicable.

## Scope

- In scope: visual and interaction review of changes to Plasma shell surfaces, widgets, applications using Kirigami/Qt Quick, System Settings modules, and Qt Widgets configuration dialogs.
- Out of scope: performance profiling, object lifetime, threading, and build-system review. Those belong to the companion engineering skill at [`../../kde-plasma-best-practices/SKILL.md`](../../kde-plasma-best-practices/SKILL.md).
- Target assumptions, verified locally on 2026-10-20: Plasma 6.8.0, Qt 6.11.1, KF6, `qmllint6` (Qt 6.11.1; the unversioned `qmllint` wrapper resolves to Qt 5 on this machine). Record the actual target you reviewed; do not inherit these values by default.

## How to use this checklist

1. Capture the environment before judging pixels: branch/commit, Plasma and Qt versions, color scheme, scale factor, locale, and whether animations are enabled.
2. Work through the groups in order. Group A is a precondition; without it, later findings are not attributable to a version.
3. Record one status per item. Use the status vocabulary below, not free text.
4. Attach evidence to every status. A finding without evidence is not a finding.
5. Record the review in [`../assets/ui-review.md`](../assets/ui-review.md). A review with no inspected evidence is `inconclusive`, never `pass`.

### Status vocabulary

| Status | Meaning |
| --- | --- |
| `Pass` | The checkable statement is true, with the evidence listed. |
| `Fail` | The statement is false, with evidence. |
| `N/A` | The item does not apply to this change; state why. |
| `Unverified` | Not checked, or evidence is missing/indirect. This is **not** a pass. |

`[Recommendation]` Never convert `Unverified` into `Pass` because the change "looks fine". State what evidence would close it.

## A. Context and version

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| A1 | The reviewed artifact is identified by repository path and, where available, commit or merge-request revision. | Pass = path and revision recorded; Fail = "latest" or no revision | Exact path plus commit hash or MR URL |
| A2 | The target Plasma, Qt, and KF6 versions are recorded and match the branch under review. | Pass = all three recorded; Fail = missing or inferred | Command output (`plasmashell --version`, `qmake6 -query QT_VERSION`, or package query) |
| A3 | The review scope lists the components and workflows inspected, and the ones deliberately excluded. | Pass = both lists present; Fail = open-ended "UI review" | Scope section in the review record |
| A4 | The environment matrix is recorded: color scheme, scale factor, locale/layout direction, animation setting. | Pass = all four recorded; Fail = any missing | Screenshots or `kreadconfig6` output for each value |
| A5 | The baseline (pre-change) behavior was captured in the same environment as the candidate. | Pass = baseline and candidate captured under identical settings; Fail = baseline missing or captured differently | Paired screenshots or recordings, same theme/scale/locale |

## B. Visual hierarchy and consistency

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| B1 | Each screen has one clear primary action and a visible hierarchy between title, section, body, and secondary text. | Pass = hierarchy visible at a glance; Fail = competing primary actions or flat hierarchy | Annotated screenshot |
| B2 | Spacing and sizing derive from `Kirigami.Units` (or the widget style's metrics), with one spacing rhythm per surface. | Pass = no arbitrary margins found; Fail = unexplained one-off values | `file:line` for each margin/spacing value |
| B3 | Icons come from the icon theme by name, and their meaning matches the action. | Pass = theme names used; Fail = bitmap/emoji/custom glyph without justification | `file:line` plus icon name; screenshot of the rendered icon |
| B4 | Typography uses theme fonts and semantic roles, not numeric point sizes. | Pass = `defaultFont`/`smallFont`/`Kirigami.Heading` used; Fail = literal point sizes | `file:line` |
| B5 | Colors match the surrounding surface's color set and the result is consistent across light and dark schemes. | Pass = both schemes inspected and coherent; Fail = one scheme unreadable or inconsistent | Side-by-side screenshots in both schemes |
| B6 | New elements reuse an existing component or pattern from the same surface instead of introducing a parallel style. | Pass = reuse named; Fail = new bespoke style with no documented limitation | Component name and `file:line`; comparison screenshot |
| B7 | Every child is positioned by an anchor, positioner, or Layout, and every `Layout.*` attached property has a Layout parent. | Pass = resolved positions and no inert layout properties; Fail = overlapping siblings or `Layout.preferred*` on a layout-less root | `file:line` plus a rendered screenshot |

## C. Interaction and states

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| C1 | Hover, pressed, focused, disabled, and selected states are all defined and visually distinct where the control supports them. | Pass = every applicable state inspected; Fail = any state missing or indistinguishable | Screenshot or recording per state, with `file:line` |
| C2 | Keyboard focus is visible, and focus appearance differs from selection in an inactive view. | Pass = focus ring visible and distinct; Fail = no visible focus or focus equals selection | Screenshots of focused vs selected, keyboard-only run |
| C3 | The full task can be completed keyboard-only, in a sensible focus order, with no focus trap. | Pass = task completed without a pointer; Fail = unreachable control or trap | Recorded key sequence and result |
| C4 | Default focus lands on the most likely first action or the first input, not on a destructive control. | Pass = default focus justified; Fail = focus on destructive/irrelevant control | Screenshot of initial state plus `file:line` |
| C5 | Loading, empty, error, and partial-data states exist and are distinguishable without color alone. | Pass = all applicable states inspected; Fail = missing state or color-only signal | Screenshot per state; `file:line` for the status text/icon |
| C6 | Destructive actions are confirmed or undoable, and the confirmation names the object affected. | Pass = confirmation or undo present and specific; Fail = irreversible action with generic prompt | Screenshot plus `file:line` |
| C7 | No essential information exists only in a hover tooltip. | Pass = essential information also visible or accessible; Fail = hover-only content | Screenshot without hover plus `file:line` |
| C8 | Animation is bounded, purposeful, and not required to understand the change. | Pass = purpose and duration source stated; Fail = decorative/looping motion or animation-only signal | Recording plus `file:line` for duration |

## D. Accessibility

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| D1 | Every interactive element exposes an accessible name and the correct role. | Pass = names/roles inspected; Fail = unnamed button, icon-only control, or wrong role | `file:line` for `Accessible.name`/`Accessible.role`; screen-reader output |
| D2 | Accessible names are translated and unique within the window. | Pass = translated and unique; Fail = duplicate or untranslated name | `file:line`; Orca output in the target locale |
| D3 | Text and meaningful non-text contrast remain legible in both color schemes and at reduced opacity/disabled states. | Pass = measured or Kontrast-checked; Fail = unreadable combination | Kontrast result or measured ratio; screenshots |
| D4 | Layout survives increased system font size (at least 14 pt, per HIG testing guidance) without clipping or overlap. | Pass = inspected at 14 pt; Fail = clipped/overlapping content | Screenshot at increased size plus `file:line` of any fixed height |
| D5 | Status, error, and selection are not communicated by color alone. | Pass = text/icon/shape also present; Fail = color-only | Screenshot in grayscale or with a different scheme |
| D6 | With system animations disabled, transitions are instant and loading indicators become static without losing meaning. | Pass = inspected with animations off; Fail = motion still required or indefinite spinner without label | Recording with animations disabled |
| D7 | The surface works at the supported scale factors (for example 100% and 200%) without clipped text, misplaced popups, or unclickable targets. | Pass = each target scale inspected; Fail = any layout break | Screenshots per scale |
| D8 | Touch targets are usable where the surface is touch-capable. | Pass = at least 24×24 px at the current scale and comfortably spaced, preferring 44×44 for touch; Fail = overlapping or tiny targets. A single `gridUnit` alone is not a pass: it defaults to 18 px. | Screenshot plus `file:line` of sizes |

## E. Theming, scaling, and localization

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| E1 | No literal colors are used in chrome (panels, popups, toolbars, dialogs). | Pass = all colors resolve through theme roles; Fail = any literal color in chrome | `file:line` for every color assignment |
| E2 | A non-default color scheme and the opposite light/dark variant were both inspected. | Pass = two schemes inspected; Fail = one scheme only | Screenshots with scheme names |
| E3 | The layout mirrors correctly in right-to-left direction, including directional icons and alignment. | Pass = RTL inspected; Fail = unmirrored layout or icon | Screenshot in an RTL locale plus `file:line` of mirroring |
| E4 | Long translations (for example German) do not clip, overlap, or truncate meaning. | Pass = long-locale inspected; Fail = clipped or ambiguous truncation | Screenshot in the long locale |
| E5 | Plurals use `i18np` (or the toolkit equivalent), not string concatenation. | Pass = plural API used; Fail = concatenated suffix or `count + " items"` | `file:line` for each plural string |
| E6 | Interpolated strings use placeholders and remain translatable as whole sentences. | Pass = placeholder-based; Fail = concatenated fragments | `file:line` |
| E7 | User-visible text added by the change is wrapped for translation, including tooltips, accessible names, and error messages. | Pass = all wrapped; Fail = any literal user-visible string | `file:line` for each new string |

## F. Technical integration

| ID | Check | Pass / Fail / N/A | Evidence requirement |
| --- | --- | --- | --- |
| F1 | The root element matches the target: `PlasmoidItem`/`ContainmentItem`, `Kirigami.ApplicationWindow`, an `org.kde.kcmutils` KCM root, or the repository's Qt Widgets root (`KPageDialog`, `KConfigDialog`, `QDialog`). | Pass = root matches target; Fail = copied root from another surface | `file:line` of the root element |
| F2 | QML imports are appropriate for the target version, with no stale Plasma 5 modules carried forward unverified. For a Qt Widgets surface, record the Qt/KF version and widget-style assumptions instead. | Pass = imports or widget assumptions reviewed against target; Fail = deprecated or version-guessed import | `file:line` plus target-version reference |
| F3 | Declarative bindings are preserved; no imperative assignment overwrites a binding that should stay live. | Pass = no suspicious assignment to a bound property; Fail = binding broken by assignment | `file:line` and the property involved |
| F4 | Changed QML passes `qmllint6` (Qt 6) with no new warnings. Not applicable to Qt Widgets-only changes. | Pass = clean run on changed files; Fail = new warning | Exact command and output |
| F5 | Models and delegates render without per-item imperative creation where a delegate is the intended mechanism. | Pass = model/delegate used; Fail = manual item creation in a loop | `file:line` |
| F6 | KCM wiring is correct: `KQuickConfigModule` or `KQuickManagedConfigModule` backend (KConfigXT-managed modules use the latter), `kcmutils_add_qml_kcm`, and a loadable module via `kcmshell6`. | Pass = module loads standalone; Fail = load error or missing metadata | Command output from `kcmshell6 <module>` |
| F7 | The change does not depend on a private or unverified API name. | Pass = every API cited in docs or target source; Fail = name asserted from memory | Citation URL or `file:line` in the target |

## G. Regressions

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| G1 | Unrelated workflows in the same surface still behave as before. | Pass = listed workflows re-run; Fail = any changed behavior | Before/after evidence per workflow |
| G2 | The change does not alter shared components in a way that affects other consumers. | Pass = consumers identified and checked; Fail = shared component changed without checking | `grep` output for consumers plus screenshots |
| G3 | Panel/widget sizing, popup placement, and multi-screen behavior are unchanged unless intended. | Pass = inspected on the recorded screen setup; Fail = clipped popup or wrong screen | Screenshots or recording |
| G4 | No new console warnings, binding loops, or `TypeError` output appears during the reviewed flows. | Pass = clean run; Fail = new warning or error | Captured stderr/stdout |
| G5 | Visual differences from the baseline are intentional and each one is explained. | Pass = diff reviewed item by item; Fail = unexplained pixel or layout change | Paired screenshots plus explanation |

## H. Deviation justification

| ID | Check | Pass / Fail / N/A | Evidence required |
| --- | --- | --- | --- |
| H1 | Every deviation from an established KDE pattern is documented with the pattern it replaces. | Pass = deviation and pattern named; Fail = undocumented deviation | `file:line` plus HIG or component reference |
| H2 | The deviation states why the standard pattern is insufficient, with evidence rather than preference. | Pass = concrete limitation cited; Fail = "looks better" or taste | Screenshot or measurement plus rationale |
| H3 | Alternatives were considered and the trade-off is recorded. | Pass = at least one alternative and its cost; Fail = single option asserted | Proposal or review record |
| H4 | The deviation does not regress accessibility, localization, or consistency elsewhere. | Pass = checked in sections D and E; Fail = known regression accepted silently | Links to the corresponding checklist items |
| H5 | Experimental or future-direction ideas are labeled `Experimental — not an official KDE decision` and are not presented as shipped behavior. | Pass = label present on every artifact; Fail = unlabeled future claim | Artifact link plus quoted label |

## Severity definitions

Assign one severity to every `Fail`. Severity describes user impact, not reviewer effort.

| Severity | Definition | Examples | Required action |
| --- | --- | --- | --- |
| Blocker | Prevents completing a core task, causes data loss, makes a core workflow inaccessible, or violates a hard repository requirement. | Keyboard trap in a settings dialog; unreadable text in the default scheme; crash on open | Must fix before merge; cannot be accepted as a known issue |
| Major | Significant usability, consistency, or accessibility defect with a workaround, or a visible break in a primary workflow. | Focus invisible but task still completable by pointer; clipped label in one locale; wrong root element | Must fix, or be explicitly accepted by the owner with a recorded rationale and follow-up |
| Minor | Noticeable defect with low user impact, or a local inconsistency in a secondary surface. | Uneven spacing in one row; icon metaphor slightly off; inconsistent capitalization | Fix when in scope; may ship with a tracked follow-up |
| Nit | Preference with no demonstrated user impact. | Alternative wording; optional alignment tweak | Optional; never blocks |

`[Recommendation]` Severity inflation ("everything is a blocker") destroys the signal. If you cannot name the affected task and the user consequence, it is not a blocker.

## Verdict rules

- `Pass`: every applicable item is `Pass`, and no `Blocker` or `Major` finding is open.
- `Fail`: at least one `Blocker` or `Major` finding is open.
- `Inconclusive`: any required evidence is missing, or any applicable item is `Unverified`. Inconclusive is not a soft pass.
- `N/A` items must state why they do not apply. A blanket "N/A" for a whole group requires justification.

## Related references

- [`./visual-consistency.md`](./visual-consistency.md) for hierarchy, spacing, and icon conventions.
- [`./interaction-patterns.md`](./interaction-patterns.md) for state and workflow expectations.
- [`./accessibility.md`](./accessibility.md) for the accessibility baseline behind section D.
- [`./qt-qml-kirigami.md`](./qt-qml-kirigami.md) for root elements, theme roles, and localization APIs.
- [`./plasma-future-proposals.md`](./plasma-future-proposals.md) for labeling deviations that are proposals rather than shipped changes.

## Sources

- KDE Human Interface Guidelines: https://develop.kde.org/hig/ (Accessed: 2026-10-20)
- KDE HIG, Accessibility and inclusiveness (keyboard, color, text size, screen reader, animations): https://develop.kde.org/hig/accessibility/ (Accessed: 2026-10-20)
- KDE HIG, Layout and navigation: https://develop.kde.org/hig/layout_and_nav/ (Accessed: 2026-10-20)
- KDE HIG, Text and labels: https://develop.kde.org/hig/text_and_labels/ (Accessed: 2026-10-20)
- KDE HIG, Icons: https://develop.kde.org/hig/icons/ (Accessed: 2026-10-20)
- Kirigami tutorial, Colors and themes: https://develop.kde.org/docs/getting-started/kirigami/style-colors/ (Accessed: 2026-10-20)
- Kirigami tutorial, Typography: https://develop.kde.org/docs/getting-started/kirigami/style-typography/ (Accessed: 2026-10-20)
- Porting Plasmoids to KF6 (root elements and KCM config UI): https://develop.kde.org/docs/plasma/widget/porting_kf6/ (Accessed: 2026-10-20)
- Settings module (KCM) development: https://develop.kde.org/docs/features/configuration/kcm/ (Accessed: 2026-10-20)
- Plasma widget translations / i18n: https://develop.kde.org/docs/plasma/widget/translations-i18n/ (Accessed: 2026-10-20)
- Qt Quick accessibility: https://doc.qt.io/qt-6/qml-qtquick-accessible.html (Accessed: 2026-10-20)
- Qt accessibility overview: https://doc.qt.io/qt-6/accessible.html (Accessed: 2026-10-20)

## Version notes

- Authoring baseline: Plasma 6.8.0, Qt 6.11.1, KF6, verified 2026-10-20.
- The 14 pt text-size check and the "animations disabled" behavior come from the current HIG testing guidance; a future HIG revision may change the number or the procedure. Re-read the accessibility page when reviewing against a newer branch.
- The severity definitions and verdict rules are this skill's proposed conventions (`[Recommendation]`), not official KDE policy.
