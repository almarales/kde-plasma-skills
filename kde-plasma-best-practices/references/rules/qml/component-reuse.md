---
title: "Reuse before you reimplement"
impact: P2
scope: qml
tags: [components, kirigami, api-design, maintainability]
---

# Reuse before you reimplement

## Principle

Use the platform's controls first: Qt Quick Controls, then Kirigami components, then a local component. Write a custom control only when a documented limitation of the existing ones blocks the required behavior, and treat that control as an API with a contract, not as a private sketch.

## Why it matters

[Official] Qt's QML best-practices guidance is to browse the list of UI controls before creating a custom one. A custom control re-implements focus handling, keyboard interaction, hover and press states, disabled behavior, accessibility metadata, right-to-left layout, and high-DPI sizing, usually incompletely.

[Official] Kirigami is built on QML and provides high-level components for convergent layouts plus low-level components and a theming API. Reusing those gives KDE applications consistent behavior and theme support without copying internal details.

[Recommendation] Forked controls drift. A local copy of a button that changes one color stops receiving upstream fixes for focus rings, touch targets, and palette changes, and the divergence is invisible until a user reports it.

## Incorrect

```qml
// Pseudocode: a private button that loses platform behavior.
Rectangle {
    id: root
    signal clicked
    color: palette.button
    radius: 4
    Text { anchors.centerIn: parent; text: root.label }
    MouseArea { anchors.fill: parent; onClicked: root.clicked() }
}
```

```qml
// Pseudocode: one component, twelve booleans, no contract.
BaseCard {
    compact: true
    elevated: true
    bordered: false
    dismissible: true
    // ... eight more flags that interact in undocumented ways
}
```

## Preferred

```qml
// Pseudocode: compose the platform control; root.open() belongs to the parent.
ItemDelegate {
    required property string title
    required property string subtitle

    text: title
    onClicked: root.open(title)

    contentItem: Column {
        Text { text: title; elide: Text.ElideRight }
        Text { text: subtitle; opacity: 0.7; visible: subtitle.length > 0 }
    }
}
```

When a custom control is justified, record the limitation it works around in the component's header comment: which standard component was evaluated, which behavior was missing, and which responsibilities (focus, keyboard, accessibility, RTL) the new control now owns. Keep its surface small: required properties as inputs, signals as outputs, no aliases into internal items.

## Exceptions and trade-offs

- A visual element with no interactive behavior (a divider, a badge, a decorative panel) may reasonably be local; it does not re-implement interaction semantics.
- A shared component couples its users to one release cycle. Duplicating twenty lines is often cheaper than a shared abstraction with a wrong contract.
- [Recommendation] Extracting on the second use is usually premature. Extract when the third use confirms the variation is a parameter, not a branch.

## Review checklist

- [ ] The change states why the standard Qt Quick Controls or Kirigami component was insufficient.
- [ ] The custom control documents which behaviors it now owns: focus, keyboard, accessibility, RTL, scaling.
- [ ] Inputs are required properties; outputs are signals; internals are not aliased out.
- [ ] Colors, spacing, and radii come from the theme or palette, not from literals.
- [ ] The abstraction has at least three real users, or a stated reason to exist sooner.

## References

- [Official] Qt: QML Best Practices — https://doc.qt.io/qt-6/qtquick-bestpractices.html (accessed 2026-10-20)
- [Official] Qt: QML Coding Conventions — https://doc.qt.io/qt-6/qml-codingconventions.html (accessed 2026-10-20)
- [Official] KDE: Kirigami UI Framework — https://develop.kde.org/frameworks/kirigami/ (accessed 2026-10-20)
- [Official] KDE: Human Interface Guidelines, Components — https://develop.kde.org/hig/components/ (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 and current KDE developer documentation on 2026-10-20, targeting Plasma 6.8.0 / KF6. Kirigami component availability depends on the KF6 version in the target branch; check the API reference for that version before depending on a component.
