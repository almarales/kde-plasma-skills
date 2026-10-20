---
title: "Static analysis in the build and CI"
impact: P2
scope: "Build / compiler warnings, qmllint, clazy, clang-tidy, CI gates"
tags: [build, static-analysis, qmllint, clazy, clang-tidy, ci]
---

# BP-BUILD-03 — Static analysis in the build and CI

## Principle

Make the analyzers part of the build, make their findings visible, and gate on regressions rather than on an absolute zero. A warning that is already there is debt; a warning introduced by a change is a defect the change owns.

## Why it matters

`qmllint` ships with Qt and verifies syntactic validity while warning about QML anti-patterns: unqualified property access, signal handlers without a matching signal, `with` statements, unused imports, deprecated components `[Official]`. It needs type information from the QML modules on its import path, so it only sees your types when the module is structured normally `[Official]`. For projects using `qt_add_qml_module()`, convenience targets such as `all_qmllint` are created automatically `[Official]` — the integration is a build target, not a separate script.

`qmllint` is also configurable enough to be usable in CI: `--max-warnings` makes the exit code non-zero past a threshold, `--ignore-settings` ignores configuration files for a reproducible run, and `--fix` with `--dry-run` previews automated fixes `[Official]`. The documentation warns that applying every fix at once may be too large a change, and recommends splitting by file or category `[Official]`. Use the Qt 6 binary (`qmllint6` on many distributions, or the `Qt6::qmllint` target) — an unversioned `qmllint` may dispatch to Qt 5 through `qtchooser` and lack these flags.

The same regression logic applies to C++: a floating compiler version can add warnings to untouched code, so `-Werror` without a baseline makes the build fail for reasons unrelated to the change under review.

## Incorrect

```cmake
# Pseudocode: illustrative only.
# Blanket -Werror with no baseline: any compiler update breaks the build.
add_compile_options(-Wall -Wextra -Werror)

# Lint is a manual step nobody runs before pushing.
# (no qmllint target, no CI job)
```

## Preferred

```cmake
# Pseudocode: illustrative only.
add_compile_options(-Wall -Wextra)          # visible, not fatal, locally

qt_add_qml_module(app
    URI Example
    QML_FILES qml/Main.qml
)
# Creates all_qmllint for the module's QML files.
add_custom_target(lint
    COMMAND qmllint6 --max-warnings 0 qml/Main.qml
    COMMENT "Lint QML"
    VERBATIM)
```

- Run `all_qmllint` in CI and compare its output against the previous run instead of assuming a clean baseline.
- Enable clazy for C++ where the project already uses it; `clazy-standalone` exists for builds that do not go through CMake `[Official]`.
- Feed `clang-tidy` a `compile_commands.json` export (`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`) and run it on changed files first, so CI time stays proportional to the change `[Recommendation]`.
- Fail the job on new findings: capture the analyzer output, compare with the recorded baseline, and fail only on additions.
- Keep the analyzer versions pinned in CI, so a tool upgrade is a deliberate change with its own diff.

## Exceptions and trade-offs

- Strict `-Werror` is defensible when the toolchain is pinned and the tree is already clean; then it is a cheap guarantee rather than a trap.
- Auto-fixing lints in bulk creates large, unreviewable diffs. Apply fixes per category and commit them separately.
- clang-tidy checks that fire on every line of a legacy file can be suppressed file-locally, but a blanket project-wide disable hides new code too.
- Analysis that is not run in CI decays. A locally documented command with no job behind it does not count as a gate.
- On this machine `qmllint6` (Qt 6.11.1) is installed; the unversioned `qmllint` wrapper resolves to Qt 5 and reports version `1.0`. `clazy` and `clang-tidy` were not verified present, so their availability must be checked before adding them to a pipeline `[Unknown]`.

## Review checklist

- [ ] The build enables a defined warning set for every target.
- [ ] QML files are linted through `all_qmllint` or an explicit `qmllint6` invocation on Qt 6.
- [ ] CI compares findings against a baseline and fails on new ones.
- [ ] Analyzer versions are pinned, not floating.
- [ ] Auto-fix commits are scoped to one lint category.
- [ ] Any project-wide suppression has an owner and a removal condition.

## References

- Qt: `qmllint` (warning categories, CMake targets, `--max-warnings`, `--fix`) — https://doc.qt.io/qt-6/qtqml-tooling-qmllint.html (accessed 2026-10-20)
- Qt: `qt_add_qml_module` — https://doc.qt.io/qt-6/qt-add-qml-module.html (accessed 2026-10-20)
- CMake: `AUTOMOC` target property — https://cmake.org/cmake/help/latest/prop_tgt/AUTOMOC.html (accessed 2026-10-20)
- clang-tidy — https://clang.llvm.org/extra/clang-tidy/ (accessed 2026-10-20)
- KDE: clazy — https://invent.kde.org/sdk/clazy (accessed 2026-10-20)
- KDE: source repositories — https://invent.kde.org/ (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The unversioned `qmllint` on this system is a `qtchooser` wrapper that reports version `1.0` and runs the Qt 5 tool; use `qmllint6` (6.11.1) for Qt 6. The available warning categories and CLI flags change between Qt releases, so re-read `qmllint6 --help` on the target branch rather than copying flags from another project. clazy and clang-tidy were not installed locally, so their integration steps above are drawn from their documentation, not from a local run.
