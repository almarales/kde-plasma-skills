---
title: "Signal/slot connections and cleanup"
impact: P1
scope: "C++ / Qt signalling, QML signal handlers, cross-thread delivery"
tags: [cpp, qt, signals, slots, connections, threads]
---

# Signal/slot connections and cleanup

## Principle

A connection is a lifetime contract between two objects, so state it explicitly: who is the receiver, which thread delivers, and when it dies. Use the context-object overload for lambdas, choose the connection type on purpose, and disconnect by handle rather than by guesswork.

## Why it matters

Qt documents the four delivery modes precisely `[Official]`:

- **Auto** — direct when the emitting thread is the receiver's thread, queued otherwise.
- **Direct** — the slot runs immediately in the emitter's thread, which is unsafe across threads when the receiver has an event loop.
- **Queued** — the slot runs later in the receiver's thread, via its event loop.
- **BlockingQueued** — queued, but the emitting thread blocks until the slot returns; used between objects in the same thread it deadlocks.

Two failure modes follow. A lambda connected without a context object outlives its captures, because nothing disconnects it when the captured object dies; Qt 6.7 added `QT_NO_CONTEXTLESS_CONNECT` specifically because that overload is error prone and always direct `[Official]`. And a disconnected queued connection may still deliver an already-scheduled call, so "disconnect" is not cancellation `[Official]`.

## Incorrect

```cpp
// Pseudocode: illustrative only.
// Context-less lambda: stays connected after `this` dies, captured state dangles.
connect(m_watcher, &Watcher::finished, [this] { updateUi(); });

// Wrong thread assumption: direct cross-thread slot touches GUI state.
connect(m_worker, &Worker::progress, this, &Panel::setProgress, Qt::DirectConnection);

// Repeat connections on every refresh; each call adds another delivery.
connect(m_model, &Model::changed, this, &Panel::refresh);
```

## Preferred

```cpp
// Pseudocode: illustrative only.
// Context object ties the connection to `this` and delivers in this thread.
connect(m_watcher, &Watcher::finished, this, [this] { updateUi(); });

// Keep the handle when the connection must be severed before destruction.
m_connection = connect(m_source, &Source::changed, this, &Panel::refresh);
disconnect(m_connection);

// Idempotent re-connection of the same signal/slot pair.
connect(m_model, &Model::changed, this, &Panel::refresh, Qt::UniqueConnection);
```

- Prefer pointer-to-member or context-object lambdas over `SIGNAL()`/`SLOT()` macros; the string forms are resolved at run time and mismatch silently.
- Prefer `Qt::UniqueConnection` for connections created in code paths that can run more than once, such as model re-attachment or panel reconfiguration.
- Store `QMetaObject::Connection` handles for lambdas; functors cannot be disconnected by name `[Official]`.
- Verify that objects used inside a lambda stay alive; the context object protects the connection, not the captures `[Official]`.

## Exceptions and trade-offs

- `Qt::DirectConnection` is legitimate for same-thread signalling and for deliberately synchronous notification, such as a model telling its own view that a row changed.
- `Qt::BlockingQueuedConnection` is legitimate only when the receiver lives in another thread with a running event loop and the emitter can afford to block; it must never be used to call back into the emitter.
- Connections to `destroyed()` and to owner objects are frequently redundant: a connection is removed when either endpoint is destroyed `[Official]`. Disconnect-all also drops `destroyed()`, which can break cleanup elsewhere, so disconnect specific signals instead `[Official]`.
- `Qt::UniqueConnection` compares the same signal/slot pair only; a second lambda with identical captures still creates a second connection.

## Review checklist

- [ ] Every lambda connection passes a context object (or the project defines `QT_NO_CONTEXTLESS_CONNECT`).
- [ ] Each connection type is explicit where threads differ; no accidental `DirectConnection` into GUI objects.
- [ ] Re-entrant setup paths use `Qt::UniqueConnection` or disconnect first.
- [ ] Long-lived connections have a stated disconnect point and a stored handle where needed.
- [ ] Cancellation does not rely on `disconnect()` alone for queued connections.

## References

- Qt: Signals & Slots — https://doc.qt.io/qt-6/signalsandslots.html (accessed 2026-10-20)
- Qt: Threads and QObjects (connection types, cross-thread rules) — https://doc.qt.io/qt-6/threads-qobject.html (accessed 2026-10-20)
- Qt: `QObject::connect` / `disconnect` — https://doc.qt.io/qt-6/qobject.html (accessed 2026-10-20)
- Qt: `Qt::ConnectionType` — https://doc.qt.io/qt-6/qt.html (accessed 2026-10-20)
- Qt: `QMetaObject::Connection` handling — https://doc.qt.io/qt-6/qobject.html#connect (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. Connection semantics are stable across Qt 6.x. `QT_NO_CONTEXTLESS_CONNECT` exists since Qt 6.7 `[Official]`; enabling it on an older branch will simply have no effect, so check the target Qt version before relying on it as a guardrail.
