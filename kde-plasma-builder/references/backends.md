# Backends

## Scope

Use this reference to decide **where the data comes from** before a widget is designed. The decision constrains the QML, the build and the test loop, so it is made first, not last.

Evidence labels are the ones used across the bundle: `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, `[Unknown]`.

## The three shapes

### 1. Pure QML

`[Recommendation]` The widget is a QML package with no compiled code. It reads what QML can reach directly: `Plasmoid.configuration`, D-Bus through a Plasma component, or a file. This is the smallest thing to build, install and review, and it should be the default.

`[Official]` The Plasma 6 porting guide describes this shape as the ordinary one: the root QML object is a `PlasmoidItem`, and a C++ plugin is an addition, not a requirement.

### 2. A C++ applet

`[Official]` The porting guide states that "for plasmoids that offer a C++ plugin as an `Applet` subclass, the C++ part doesn't change" — the applet is a `Plasma::Applet` subclass, and the QML side drops the `nativeInterface` intermediary, so a property moves from `Plasmoid.nativeInterface.myProperty` to `Plasmoid.myProperty`.

`[Official]` The System Monitor's own panel widget is exactly this shape: a C++ `Plasma::Applet` that owns a `KSysGuard::SensorFaceController` and exposes it to its QML as a property (`../kde-plasma-best-practices/references/plasma-development.md`).

`[Recommendation]` Reach for a C++ applet when the widget needs native API, a privileged operation, or a type the shell must own. It costs a build, a compiler on every contributor's machine, and a longer review cycle; take that cost only when the shape buys something.

### 3. An external process

`[Recommendation]` The widget stays pure QML and reads from a separate process over D-Bus or by running a command and parsing its output. This is the right shape when the data is expensive to collect, needs privileges, or belongs to a daemon that already exists.

`[Recommendation]` The contract between the widget and the process must be small, versioned and cheap to call: the widget is on the GUI thread, and a slow call is a frozen panel.

## The Python trap

`[Recommendation]` A Python `QObject` cannot serve a plasmoid. The QML engine that instantiates the widget's `contents/ui/main.qml` belongs to `plasmashell`, a C++ process. A `QObject` subclass registered from Python with `@QmlElement` lives in a **Python** QML engine, and `import com.example.widget` in the widget's QML is resolved by the shell's engine, which has never heard of it. The two engines are in different processes; there is no import bridge between them.

`[Recommendation]` A Python process is still useful — as the *data source* behind shape 3, not as the widget's object model. If the widget must expose native API to the shell, that API has to be C++.

`[Unknown]` Whether any packaging route exists that ships a Python interpreter and a QML plugin together for a plasmoid was not verified for this bundle. Check the current KDE developer documentation before planning around it.

## Choosing

| The widget needs | Shape |
| --- | --- |
| Only configuration and Plasma APIs | Pure QML |
| Native API, privileges, or a type the shell owns | C++ applet |
| Data from an expensive collector or an existing daemon | External process, pure QML widget |

`[Recommendation]` Decide this before designing the interface, and record the decision with its reason. The cost of changing later is a rewrite of the data path, not a refactor.

## Sources

- KDE: Porting Plasmoids to KF6 — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial, properties — https://develop.kde.org/docs/plasma/widget/properties/ (accessed 2026-10-20)
- KDE: Plasma developer documentation index — https://develop.kde.org/docs/plasma/ (accessed 2026-10-20)

## Version notes

- Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The applet base class and the QML property group are stable across Plasma 6, but a major release may move them again; the porting guide is the authority for the target branch.
- The Python conclusion follows from where the QML engine lives, not from a version-specific fact. It is `[Recommendation]` because it is engineering reasoning over documented architecture, not a quotation from the documentation.
