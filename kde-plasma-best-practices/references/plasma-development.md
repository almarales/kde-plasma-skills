# Plasma development map

Scope: a working map of how a Plasma 6 desktop is assembled and where a change belongs — shell, containment, applet, package, configuration, KCM, plugin. It is an orientation document for engineers and review agents, not a tutorial replacement for the KDE developer documentation.

Target assumptions: Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. Plasma's QML API and package format have changed between major versions, so every claim below is paired with what must be re-verified on a different target.

Evidence labels: `[Official]` documented by KDE or Qt, `[Observed]` reproduced on the verification machine, `[Recommendation]` engineering judgement from this skill, `[Unknown]` not verified.

## The object model

Plasma's own porting documentation describes the structure directly `[Official]`:

- A plasmoid's base is a C++ class `Applet`, which is a `QObject`.
- Applets are contained in an `Applet` subclass called `Containment`, which manages the lifecycle of its applets.
- On Plasma Desktop, each screen has one containment for its desktop area and another for each panel.
- The root of the QML side is a C++ `QQuickItem` implementation called `AppletInterface`; if the plasmoid is also a containment, the root is `ContainmentItem`, a subclass of `ContainmentInterface`.
- In Plasma 6 the root QML object must be a `PlasmoidItem` (the QML name for `AppletInterface`), or `ContainmentItem` for a containment.
- `AppletInterface` and `ContainmentInterface` now expose only Qt Quick–specific API; the wrapper properties were removed, and the `Plasmoid` attached property is an instance of the underlying `Applet`.

`[Observed]` The installed desktop containment is the package `org.kde.desktopcontainment`, installed at `/usr/share/plasma/plasmoids/org.kde.desktopcontainment` with `metadata.json` and `contents/ui/main.qml`. The shell itself is `org.kde.plasma.desktop` under `/usr/share/plasma/shells`, and panel arrangements ship as layout templates (for example `org.kde.plasma.desktop.defaultPanel`) under `/usr/share/plasma/layout-templates`.

`[Recommendation]` When deciding where a change belongs, ask which of these objects owns the state: a widget that only draws belongs in an applet package; a panel behaviour belongs in the shell or containment; anything that must exist without a widget belongs in a background service or the shell.

## QML API surface in Plasma 6

| Import | What it provides | Notes |
| --- | --- | --- |
| `org.kde.plasma.components` | Plasma-styled controls (buttons, sliders, list items) | Module present on the verification machine `[Observed]`; the porting guide documents which Plasma 5 components to replace `[Official]` |
| `org.kde.plasma.extras` | Plasmoid-level helpers such as config pages and expandable list items | Module present on the verification machine `[Observed]` |
| `org.kde.plasma.core` | `PlasmaCore` primitives (theme, units) | Module present `[Observed]`; `PlasmaCore.SortFilterModel` moved to `KItemModels.KSortFilterProxyModel` in Plasma 6 `[Official]` |
| `org.kde.kirigami` | Kirigami components for apps and KCMs | Kirigami is a KF6 framework, usable outside Plasma `[Official]` |
| `org.kde.plasma.plasma5support` | Compatibility layer for Plasma 5 APIs during porting | A migration aid, not a destination `[Official]` |

`[Official]` The porting guide states that QML module imports should be un-versioned in Qt 6; keeping versions is unnecessary and can cause bugs.

`[Recommendation]` Do not infer the available imports from a Plasma 5 tutorial. Enumerate the imports actually present in the target environment (`/usr/lib/*/qt6/qml`, or the QML import paths reported by the running shell) before writing an import line.

## Package format (KPackage)

`[Observed]` An installed plasmoid on the verification machine looks like this:

```text
/usr/share/plasma/plasmoids/<plugin-id>/
├── metadata.json
└── contents/
    ├── ui/main.qml
    ├── config/main.xml
    └── config/config.qml      # when the widget is configurable
```

`[Official]` Requirements for Plasma 6 metadata, per the porting guide:

- All plasmoids must use JSON metadata; a legacy `.desktop` file can be converted with the `desktoptojson` utility.
- `"X-Plasma-API-Minimum-Version": "6.0"` must be present, otherwise the plasmoid is treated as Plasma 5 only and is not offered in the UI.
- `X-Plasma-MainScript` must be removed: `ui/main.qml` is always the entry point.
- `X-Plasma-API` must be removed.
- `ServiceTypes` must be replaced by a top-level `"KPackageStructure": "Plasma/Applet"`.

`[Observed]` A real installed `metadata.json` contains `KPackageStructure`, and a `KPlugin` object with `Id`, `Name`, `Description`, `Icon`, `License`, `Category`, `Website`, `EnabledByDefault`, and a localized `Authors` array, plus `X-Plasma-API-Minimum-Version: "6.0"`.

`[Recommendation]` Treat the metadata file as an API: `KPlugin.Id` is the identity used by configuration, layout, and translations, so changing it migrates no user settings.

## Plasmoid build, install, and test loop

`[Official]` There is no packaging subcommand: a `.plasmoid` is a zip whose root holds `metadata.json` and `contents/`. Do not nest them inside an extra directory, or installation fails.

```bash
cd my-plasmoid/package
zip -r ../../my-plasmoid-1.0.0.plasmoid metadata.json contents
unzip -l ../../my-plasmoid-1.0.0.plasmoid                 # metadata.json must be at the root
unzip -p ../../my-plasmoid-1.0.0.plasmoid metadata.json | jq .KPlugin
```

`[Observed]` `kpackagetool6 --help` on the verification machine lists `-t/--type`, `-i/--install`, `-u/--upgrade`, `-r/--remove`, `-l/--list`, and `-g/--global`:

```bash
kpackagetool6 -t Plasma/Applet -i my-plasmoid-1.0.0.plasmoid   # install
kpackagetool6 -t Plasma/Applet -u my-plasmoid-1.0.0.plasmoid   # upgrade after a rebuild
kpackagetool6 -t Plasma/Applet -r com.example.my-plasmoid      # remove by KPlugin.Id
kpackagetool6 -t Plasma/Applet -l                              # list installed
sudo kpackagetool6 -g -t Plasma/Applet -i my-plasmoid-1.0.0.plasmoid   # all users
```

`[Observed]` `plasmapkg2` is absent on the verification machine and belongs to Plasma 5 tooling; do not mix it with `kpackagetool6`.

`[Official]` `plasmoidviewer` (from the `plasma-sdk` package) runs an unpacked package without installing it; `plasmawindowed` needs the widget installed under `~/.local/share/plasma/plasmoids` and preserves configuration changes, so use it to test save and restore:

```bash
plasmoidviewer -a ./package                            # defaults: floating location, planar form factor
plasmoidviewer -a ./package -f horizontal -l topedge   # panel form factor
QT_SCALE_FACTOR=2 plasmoidviewer -a ./package          # HiDPI check
plasmawindowed com.example.my-plasmoid                 # installed widget, remembers config
systemctl --user restart plasma-plasmashell.service    # real shell after install
```

`[Official]` `-f` accepts `horizontal`, `vertical`, `mediacenter`, `planar`, `application`; `-l` accepts `floating`, `desktop`, `fullscreen`, `topedge`, `bottomedge`, `leftedge`, `rightedge`. `--location=desktop` is the desktop wallpaper containment, not a desktop widget.

`[Official]` QML `console.log()` output is hidden by default: enable it with `QT_LOGGING_RULES="qml.debug=true" plasmoidviewer -a ./package`, or persistently with `qml.debug=true` under `[Rules]` in `~/.config/QtProject/qtlogging.ini`. The official page still shows `kwriteconfig5` for that file; on Plasma 6 use `kwriteconfig6`. `journalctl --user -u plasma-plasmashell.service -f` follows the shell log.

`[Recommendation]` Diagnose in this order: widget missing from *Add Widgets* means invalid `metadata.json` or a missing `"KPackageStructure": "Plasma/Applet"`; installation failure means `metadata.json` is not at the archive root; settings that do not persist mean `main.xml` entry names and `cfg_` aliases diverge, or the test ran under `plasmoidviewer` instead of `plasmawindowed`.

## Configuration

`[Recommendation]` Keep three things separate:

1. **Schema** — `contents/config/main.xml` (KConfigXT) declares the keys, types, and defaults.
2. **UI** — `contents/config/config.qml` declares the configuration pages.
3. **Runtime access** — the widget reads its settings through the configuration object the Plasma stack provides, not by opening a `KConfig` file directly.

The KDE widget documentation covers the configuration UI and KConfigXT flow `[Official]`. `[Observed]` A `KConfig` object opened without isolation reads the user's real configuration; tests must set `QStandardPaths` test mode or an isolated `HOME` (see `references/rules/testing/integration-tests.md`).

`[Official]` Every `main.xml` value is exposed on the config page as a top-level `cfg_<entry>` property. Declare one `property alias cfg_showLabel: showLabel.checked` per key; that indirection is what gives Apply and Discard its transaction. Assigning to `plasmoid.configuration.<key>` from the page instead writes immediately and skips Apply, so pick one model per page rather than mixing them. The official page's samples still use versioned `QtQuick 2.0` and `org.kde.kirigami 2.4` imports; target Plasma 6 uses unversioned imports.

## KCMs (System Settings modules)

`[Official]` A KCM is a plugin loaded by System Settings, not a standalone application. KF6 KCMUtils provides `KCModule`, `KCModuleLoader`, `KCMultiDialog`, and `KPluginWidget`, and CMake helpers `kcmutils_add_qml_kcm`, `kcmutils_generate_module_data`, and `kcmutils_generate_desktop_file`. `[Observed]` The same installation also exposes `__kcmutils_target_qml_sources`, but the double underscore marks it internal: use `kcmutils_add_qml_kcm` instead.

`[Observed]` On KF6 6.31.0 the Qt Quick KCM bases are `KQuickConfigModule` (`KCMUtilsQuick/kquickconfigmodule.h`) and `KQuickManagedConfigModule` (`kquickmanagedconfigmodule.h`, since 6.0). Availability still depends on the KCMUtils build and on whether the Qt Quick KCM support is packaged, so verify the headers actually present before writing `#include`s.

`[Recommendation]` A KCM should apply changes through the same API the application uses, handle defaults and reset explicitly, and never assume it owns the process. Test it by instantiating the module directly rather than by driving System Settings.

## Plugins and factories

`[Observed]` KF6 KCoreAddons provides `KPluginFactory` with the `K_PLUGIN_FACTORY`, `K_PLUGIN_FACTORY_DEFINITION`, and `K_PLUGIN_FACTORY_WITH_JSON` macros.

`[Recommendation]` Use a factory plus an interface, and construct through the factory's API rather than by naming a concrete class at the call site. A factory whose result is immediately downcast is a linked dependency with extra steps (see `references/rules/architecture/module-boundaries.md`).

## Pluggable view packages: the System Monitor face architecture

`[Official]` The System Monitor is the first-party Plasma surface where a rendered item is itself an installable plugin. It is the reference implementation for "the user picks how a datum is drawn", and its mechanism is KPackage, not a C++ factory.

Discovery, declaration, and installation:

- A view is a KPackage whose structure is `KSysguard/SensorFace`, declared in its `metadata.json` as `"KPackageStructure": "KSysguard/SensorFace"` with a `KPlugin` object; the shipped line chart declares `"Id": "org.kde.ksysguard.linechart"`, `"Icon": "office-chart-line"`, and `"Version": "1.0"` (`libksysguard/faces/facepackages/linechart/metadata.json`).
- The id prefix is `org.kde.ksysguard.<view>`; the library ships `barchart`, `colorgrid`, `facegrid`, `horizontalbars`, `linechart`, `piechart`, and `textonly` (`libksysguard/faces/facepackages/`), and the application ships `applicationstable` and `processtable` itself (`plasma-systemmonitor/src/faces/CMakeLists.txt`).
- Installation is `kpackage_install_package(<dir> <plugin-id> sensorfaces ksysguard)`, so views land in `…/ksysguard/sensorfaces/<plugin-id>` (`plasma-systemmonitor/src/faces/CMakeLists.txt`).
- A view package holds `metadata.json` plus `contents/ui/` (`FullRepresentation.qml`, `CompactRepresentation.qml`, `Config.qml`), `contents/config/`, and `contents/faceproperties` (`libksysguard/faces/facepackages/linechart/contents/`).
- The file names are not conventional: the structure is a **custom `KPackage::PackageStructure` subclass** (`SensorFacePackage`) that maps logical names to paths and marks three of them required — `CompactRepresentation` → `ui/CompactRepresentation.qml`, `FullRepresentation` → `ui/FullRepresentation.qml`, and `FaceProperties` → `faceproperties` — with `ConfigUI` → `ui/Config.qml` and `mainconfigxml` → `config/main.xml` optional, and the default package root set to `ksysguard/sensorfaces` (`libksysguard/faces/packagestructure/sensorfacepackage.cpp`).

`[Official]` The supporting library is a separate QML module, not a namespace of the application: `ecm_add_qml_module(SensorFaces URI "org.kde.ksysguard.faces" VERSION 1.0 …)`, with a private companion `org.kde.ksysguard.faces.private`; the target is `KSysGuard::SensorFaces` (library `KSysGuardSensorFaces`), its headers install to `<includedir>/ksysguard/faces`, and its logging category is `org.kde.libksysguard.faces` (`libksysguard/faces/CMakeLists.txt`).

`[Official]` Both the application and the views import that module: `import org.kde.ksysguard.faces as Faces`. The module provides the base type the views derive from (`Faces.AbstractSensorFace`, which exposes the app-owned `controller` to the view's QML) and the space hint the host sets before showing a view (`Faces.SensorFace.Constrained`) (`libksysguard/faces/import/SensorFace.qml`, `plasma-systemmonitor/src/page/FaceControl.qml`).

`[Official]` The host swaps the view in place by reassigning the container's content item — `control.contentItem = loader.controller.fullRepresentation` — and repeats it when `faceIdChanged` fires; the host also forwards `missingSensorsChanged` so the app, not the view, decides how to report unresolvable sensors (`plasma-systemmonitor/src/page/FaceControl.qml → FaceControl.updateContentItem`).

`[Official]` The runtime contract, in `libksysguard/faces/SensorFaceController.cpp`:

- Discovery: `KPackage::PackageLoader::self()->listPackages("KSysguard/SensorFace")` fills the picker with `plugin.name()` and `plugin.pluginId()`.
- Loading: `KPackage::PackageLoader::self()->loadPackage("KSysguard/SensorFace", faceId)` resolves one view; an invalid package returns early and leaves the item unrendered.
- Instantiation is C++-side, through `QQmlComponent(engine, qmlPath)` with `beginCreate()` / `completeCreate()` and a `qobject_cast` to the expected base — **not** a QML `Loader` with a `source:` URL. A plugin's path is only known at runtime, after the package is resolved, so the URL cannot be a static QML property.
- The controller is constructed as `new SensorFaceController(configGroup, engine, configEngine)`. The library's own loader hands it a **dedicated** `QQmlEngine` for configuration so that the Plasma theme colours are not re-used, and records why in the source (`BUG:483689`); the application instead passes its own engine for both arguments (`libksysguard/faces/FaceLoader.cpp → FaceLoader::Private::setupController`, `plasma-systemmonitor/src/page/FaceLoader.cpp`).

`[Official]` Configuration is layered, and every layer has an owner:

- The app owns the per-item groups `Appearance` (`chartFace`, `Title`, `showTitle`, `updateRateLimit`), `Sensors` (`totalSensors`, `highPrioritySensorIds`, `lowPrioritySensorIds`), `SensorColors`, and `SensorLabels`.
- The view owns its own keys, namespaced by its plugin id: a shipped page preset reads `[Face-106123380916688][org.kde.ksysguard.piechart][General] showLegend=false` (`plasma-systemmonitor/src/pages/overview.page`).
- A view that needs structured settings ships `mainconfigxml`, loaded through `KConfigLoader` and exposed as a `KConfigPropertyMap` (`SensorFaceController::reloadFaceConfiguration`).
- Capabilities are declared by the view in `contents/faceproperties` and read by the app: `SupportsSensors`, `SupportsTotalSensors`, `MaxTotalSensors`, `SupportsSensorsColors`, `SupportsLowPrioritySensors`, and `ForceSaveOnDestroy`.

`[Recommendation]` Writes are batched: the controller holds a single-shot 5 s timer and syncs the appearance and sensors groups together, so a slider drag produces one config write instead of dozens. A view that writes its own config on every property change reintroduces the problem.

`[Official]` Teardown is explicit, because a QML-visible object still referenced by the runtime cannot simply be deleted: `SensorFaceController::~SensorFaceController` calls `markAsClean()` on the groups when it must not sync, reloads the config loader to discard pending changes, and only saves on destruction when the view asked for it with `ForceSaveOnDestroy`. The application states the same constraint in its own code: deleting the face controller with `deleteLater()` "will trigger a crash in the QML runtime because it still has references to the object that do not get cleared", so the old controller is kept alive until a new one exists (`plasma-systemmonitor/src/page/FaceLoader.cpp → FaceLoader::reset`).

`[Recommendation]` Replacing a QML-visible component is a two-step operation: create the successor first, then release the predecessor. Deleting the old object while the engine still holds a reference to it is a crash, not a leak, and `deleteLater()` does not fix it because the reference outlives the event loop turn.

`[Official]` Layout and views are persisted as data, not as code. The page tree is a hierarchy of KConfig groups — `[page]`, `[page][row-0]`, `[page][row-0][column-0]`, `[page][row-0][column-0][section-0]` — with each section pointing at a face instance through `face=Face-<id>`; the shipped defaults are `.page` files in the same KConfig format (`plasma-systemmonitor/src/pages/overview.page`). A saved layout is a `Plasma/Applet` package with `X-Plasma-RootPath: org.kde.plasma.systemmonitor`, installed with `KPackage::PackageJob::install` and rediscovered by scanning `Plasma/Applet` packages for that root path (`SensorFaceController::savePreset`, `PresetsModel::reload`).

`[Official]` Configuration migrations belong in the reader, not in the interface. `SensorFaceControllerPrivate::readSensors` applies a table of regular-expression replacements to legacy sensor ids (`cpu/system/*` → `cpu/all/*`, `mem/*` → `memory/*`, the old network and disk spellings) and writes the corrected ids back to the config on load (`libksysguard/faces/SensorFaceController.cpp → SensorFaceControllerPrivate::readSensors`).

`[Recommendation]` When a plugin-provided view is replaced, check that the new view declares the capabilities the stored configuration assumes. A stored `showLegend` for a view that no longer supports it is silently ignored by the app and looks like a bug in the view.

`[Recommendation]` The whole mechanism is heavier than a widget needs. Reach for it only when the user must choose the rendering, the choice must survive upgrades, and third parties must be able to add views; otherwise ship one rendering and keep the boundary in one file.

## Reusing the System Monitor faces in a plasmoid

`[Official]` The System Monitor ships a Plasma applet that consumes the same face packages, and it is the reference for this task: `org.kde.plasma.systemmonitor` in `plasma-workspace` (`applets/systemmonitor/systemmonitor/`) is a `Plasma::Applet` subclass that owns a `KSysGuard::SensorFaceController` and a QML layer that places the face's own item.

### The constraint that decides the design

`[Official]` Three facts force a C++ backend:

- `KSysGuard::SensorFaceController` is declared `QML_ELEMENT` **and** `QML_UNCREATABLE("It's not possible to create objects of type SensorFaceController")`: QML can see the type and call its methods, but cannot create one (`libksysguard/faces/SensorFaceController.h`).
- `KSysGuard::SensorFace::setController()` is a C++ setter and is explicitly not writable from QML; the controller is what attaches a face to its data (`libksysguard/faces/SensorFace_p.h`).
- The QML-instantiable `KSysGuard::FaceLoader` cannot bootstrap: its `setupController()` returns early unless a `parentController` is set and `groupName` is not empty. It exists so that a face can load a child face, not to start a chain (`libksysguard/faces/FaceLoader.cpp → FaceLoader::Private::setupController`).

`[Recommendation]` So a QML-only plasmoid can read the same sensor data, but it cannot mount the face packages. Pick the path that matches the data and the customization the product needs, not the one that is cheaper to ship.

### Path A — reuse the faces (C++ applet)

`[Official]` The upstream applet does this in a few lines (`plasma-workspace applets/systemmonitor/systemmonitor/systemmonitor.cpp`):

```cpp
// Quoted from upstream, not pseudocode.
KConfigGroup cg = config();
m_sensorFaceController = new KSysGuard::SensorFaceController(
    cg,                                  // the applet's own config group
    PlasmaQuick::globalEngine().get(),  // the shell's global QML engine
    new QQmlEngine(this));               // a separate engine for the config UI
```

and exposes the controller to its own QML (`systemmonitor.h`):

```cpp
// Quoted from upstream, not pseudocode.
Q_PROPERTY(KSysGuard::SensorFaceController *faceController READ faceController CONSTANT)
```

`[Official]` The QML side places the face's item and tells it how much space it has (`package/contents/ui/FullRepresentation.qml`):

```qml
// Quoted from upstream, not pseudocode.
contentItem: Plasmoid.faceController.fullRepresentation

Binding {
    target: Plasmoid.faceController.fullRepresentation
    property: "formFactor"
    value: Plasmoid.formFactor === PlasmaCore.Types.Horizontal
         ? Faces.SensorFace.Horizontal
         : Faces.SensorFace.Planar
    restoreMode: Binding.RestoreBinding
}
```

`[Official]` The customization comes from the controller, not from new code: `availableFacesModel` (display name plus `pluginId` of every installed face), the writable `faceId`, `faceConfigUi`, `appearanceConfigUi` and `sensorsConfigUi` (each face's own configuration pages), the capability properties `supportsSensorsColors`, `supportsTotalSensors`, `supportsLowPrioritySensors` and `maxTotalSensors`, and the `Q_INVOKABLE` `loadPreset()`, `savePreset()` and `uninstallPreset()`.

`[Official]` Live values for a surface that shows a number instead of a chart come from the sensors module, which is QML-first: `Sensors.Sensor` is a `QML_ELEMENT` exposing `sensorId`, `name`, `shortName`, `unit`, `value`, `formattedValue`, `status` (`Unknown`, `Loading`, `Ready`, `Error`, `Removed`) and a rate-limiting `updateRateLimit` (`libksysguard/sensors/Sensor.h`).

`[Official]` Build integration: `find_package(KSysGuard REQUIRED)`, then link `KSysGuard::SensorFaces` plus `KSysGuard::Sensors` and `KSysGuard::Formatter`. The export is namespaced (`install(EXPORT libksysguardLibraryTargets NAMESPACE KSysGuard::)`) and the headers install to `<includedir>/ksysguard/faces/` (`libksysguard/CMakeLists.txt`).

`[Recommendation]` Three upstream details are worth copying instead of rediscovering:

- **The engine is the shell's.** The face is instantiated in `PlasmaQuick::globalEngine()`, so its QML imports resolve against the shell's import paths. A face built in a private engine is a different animal.
- **The config group is the applet's own.** The controller reads and writes `config()`, so the selected face, the title, the colours and the sensor list persist with the widget and follow it to another panel.
- **BUG 424458**: reusing the controller and its item breaks the appearance configuration UI. The applet works around it with `workaroundController(QQuickItem *context)`, which builds a controller bound to the applet's own engine instead of the global one (`plasma-workspace applets/systemmonitor/systemmonitor/systemmonitor.h`).

`[Recommendation]` The applet also reads `CurrentPreset` from its config and calls `loadPreset(preset)`, then rewrites the entry to the root plugin id, so a widget can ship as a preset of the System Monitor and be switched at runtime.

### Path B — QML only: reuse the data, not the faces

`[Official]` Without C++ the sensor layer is still fully available from QML:

- `import org.kde.ksysguard.sensors as Sensors` provides `Sensors.Sensor`.
- `import org.kde.ksysguard.formatter as Formatter` provides the value formatting the faces themselves use (`Formatter.Formatter.formatValueShowNull(...)`).

`[Recommendation]` With those two plus KQuickCharts you can show system metrics that look and behave like Plasma's, inheriting the rate limiting and the value formatting for free. What you give up is exactly the part a customizable product wants: there is no face picker, no per-face configuration UI, and no presets, because all three live behind `SensorFaceController`. If the customization is the point, Path B does not deliver it.

### Writing a third-party face

`[Official]` A face is a KPackage with the structure `KSysguard/SensorFace`, installed under `…/ksysguard/sensorfaces/<plugin-id>`, whose required files are `ui/FullRepresentation.qml`, `ui/CompactRepresentation.qml` and `faceproperties` (see the package structure above). The QML root derives from the module's `SensorFace` type, whose contract is small: assign the visualization to `contentItem`, read the sensors from `controller`, and honour `formFactor` (`Planar`, `Vertical`, `Horizontal`, `Constrained`).

`[Recommendation]` Declare the capabilities you support in `faceproperties`. An app that cannot ask for a capability the face does not have should not offer the option, and that negotiation is what lets a third-party face behave like a first-party one instead of becoming a special case in the app.

### Limits

`[Recommendation]` The faces render KSysGuard sensors. If the plasmoid shows its own domain data, reuse the *pattern* — a KPackage per visualization, capability negotiation, per-view configuration — and write the views on KQuickCharts; the face packages themselves do not apply.

## Version matrix

| Component | Assumed version | How it was established |
| --- | --- | --- |
| Plasma | 6.8.0 | `plasmashell --version` `[Observed]` |
| Qt | 6.11.1 | `qmake6 -query QT_VERSION`, `pkg-config --modversion Qt6Core` `[Observed]` |
| KF6 / ECM | 6.31.0 | `ECMConfigVersion.cmake` `[Observed]` |
| `qmllint6` | 6.11.1 (Qt 6) | `qmllint6 --version` `[Observed]`; the unversioned `qmllint` is a `qtchooser` wrapper that reports `1.0` and runs Qt 5 |
| `kpackagetool6`, `plasmoidviewer`, `plasmawindowed` | present | `which` `[Observed]` |
| clazy, clang-tidy | not installed | `which` returned nothing `[Observed]` |

These are the versions this skill was written against, not requirements. A different checkout must restate them from its own environment.

## What must be verified per target version

- **QML imports and their names.** `org.kde.plasma.components` replaced the Plasma 5 import; other modules moved or were absorbed. Enumerate the target's import paths.
- **Metadata keys.** `KPackageStructure`, `X-Plasma-API-Minimum-Version`, and the removal of `X-Plasma-MainScript`/`X-Plasma-API` are Plasma 6 requirements; older or newer branches may differ.
- **Root element.** `PlasmoidItem`/`ContainmentItem` are Plasma 6 roots; Plasma 5 material uses a plain `Item` plus the `plasmoid` context property.
- **Tool names.** `kpackagetool6` and `desktoptojson` replace Plasma 5 tooling; tutorials frequently still show `kpackagetool5`.
- **KCM base classes and CMake helpers.** Confirm against installed headers.
- **Translation domain.** The widget documentation describes a `plasma_applet_<plugin-id>` domain, but that material predates Plasma 6; check the domain your build actually produces.
- **Deprecation state of compatibility modules.** `org.kde.plasma.plasma5support` exists to ease porting and is not a long-term target.

## Sources

- KDE: Plasma/DeveloperGuide — https://community.kde.org/Plasma/DeveloperGuide
- KDE: Porting Plasmoids to KF6 — https://develop.kde.org/docs/plasma/widget/porting_kf6/
- KDE: Plasma Widget tutorial (index) — https://develop.kde.org/docs/plasma/widget/
- KDE: Plasma Widget tutorial — setup — https://develop.kde.org/docs/plasma/widget/setup/
- KDE: Plasma Widget tutorial — configuration — https://develop.kde.org/docs/plasma/widget/configuration/
- KDE: Plasma Widget tutorial — properties — https://develop.kde.org/docs/plasma/widget/properties/
- KDE: Plasma Widget tutorial — testing — https://develop.kde.org/docs/plasma/widget/testing/
- KDE: Plasma Widget tutorial — translations/i18n — https://develop.kde.org/docs/plasma/widget/translations-i18n/
- KDE: Plasma developer documentation index — https://develop.kde.org/docs/plasma/
- KDE: Kirigami documentation — https://develop.kde.org/frameworks/kirigami/
- KDE: KCMUtils API — https://api.kde.org/kcmutils-index.html
- KDE: KPackage API — https://api.kde.org/kpackage-index.html
- KDE: KConfig API — https://api.kde.org/kconfig-index.html
- KDE: Plasma API — https://api.kde.org/plasma-index.html
- KDE: KDE Visual Design Group — https://community.kde.org/KDE_Visual_Design_Group
- KDE Invent: plasma-systemmonitor, `src/page/` and `src/pages/overview.page` — https://invent.kde.org/plasma/plasma-systemmonitor/-/tree/master/src/page — Accessed: 2026-10-20
- KDE Invent: libksysguard, `faces/` (SensorFaceController, face packages, QML module) — https://invent.kde.org/plasma/libksysguard/-/tree/master/faces — Accessed: 2026-10-20
- KDE: KDE Human Interface Guidelines — https://develop.kde.org/hig/

Accessed: 2026-10-20. All URLs returned HTTP 200 on that date. The Developer Guide is a community wiki and contains Plasma 5-era tooling (`metadata.desktop`, `kpackagetool5`); it was used for architecture, not for tooling instructions.
