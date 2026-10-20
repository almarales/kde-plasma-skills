---
title: "KDE and Qt API compatibility"
impact: P1
scope: "Architecture / Qt, KF6, Plasma, ECM, CMake minimums"
tags: [architecture, compatibility, versioning, kde-frameworks, qt, cmake]
---

# KDE and Qt API compatibility

## Principle

State the platform you support, encode it in the build files, and treat every API from a newer version as opt-in. The target branch — not the newest documentation page — decides which symbols, properties, and CMake modules are available.

## Why it matters

Qt and KDE Frameworks evolve on separate schedules, and documentation sites serve the latest release by default. A symbol that exists in Qt 6.12 docs may not exist in the 6.11 the project builds against, and a KF6 API page describes the newest framework rather than the one in the target distribution. The mismatch is invisible at review time and obvious at build time on someone else's machine.

KDE's binary compatibility policy also makes API use a long-term decision: exported classes and their virtuals are constrained, so an accidental dependency on an internal symbol is not a local mistake you can fix later `[Official]`. Qt provides `QT_VERSION_CHECK` for compile-time guards `[Official]`, and the Plasma 6 porting guide shows how much moved between major versions — `Plasmoid`/`PlasmoidItem`, metadata format, and imports all changed `[Official]`.

## Incorrect

```cmake
# Pseudocode: illustrative only.
# Floating minimums: builds here, fails on the target distro.
find_package(Qt6 REQUIRED COMPONENTS Quick)
find_package(KF6 REQUIRED COMPONENTS CoreAddons)
```

```cpp
// Pseudocode: illustrative only.
// Guard that silently drops the feature instead of stating support.
#if QT_VERSION >= QT_VERSION_CHECK(6, 99, 0)
    useNewApi();
#endif
```

## Preferred

```cmake
# Pseudocode: illustrative only.
cmake_minimum_required(VERSION <target-minimum>)
find_package(ECM 6.31 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

find_package(Qt6 6.11 REQUIRED COMPONENTS Core Quick Qml)
find_package(KF6 6.31 REQUIRED COMPONENTS CoreAddons Config)
```

```cpp
// Pseudocode: illustrative only.
#if QT_VERSION >= QT_VERSION_CHECK(6, 9, 0)
    // API introduced in 6.9; the minimum stays 6.11, so this is documentation,
    // not a compatibility shim.
#endif
```

- Pin minimums to the versions you actually test, and bump them deliberately when you adopt newer APIs.
- Verify each uncertain symbol against `api.kde.org` for the target framework branch and against the installed headers, rather than a tutorial or the newest docs page.
- Keep one place that defines the platform floor; do not repeat version numbers across subdirectories.
- Prefer a raised minimum over an ever-growing pile of `#if` branches. Conditional code doubles the paths you must test.
- When porting from Plasma 5 material, re-check imports, metadata, and component names against the Plasma 6 guide before copying `[Official]`.

## Exceptions and trade-offs

- Distributions that ship older frameworks justify a compatibility branch, but then both branches need build coverage; an untested branch is not support.
- Feature detection by symbol (`__has_include`, CMake `check_cxx_source_compiles`) is sometimes better than version comparison, but it hides intent and complicates reasoning. Use it only for genuinely optional integrations.
- Optional dependencies are legitimate for features that degrade gracefully, provided the degraded path is tested.
- Raising a minimum version is a product decision; document it in the release notes rather than letting it happen implicitly through a dependency bump.

## Review checklist

- [ ] The supported Qt, KF6, and Plasma versions are written down in one place.
- [ ] Every `find_package()` carries a minimum version.
- [ ] No API newer than the stated minimum is used without a guard or a minimum bump.
- [ ] Porting advice taken from Plasma 5 material has been re-checked against the Plasma 6 guide.
- [ ] Symbols that changed in the target branch were verified in `api.kde.org` or the installed headers.
- [ ] Conditional branches have matching build coverage.

## References

- Qt: `QT_VERSION_CHECK` and version macros — https://doc.qt.io/qt-6/qtversionchecks.html (accessed 2026-10-20)
- Qt: `qt_standard_project_setup` (policies and defaults) — https://doc.qt.io/qt-6/qt-standard-project-setup.html (accessed 2026-10-20)
- KDE: API documentation index — https://api.kde.org/ (accessed 2026-10-20)
- KDE: Extra CMake Modules — https://api.kde.org/ecm/ (accessed 2026-10-20)
- KDE: Binary Compatibility Issues With C++ — https://community.kde.org/Policies/Binary_Compatibility_Issues_With_C%2B%2B (accessed 2026-10-20)
- KDE: Porting Plasmoids to KF6 — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-20)

## Version notes

Local target verified 2026-10-20: Plasma 6.8.0, Qt 6.11.1, KF6 with ECM 6.31.0. These are the versions this skill assumes, not universal requirements: a different checkout must restate them from its own `CMakeLists.txt`. `api.kde.org` serves the newest framework docs, so confirm the branch you are reading matches the KF6 release you build against.
