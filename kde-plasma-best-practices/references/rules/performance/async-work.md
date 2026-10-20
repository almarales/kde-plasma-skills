---
title: "Deliver async results safely to the GUI thread"
impact: P1
scope: cpp, qml
tags: [threading, queued-connections, lifetime, cancellation]
---

# Deliver async results safely to the GUI thread

## Principle

Background work is only half the contract. The other half is a defined path back: a queued signal, a `QFutureWatcher`, or an explicit queued invocation, delivered to a receiver that is guaranteed to exist, with cancellation and shutdown decided before the first line is written.

## Why it matters

[Official] A `QObject` lives in the thread that created it, and events for it are dispatched by that thread's event loop. A queued connection runs the slot in the receiver's thread; an auto connection becomes queued when sender and receiver live in different threads. GUI classes, notably `QWidget` and subclasses, are not reentrant and may only be used from the main thread.

[Official] Deleting a `QThread` while it is still running crashes the program; wait for `finished()` first. Deleting a `QObject` from another thread is unsafe unless you know it is not processing events; use `deleteLater()` so the owning thread performs the deletion. A `QFuture` returned by `QtConcurrent::run()` cannot be canceled, so cancellation must be designed into the work: a `QPromise` that checks `isCanceled()`, or an atomic flag the worker polls.

[Recommendation] The most common lifetime bug is a lambda that captures `this` raw and runs on a pool thread after the receiver was destroyed. Always pass a context object to `connect`, or guard the capture with `QPointer`.

## Incorrect

```cpp
// Pseudocode: worker writes UI state directly and outlives the receiver.
QtConcurrent::run([this] {
    const QImage scaled = renderPreview();      // CPU work: acceptable
    m_previewLabel->setPixmap(QPixmap::fromImage(scaled)); // GUI thread only
    m_ready = true;                             // data race with QML bindings
});
```

A context-free connection — a lambda with no receiver object — has the same defect: nothing ties it to the receiver's lifetime.

## Preferred

```cpp
// Pseudocode: worker object with queued results and an ordered shutdown.
class Worker : public QObject { Q_OBJECT
signals:
    void chunkReady(const Result &r);
    void finished();
public slots:
    void run() {
        while (!m_cancel.loadAcquire()) Q_EMIT chunkReady(computeChunk());
        Q_EMIT finished();
    }
private:
    std::atomic_bool m_cancel{false};
};
// Owner side: the context object ties each connection to the receiver.
auto *thread = new QThread(this);
auto *worker = new Worker;
worker->moveToThread(thread);
connect(thread, &QThread::started, worker, &Worker::run);
connect(worker, &Worker::finished, thread, &QThread::quit);
connect(worker, &Worker::chunkReady, this, &Controller::applyChunk); // queued
connect(thread, &QThread::finished, worker, &QObject::deleteLater);
thread->start();
// Shutdown: requestCancellation(); thread->quit(); thread->wait();
```

Use `QFutureWatcher` when the work is a `QFuture`: connect to `finished()` or `resultReadyAt()`, parent the watcher to the GUI object, and read the result only after the notification. See `QtConcurrent::run`.

## Exceptions and trade-offs

- Fire-and-forget work with no UI effect and no captured `QObject` needs no result channel, but it still needs a shutdown story.
- A short task may run on the GUI thread when its bound is measured; see `blocking-gui-thread.md`.
- A dedicated `QThreadPool` isolates long jobs from the global pool used by other `QtConcurrent::run` callers, at the cost of another pool's memory and tuning.

## Review checklist

- [ ] No worker thread touches `QQuickItem`, `QWidget`, `QPixmap`, or a QML-owned property.
- [ ] Every cross-thread connection names a context object or uses `QPointer`.
- [ ] `QFutureWatcher` results are read in `finished()` or `resultReadyAt()`, never via `result()` on the GUI path.
- [ ] Cancellation is cooperative and documented; no code assumes `QFuture::cancel()` stops `QtConcurrent::run`.
- [ ] Shutdown order is explicit: request, quit, `wait()`, then delete; no running `QThread` is destroyed.
- [ ] Errors reach the UI as a signal or a result type, not as a silent `qWarning()`.

## References

- [Official] Qt: Threads and QObjects — https://doc.qt.io/qt-6/threads-qobject.html (accessed 2026-10-20)
- [Official] Qt: QThread — https://doc.qt.io/qt-6/qthread.html (accessed 2026-10-20)
- [Official] Qt: QFuture — https://doc.qt.io/qt-6/qfuture.html (accessed 2026-10-20)
- [Official] Qt: QFutureWatcher — https://doc.qt.io/qt-6/qfuturewatcher.html (accessed 2026-10-20)
- [Official] Qt: QtConcurrent::run — https://doc.qt.io/qt-6/qtconcurrentrun.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation on 2026-10-20. `QFuture` gained continuations in Qt 6.0 (`then`, `onCanceled`, `onFailed`); older code that polls `isFinished()` is not a safe substitute for a watcher.
