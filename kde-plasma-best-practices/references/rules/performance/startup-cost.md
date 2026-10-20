---
title: "Keep startup work off the first frame"
impact: P2
scope: qml, cpp, build
tags: [startup, lazy-loading, loader, plugins]
---

# BP-PERF-04 — Keep startup work off the first frame

## Principle

Startup cost is everything that happens before the first usable frame: object construction, plugin loading, QML compilation, file and network reads, and binding evaluation for objects the user cannot see yet. Defer what the first frame does not need, and measure what remains.

## Why it matters

[Official] Qt's guidance is blunt: "there is no better way to reduce startup time than to avoid doing work you don't need to do, and delaying the work until it is necessary." The same page notes that elements invisible because a parent is invisible should usually be initialized lazily, and that a hidden item still pays for bindings and animations even when it is not painted.

[Official] Building a QML module with `qt_add_qml_module` compiles the listed `QML_FILES` ahead of time, which moves compilation out of the user's startup. Loading plain `.qml` files at runtime leaves that work in the measured path.

[Recommendation] Applet and application startup regressions usually come from a small number of habits: constructing every settings page at launch, instantiating every plugin candidate to test availability, and populating large models synchronously before the window is shown.

[Recommendation] Report startup as a defined window, for example process spawn to first painted frame, and say whether dynamic linking is included. Two numbers with different windows cannot be compared.
## Incorrect

```qml
// Pseudocode: every page is built, then hidden.
StackLayout {
    currentIndex: 0
    SettingsPage {}          // constructed at startup
    PluginBrowserPage {}     // constructed at startup
    AboutPage {}             // constructed at startup
}
```

A hidden `Loader` with `visible: false` is not deferred either: it still loads the source and evaluates bindings.

## Preferred

```qml
// Pseudocode: instantiate a page only when it is selected; root and showFallback are app code.
Loader {
    id: pageLoader
    active: false
    asynchronous: true
    source: ""                            // set when the user navigates
    visible: status === Loader.Ready      // avoid progressive flicker
    onStatusChanged: if (status === Loader.Error) showFallback()
}
```

```cmake
# Preferred: compile QML ahead of time as part of the module.
qt_add_qml_module(app
    URI App
    VERSION 1.0
    QML_FILES Main.qml HeavyGraph.qml
)
```

Also defer plugin instances until their UI is needed, and keep linked shared libraries proportional to what the first frame uses. Both are trade-offs against modularity, not free wins.

## Exceptions and trade-offs

- Deferral adds a loading state, an error path, and a null-item period; a `Loader` around a three-line label is more complexity than it saves.
- State restoration may legitimately need work before the first frame; measure it instead of assuming it is cheap.
- `asynchronous` spreads instantiation across frames and reduces animation glitches, but it does not reduce total work and can show content arriving progressively.
- A warm runtime cache can hide parsing cost. Say whether the measured run included it.

## Review checklist

- [ ] The first frame needs every object constructed before it; the rest is deferred.
- [ ] Deferred pages handle `Loader.Error`, not just `Loader.Ready`.
- [ ] Hidden pages use `active: false` rather than `visible: false` when the cost is construction.
- [ ] QML is compiled through `qt_add_qml_module`, not parsed from loose files in the release package.
- [ ] The startup number states the measurement window, build type, and cache state.

## References

- [Official] Qt: QML Performance Considerations And Suggestions — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)
- [Official] Qt: Loader QML Type — https://doc.qt.io/qt-6/qml-qtquick-loader.html (accessed 2026-10-20)
- [Official] Qt: QML Best Practices — https://doc.qt.io/qt-6/qtquick-bestpractices.html (accessed 2026-10-20)
- [Official] Qt: qt_add_qml_module — https://doc.qt.io/qt-6/qt-add-qml-module.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation on 2026-10-20, Plasma 6.8.0 / KF6 target. `qt_add_qml_module` and the `Loader` properties used here exist across Qt 6; re-check the target branch's CMake API before copying the snippet.
