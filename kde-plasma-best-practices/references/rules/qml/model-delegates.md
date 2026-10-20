---
title: "Use models and delegates that scale"
impact: P1
scope: qml, cpp
tags: [models, delegates, listview, performance]
---

# BP-QML-03 — Use models and delegates that scale

## Principle

A view pays for the delegates it instantiates and for the work each delegate does when it is created, bound, and updated. Use a model that exposes named roles, instantiate only what is visible, keep the delegate small, and keep state out of it.

## Why it matters

[Official] `Repeater` "creates all of its delegate items when the repeater is first created. This can be inefficient if there are a large number of delegate items and not all of the items are required to be visible at the same time." `ListView` instead loads only as many delegates as needed to fill the view, plus whatever `cacheBuffer` allows.

[Official] Delegates "are instantiated as needed and may be destroyed at any time. As such, state should never be stored in a delegate." With `reuseItems: true`, items are recycled, so stale state from a previous row can reappear unless it is reset.

[Official] For model data, "in most cases you should use required properties to pass model data into your delegates". Context-property roles are invisible to tooling and "prevent the Qt Quick Compiler from optimizing your code"; required properties are documented as more performant.

[Official] Delegate guidance: fewer elements, minimum bindings, anchors instead of bindings for relative positioning, no `ShaderEffect`, and never enable clipping on a delegate.

## Incorrect

```qml
// Pseudocode: every row is created up front.
Flickable {
    Column {
        Repeater {
            model: 5000
            delegate: Item { height: 40 }   // 5000 items at load
        }
    }
}
```

## Preferred

```qml
// Pseudocode: contactModel exposes these roles and a toggleSelected(int) method.
ListView {
    model: contactModel
    reuseItems: true
    cacheBuffer: 200                                  // after measuring
    delegate: ItemDelegate {
        required property string name
        required property string email
        required property bool selected
        required property int index

        width: ListView.view.width
        text: name
        highlighted: selected
        onClicked: contactModel.toggleSelected(index)
    }
}
```

The C++ side exposes the roles once, for example through `QAbstractItemModel::roleNames()`, so delegates name them instead of reading an implicit context. Selection and other persistent state live in the model, not in the delegate. [Recommendation] Avoid per-delegate JavaScript allocation in hot paths: string concatenation, `split()`, `RegExp`, and object literals inside frequently re-evaluated bindings allocate on every update. Precompute the display string as a role, or expose it from C++.

## Exceptions and trade-offs

- `cacheBuffer` keeps extra delegates in memory and, in rare cases, can reduce frame rate under memory pressure; pick the value by measurement, not by habit.
- `reuseItems` changes delegate lifecycle. Reset state on the `reused` signal, or keep delegates stateless and skip it.
- `Repeater` is fine for a small, fixed set of items inside a positioner; it becomes a defect when the model can grow.
- A QML `ListModel` is adequate for small static data; move to a C++ model when the data is large, dynamic, or shared.

## Review checklist

- [ ] A repeating view over an unbounded or large model is a `ListView`/`TableView`, not a `Repeater`.
- [ ] Delegates use `required property` for roles, not unqualified context lookups.
- [ ] No state is stored in a delegate; selection and expansion live in the model.
- [ ] Delegates contain no `clip`, no `ShaderEffect`, and no layout attached properties.
- [ ] `cacheBuffer` and `reuseItems` values are justified by a measurement.
- [ ] Hot-path bindings do not allocate strings or objects per evaluation.

## References

- [Official] Qt: ListView QML Type — https://doc.qt.io/qt-6/qml-qtquick-listview.html (accessed 2026-10-20)
- [Official] Qt: Repeater QML Type — https://doc.qt.io/qt-6/qml-qtquick-repeater.html (accessed 2026-10-20)
- [Official] Qt: Models and Views in Qt Quick — https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html (accessed 2026-10-20)
- [Official] Qt: QML Performance Considerations — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)
- [Official] Qt: QML Coding Conventions, required properties — https://doc.qt.io/qt-6/qml-codingconventions.html (accessed 2026-10-20)
- [Official] Qt: QAbstractItemModel — https://doc.qt.io/qt-6/qabstractitemmodel.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation on 2026-10-20. `reuseItems` exists since Qt 5.15 and remains off by default; `required property` in delegates requires Qt 6.
