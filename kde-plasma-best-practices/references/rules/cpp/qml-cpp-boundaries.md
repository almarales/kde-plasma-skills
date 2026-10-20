---
title: "QML and C++ boundaries"
impact: P1
scope: "C++ / QML integration, models, exposed API surface"
tags: [cpp, qml, architecture, models, integration]
---

# BP-CPP-04 — QML and C++ boundaries

## Principle

QML declares presentation and interaction; C++ owns state, I/O, and policy. The boundary between them should be a small, typed, documented API: properties to read, signals to react, a few `Q_INVOKABLE` verbs to act, and models to enumerate. Everything else stays on the C++ side.

## Why it matters

Qt's own best-practices page recommends separating UI from business logic and warns against duplicating state that belongs in a model `[Official]`. The cost of a wide boundary is paid on every frame: property reads that cross into C++ can allocate and convert, and property resolution plus JavaScript execution are explicitly listed as performance costs in the Qt Quick performance guide `[Official]`. That guide also notes the Qt Quick Compiler makes simple bindings fast, so the risk is not "JavaScript is slow" but "unnecessary or repeated cross-boundary work is slow" `[Official]`.

A typed boundary also buys tooling: types registered through `qt_add_qml_module()` are visible to `qmllint6`, the QML Language Server, and the compiler, while context properties are invisible to all three `[Official]`.

## Incorrect

```qml
// Pseudocode: illustrative only.
// Business logic, I/O, and formatting implemented in QML.
Item {
    function refresh() {
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            var rows = JSON.parse(xhr.responseText)
            for (var i = 0; i < rows.length; ++i)
                list.append({ "name": rows[i].n.toUpperCase() })
        }
        xhr.open("GET", "https://example.invalid/sessions")
        xhr.send()
    }
}
```

## Preferred

```cpp
// Pseudocode: illustrative only.
class SessionModel : public QAbstractListModel {
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(bool busy READ busy NOTIFY busyChanged)
public:
    Q_INVOKABLE void refresh();       // verbs, not implicit remote properties
signals:
    void busyChanged();
};
```

```qml
// Pseudocode: illustrative only.
ListView {
    model: SessionModel { id: sessions }
    delegate: Text { text: model.name }
}
BusyIndicator { running: sessions.busy }
```

- Expose a model instead of a `QVariantList` of maps when rows change incrementally; `QAbstractItemModel` gives views the roles and notifications they need `[Official]`.
- Keep the QML-facing API minimal: read-only properties plus explicit verbs. Every exposed member is a compatibility promise.
- Never leave heavy loops in bindings or `onCompleted` handlers; move them to C++ and deliver a result `[Recommendation]`.

## Exceptions and trade-offs

- Prototypes and throwaway tools may use `XMLHttpRequest` or inline JS for iteration speed; do not ship that shape in a plasmoid or KCM.
- A `Q_INVOKABLE` returning a newly allocated QObject shifts ownership to the engine unless the object is parented or marked `CppOwnership`.

## Review checklist

- [ ] Business rules, network access, and persistence live in C++, not in `.qml` or `.js`.
- [ ] The QML-facing API is enumerated and reviewed as a compatibility surface.
- [ ] Collections that change incrementally are models, not rebuilt arrays.
- [ ] No non-trivial loop or allocation runs inside a binding or a per-frame handler.
- [ ] Types are registered with `QML_ELEMENT`/`QML_SINGLETON`; user-visible strings go through `i18n()`.

## References

- Qt: Best Practices for QML and Qt Quick (separate UI from logic, store state in models) — https://doc.qt.io/qt-6/qtquick-bestpractices.html (accessed 2026-10-20)
- Qt: Performance considerations and suggestions (bindings, JS, property resolution) — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)
- Qt: Overview — QML and C++ integration — https://doc.qt.io/qt-6/qtqml-cppintegration-overview.html (accessed 2026-10-20)
- Qt: Data Type Conversion Between QML and C++ — https://doc.qt.io/qt-6/qtqml-cppintegration-data.html (accessed 2026-10-20)
- Qt: Defining QML Types from C++ — https://doc.qt.io/qt-6/qtqml-cppintegration-definetypes.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The boundary guidance is stable across Qt 6.x. `QML_ELEMENT` requires CMake processing by `qt_add_qml_module()`; hand-written `qmlRegisterType()` calls still work but lose the compile-time tooling benefits described above.
