---
title: "Integration tests for QML and KDE components"
impact: P1
scope: "Testing / Qt Quick Test, offscreen runs, config isolation, DBus"
tags: [testing, qml, qtquicktest, offscreen, kconfig, dbus]
---

# Integration tests for QML and KDE components

## Principle

Integration tests drive the real QML tree and the real configuration stack, but never the developer's desktop. Run headless, isolate every writable location into a temporary directory, and treat the session bus, the compositor, and the user's config as external systems you either fake or do without.

## Why it matters

Qt Quick Test runs QML test cases directly against components, and the documentation is explicit that a Qt Quick test case always shows a window even when the code under test involves no visible UI — so it must be run with `-platform offscreen` to stay headless `[Official]`. Keyboard and mouse events can only be delivered once the main window is shown, which is why the documented pattern gates input tests on `when: windowShown` `[Official]`. Asynchronous property changes are asserted with `tryCompare()`, and `waitForRendering()` exists for cases that need a rendered frame `[Official]`.

Configuration is the other isolation problem. `QStandardPaths::setTestModeEnabled(true)` redirects writable locations to test directories so tests do not read or write the user's configuration; on Unix that means `~/.qttest/share`, `~/.qttest/config`, `~/.qttest/state`, and `~/.qttest/cache` `[Official]`. That is better than the real config, but it still writes inside `$HOME`. If a test must leave no trace, point `HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, and `TMPDIR` at a `mktemp -d` directory outside the worktree for the duration of the run.

## Incorrect

```qml
// Pseudocode: illustrative only.
TestCase {
    name: "PanelButton"
    // No `when`: events are delivered before the window is shown.
    function test_click() {
        mouseClick(button)
        compare(button.checked, true)
    }
}
```

## Preferred

```qml
// Pseudocode: illustrative only.
TestCase {
    name: "PanelButton"
    when: windowShown

    function test_click() {
        mouseClick(button)
        tryCompare(button, "checked", true)     // condition-based, with timeout
    }

    function test_label() {
        tryCompare(label, "text", "Ready")
    }
}
```

```cpp
// Pseudocode: illustrative only.
int main(int argc, char **argv) {
    QStandardPaths::setTestModeEnabled(true);   // ~/.qttest, not the real config
    QGuiApplication app(argc, argv);
    return quick_test_main(argc, argv, "panelbutton", QUICK_TEST_SOURCE_DIR);
}
```

- Run the test binary with `-platform offscreen` in CI and record that flag in the test's own documentation.
- Isolate `HOME`/`XDG_*`/`TMPDIR` into a temporary directory created outside the worktree, and let the harness delete it.
- Never touch `QDBusConnection::sessionBus()` services that belong to the running desktop; if a private bus is genuinely needed, start one (`dbus-run-session`) rather than reusing the user's.
- Test KCMs by instantiating the module directly; do not require System Settings or a running Plasma session.

## Exceptions and trade-offs

- Offscreen rendering is not pixel-identical to a GPU session: effects, shaders, and compositing may differ or be unavailable. Visual correctness still needs a human or screenshot check, not just a green test `[Recommendation]`.
- Some plasmoid behaviour only exists inside a containment (panel geometry, location, form factor). Those cases need `plasmoidviewer`/`plasmawindowed` as a manual or dedicated integration step, not a unit test `[Official]`.
- Skipping a DBus-dependent test in CI is honest; silently mocking the whole bus is not.

## Review checklist

- [ ] Qt Quick tests run with `-platform offscreen` in CI.
- [ ] Input tests set `when: windowShown`.
- [ ] Async assertions use `tryCompare()`/`waitForRendering()`, not fixed sleeps.
- [ ] `QStandardPaths` test mode or an isolated `HOME` is set before any config access; temporary directories live outside the worktree and are removed by the harness.
- [ ] No test depends on the user's running desktop, session bus, or Plasma configuration.

## References

- Qt: Qt Quick Test (headless `-platform offscreen`, `QUICK_TEST_MAIN`) — https://doc.qt.io/qt-6/qtquicktest-index.html (accessed 2026-10-20)
- Qt: `TestCase` (`when`, `windowShown`, `tryCompare`, `waitForRendering`) — https://doc.qt.io/qt-6/qml-qttest-testcase.html (accessed 2026-10-20)
- Qt: `QStandardPaths` test mode — https://doc.qt.io/qt-6/qstandardpaths.html (accessed 2026-10-20)
- KDE: Plasma Widget tutorial — testing (`plasmoidviewer`, `plasmawindowed`) — https://develop.kde.org/docs/plasma/widget/testing/ (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The offscreen requirement, `windowShown` idiom, and `QStandardPaths` test-mode locations are documented Qt behaviour for Qt 6. `plasmoidviewer` and `plasmawindowed` are present on this system; their options vary by Plasma version, so read `--help` on the target system instead of copying flags from a tutorial.
