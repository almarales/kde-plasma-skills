---
title: "CMake structure for Qt and KF6"
impact: P2
scope: "Build / CMake, ECM, Qt 6 targets, QML modules"
tags: [build, cmake, ecm, qt6, kf6, qml]
---

# CMake structure for Qt and KF6

## Principle

Describe targets, not files. Bootstrap Qt and KF6 once at the top, give each artifact one target, attach sources and QML files to that target explicitly, and link the exact libraries it needs. The build file should read as a dependency declaration, not as a script that collects whatever is on disk.

## Why it matters

CMake's own documentation states that `file(GLOB)` should not be used to collect source files, because adding or removing a file does not change any `CMakeLists.txt` and the generated build system cannot know to regenerate `[Official]`. Qt's `qt_standard_project_setup()` sets `CMAKE_AUTOMOC` and `CMAKE_AUTOUIC` for subsequently created targets, which is what makes `Q_OBJECT` work without per-file boilerplate `[Official]`; calling it after targets exist silently skips them `[Official]`.

`qt_add_qml_module()` is the supported path for QML: it compiles QML ahead of time, wires the module's import URI, and creates the lint targets used by `qmllint` `[Official]`. Since Qt 6.5, `qt_standard_project_setup()` can opt into Qt CMake policies with `REQUIRES`, and policy `QTP0001` makes `/qt/qml/` the default resource prefix for QML modules `[Official]`. Hand-rolled `qt5_add_resources`-style plumbing bypasses all of that.

Target-based linking also keeps the install interface honest: what a library links `PRIVATE` stays out of its consumers' requirements, while `PUBLIC` becomes part of the contract `[Recommendation]`.

## Incorrect

```cmake
# Pseudocode: illustrative only.
cmake_minimum_required(VERSION <target-minimum>)
find_package(Qt6 REQUIRED)

# Glob: new files stay invisible until someone reruns cmake by hand.
file(GLOB SOURCES "src/*.cpp")

# Directory-wide effects leak into every target created afterwards.
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)
link_libraries(Qt6::Core)
qt_add_executable(thing ${SOURCES})
```

## Preferred

```cmake
# Pseudocode: illustrative only.
cmake_minimum_required(VERSION <target-minimum>)
project(thing LANGUAGES CXX)

find_package(ECM 6.31 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})
include(KDEInstallDirs)

find_package(Qt6 6.11 REQUIRED COMPONENTS Core Quick Qml)
find_package(KF6 6.31 REQUIRED COMPONENTS CoreAddons)
qt_standard_project_setup(REQUIRES 6.5)

qt_add_executable(thing src/main.cpp src/controller.cpp src/controller.h)

qt_add_qml_module(thing
    URI Thing
    VERSION 1.0
    QML_FILES qml/Main.qml
    SOURCES src/sessionmodel.cpp src/sessionmodel.h
)

target_link_libraries(thing PRIVATE Qt6::Quick Qt6::Qml KF6::CoreAddons)
```

- List headers next to their sources; `AUTOMOC` needs to see them to generate and attach the meta-object code.
- Put `QML_FILES` in the module and let `qt_add_qml_module()` own the resource prefix instead of adding `.qrc` files by hand.
- Use `PRIVATE`/`PUBLIC` deliberately; every `PUBLIC` link becomes a requirement for downstream consumers.

## Exceptions and trade-offs

- `file(GLOB CONFIGURE_DEPENDS ...)` restores correctness at the cost of re-checking on every build; explicit lists are still clearer and faster.
- Reproducible builds require care with embedded paths and timestamps. If the project claims reproducibility, verify it by building twice in different directories and comparing artifacts; do not assume `qt_add_qml_module()` alone provides it `[Recommendation]`.

## Review checklist

- [ ] No `file(GLOB)` used to collect sources.
- [ ] `qt_standard_project_setup()` is called before any target is created.
- [ ] QML files are declared in `qt_add_qml_module()`, not in hand-written `.qrc` files.
- [ ] Linking is target-based; no `link_libraries()` or `include_directories()` at directory scope.

## References

- CMake: `file()` — GLOB caveat — https://cmake.org/cmake/help/latest/command/file.html (accessed 2026-10-20)
- Qt: `qt_standard_project_setup` — https://doc.qt.io/qt-6/qt-standard-project-setup.html (accessed 2026-10-20)
- Qt: `qt_add_qml_module` — https://doc.qt.io/qt-6/qt-add-qml-module.html (accessed 2026-10-20)
- KDE: Extra CMake Modules — https://api.kde.org/ecm/ (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. `qt_standard_project_setup()` exists since Qt 6.3 and gained `REQUIRES` in 6.5 `[Official]`; older branches must set `CMAKE_AUTOMOC` manually. ECM module names and minimum recommendation change with the framework release, so confirm the `find_package(ECM ...)` version against the target environment before raising or lowering it.
