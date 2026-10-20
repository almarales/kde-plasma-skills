---
title: "Measure before optimizing"
impact: P1
scope: cpp, qml, build
tags: [profiling, performance, evidence]
---

# BP-PERF-03 — Measure before optimizing

## Principle

A performance change starts with a baseline, names the metric and the scenario, changes one thing, and re-measures with the same method. Without that loop there is no evidence, only a preference. Refuse "faster" as a claim unless it carries a command, an environment, and a number.

## Why it matters

[Official] Qt states that knowing where time is spent lets you focus on problems that actually exist, and that "attempting to optimize code without profiling is likely to result in very minor rather than significant performance improvements". The QML Profiler documentation names the usual causes it exposes: too much JavaScript in too few frames, creating or updating invisible items, and long-running C++ in paint methods or signal handlers.

[Recommendation] Unmeasured optimization usually trades a cheap cost for an expensive one: `cacheBuffer` grows memory, per-delegate caches grow startup time, and replacing bindings with imperative updates removes the declarative model that made the code reviewable.

[Recommendation] Treat a profile from a debug build, a software renderer, or a different compositor setting as a different environment. Label it and do not compare it to a release baseline.

## Incorrect

```text
Review comment: "Bindings are slow here. Replace width: parent.width with an
onWidthChanged handler that assigns width once."

Missing: which binding, how often it evaluates, on which build, with what
frame time, and what the handler costs when the parent resizes continuously.
```

## Preferred

```text
Scenario : <steps, window size, model size, hardware>
Build    : <Release, Qt 6.11.1, Plasma 6.8.0, compositor settings>
Baseline : <metric> = <value>  [Observed, <date>, <exact command>]
Change   : <one change, one variable>
After    : <metric> = <value>  [Observed, <date>, <exact command>]
Verdict  : keep or revert, because <reason>; residual risk: <risk>
```

```bash
# Pseudocode: a repeatable measurement, not a benchmark result.
# 1. Record the release build and the exact scenario.
# 2. Capture a baseline trace with the QML Profiler.
# 3. Apply one change, rebuild, capture the same trace.
# 4. Compare the same ranges; keep the raw traces next to the change.
```

Tool selection, from cheapest to most specific:

| Tool | Use it for |
| --- | --- |
| QML Profiler (Qt Creator) | binding/JS cost, frame timing, invisible-item work |
| CPU Usage Analyzer (Qt Creator) | native hot spots the QML Profiler cannot attribute |
| GammaRay | live object tree, property and signal inspection |
| heaptrack | allocation volume, leaks, retention across a scenario |
| `perf` | whole-process sampling, off-CPU time, scheduler effects |

## Exceptions and trade-offs

- Correctness and unbounded blocking are defects independent of measurement; a `waitForFinished()` on the GUI path does not need a profile to be rejected.
- A measured fix can still be the wrong trade: faster scrolling at the cost of 200 MB of retained delegates is a regression somewhere else. State the trade.
- Micro-benchmarks of a single binding rarely predict application behavior; prefer a scenario trace.

## Review checklist

- [ ] The change states the metric, scenario, build type, and hardware.
- [ ] A baseline exists and was captured with the same method as the result.
- [ ] Exactly one variable changed between baseline and result.
- [ ] Debug-build and warm-cache numbers are labeled as such.
- [ ] The claimed gain includes a memory or complexity cost, or says there is none.
- [ ] No invented number appears anywhere in the review or the commit message.

## References

- [Official] Qt: QML Performance Considerations And Suggestions — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)
- [Official] Qt Creator: Profiling QML applications — https://doc.qt.io/qtcreator/creator-qml-performance-monitor.html (accessed 2026-10-20)
- [Official] Qt Creator: CPU Usage Analyzer — https://doc.qt.io/qtcreator/creator-cpu-usage-analyzer.html (accessed 2026-10-20)
- [Official] KDAB: GammaRay — https://github.com/KDAB/GammaRay (accessed 2026-10-20)
- [Official] KDE: heaptrack — https://invent.kde.org/sdk/heaptrack (accessed 2026-10-20)
- [Official] Linux kernel: perf wiki — https://perf.wiki.kernel.org/index.php/Main_Page (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 and Qt Creator documentation on 2026-10-20. Tool availability differs per distribution; state which tool produced a number so the result can be reproduced.
