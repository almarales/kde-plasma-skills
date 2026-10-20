---
title: "Scope timers and animations to visible surfaces"
impact: P2
scope: "QML / repeating timers, animations, polling, hidden or collapsed surfaces"
tags: [qml, performance, timers, animations, visibility, plasma]
---

# Scope timers and animations to visible surfaces

## Principle

A repeating timer or a running animation is work with a cost per tick. Bind `running` to the condition that makes the work useful — visibility, expansion, or an explicit user-started state — instead of starting it unconditionally and leaving it on.

## Why it matters

A repeating `Timer` keeps waking the event loop until `running` becomes false. At a 16 ms interval that is roughly 60 wakeups per second, and each tick runs its handler on the GUI thread. A collapsed Plasma applet is still loaded: a timer created for the full representation can keep firing while the compact representation is shown, spending CPU and battery on a surface nobody is looking at `[Recommendation]`.

Qt Quick animations are driven by the render loop. An animation that keeps running offscreen still advances state and can keep the scene graph busy. Stopping it when the target is not visible removes work without changing the visible result `[Recommendation]`.

The QML `Timer` type documents `interval`, `repeat`, and `running`; a repeating timer triggers until it is stopped, and a triggering whose handling overruns the interval restarts the count `[Official]`. Nothing in the type stops it when the surrounding item becomes invisible.

## Incorrect

```qml
// Pseudocode: illustrative only.
// Runs at ~60 Hz for the whole process, even when the widget is collapsed.
Timer {
    interval: 16
    repeat: true
    running: true
    onTriggered: root.tick()
}

// An animation that keeps running behind a hidden page.
NumberAnimation {
    target: indicator
    property: "rotation"
    from: 0; to: 360
    duration: 1000
    loops: Animation.Infinite
    running: true
}
```

## Preferred

```qml
// Pseudocode: illustrative only.
Timer {
    interval: 16
    repeat: true
    // Full representation only; verify the property in the target Plasma branch.
    running: root.visible && plasmoid.expanded
    onTriggered: root.tick()
}

NumberAnimation {
    target: indicator
    property: "rotation"
    from: 0; to: 360
    duration: 1000
    loops: Animation.Infinite
    running: root.visible
}
```

- Prefer a signal or a model change over polling. A timer is justified when the source cannot notify you, and the interval should be the slowest that meets the requirement.
- If the work must continue while hidden (for example a download or a notification watcher), keep it out of the view layer and document why the timer stays active.
- One-shot timers (`repeat: false`) are not the problem; the rule targets repeating work.

## Exceptions and trade-offs

- A timer that keeps a cache warm or drives a background service may need to run while the surface is hidden. That is a service concern: move it out of the QML view and state the lifetime.
- `visible: false` does not always mean the item is cheap to keep: bindings can still evaluate. Stop the timer as well.

## Review checklist

- [ ] Every repeating `Timer` binds `running` to visibility, expansion, or an explicit user action; no unconditional `running: true` remains for work that only matters while shown.
- [ ] Animations stop when their target is not visible, except deliberate background progress.
- [ ] Polling intervals are justified, and the claimed saving was measured rather than assumed.

## References

- Qt: `Timer` QML Type — https://doc.qt.io/qt-6/qml-qtqml-timer.html (accessed 2026-10-20)
- Qt: Animation QML Type — https://doc.qt.io/qt-6/qml-qtquick-animation.html (accessed 2026-10-20)
- Qt: Qt Quick Performance Considerations — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The `Timer` API is stable across Qt 6. Plasma visibility properties such as `Plasmoid.expanded` and the exact `visible` semantics of a representation vary by release; confirm them in the target branch.
