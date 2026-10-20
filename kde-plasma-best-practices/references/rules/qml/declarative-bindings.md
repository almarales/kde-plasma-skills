---
title: "Keep relationships declarative"
impact: P1
scope: qml
tags: [bindings, declarative, qml-performance]
---

# BP-QML-01 — Keep relationships declarative

## Principle

A binding describes a relationship: when its dependencies change, the value follows. An imperative assignment records a snapshot and removes the relationship. Write the relationship as a binding; use JavaScript only for events, one-shot setup, and genuinely imperative actions.

## Why it matters

[Official] Qt lists the costs of the imperative form directly. `Rectangle { Component.onCompleted: color = "red" }` is slower, because the property is evaluated once with a default value and again later; it delays build-time errors to runtime; it "overwrites any declarative binding that was in place"; and it defeats tooling that cannot execute JavaScript.

[Official] A binding with a static value assigned from JavaScript loses the binding. Complex bindings, especially multi-line ones or those containing loops, reduce performance and readability, and code should not rely on binding evaluation order. [Recommendation] Bindings that call into C++ on every dependency change are a plausible source of "QML is slow" reports; the expression is re-evaluated whenever any referenced property changes, including during animations.

## Incorrect

```qml
// Pseudocode: one-shot assignment where a binding belongs.
Rectangle {
    id: root
    property int base: 10
    width: base * 2
    Component.onCompleted: width = 300   // relationship destroyed
}
```

## Preferred

```qml
// Preferred: the value follows its inputs.
Rectangle {
    id: root
    property int base: 10
    property bool pinned: false
    width: pinned ? 300 : base * 2
}
```

```qml
// Preferred: conditional binding with automatic restoration.
Item {
    id: root
    property bool expanded: false
    property int expandedWidth: 400

    Binding on width {
        when: root.expanded
        value: root.expandedWidth
    }
}
```

Use `Qt.binding()` when a binding must be re-established imperatively, for example `root.width = Qt.binding(() => root.base * 2)` after a deliberate assignment.

[Recommendation] Keep binding expressions cheap: resolve ids once, avoid loops, and move formatting or aggregation that runs often into C++ or into a property updated by an explicit signal.

## Exceptions and trade-offs

- `Component.onCompleted` is appropriate for actions that are not property relationships: requesting focus, calling an initialization method, connecting a non-declarative backend.
- A deliberate assignment is fine when the property is an input, not a derived value, and nothing else binds it. Document that decision where the assignment lives.
- Conditional bindings add a restoration state to reason about; when the condition is stable for the object's lifetime, a plain ternary is simpler.

## Review checklist

- [ ] Derived properties are bound, not assigned in `Component.onCompleted`.
- [ ] No binding mutates state or calls a method with side effects.
- [ ] Binding expressions stay short; repeated work is moved to C++ or a cached property.
- [ ] No dependency cycle exists; the application log shows no "Binding loop detected".
- [ ] `Qt.binding()` is used only where a binding is genuinely re-established at runtime.

## References

- [Official] Qt: QML Best Practices — https://doc.qt.io/qt-6/qtquick-bestpractices.html (accessed 2026-10-20)
- [Official] Qt: Property Binding — https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html (accessed 2026-10-20)
- [Official] Qt: Binding QML Type — https://doc.qt.io/qt-6/qml-qtqml-binding.html (accessed 2026-10-20)
- [Official] Qt: Qt QML Type (`Qt.binding`) — https://doc.qt.io/qt-6/qml-qtqml-qt.html (accessed 2026-10-20)
- [Official] Qt: QML Performance Considerations — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation on 2026-10-20. The `Binding` element's `value` expression is evaluated even when `when` is false, so guard against null or undefined inside the expression.
