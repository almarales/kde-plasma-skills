---
title: "Keep main.qml a composition root; representations live in their own files"
impact: P2
scope: qml
tags: [plasmoid, representations, composition-root, structure, maintainability]
---

# BP-QML-07 — Keep `main.qml` a composition root; representations live in their own files

## Principle

`ui/main.qml` is the composition root of a Plasma 6 widget: the `PlasmoidItem`, the configuration bindings, the backend object that owns process and timer logic, and the assignment of `compactRepresentation` / `fullRepresentation` to components defined in their own files under `contents/ui/`. A representation body inlined in `main.qml` couples the always-loaded panel face to the popup subtree and re-parses the whole popup with the widget.

Load the companion rules as usual: `qml/component-reuse.md` governs the contract of each extracted component, `qml/loader-usage.md` governs deliberate deferred creation inside a representation.

## Why it matters

- `[Official]` Plasma 6 requires the root QML object to be a `PlasmoidItem` and keeps `compactRepresentation` / `fullRepresentation` / `preferredRepresentation` as its properties: https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-22).
- `[Official]` `ui/main.qml` is always the widget entry point and `X-Plasma-MainScript` no longer selects a custom one: https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-22).
- `[Official]` Widget popups are lazy-loaded: `fullRepresentationItem` "is `null` until the popup is opened" — https://develop.kde.org/docs/plasma/widget/properties/ (accessed 2026-10-22).
- `[Recommendation]` The lazy instantiation of the popup applies to the subtree the engine evaluates when the popup opens. An inline representation body is part of `main.qml`'s compilation unit, so the collapsed widget pays for its parse; an external `FullView.qml` referenced only by the representation defers its parse to the first expand. Measure the difference on the target build before claiming a startup cost.
- `[Recommendation]` Composition-root thresholds used by this skill and by `lint_qml.py` (EN03/EN04): an inline representation body should stay under ~30 whole lines, and `main.qml` under ~200 lines. They are engineering judgement, not KDE policy; extract when a body crosses them, not at ten lines.
- `[Recommendation]` The backend logic (process spawning and parsing, polling timers) belongs in its own component, so the popup face and the panel face both consume the same clean properties. Graphs, gauges, and lists in a GlassWire-style widget belong in sub-files so one error names one file.
- `[Observed]` A 1,167-line `main.qml` with an inline ~226-line `fullRepresentation` and an inline ~34-line `compactRepresentation` passes every pre-existing check in this bundle's `lint_qml.py`; hyalonet ships exactly that shape, and its `po/*.pot` anchors translations to dozens of `main.qml` line numbers, so every edit above the popup churns the whole translation catalog.

## Incorrect

```qml
// Pseudocode: the popup and the graph live inside main.qml, parsed with the widget.
PlasmoidItem {
    id: root
    Timer {
        interval: 1000
        running: true
        onTriggered: parseNetHogsOutput()   // backend logic inside the UI file
    }
    fullRepresentation: ColumnLayout {      // ~226 lines inline
        GlassWireGraph { ... }
        DataDonut { ... }
        AppTrafficList { ... }
        // ...
    }
}
```

The popup subtree is compiled with `main.qml`, backend logic is unreachable from a second representation or view, and every future edit re-reads a thousand-line file.

## Preferred

```qml
// Pseudocode: main.qml is the composition root (see the builder scaffold for the real shape).
NetworkBackend {
    id: backend          // owns the process and timers; exposes plain properties
}

compactRepresentation: CompactView {
    bytesInSession: backend.sessionBytes
}

fullRepresentation: FullView {
    processList: backend.processList
}
```

`CompactView.qml`, `FullView.qml`, and the heavy qml subtrees (`GlassWireGraph.qml`, `DataDonut.qml`, `AppTrafficList.qml`) are files under `contents/ui/`. Sub-components take data in as `required property` and report actions back as signals (see `qml/component-reuse.md`); `main.qml` binds the two sides.

## Exceptions and trade-offs

- A widget whose full representation is one control may inline it; `kde-plasma-builder`'s scaffold does exactly that within the thresholds. The cost of extraction (one more file, indirection when reading the asymmetrical pair) outweighs the benefit below the guideline.
- `preferredRepresentation: Plasmoid.fullRepresentation` icons that render full-width on the desktop pay the parse at load regardless; the split is then maintainability, not startup.
- Many small files marginally win on startup but lose on grepability. Extract one responsibility per file; do not split a 26-line view into eight.
- The `[Official]` guarantees cover the API surface, not the line numbers: thresholds here are this skill's judgement and may be revised against measurements.

## Review checklist

- [ ] `main.qml` declares only the `PlasmoidItem`, configuration bindings, the backend, and representation assignment.
- [ ] Each inlined representation body is under ~30 whole lines or carries a written justification in the change.
- [ ] `main.qml` is under ~200 lines or carries a written justification in the change.
- [ ] Representation and sub-components take parent data as `required properties` and emit signals upward; no aliases into their internals.
- [ ] The heaviest subtrees (graphs, gauges, long lists) live in their own files, so they parse on the first expand rather than with the widget.
- [ ] Backend process/timer logic is out of the UI files and consumed through plain properties.

## References

- [Official] KDE: Porting Plasmoids to KF6 (`PlasmoidItem`, representations, entry point) — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-22)
- [Official] KDE: Widget Properties (`fullRepresentationItem` lazy loading) — https://develop.kde.org/docs/plasma/widget/properties/ (accessed 2026-10-22)
- BP-QML-04 `references/rules/qml/loader-usage.md` and BP-QML-05 `references/rules/qml/component-reuse.md` for the contract of each extracted component.
- BP-ARCH-01 `references/rules/architecture/module-boundaries.md` for "one composition root per artifact" at the module level.

## Version notes

Written against the Plasma 6 developer documentation (Plasma 6.8.x era) accessed on 2026-10-22. The `PlasmoidItem` representations API is stable from Plasma 6.0 onward; re-check the target branch before porting advice from older Plasma 5 material, where representations were attached-property declarations. The thresholds are recomputable labelling: they may be revisited, but changing them is a policy change to this rule, not a code tweak.
