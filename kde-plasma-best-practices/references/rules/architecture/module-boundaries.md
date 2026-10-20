---
title: "Module boundaries and dependency direction"
impact: P1
scope: "Architecture / libraries, plugins, plasmoids, KCMs, applications"
tags: [architecture, plugins, kplugin, kcm, dependencies]
---

# Module boundaries and dependency direction

## Principle

Split the system into a core with no knowledge of its consumers, plugins that depend on the core, and thin entry points (application, plasmoid package, KCM) that assemble them. Dependencies point inward and never back out toward a specific consumer, and each boundary has one reason to change.

## Why it matters

Plasma's own architecture makes the boundary explicit: a plasmoid's base is a C++ `Applet` (a QObject), applets live in a `Containment` that manages their lifecycle, and the QML root is a `PlasmoidItem` that fronts an `AppletInterface` `[Official]`. Panels and desktops are containments; a widget is an applet. If a widget's QML reaches into shell internals, or the core library starts naming one widget's classes, that separation collapses and every change becomes cross-cutting.

KDE's plugin mechanism is `KPluginFactory`, with `K_PLUGIN_FACTORY` and `K_PLUGIN_FACTORY_WITH_JSON` available in KF6 KCoreAddons `[Observed]`. A factory that returns a concrete type to a caller who then downcasts is not a plugin boundary; it is a linked dependency with extra steps.

Binary compatibility raises the cost of a leaky boundary: exported classes are constrained by KDE's binary compatibility policy, so widening a public header is a long-term commitment, not a local edit `[Official]`.

## Incorrect

```cpp
// Pseudocode: illustrative only.
// Core library knows one concrete consumer.
class Core {
public:
    void notifyWidget(MyWeatherWidget *w);   // core -> specific widget
};

// Application constructs a plugin type directly and downcasts it.
auto *obj = factory->create<MyWeatherWidget>(this, args);
```

## Preferred

```cpp
// Pseudocode: illustrative only.
// Core exposes a capability; consumers subscribe.
class Core : public QObject {
    Q_OBJECT
public:
    Q_INVOKABLE void requestRefresh();
signals:
    void refreshed(const Data &data);
};

// Plugin implements an interface from the core, registered via a factory.
class Provider : public QObject, public RefreshProvider {
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.example.provider" FILE "provider.json")
    Q_INTERFACES(RefreshProvider)
};
```

- Keep the core free of consumer names: no widget, KCM, or application class in a core header.
- Depend on interfaces or on `KF6::`/`Qt6::` targets, never on a sibling plugin target.
- Expose the smallest header set that satisfies the consumer; private headers stay out of the install interface.
- Put the assembly in one place per artifact: `main.cpp` for an application, `ui/main.qml` plus the package metadata for a plasmoid, the KCM plugin entry for a settings module.
- A KCM is a plugin loaded by System Settings, not a standalone application: it must not assume it owns the process lifecycle, and it must handle defaults, apply, and reset explicitly.

## Exceptions and trade-offs

- A single-binary internal tool does not need a plugin layer; adding factories there is pure indirection.
- Header-only value types shared by several modules are fine and often better than a library target, as long as they carry no consumer-specific logic.
- Extra interfaces cost indirection and debugging effort. Introduce a boundary when a second consumer appears, not in anticipation of one.
- Some KDE frameworks are effectively hard dependencies of the desktop shell; treat them as part of the platform, not as optional plugins.

## Review checklist

- [ ] The core library does not include headers from plugins, KCMs, or applications.
- [ ] Public headers are intentional and minimal; private headers are not installed.
- [ ] Plugin loading goes through a factory and an interface, not a concrete type.
- [ ] Each artifact has exactly one composition root.
- [ ] A KCM does not depend on the application's `main()` or global state.
- [ ] No target depends on another target's implementation detail to avoid a circular dependency.

## References

- KDE: Plasma/DeveloperGuide (Applet, Containment, package structure) — https://community.kde.org/Plasma/DeveloperGuide (accessed 2026-10-20)
- KDE: Porting Plasmoids to KF6 (`PlasmoidItem`, `ContainmentItem`, metadata) — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-20)
- KDE: KCoreAddons API (`KPluginFactory`) — https://api.kde.org/kcoreaddons.html (accessed 2026-10-20)
- KDE: KCMUtils API — https://api.kde.org/kcmutils-index.html (accessed 2026-10-20)
- KDE: Binary Compatibility Issues With C++ — https://community.kde.org/Policies/Binary_Compatibility_Issues_With_C%2B%2B (accessed 2026-10-20)
- KDE: Plasma API index — https://api.kde.org/plasma-index.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The `Applet`/`Containment`/`PlasmoidItem` split is a Plasma 6 change, not a Plasma 5 one; confirm against the target branch before porting advice from older Material. KCM base classes shipped in KCMUtils vary by framework version and by whether the Qt Quick KCM support is installed — verify against the headers actually present in the target environment.
