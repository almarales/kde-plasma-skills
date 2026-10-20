# Audit criteria

## Scope

Use this reference when the deliverable of a Plasma code review is a **written audit with a verdict** rather than a chat answer. It defines how to scope an audit, how to classify a finding, which checks are required, and how the verdict is reached.

It does not restate the rule catalog. The rules in `references/rules/` remain the authority on what is wrong; this file is the authority on how a finding is written, classified, and judged. The report itself is written with `assets/audit-report.md`.

Evidence labels are the ones used across this skill: `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, `[Unknown]`. Every substantive claim in an audit carries one.

## What an audit is

`[Recommendation]` An audit is a scoped, revision-pinned, evidence-carrying verdict. Three properties make it an audit, and losing any one of them downgrades it to an impression:

- **Scope**: the exact revision and the exact file set.
- **Evidence**: something was inspected, and the inspection is reproducible.
- **Verdict**: a stated outcome, including the possibility of "inconclusive".

A review without inspected evidence is `inconclusive`, never a pass.

## Scope before inspection

Record these before reading code, because they decide what the audit is allowed to claim:

| Field | Why it is required |
| --- | --- |
| Revision | A finding without a commit SHA cannot be reproduced or re-checked. |
| Files inspected | The auditable set. Anything else is out of scope by definition. |
| Files read but not audited | Prevents a reader from assuming a read file was judged. |
| Rules loaded | The rules selected from `references/rules/_sections.md` by the signals in the change, listed by ID. |
| Out of scope | Named explicitly, so a later reader does not treat silence as a pass. |

`[Recommendation]` Load only the rules the change touches, and state which ones were loaded. A rule that was not loaded cannot produce a finding, and a finding with no loaded rule behind it is an observation, not a finding (see severity, below).

`[Recommendation]` Cite a rule by its **ID** (`BP-QML-04`), never by its path. The ID is stable across refactors and renames; the path is not. `references/rules/_sections.md` maps every ID to its file, impact and tags, so a reader can go from `BP-CPP-01` to the rule without guessing a directory layout.

## The three axes

`[Recommendation]` Every audit states its outcome on three axes, explicitly, whether or not the change touches all of them:

| Axis | Question | Typical rules |
| --- | --- | --- |
| Correctness | Does it behave as specified, and can it break? | `cpp/ownership-lifetime`, `cpp/threading`, `cpp/signals-slots`, `qml/binding-overwrites` |
| Performance | Is the GUI thread free of blocking work, and is the cost measured? | `performance/blocking-gui-thread`, `performance/async-work`, `performance/profiling-first`, `qml/model-delegates` |
| Maintainability | Is the structure modular, consistent, and covered? | `architecture/*`, `qml/component-reuse`, `build/*`, `testing/*` |

An axis that was not inspected is reported as `Unverified`, never as `Pass`. Silence is not a pass.

## Severity is derived, not invented

`[Recommendation]` The severity of a finding is the `impact` of the rule it violates, as declared in `references/rules/_sections.md`. The bundle has one severity vocabulary; a second taxonomy is how a catalog stops being comparable.

| Rule impact | Finding severity | Meaning in the report |
| --- | --- | --- |
| `P0` | **Blocker** | Breaks responsiveness, correctness, or resource safety in normal use |
| `P1` | **Major** | Major architectural, lifecycle, or performance concern that will be expensive later |
| `P2` | **Minor** | Recurring inefficiency or maintainability issue with a local fix |
| `P3` | **Nit** | Consistency, tooling, or cleanup with low individual impact |

Rules for using it:

- Take the severity from the rule's frontmatter. Assign by expected impact under normal use, not by how alarming the example looks.
- **Downgrading** a finding requires evidence that the affected path cannot be reached in the target configuration. Record that evidence in the finding's evidence cell; a downgrade without evidence is not a downgrade.
- **Raising** a finding above its rule's impact requires a cited reason — for example, a change that multiplies the frequency of a P2 condition. Record the reason.
- A defect that **no rule covers** is an *observation*, not a finding. It is reported in the observations table, at most `Minor`, and it is a candidate for `references/rule-authoring.md`. It never becomes a `Blocker` without a rule that says so.
- Never assign a severity the catalog does not define.

## Status and disposition

`[Recommendation]` A finding's status is `Fail` or `Unverified`. A finding is never `Pass`: it is either present or its applicability was not established.

A finding stays open until it is fixed, or until it is explicitly accepted with a named owner and a stated reason. Both dispositions appear in the verdict table; neither is implicit.

## Evidence discipline

- Every finding cites `path:line`, the rule file that condemns it, what was observed, what should happen, and the evidence that shows it.
- Every executed check reports the **exact command and its observed result**. A command that was not run is listed under "Checks not run" with the reason and the evidence that would close it.
- Never claim a speed-up without before-and-after numbers taken in the same environment, with the measurement command named.
- Never report analyzer output that was not produced. On the verification machine `qmllint6` (Qt 6.11.1) is available; the unversioned `qmllint` is a Qt 5 wrapper; `clazy` and `clang-tidy` were **not** installed, so their output must never appear in an audit unless the audit was run on a machine where they are.
- A URL that returns a directory listing or an error page is not a source, even when the status is 200.

## Required checks

`[Recommendation]` These are the checks an audit runs when the change touches the area. They are not optional extras, and each one that cannot run must be declared in "Checks not run":

| Change touches | Required check | Command shape | Evidence to keep |
| --- | --- | --- | --- |
| QML files | Lint | `qmllint6 <file>` on Qt 6, or the project's `all_qmllint` target | stdout, stderr, exit code |
| C++ | Build with the project's own warning set | the project's build command | warning count before and after |
| A performance claim | Measurement | the command named in the claim | before, after, environment |
| A bug fix | Regression | a test that fails at the baseline revision | failing run at base, passing run after |
| Build or packaging | Install path | the project's own install/uninstall | install log |
| Anything claimed as measured | Reproduction | the exact command from the claim | the raw output |

`[Recommendation]` A regression test belongs to the change, not to the audit. If the audit produces one, it is committed with the fix, and the audit records the failing-at-baseline and passing-after runs as its evidence.

## The verdict

`[Recommendation]` The verdict vocabulary is the same one the UI review uses, so a reader learns one vocabulary for the whole bundle:

- **`pass`** — every applicable check is `Pass` with evidence, and no `Blocker` or `Major` finding is open.
- **`fail`** — at least one `Blocker` or `Major` finding is open.
- **`inconclusive`** — any required evidence is missing, or any applicable check is `Unverified`. A review without inspected evidence is always `inconclusive`.

`[Recommendation]` The verdict is a statement about the audited revision, not about the change's author and not about whether the change should ship. Delivery stays a separate decision under the repository's own policy; an audit never authorizes it.

## Boundaries

- Visual, interaction, and accessibility findings belong to `kde-plasma-ui-ux`. An audit may note that a decision is visual, and stop there.
- The audit does not restate the rule catalog. It cites rules; `references/rules/` is where they live.
- The audit does not replace the repository's CI, its own tests, or its maintainers' judgment.
- Findings about code outside the audited revision are observations, not findings.

## Audit checklist

- [ ] The revision, the file set, and the out-of-scope items are recorded.
- [ ] The rules loaded are listed by ID, and every finding cites one of them.
- [ ] Each of the three axes has a stated outcome, and uninspected axes are `Unverified`.
- [ ] Every severity comes from a rule's `impact`, or the finding is filed as an observation.
- [ ] Every finding carries `path:line`, observed, expected, and evidence.
- [ ] Every executed check reports the exact command and its result; the rest are in "Checks not run".
- [ ] No measurement, analyzer output, or API name appears that was not actually observed.
- [ ] The verdict follows the rules above, and open findings are counted by severity.

## Sources

- Rule index and impact classes — `references/rules/_sections.md`
- Rule authoring and evidence standard — `references/rule-authoring.md`
- Static analysis commands and local availability — `references/rules/build/static-analysis.md`
- Report template — `assets/audit-report.md`
- Sibling verdict vocabulary — `../kde-plasma-ui-ux/references/review-checklist.md` and `../kde-plasma-ui-ux/assets/ui-review.md`
- Qt: `qmllint` — https://doc.qt.io/qt-6/qtqml-tooling-qmllint.html (accessed 2026-10-20)
- Qt: `qt_add_qml_module` — https://doc.qt.io/qt-6/qt-add-qml-module.html (accessed 2026-10-20)
- KDE: API documentation — https://api.kde.org/ (accessed 2026-10-20)

## Version notes

- Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The severity mapping is this skill's convention, not an official KDE taxonomy, and it is bound to the `impact` values in `references/rules/_sections.md`: change one and change both.
- The `P0`–`P3` classes and the `pass` / `fail` / `inconclusive` verdicts are shared with the UI review skill on purpose. Keep one vocabulary for the bundle.
- Analyzer availability is machine-specific. Re-check `qmllint6`, `clazy`, and `clang-tidy` on the audit machine before listing them as run.
