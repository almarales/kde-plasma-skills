# Qt Quick performance: a labelled synthesis

Scope: a working summary of Qt's official Qt Quick performance guidance, organised for review work on KDE Plasma QML. It explains *where* cost comes from and *what to check*; it deliberately contains no benchmark numbers.

Target assumptions: Plasma 6.8.0, Qt 6.11.1, KF6, verified 2026-10-20. Qt's performance guide is versioned with Qt, so re-read it against the Qt release in the target branch before acting on a detail.

Evidence labels used throughout: `[Official]` (stated in the linked Qt or KDE documentation), `[Observed]` (reproduced locally or visible in an installed package), `[Recommendation]` (this skill's engineering judgement, not a documented rule), `[Experimental]`, `[Unknown]`.

## The frame budget

Qt's guide states the common target of 60 frames per second and derives the budget from it: roughly 16 milliseconds per frame, including the time needed to get draw primitives to the GPU `[Official]`. It then converts that into four rules: prefer asynchronous event-driven code, move significant processing to worker threads, never manually spin the event loop, and never spend more than a couple of milliseconds per frame inside blocking functions `[Official]`.

The guide calls out one specific anti-pattern with unusual force: creating a private `QEventLoop` or calling `QCoreApplication::processEvents()` to avoid blocking. When an event loop is entered from a signal handler or binding, the QML engine keeps running bindings, animations, and transitions, and those can destroy the very object hierarchy that contains the nested loop `[Official]`. Treat "spin the loop to keep the UI alive" as a defect, not a workaround.

## Profile before optimizing

The guide's first instruction is to profile, and it names the QML Profiler in Qt Creator (or the trace viewer in the Qt extension for Visual Studio Code) `[Official]`. Its stated reason is worth quoting in review comments: knowing where time is spent lets you work on problems that exist rather than problems that might exist, and optimizing without profiling tends to produce very small rather than significant improvements `[Official]`.

`[Recommendation]` For a Plasma component, a useful first pass is: profile with the real containment (panel or desktop) rather than a bare `plasmoidviewer` window, note which bindings re-evaluate most often, and only then change code.

## Bindings and imperative updates

A binding re-evaluates whenever any property it references changes, so bindings should stay as simple as possible `[Official]`. The guide's worked example is a loop that increments a property on every iteration, which re-triggers downstream bindings, text layout, and change handlers once per iteration; accumulating into a local temporary and assigning once avoids all of it `[Official]`.

`[Observed]` Assigning to a bound property from a signal handler or from `Component.onCompleted` silently removes the binding. The value then stops tracking its source, which surfaces later as stale UI rather than as an error. The declarative-bindings rule in this skill's QML catalog covers the correctness side; this reference only covers the cost side.

## JavaScript, type conversion, property resolution

Qt's position is not that JavaScript is slow: it notes that simple functions and bindings can be very fast thanks to the Qt Quick Compiler, and that the real risk is unnecessary processing being triggered accidentally `[Official]`.

Two costs are documented in detail:

- **Type conversion.** Accessing a property can allocate a JavaScript wrapper around C++ data, which is usually cheap but can be expensive for large or complicated value types and sequence types, because those are copied when changed in place or assigned to another property `[Official]`. Lists of object types do not have that problem, since they are implemented with `QQmlListProperty` `[Official]`.
- **Property resolution.** Repeatedly resolving the same `id.property` in a hot loop allocates a wrapper, runs the getter, and copies the value each time; resolving the common base once outside the loop avoids the repetition `[Official]`.

`[Recommendation]` In review, the question to ask is not "is there JavaScript here" but "does this expression run per frame, per delegate instance, or per model row, and does it allocate?"

## Models and views

The guide is explicit that `ListModel` is useful for quick prototyping but not suitable for larger amounts of data, and that a proper `QAbstractItemModel` should be used where necessary `[Official]`. It also warns against enabling `dynamicRoles`: the model assumes role types are stable, and dynamic typing makes performance much worse `[Official]`.

For views, the documented guidance is a compact list `[Official]`:

- Fewer elements in a delegate means faster creation and smoother scrolling.
- Keep delegate bindings to a minimum; use anchors rather than bindings for relative positioning inside a delegate.
- Avoid `ShaderEffect` inside delegates.
- Never enable clipping on a delegate.
- `cacheBuffer` allows asynchronous creation of off-screen delegates and is recommended for non-trivial delegates, but it keeps them in memory, and the guide notes the memory pressure can in rare cases reduce frame rate; the right value is a benchmarking question, not a constant to copy `[Official]`.
- Item reuse in views is worth considering for additional gains `[Official]`.

`[Recommendation]` For Plasma, delegates are the highest-leverage place to look: plasmoid lists, menus, and system tray popups are all delegate-heavy, and they are also the place where a single extra `Loader` or `ShaderEffect` multiplies by row count.

## Element lifetime: Loader and deferred creation

Qt's stated principle is that there is no better way to reduce startup time than to avoid work you do not need and delay the rest `[Official]`. `Loader` is the documented mechanism: delay initialization with `active`, supply initial values through the overloaded `setSource()`, and consider `asynchronous: true` to improve fluidity while a component is instantiated `[Official]`.

Unloading is equally documented: resetting `source` or `sourceComponent` releases the loaded item, and `destroy()` releases items created imperatively `[Official]`. The `Loader` page adds that setting `source` to a new URL destroys the previously instantiated items, and that changing `asynchronous` back to `false` mid-load forces immediate completion — useful when the content must be touched before the async load finishes `[Official]`.

`[Recommendation]` A `Loader` that is never deactivated is just an extra layer. Check that `active`/`source` actually return to a released state when the popup closes; otherwise the "lazy" component is resident for the lifetime of the panel.

## Rendering

The guide's rendering section contains several claims that are easy to get backwards `[Official]`:

- **Clipping is not an optimization.** It is disabled by default, it increases renderer complexity, it prevents free reordering of drawing, and clipping inside a delegate is "especially bad and should be avoided at all costs" `[Official]`.
- **Overdraw matters.** Elements fully covered by opaque elements should have `visible: false`; invisible-but-initialized elements should also be hidden so they are not drawn `[Official]`.
- **Opacity has structure.** Opaque content draws faster than translucent content because blending is avoided, and an image with a single translucent pixel is treated as fully translucent, as is a `BorderImage` with transparent edges `[Official]`.

`[Observed]` The translucent-pixel rule is easy to violate with a "nearly opaque" background SVG: the whole item pays the blending cost. Plasma theme SVGs with soft shadows are a common source.

## Images and text

- Load images asynchronously where the source is not local and guaranteed fast `[Official]`.
- Set an explicit `sourceSize` instead of letting a large image be scaled at run time `[Official]`.
- Avoid run-time composition of images (for example building one image from several at paint time) `[Official]`.
- Avoid smoothing when upscaling `[Official]`.
- Text elements carry layout and shaping cost; the guide lists them under common interface elements alongside images `[Official]`.

## Animations and effects

Animations and particles are listed in the same guide as visual effects with a cost, and an invisible item still evaluates its bindings and animations — hiding it only removes drawing `[Official]`. `[Recommendation]` Stop animations when the surface is not visible, rather than relying on `visible: false` alone.

## Memory and allocation

The guide closes with memory allocation and garbage collection, noting that allocation and collection interact with frame timing `[Official]`. `[Recommendation]` The practical review question is whether a per-frame handler creates objects, arrays, or string concatenations; those become visible as GC pauses under sustained use.

## What this reference does not claim

- No millisecond figures, frame counts, or percentage improvements are asserted here. Qt's guide gives one budget figure (roughly 16 ms at 60 FPS) and explicitly frames it as hardware- and requirement-dependent `[Official]`.
- No claim is made that any specific change improves performance on a given system. That requires a measurement on that system.
- Behaviour of the Qt Quick renderer under a specific GPU, driver, or Plasma compositor configuration is `[Unknown]` until measured there.

## Sources

- Qt: Performance considerations and suggestions — https://doc.qt.io/qt-6/qtquick-performance.html
- Qt: Best Practices for QML and Qt Quick — https://doc.qt.io/qt-6/qtquick-bestpractices.html
- Qt: QML Coding Conventions — https://doc.qt.io/qt-6/qml-codingconventions.html
- Qt: `Loader` — https://doc.qt.io/qt-6/qml-qtquick-loader.html
- Qt: `ListView` — https://doc.qt.io/qt-6/qml-qtquick-listview.html
- Qt: `Image` — https://doc.qt.io/qt-6/qml-qtquick-image.html
- Qt: Property binding — https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html

Accessed: 2026-10-20. All URLs returned HTTP 200 on that date.
