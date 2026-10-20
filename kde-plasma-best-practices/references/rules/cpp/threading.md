---
title: "Thread affinity, cancellation, and shutdown"
impact: P0
scope: "C++ / Qt threading, QThread, QtConcurrent, QThreadPool, application shutdown"
tags: [cpp, qt, threading, qthread, concurrency, shutdown]
---

# BP-CPP-03 — Thread affinity, cancellation, and shutdown

## Principle

Treat a QObject's thread affinity as part of its type contract. Create it in the thread that will run it, move it before it has a parent or children, communicate with queued signals, and give every worker a defined stop path that runs before the owner is destroyed.

## Why it matters

Qt documents the constraints directly `[Official]`:

- An object lives in the thread where it was created, and that thread's event loop dispatches its events.
- `moveToThread()` moves the object and its children, and **cannot move an object that has a parent**.
- A child must always be created in the thread where its parent was created, which is why passing the `QThread` object as parent of objects created in `run()` is wrong.
- Without a running event loop, timers never fire and `deleteLater()` never runs.
- All objects created in a thread must be deleted before the `QThread` is deleted.

The GUI classes are not reentrant and may only be used from the main thread `[Official]`. A worker that touches a `QQuickItem`, a model attached to a view, or a widget from another thread is a correctness bug, not a performance trade-off.

## Incorrect

```cpp
// Pseudocode: illustrative only.
// Worker parented to a controller that lives in another thread.
auto *worker = new Worker(this);          // parent in GUI thread
worker->moveToThread(&m_thread);          // no-op: object has a parent

// Slots on a QThread subclass run in the creating thread, not the new one.
class Job : public QThread {
    Q_OBJECT
public slots:
    void startWork();                      // runs in the old thread
};
// No event loop: deleteLater and timers silently never happen.
void Job::run() { auto *t = new QTimer; t->start(100); }
```

## Preferred

```cpp
// Pseudocode: illustrative only.
auto *worker = new Worker;                 // no parent
worker->moveToThread(&m_thread);
connect(&m_thread, &QThread::finished, worker, &QObject::deleteLater);
connect(this, &Controller::request, worker, &Worker::handle);
connect(worker, &Worker::result, this, &Controller::apply);
m_thread.start();

// Shutdown: ask, wait, then let the owner go away.
m_thread.quit();
m_thread.wait();
```

- Prefer the worker-object pattern: `moveToThread()` plus queued signals, as shown in the Qt `QThread` documentation `[Official]`.
- Subclassing `QThread` is acceptable when the work is a single `run()` body that needs no event loop and no slots. It is not acceptable to add slots to the subclass and expect them to run in the new thread `[Official]`.
- Use `QtConcurrent::run()` and `QThreadPool` for short, independent tasks that do not need a dedicated event loop; report through `QFutureWatcher`, which emits in the thread where the watcher lives `[Official]`.
- Protect shared state with `QMutex`/`QMutexLocker` or atomics; `QObject` and the whole event-delivery system are not thread-safe `[Official]`.
- Make cancellation cooperative: a `std::atomic<bool>` checked in the work loop, plus a documented maximum wait, so shutdown cannot hang forever.

## Exceptions and trade-offs

- A dedicated `QThread` is justified for a long-lived subsystem that owns several QObjects and its own timers or sockets; a thread pool is better for many short jobs.
- `QThread::terminate()` is not a shutdown strategy: it can leave locks held and objects half-destroyed. Use a cancellation flag and `wait()`.
- `QMutex` is a correctness tool, not a throughput tool; if a hot path needs a mutex on every frame, restructure the ownership instead.

## Review checklist

- [ ] Every QObject is created in the thread that will run it.
- [ ] `moveToThread()` is called before a parent or children are attached.
- [ ] No `QThread` object is used as the parent of objects created inside `run()`.
- [ ] Every worker thread has an explicit `quit()`/`wait()` shutdown path before its owner is destroyed.
- [ ] Cross-thread communication uses signals or `postEvent`, not direct calls into a live QObject.
- [ ] Cancellation is cooperative and bounded, never `terminate()`; GUI types are touched only from the main thread.

## References

- Qt: Threads and QObjects — https://doc.qt.io/qt-6/threads-qobject.html (accessed 2026-10-20)
- Qt: `QThread` (worker-object pattern, subclassing constraints) — https://doc.qt.io/qt-6/qthread.html (accessed 2026-10-20)
- Qt: `QThreadPool` — https://doc.qt.io/qt-6/qthreadpool.html (accessed 2026-10-20)
- Qt: Qt Concurrent — https://doc.qt.io/qt-6/qtconcurrent-index.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. Thread-affinity rules have been stable since Qt 4 and remain documented as above in Qt 6. `QFuture`-based cancellation support differs per API; confirm the contract of the specific call you use instead of assuming a running task can be interrupted.
