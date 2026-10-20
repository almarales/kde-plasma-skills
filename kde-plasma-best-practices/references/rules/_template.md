---
title: "Imperative rule title"
impact: P2
scope: qml
tags: [topic, topic]
---

# Imperative rule title

> **Template, not a rule.** Copy this file, replace every placeholder, and delete this notice. A rule that still contains placeholder text is not ready to publish. Keep only claims you verified against the target branch.

## Principle

State the rule in one or two sentences. Name the mechanism, not the symptom. If the rule only holds under a precondition, say so here.

## Why it matters

Explain the consequence: correctness, responsiveness, memory, maintainability, or accessibility. Support it with the authoritative statement and label the claim:

- `[Official]` documented by Qt, KDE, or another primary source, with a checked URL.
- `[Observed]` reproduced in a repository, build, or runtime you inspected; say where.
- `[Recommendation]` engineering judgement from this skill, not vendor policy.
- `[Experimental]` plausible but unverified; never presented as approved.
- `[Unknown]` open question; state which evidence would settle it.

## Incorrect

```qml
// Pseudocode: smallest reproduction of the bad pattern.
Item {
    property int value: 0
}
```

One sentence on why this is wrong. A reader must recognize the bad pattern without reading the prose twice.

## Preferred

```qml
// Preferred: smallest correct version of the same behavior.
Item {
    property int value: 0
}
```

Point to a shipped helper or component when one exists; never invent an API.

## Exceptions and trade-offs

Name at least one legitimate exception and its cost. If the rule is unconditional, say so and explain why. State the measurable condition under which the trade-off is acceptable.

## Review checklist

- [ ] Observable check a reviewer can run on the diff.
- [ ] Second check tied to the rule's mechanism.
- [ ] Check that any exception used is documented in the change.

## References

- [Official] Publisher: Page title — https://doc.qt.io/qt-6/ (accessed 2026-10-20)

Replace this example with the sources you actually opened. Do not cite an unchecked URL.

## Version notes

- Verified against Plasma 6.8.0, Qt 6.11.1, KF6, `qmllint6` (Qt 6.11.1) available (2026-10-20). The unversioned `qmllint` on the verification machine is a Qt 5 wrapper.
- Re-verify against the target branch and Qt minor version before publishing.
