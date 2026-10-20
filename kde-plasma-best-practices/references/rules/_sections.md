# Rule index

Load only the rules that match the change under review. Paths are relative to `references/rules/`.

Impact classes are proposed conventions for this skill, not an official KDE taxonomy: `P0` critical responsiveness, correctness, or resource problem; `P1` major architectural, lifecycle, or performance concern; `P2` recurring implementation inefficiency or maintainability issue; `P3` lower-impact consistency, tooling, or cleanup.

Every rule labels substantive claims `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, or `[Unknown]`. Status `shipped` means the file is present in this bundle; `planned` means the path is reserved and may not exist yet in your checkout.

## Performance

| Rule | Impact | Tags | Status |
| --- | --- | --- | --- |
| [`performance/blocking-gui-thread.md`](performance/blocking-gui-thread.md) | P0 | event-loop, responsiveness, threading | shipped |
| [`performance/async-work.md`](performance/async-work.md) | P1 | threading, queued-connections, lifetime, cancellation | shipped |
| [`performance/profiling-first.md`](performance/profiling-first.md) | P1 | profiling, performance, evidence | shipped |
| [`performance/startup-cost.md`](performance/startup-cost.md) | P2 | startup, lazy-loading, loader, plugins | shipped |

## QML

| Rule | Impact | Tags | Status |
| --- | --- | --- | --- |
| [`qml/declarative-bindings.md`](qml/declarative-bindings.md) | P1 | bindings, declarative, qml-performance | shipped |
| [`qml/binding-overwrites.md`](qml/binding-overwrites.md) | P1 | bindings, debugging, qmllint, state | shipped |
| [`qml/model-delegates.md`](qml/model-delegates.md) | P1 | models, delegates, listview, performance | shipped |
| [`qml/loader-usage.md`](qml/loader-usage.md) | P2 | loader, lazy-loading, startup, error-handling | shipped |
| [`qml/component-reuse.md`](qml/component-reuse.md) | P2 | components, kirigami, api-design, maintainability | shipped |
| [`qml/timer-lifecycle.md`](qml/timer-lifecycle.md) | P2 | timers, animations, visibility, polling, performance | shipped |

## C++

| Rule | Impact | Tags | Status |
| --- | --- | --- | --- |
| [`cpp/ownership-lifetime.md`](cpp/ownership-lifetime.md) | P0 | cpp, qt, ownership, lifetime, qobject, qml | shipped |
| [`cpp/signals-slots.md`](cpp/signals-slots.md) | P1 | cpp, qt, signals, slots, connections, threads | shipped |
| [`cpp/threading.md`](cpp/threading.md) | P0 | cpp, qt, threading, qthread, concurrency, shutdown | shipped |
| [`cpp/qml-cpp-boundaries.md`](cpp/qml-cpp-boundaries.md) | P1 | cpp, qml, architecture, models, integration | shipped |

## Architecture

| Rule | Impact | Tags | Status |
| --- | --- | --- | --- |
| [`architecture/module-boundaries.md`](architecture/module-boundaries.md) | P1 | architecture, plugins, kplugin, kcm, dependencies | shipped |
| [`architecture/kde-api-compatibility.md`](architecture/kde-api-compatibility.md) | P1 | architecture, compatibility, versioning, kde-frameworks, qt, cmake | shipped |

## Build

| Rule | Impact | Tags | Status |
| --- | --- | --- | --- |
| [`build/cmake.md`](build/cmake.md) | P2 | build, cmake, ecm, qt6, kf6, qml | shipped |
| [`build/resources-packaging.md`](build/resources-packaging.md) | P2 | build, resources, kpackage, plasmoid, install, i18n | shipped |
| [`build/static-analysis.md`](build/static-analysis.md) | P2 | build, static-analysis, qmllint, clazy, clang-tidy, ci | shipped |

## Testing

| Rule | Impact | Tags | Status |
| --- | --- | --- | --- |
| [`testing/unit-tests.md`](testing/unit-tests.md) | P1 | testing, qt, qttest, unit-tests, signalspy, ci | shipped |
| [`testing/integration-tests.md`](testing/integration-tests.md) | P1 | testing, qml, qtquicktest, offscreen, kconfig, dbus | shipped |
| [`testing/regression-tests.md`](testing/regression-tests.md) | P1 | testing, regression, benchmarks, visual-regression, baselines | shipped |

## Adding a rule

Copy `_template.md`, keep the section order, cite at least one checked official URL with an access date, and add the row here with its impact and tags. If a rule cannot show a correct and an incorrect example, it is a note, not a rule.
