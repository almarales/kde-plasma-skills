---
name: kde-plasma-best-practices
description: "Trigger: KDE Plasma code review, QML performance, GUI thread stall, Qt/Kirigami implementation. Apply evidence-based Plasma engineering rules."
license: GPL-3.0-or-later
metadata:
  author: "Javier Reinaldo Almarales"
  version: "1.0"
---

## Activation Contract

Use for KDE Plasma code: QML/Qt Quick, Kirigami, Plasma applets, C++/Qt, CMake, tests. Its complement `kde-plasma-ui-ux` owns visual and interaction decisions; this skill owns implementation quality.

Not for non-Qt code or uninspected approvals.

## Hard Rules

- Label each substantive claim `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, or `[Unknown]`.
- Never claim a speed-up you did not measure on the target build; name the command and environment.
- Never fix a stall with `processEvents()` or a nested `QEventLoop`.
- Do not replace a live QML binding with a JS assignment without documenting why.
- Cite only references you opened. Keep version assumptions explicit: Plasma 6.8.0, Qt 6.11.1, KF6 (verified 2026-10-20).
- These rules are community conventions, not KDE policy or endorsement.

## Decision Gates

| Signal in the change | Load |
| --- | --- |
| Frozen UI, jank, "not responding" | `performance/blocking-gui-thread.md` |
| Background work, results, cancellation | `performance/async-work.md` |
| "Make it faster" with no measurement | `performance/profiling-first.md` |
| Slow launch or applet load | `performance/startup-cost.md` |
| Binding behavior, handler assignment | `qml/declarative-bindings.md`, `qml/binding-overwrites.md` |
| Large model, delegate cost | `qml/model-delegates.md` |
| Deferred creation, `Loader` | `qml/loader-usage.md` |
| New or forked QML control | `qml/component-reuse.md` |
| Repeating timer or animation while hidden | `qml/timer-lifecycle.md` |
| C++, ownership, threads, shutdown | `cpp/` rules in `references/rules/_sections.md` |
| Pluggable views, plugin-provided renderings, KPackage structures, reusing OS components in a plasmoid | `references/plasma-development.md` |
| A formal audit with a written verdict | `references/audit-criteria.md`, `assets/audit-report.md` |
| A widget that must survive the next Plasma release: removed APIs, imports, metadata | `references/forward-compatibility.md`, `scripts/lint_qml.py` |

Bare paths are relative to `references/rules/`; `references/…` and `assets/…` to the skill root.

## Execution Steps

1. Read `references/rules/_sections.md` and select only the rules the diff touches.
2. Read each selected rule before judging code; check its version notes against the target branch.
3. Run `scripts/lint_qml.py` on the changed QML and `metadata.json`; report its findings with the command and output. A floor, not a verdict.
4. Measure or reproduce a performance problem before recommending a change.
5. Report `path:line`, rule, impact, mechanism, smallest fix.
6. Defer visual and accessibility goals to `kde-plasma-ui-ux`.
7. Keep unknowns visible; invent no APIs or numbers.

## Output Contract

Return:
- Rules applied, each with impact and evidence label.
- Findings with `path:line`, why it matters, and the preferred fix.
- Measurements: exact command, environment, before and after.
- Trade-offs accepted and checks still unverified.
- Checker output, when the checker ran: the command and its findings, separate from the reviewer's own.

A formal audit uses `assets/audit-report.md` and `references/audit-criteria.md`: a finding's severity is the violated rule's `impact`, the verdict is `pass`, `fail`, or `inconclusive`, and an audit without inspected evidence is `inconclusive`.

## References

- `references/rules/_sections.md` — rule index by area, impact, and tags; `references/rules/_template.md` — required rule format.
- `references/rules/` — the P0-P3 catalog: performance, qml, cpp, architecture, build, testing.
- `references/qt-quick-performance.md`, `references/plasma-development.md`, `references/rule-authoring.md`, `references/sources.md` — syntheses and verified source ledger.
- `references/audit-criteria.md` — audit scope, severity derivation, required checks, verdict rules.
- `references/forward-compatibility.md` — the public-surface contract for surviving future Plasma releases.
- `assets/audit-report.md` — template for a written audit with a verdict.
- `scripts/lint_qml.py` — checker for the machine-checkable subset; each finding cites its rule.
