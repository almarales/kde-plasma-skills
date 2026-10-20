---
title: "Use Loader deliberately"
impact: P2
scope: qml
tags: [loader, lazy-loading, startup, error-handling]
---

# Use Loader deliberately

## Principle

`Loader` trades a little structural complexity for deferring instantiation. Use it when a component is expensive and not needed on the first frame, and handle the three states it introduces: loading, ready, and error. Do not wrap cheap components "just in case".

## Why it matters

[Official] `active` defaults to `true`. Setting it to `false` releases any loaded item but keeps `source`/`sourceComponent`, so the component is instantiated when the loader becomes active. The `status` of an inactive loader is `Loader.Null`.

[Official] `asynchronous: true` creates the component's objects across multiple frames and reduces glitches in animation. With `source` set to a URL, loading and compilation are also performed in a background thread. The property affects object instantiation only; it is not about network loading.

[Official] `status` is `Null`, `Loading`, `Ready`, or `Error`. For a local file the status is initially `Ready` or `Error`; there is no `Loading` phase and no `statusChanged` signal, though `onLoaded` still fires. Code that assumes a loading phase for local files is wrong.

[Recommendation] Two failure modes dominate: binding to `loader.item.someProperty` while `item` is still null, and treating `Loader.Error` as "cannot happen" because the file exists in the source tree.

## Incorrect

```qml
// Pseudocode: unguarded access to a not-yet-created item.
Loader {
    id: chartLoader
    source: "Chart.qml"
    asynchronous: true
}
Text { text: chartLoader.item.seriesCount }   // null until Ready
```

```qml
// Pseudocode: deferral with no error path and no loading state.
Loader {
    id: detailsLoader
    active: false
    source: "Details.qml"
}   // nothing renders and nothing reports failure
```

## Preferred

```qml
// Pseudocode: explicit lifecycle; root.detailsVisible and showFallback belong to the app.
Loader {
    id: detailsLoader
    active: root.detailsVisible
    asynchronous: true
    source: root.detailsVisible ? "Details.qml" : ""

    onStatusChanged: if (status === Loader.Error) console.warn("Details failed to load")
}

Text {
    visible: detailsLoader.status === Loader.Ready
    text: detailsLoader.status === Loader.Ready ? detailsLoader.item.summary : qsTr("Loading…")
}
```

When loading a delegate member, prefer a separate file or an inline `Component` over a `sourceComponent` declared in another context: the loader uses the component's creation context, so `index` and other delegate context properties are not visible unless you pass them as loader properties.

## Exceptions and trade-offs

- Deferral adds a null period, a loading indicator, an error path, and one more file to navigate. For a component that is small or needed immediately, direct instantiation is simpler and faster.
- `asynchronous` spreads work; total work and total memory do not drop. It can also make content appear progressively, which is worse for a dialog that must appear complete.
- `active: false` plus `setSource(url, properties)` caches initial properties until activation, which is useful for pre-built pages but adds state to reason about.

## Review checklist

- [ ] Every `Loader` that can fail handles `Loader.Error` and shows a fallback.
- [ ] Access to `item` is guarded by `status === Loader.Ready`.
- [ ] The deferred component is expensive enough to justify the indirection.
- [ ] Deferred pages use `active: false`, not `visible: false`.
- [ ] Loader focus behavior is intentional: `Loader` is a focus scope.
- [ ] Delegate-context properties are passed explicitly to the loaded component.

## References

- [Official] Qt: Loader QML Type — https://doc.qt.io/qt-6/qml-qtquick-loader.html (accessed 2026-10-20)
- [Official] Qt: QML Performance Considerations, "Using Loader" — https://doc.qt.io/qt-6/qtquick-performance.html (accessed 2026-10-20)
- [Official] Qt: Component QML Type — https://doc.qt.io/qt-6/qml-qtqml-component.html (accessed 2026-10-20)

## Version notes

Verified against Qt 6.11.1 documentation on 2026-10-20. The `Loader` API used here is stable across Qt 6; re-check status semantics on the target branch.
