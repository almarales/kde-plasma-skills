---
title: "Do not overwrite bindings by accident"
impact: P1
scope: qml
tags: [bindings, debugging, qmllint, state]
---

# BP-QML-02 — Do not overwrite bindings by accident

## Principle

Assigning a value to a bound property from JavaScript removes the binding. That is sometimes the intent, but when it is not, the UI stops following its data and the bug looks like a stale or frozen value. Decide per property whether it is derived or owned, and make the ownership visible.

## Why it matters

[Official] Qt documents the mechanism plainly: "if the property is later assigned a static value from a JavaScript statement, the binding will be removed." The QML best-practices page lists this as a disadvantage of imperative assignment and points to the diagnostic category below.

[Official] The engine can report lost bindings: enable the informational output with `QLoggingCategory::setFilterRules(QStringLiteral("qt.qml.binding.removal.info=true"))`. Each message is a diagnostic aid, not proof of a defect; some overwrites are intended.

[Recommendation] The usual pattern is a change handler that writes to a property which is also bound. `onValueChanged: root.width = value * 2` either kills `root.width`'s binding or fights it, producing a binding loop and a "Binding loop detected" warning in the log.

[Recommendation] Static tooling helps only up to a point. `qmllint6` (Qt 6) has a `DuplicatePropertyBinding` warning category and flags unqualified access, but it cannot see a runtime assignment made inside a handler. Enable the categories you care about in `.qmllint.ini`:

```ini
[Warnings]
DuplicatePropertyBinding=error
UnqualifiedAccess=warning
```

## Incorrect

```qml
// Pseudocode: a one-time assignment silently ends the relationship.
Item {
    id: root
    property int base: 10
    width: base * 2
    Component.onCompleted: width = 300   // width no longer follows base
}
```

## Preferred

```qml
// Pseudocode: conditional binding; root is the Item from the example above.
Binding {
    target: root
    property: "width"
    value: 300
    when: root.pinned
}
```

The handler example above is also fixed by not writing to a derived property: react to the change on an input (`root.base`) inside `Connections`, and let the binding recompute the derived value.

If a deliberate assignment must be undone, restore the relationship explicitly with `Qt.binding()`. Do not animate a property that must stay bound: an animation writes to the target property, so derive the animated value or disable the binding deliberately and restore it on completion.

## Exceptions and trade-offs

- Assigning to a property that is an input, with no competing binding, is normal and needs no ceremony.
- `Binding` adds an object and a restoration mode to reason about; a plain ternary is clearer when the condition is stable.
- The removal log is noisy in applications that intentionally assign to bound properties. Scope the category to a debugging run instead of shipping it enabled.

## Review checklist

- [ ] Every assignment to a property is either to an input property or documented as an intentional override.
- [ ] Change handlers do not write to properties derived elsewhere.
- [ ] Overrides use `Binding { when: ... }`, a state, or an explicit restore.
- [ ] A debug run with `qt.qml.binding.removal.info=true` shows no unexplained messages.
- [ ] The application log is free of "Binding loop detected" during the scenario.

## References

- [Official] Qt: Property Binding, "Debugging overwriting of bindings" — https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html (accessed 2026-10-20)
- [Official] Qt: QML Best Practices — https://doc.qt.io/qt-6/qtquick-bestpractices.html (accessed 2026-10-20)
- [Official] Qt: Binding QML Type — https://doc.qt.io/qt-6/qml-qtqml-binding.html (accessed 2026-10-20)
- [Official] Qt: qmllint — https://doc.qt.io/qt-6/qtqml-tooling-qmllint.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation and a local `qmllint6` (6.11.1) run on 2026-10-20. The warning categories listed in `.qmllint.ini` come from the documented defaults; `qmllint6` requires type information from the correct import paths.
