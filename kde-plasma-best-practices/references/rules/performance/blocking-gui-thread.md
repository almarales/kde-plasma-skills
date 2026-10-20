---
title: "Never block the GUI thread"
impact: P0
scope: cpp, qml
tags: [event-loop, responsiveness, threading]
---

# Never block the GUI thread

## Principle

The GUI thread runs the event loop, evaluates QML bindings, lays out and paints items, and dispatches input. Any work that occupies it past the frame budget is a user-visible defect, not a tuning preference. Move I/O and long computation off it, or make them incremental.

## Why it matters

[Official] Qt's guidance is to "use asynchronous, event-driven programming wherever possible". The same page states that creating a private `QEventLoop` or calling `QCoreApplication::processEvents()` to avoid blocking "should never be used": re-entering the event loop from a signal handler or binding lets the QML engine run other bindings, animations, and transitions, and those can destroy the object hierarchy that contains the nested loop.

[Recommendation] Expect these symptoms rather than a silent slowdown: input latency, frozen animations, a window-manager "not responding" state, and a compositor that stops receiving frame callbacks. At 60 Hz one frame is ~16.7 ms; a synchronous network call does not fit in that budget. Measure on the target to confirm which one the user sees.

[Recommendation] Set the budget for the target device, then verify it there. A development workstation hides stalls that a laptop or a phone exposes.

## Incorrect

```qml
// Pseudocode: blocking work in a QML event handler.
Button {
    onClicked: {
        const text = backend.readConfigSync("/etc/app/config.rc") // blocks
        label.text = backend.parseConfig(text)                   // blocks again
    }
}
```

```cpp
// Pseudocode: hiding the block behind a nested event loop.
QNetworkReply *reply = manager.get(request);
QEventLoop loop;                        // re-enters the event loop
QObject::connect(reply, &QNetworkReply::finished, &loop, &QEventLoop::quit);
loop.exec();                            // bindings and animations keep running
```

`processEvents()` does not make the operation fast. It converts one stall into reentrancy bugs that are harder to reproduce.

## Preferred

```cpp
// Pseudocode: async request, result delivered on the GUI thread.
auto *reply = manager.get(request);             // returns immediately
QObject::connect(reply, &QNetworkReply::finished, this, [this, reply] {
    reply->deleteLater();
    if (reply->error() != QNetworkReply::NoError) {
        Q_EMIT fetchFailed(reply->errorString());
        return;
    }
    Q_EMIT configReady(reply->readAll());
});
```

```qml
// Pseudocode: the handler starts work and returns; backend is app code.
Button { onClicked: backend.fetchConfig() }
Label { text: backend.configText }
```

CPU-bound work goes to `QtConcurrent::run` with a `QFutureWatcher`, or to a worker `QObject` moved to a `QThread`. See `async-work.md` for result delivery, cancellation, and shutdown.

## Exceptions and trade-offs

- A genuinely short, bounded operation may stay inline, but only when the bound is known and measured on target. "It is a small file" is not a bound.
- Work before the first window is shown does not freeze a visible UI, but it still delays startup; account for it under `startup-cost.md`.
- Moving work off-thread adds synchronization, cancellation, and shutdown obligations. Budget for that work instead of adding a thread to hide a design problem.

## Review checklist

- [ ] No `processEvents()`, nested `QEventLoop`, `QThread::sleep()`, `waitForFinished()`, or `QFuture::result()` on the GUI path.
- [ ] Network, disk, DBus round-trips, and parsing of unbounded input are asynchronous.
- [ ] Handlers expected to be fast have a measured upper bound on target hardware.
- [ ] Blocking work in a binding, `Component.onCompleted`, or a delegate is moved out.
- [ ] A QML Profiler or `perf` trace shows no GUI-thread block above the agreed budget.

## References

- [Official] Qt: QML Performance Considerations And Suggestions — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)
- [Official] Qt: Threads and QObjects — https://doc.qt.io/qt-6/threads-qobject.html (accessed 2026-10-20)
- [Official] Qt: QtConcurrent::run — https://doc.qt.io/qt-6/qtconcurrentrun.html (accessed 2026-10-20)
- [Official] Qt: QNetworkAccessManager — https://doc.qt.io/qt-6/qnetworkaccessmanager.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation on 2026-10-20, on a Plasma 6.8.0 / KF6 target. Re-check against the branch you build: Qt 6 minor releases have changed `QFuture` and QML threading details.
