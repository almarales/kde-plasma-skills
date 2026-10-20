---
title: "Regression tests and baselines"
impact: P1
scope: "Testing / bug regression, performance baselines, visual baselines"
tags: [testing, regression, benchmarks, visual-regression, baselines]
---

# BP-TEST-03 — Regression tests and baselines

## Principle

A bug is not fixed until a test fails without the fix. Reproduce first, encode the reproduction as one focused test, and keep the baseline artefacts that later changes are compared against. Baselines are reviewed inputs, never auto-accepted output.

## Why it matters

A regression test is the only durable proof that a defect cannot return; a fix without one is a fix that will be re-broken by the next refactor. The reproduction is also the cheapest way to confirm the diagnosis: if the test does not fail before the fix, the change did not address the reported cause.

Performance and visual checks need the same discipline with more caution. QtTest offers `QBENCHMARK` for timing loops `[Official]`, but a timing number from one machine is not evidence about another: results depend on hardware, load, and build type, so a benchmark needs a recorded baseline, a stated tolerance, and a controlled environment before it can gate anything `[Recommendation]`.

Visual comparison has comparable hazards. Rendering depends on fonts, display scaling, the active theme and colour scheme, the GPU and its driver, and whether the run is offscreen. A screenshot diff that ignores those inputs produces noise, and a diff that tolerates everything produces nothing.

## Incorrect

```cpp
// Pseudocode: illustrative only.
// Fix applied, no test: nothing stops the bug from returning.
void Model::normalizeNames() {
    for (auto &row : m_rows)
        row.name = row.name.trimmed();
}
```

```text
# Pseudocode: illustrative only.
# Baseline regenerated automatically on every run, so it always "passes".
compare_screenshots --update-baseline
```

## Preferred

```cpp
// Pseudocode: illustrative only.
// Regression test named after the report; fails on the pre-fix code.
void TestModel::normalizeNames_leavesInnerSpaces() {
    Model model;
    model.append({ "  Alpha   Beta  " });
    model.normalizeNames();
    QCOMPARE(model.at(0).name, QStringLiteral("Alpha   Beta"));
}
```

- Write the failing test first and paste its failure output in the change description; that output is the evidence the fix addresses the cause.
- Keep one regression test per defect, linked to the report, and keep it passing forever.
- Record benchmark baselines with the machine, build type, and commit; compare only like with like.
- Fix the visual baseline inputs (theme, font, scale, offscreen flag) and document them next to the baseline images.
- Review baseline updates as part of the change; an unexplained baseline churn is a finding, not a formality.

## Exceptions and trade-offs

- Flaky environment-dependent tests are worse than no test: disable the test explicitly with a reason, or fix the isolation, rather than loosening the assertion until it always passes.
- Micro-benchmarks with sub-millisecond runtimes are dominated by noise; either increase the workload or use a metric that is stable on the target hardware.
- Pixel-exact screenshot comparison is appropriate for icon rendering and static chrome; for animated or composited surfaces, assert structure and properties instead.
- A regression test that requires the full desktop should live in an integration suite, not in the unit-test binary.

## Review checklist

- [ ] The new test fails on the pre-fix revision and passes after the fix.
- [ ] One defect, one test, with a link to the report or issue.
- [ ] Performance claims cite a baseline, a tolerance, and the environment used.
- [ ] Visual baselines pin theme, fonts, scale, and platform flags.
- [ ] Baseline changes are explained in the change itself.
- [ ] No assertion was weakened just to make the suite green.

## References

- Qt: Qt Test overview (`QBENCHMARK`, data-driven tests) — https://doc.qt.io/qt-6/qtest-overview.html (accessed 2026-10-20)
- Qt: `QTest` (`QBENCHMARK`, `QTRY_*`) — https://doc.qt.io/qt-6/qtest.html (accessed 2026-10-20)
- Qt: `QSignalSpy` for behavioural assertions — https://doc.qt.io/qt-6/qsignalspy.html (accessed 2026-10-20)
- Qt: Qt Quick Test (offscreen runs and rendering) — https://doc.qt.io/qt-6/qtquicktest-index.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. `QBENCHMARK` and the Qt Quick Test facilities exist across Qt 6, but benchmark metrics and reporting options differ between releases; confirm the options your Qt version supports before wiring a benchmark into CI. No performance numbers are claimed in this rule because none were measured.
