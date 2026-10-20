---
title: "QObject ownership and lifetime"
impact: P0
scope: "C++ / Qt object model, QML exposure, plugin and singleton lifetimes"
tags: [cpp, qt, ownership, lifetime, qobject, qml]
---

# BP-CPP-01 — QObject ownership and lifetime

## Principle

Every QObject has exactly one stated owner. Choose between three contracts and never blend them: a C++ parent (parent-child ownership), the QML engine (JavaScript ownership), or an explicit C++ owner marked with `CppOwnership`. A pointer that does not own should say so, ideally by being a `QPointer`.

## Why it matters

The engine and the C++ parent destructor can both free an object, so an unstated owner becomes a double delete or a leak. The documented rules are narrow: the QML engine respects QObject parent semantics and never deletes an object that has a parent; when a QObject is returned from an explicit C++ method call the engine assumes ownership unless you called `QQmlEngine::setObjectOwnership(obj, QQmlEngine::CppOwnership)` first; objects created by QML are engine-owned; and a `QML_SINGLETON` built by default construction is created and destroyed by the `QQmlEngine` `[Official]`. Services that must outlive the engine therefore have to be C++-owned.

Deleting from the wrong place is the other half: `delete` on an object from another thread, or while it may still process events, is unsafe. `deleteLater()` posts a `DeferredDelete` event that the object's own event loop eventually handles `[Official]`.

A parent can be stated and still be too broad. A helper parented to a long-lived controller lives for the whole process and accumulates one child per call; `attach()` called repeatedly leaks until the controller dies. Match the parent to the intended lifetime — the narrowest owner that fits it — and give repeated setup a cleanup path. Related: `QObject::property("name")` is untyped and returns an invalid `QVariant` for a property that does not exist, so a typo or a plain `QObject` fails silently `[Official]`. Use a typed getter or check `isValid()`.

## Incorrect

```cpp
// Pseudocode: illustrative only, not production-ready.
// No parent, raw pointer kept in C++, QML assumes ownership on return.
Q_INVOKABLE Session *createSession() {
    m_session = new Session;
    return m_session;
}

void Cache::onInvalidated() {
    delete m_model;      // may run while m_model is emitting or has queued calls
    m_model = nullptr;
}

// Long-lived service handed to QML as an untyped global.
engine.rootContext()->setContextProperty("backend", m_backend);
```

## Preferred

```cpp
// Pseudocode: illustrative only.
// 1. C++ parent decides the lifetime; QML only borrows.
auto *session = new Session(this);
engine.setObjectOwnership(session, QQmlEngine::CppOwnership);

// 2. Or keep engine ownership and hold a QPointer, never a raw pointer.
QPointer<Session> m_session;

// 3. Typed registration instead of context properties.
class Backend : public QObject {
    Q_OBJECT
    QML_ELEMENT
    QML_SINGLETON
public:
    explicit Backend(QObject *parent = nullptr);
};
```

- Prefer `QML_ELEMENT` and `QML_SINGLETON` over `setContextProperty`: context properties are invisible to `qmllint6`, the QML Language Server, and the Qt Quick Compiler, and access to them is reported as unqualified access `[Official]`. A context property is also a non-owning reference: if the C++ object dies while the engine lives, QML is left with a null or invalid object, so make the owner outlive the engine or clear the property during teardown `[Recommendation]`.
- Use `QPointer` for cross-object references that may be destroyed; it nulls itself instead of dangling `[Official]`.
- Mark non-instantiable bases `QML_UNCREATABLE` so QML cannot construct an object whose lifetime C++ controls.

## Exceptions and trade-offs

- `qmlRegisterSingletonInstance()` exposes a C++-owned singleton that must outlive every engine importing it; verify its ownership and thread-affinity requirements for your Qt version `[Recommendation]`.
- `QPointer` protects against dangling references, not against concurrent access.

## Review checklist

- [ ] Every `new` QObject has a stated owner whose lifetime matches the intended scope; repeated setup does not accumulate children on a long-lived parent.
- [ ] Every QObject returned from a `Q_INVOKABLE` is parented or explicitly marked `CppOwnership`.
- [ ] `delete` does not appear where `deleteLater()` is required (cross-thread, in a slot, in a signal path), and a QML-visible component is released only after its replacement exists (`references/plasma-development.md` records the upstream pattern).
- [ ] Cross-object references use `QPointer`; QML-facing types are registered instead of injected as context properties, and required data never comes from an unchecked `QObject::property("name")`.
- [ ] Singletons and services state whether they outlive the engine.

## References

- Qt: Data Ownership — https://doc.qt.io/qt-6/qtqml-cppintegration-data.html (accessed 2026-10-20)
- Qt: Registering an Instantiable Object Type (`QML_ELEMENT`, `QML_SINGLETON`) — https://doc.qt.io/qt-6/qtqml-cppintegration-definetypes.html (accessed 2026-10-20)
- Qt: Context Properties — https://doc.qt.io/qt-6/qtqml-cppintegration-contextproperties.html (accessed 2026-10-20)
- Qt: Threads and QObjects (`deleteLater`, affinity) — https://doc.qt.io/qt-6/threads-qobject.html (accessed 2026-10-20)
- Qt: `QObject` (`deleteLater`, parent-child) — https://doc.qt.io/qt-6/qobject.html (accessed 2026-10-20)
- Qt: `QPointer` — https://doc.qt.io/qt-6/qpointer.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. Ownership rules are documented Qt behaviour and stable across Qt 6.x; registration APIs changed since Qt 5, so re-verify against the Qt version in your target branch rather than an older tutorial. `QML_ELEMENT` only takes effect when the type is processed by `qt_add_qml_module()` or `qmltyperegistrar`.
