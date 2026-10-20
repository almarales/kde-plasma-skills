# Source ledger

Every URL below was re-checked in this authoring session with:

```bash
curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 <url>
```

All listed entries returned **HTTP 200**. Access date for every row: **2026-10-20**.

Columns: URL · what the source is used to support in this skill · status.

## KDE documentation and policy

| URL | Supports | Status |
| --- | --- | --- |
| https://develop.kde.org/hig/ | KDE Human Interface Guidelines: interaction principles, "simple by default, powerful when needed", consistency expectations | 200 |
| https://develop.kde.org/hig/accessibility/ | Accessibility expectations: keyboard operation, focus, contrast, scaling | 200 |
| https://develop.kde.org/docs/ | Entry point to current KDE developer documentation | 200 |
| https://develop.kde.org/docs/plasma/ | Plasma development documentation index | 200 |
| https://develop.kde.org/docs/plasma/widget/ | Plasma widget/plasmoid tutorial index; the reference page set used across the build and testing rules | 200 |
| https://develop.kde.org/docs/plasma/widget/setup/ | Project setup for a widget: package layout, build integration | 200 |
| https://develop.kde.org/docs/plasma/widget/configuration/ | KConfigXT-based configuration UI for widgets | 200 |
| https://develop.kde.org/docs/plasma/widget/properties/ | Widget properties exposed through the `Plasmoid` API | 200 |
| https://develop.kde.org/docs/plasma/widget/testing/ | `plasmawindowed`, `plasmoidviewer`, scale-factor and logging options used in integration-test guidance | 200 |
| https://develop.kde.org/docs/plasma/widget/translations-i18n/ | `i18n()`/`i18np`, translation catalog layout, `plasma_applet_<id>` domain naming | 200 |
| https://develop.kde.org/docs/plasma/widget/porting_kf6/ | Plasma 6 architecture (`Applet`, `Containment`, `PlasmoidItem`), metadata.json requirements, entry point, import changes | 200 |
| https://develop.kde.org/frameworks/kirigami/ | Kirigami framework documentation | 200 |
| https://develop.kde.org/docs/getting-started/kirigami/ | Kirigami getting-started path | 200 |
| https://community.kde.org/Plasma/DeveloperGuide | Plasma component map: applets, containments, PlasmaCore/PlasmaExtras, KPackage, plugin system (community wiki; contains Plasma 5-era tooling) | 200 |
| https://community.kde.org/KDE_Visual_Design_Group | Visual Design Group context for Plasma visual language | 200 |
| https://community.kde.org/Policies/Binary_Compatibility_Issues_With_C%2B%2B | KDE binary compatibility policy; used to justify the cost of widening a public header | 200 |
| https://api.kde.org/ | KDE API documentation index; note it serves the newest frameworks | 200 |
| https://api.kde.org/kcoreaddons.html | KCoreAddons API entry, including `KPluginFactory` | 200 |
| https://api.kde.org/kconfig-index.html | KConfig API index | 200 |
| https://api.kde.org/kpackage-index.html | KPackage API index | 200 |
| https://api.kde.org/kcmutils-index.html | KCMUtils API index; KCM plugin classes | 200 |
| https://api.kde.org/kirigami-index.html | Kirigami API index | 200 |
| https://api.kde.org/plasma-index.html | Plasma libraries API index | 200 |
| https://api.kde.org/ecm/ | Extra CMake Modules documentation index | 200 |
| https://api.kde.org/ecm/kde-module/KDEInstallDirs6.html | `KDEInstallDirs` install-path variables used in the packaging rule | 200 |
| https://invent.kde.org/ | KDE source repositories; the place to confirm behaviour against real code | 200 |
| https://invent.kde.org/sdk/clazy | clazy static analyzer | 200 |

## Qt documentation

| URL | Supports | Status |
| --- | --- | --- |
| https://doc.qt.io/qt-6/qtquick-performance.html | Frame budget, profiling, bindings, JS/type conversion, property resolution, models/views, delegate guidance, Loader/lazy init, clipping/overdraw/opacity, images, animations, memory | 200 |
| https://doc.qt.io/qt-6/qtquick-bestpractices.html | Separate UI from business logic, store state in models, prefer declarative bindings, bundle resources, translatable strings | 200 |
| https://doc.qt.io/qt-6/qml-codingconventions.html | QML code conventions referenced by the boundaries rule | 200 |
| https://doc.qt.io/qt-6/threads-qobject.html | Thread affinity, `moveToThread` parent constraint, per-thread event loop, `deleteLater` across threads, connection types | 200 |
| https://doc.qt.io/qt-6/qthread.html | Worker-object pattern and the documented constraints on subclassing `QThread` | 200 |
| https://doc.qt.io/qt-6/qthreadpool.html | Thread-pool use for short independent tasks | 200 |
| https://doc.qt.io/qt-6/qtconcurrent-index.html | `QtConcurrent` and `QFuture`-based work | 200 |
| https://doc.qt.io/qt-6/qobject.html | `connect`/`disconnect` semantics, context object, `QMetaObject::Connection`, `QT_NO_CONTEXTLESS_CONNECT`, `deleteLater` | 200 |
| https://doc.qt.io/qt-6/signalsandslots.html | Signals and slots overview | 200 |
| https://doc.qt.io/qt-6/qt.html | `Qt::ConnectionType` reference (Auto/Direct/Queued/BlockingQueued/Unique) | 200 |
| https://doc.qt.io/qt-6/qpointer.html | `QPointer` for non-owning references | 200 |
| https://doc.qt.io/qt-6/qqmlintegration-h.html | QML type-registration macros (`QML_ELEMENT`, `QML_SINGLETON`, `QML_UNCREATABLE`, …) | 200 |
| https://doc.qt.io/qt-6/qtqml-cppintegration-overview.html | Overview of QML/C++ integration options | 200 |
| https://doc.qt.io/qt-6/qtqml-cppintegration-data.html | Data ownership rules: engine ownership on method return, parent semantics, `CppOwnership` | 200 |
| https://doc.qt.io/qt-6/qtqml-cppintegration-definetypes.html | Registering types, singleton ownership by the engine, `QML_SINGLETON` semantics | 200 |
| https://doc.qt.io/qt-6/qtqml-cppintegration-contextproperties.html | Documented warnings about context properties: hidden from tooling, reported as unqualified access, re-evaluation cost | 200 |
| https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html | Property binding syntax and re-evaluation | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-loader.html | `active`, `asynchronous`, `setSource`, `sourceComponent`, `status` semantics | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-listview.html | View behaviour used in the models/views guidance | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-image.html | Image loading and `sourceSize` behaviour | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-item.html | Base item properties referenced in examples | 200 |
| https://doc.qt.io/qt-6/qmlapplications.html | QML application structure context | 200 |
| https://doc.qt.io/qt-6/qtest-overview.html | Qt Test overview: data-driven tests, `QSignalSpy`, `QTRY_*`, `QBENCHMARK` | 200 |
| https://doc.qt.io/qt-6/qtest.html | Macro reference: `QTRY_*` five-second default, benchmark macros | 200 |
| https://doc.qt.io/qt-6/qsignalspy.html | `QSignalSpy::isValid`, `wait()` defaults and chrono overload | 200 |
| https://doc.qt.io/qt-6/qtquicktest-index.html | Qt Quick Test: `QUICK_TEST_MAIN`, headless `-platform offscreen` requirement | 200 |
| https://doc.qt.io/qt-6/qml-qttest-testcase.html | `when`/`windowShown`, `tryCompare`, `wait`, `waitForRendering`, event delivery after show | 200 |
| https://doc.qt.io/qt-6/qml-qttest-signalspy.html | QML-side signal spy | 200 |
| https://doc.qt.io/qt-6/qstandardpaths.html | Test mode: redirected writable locations (`~/.qttest/...` on Unix) | 200 |
| https://doc.qt.io/qt-6/qml-qtqml-timer.html | QML `Timer`: `interval`, `repeat`, `running`, triggering behavior | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-animation.html | QML animation base: `running`, `loops`, `duration` | 200 |
| https://doc.qt.io/qt-6/qtqml-tooling-qmllint.html | `qmllint` warning categories, `all_qmllint` CMake target, `--max-warnings`, `--ignore-settings`, `--fix`, `--dry-run` | 200 |
| https://doc.qt.io/qt-6/qt-add-qml-module.html | `qt_add_qml_module()` behaviour, QML compilation, RESOURCES | 200 |
| https://doc.qt.io/qt-6/qt-standard-project-setup.html | `CMAKE_AUTOMOC`/`AUTOUIC` defaults, Qt CMake policies, version requirements | 200 |
| https://doc.qt.io/qt-6/qt-cmake-policy-qtp0001.html | `/qt/qml/` default resource prefix policy | 200 |
| https://doc.qt.io/qt-6/qtversionchecks.html | `QT_VERSION_CHECK` for version guards | 200 |

## Build tooling and general

| URL | Supports | Status |
| --- | --- | --- |
| https://cmake.org/cmake/help/latest/command/file.html | CMake's explicit statement that `file(GLOB)` should not collect sources | 200 |
| https://cmake.org/cmake/help/latest/prop_tgt/AUTOMOC.html | `AUTOMOC` target property | 200 |
| https://clang.llvm.org/extra/clang-tidy/ | clang-tidy integration guidance | 200 |
| https://vercel.com/blog/introducing-react-best-practices | Organisation model for a rule catalog (inspiration only; no React guidance is translated mechanically) | 200 |

## Additional sources cited by individual rules

| URL | Supports | Status |
| --- | --- | --- |
| https://develop.kde.org/hig/components/ | KDE HIG component guidance used by the component-reuse rule | 200 |
| https://doc.qt.io/qt-6/ | Qt 6 documentation index, cited as the entry point for Qt API claims | 200 |
| https://doc.qt.io/qt-6/qabstractitemmodel.html | `QAbstractItemModel` contract behind models and delegates | 200 |
| https://doc.qt.io/qt-6/qfuture.html | `QFuture` result access after asynchronous work | 200 |
| https://doc.qt.io/qt-6/qfuturewatcher.html | `QFutureWatcher` signals used to deliver results on the GUI thread | 200 |
| https://doc.qt.io/qt-6/qml-qtqml-binding.html | `Binding` element and delayed/restart semantics used by binding-overwrite guidance | 200 |
| https://doc.qt.io/qt-6/qml-qtqml-component.html | `Component` element and deferred creation | 200 |
| https://doc.qt.io/qt-6/qml-qtqml-qt.html | `Qt` object (`callLater`, `application`) referenced in QML examples | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-repeater.html | `Repeater` instantiation behaviour compared with views | 200 |
| https://doc.qt.io/qt-6/qnetworkaccessmanager.html | Asynchronous network API used as a non-blocking example | 200 |
| https://doc.qt.io/qt-6/qtconcurrentrun.html | `QtConcurrent::run` as an offloading mechanism | 200 |
| https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html | Models, views, and delegates guidance | 200 |
| https://doc.qt.io/qtcreator/creator-cpu-usage-analyzer.html | CPU usage analyzer used in profiling guidance | 200 |
| https://doc.qt.io/qtcreator/creator-qml-performance-monitor.html | QML performance monitor used in profiling guidance | 200 |
| https://github.com/KDAB/GammaRay | Runtime Qt/QML inspection tool named in profiling guidance | 200 |
| https://invent.kde.org/sdk/heaptrack | Heap profiler named in profiling guidance | 200 |
| https://perf.wiki.kernel.org/index.php/Main_Page | Linux `perf` documentation named in profiling guidance | 200 |

## Sources considered and rejected

- `https://develop.kde.org/docs/features/kcm/` returned HTTP 200 but served an Apache directory listing, not documentation. It is not cited.
- `https://develop.kde.org/hig/patterns/`, `https://doc.qt.io/qt-6/thread-basics.html`, `https://doc.qt.io/qt-6/qtqml-cmake-qt-add-qml-module.html`, `https://api.kde.org/frameworks/kcoreaddons/html/index.html` returned 404 on 2026-10-20. They are not cited; equivalent live pages are used instead.

## Local observations (not URLs)

Recorded on 2026-10-20 on the verification machine:

- `plasmashell --version` → `plasmashell 6.8.0`.
- `qmake6 -query QT_VERSION` and `pkg-config --modversion Qt6Core` → `6.11.1`.
- `/usr/share/ECM/cmake/ECMConfigVersion.cmake` → `PACKAGE_VERSION "6.31.0"`.
- `qmllint` (a `qtchooser` wrapper reporting `1.0`, running Qt 5) and `qmllint6` (6.11.1) present in `/usr/bin`; use `qmllint6` for Qt 6 QML.
- `kpackagetool6`, `plasmoidviewer`, `plasmawindowed`, `kcmshell6`, `systemsettings` present in `/usr/bin`; `plasma-settings` was not present.
- `clazy` and `clang-tidy` not found on `PATH`.
- Installed plasmoid package shape: `/usr/share/plasma/plasmoids/<id>/{metadata.json,contents/ui/main.qml}`.
- `K_PLUGIN_FACTORY`, `K_PLUGIN_FACTORY_DEFINITION`, `K_PLUGIN_FACTORY_WITH_JSON` present in KF6 KCoreAddons headers.
- `kcmutils_add_qml_kcm`, `kcmutils_generate_module_data`, `kcmutils_generate_desktop_file` are public in the KF6KCMUtils CMake package; `__kcmutils_target_qml_sources` is present but internal.
- `KQuickConfigModule` and `KQuickManagedConfigModule` headers present under `/usr/include/KF6/KCMUtilsQuick/` on KF6 6.31.0.

## Additional sources cited across the bundle

Added during integration on 2026-10-20 after a full-bundle sweep. Every row was requested with the same `curl` command and returned the status shown.

| URL | Cited by | Status |
| --- | --- | --- |
| https://api.kde.org/kconfigdialog.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://api.kde.org/kpagedialog.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://api.kde.org/kquickconfigmodule.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://api.kde.org/qml-org-kde-kcmutils-simplekcm.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://api.kde.org/qml-org-kde-kirigami-platform-theme.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://develop.kde.org/docs/features/configuration/configdialog/ | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://develop.kde.org/docs/features/configuration/kcm/ | kde-plasma-ui-ux/assets/ui-review.md, kde-plasma-ui-ux/references/plasma-components.md, kde-plasma-ui-ux/references/qt-qml-kirigami.md, kde-plasma-ui-ux/references/review-checklist.md | 200 |
| https://develop.kde.org/docs/features/configuration/kconfig_xt/ | kde-plasma-ui-ux/references/plasma-components.md, kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://develop.kde.org/docs/features/configuration/porting_kf6/ | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://develop.kde.org/docs/getting-started/kirigami/components-dialogs/ | kde-plasma-ui-ux/references/plasma-components.md | 200 |
| https://develop.kde.org/docs/getting-started/kirigami/components-scrollablepages_listviews/ | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://develop.kde.org/docs/getting-started/kirigami/style-colors/ | kde-plasma-ui-ux/references/qt-qml-kirigami.md, kde-plasma-ui-ux/references/review-checklist.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://develop.kde.org/docs/getting-started/kirigami/style-typography/ | kde-plasma-ui-ux/references/qt-qml-kirigami.md, kde-plasma-ui-ux/references/review-checklist.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://develop.kde.org/docs/plasma/widget/plasma-qml-api/ | kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/plasma-components.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://develop.kde.org/docs/plasma/widget/qml/ | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://develop.kde.org/hig/displaying_content/ | kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/plasma-components.md | 200 |
| https://develop.kde.org/hig/getting_input/ | kde-plasma-ui-ux/references/interaction-patterns.md | 200 |
| https://develop.kde.org/hig/icons/ | kde-plasma-ui-ux/references/review-checklist.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://develop.kde.org/hig/kde_app_design/ | kde-plasma-ui-ux/references/design-principles.md | 200 |
| https://develop.kde.org/hig/layout_and_nav/ | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/review-checklist.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://develop.kde.org/hig/powerful_when_needed/ | kde-plasma-ui-ux/references/design-principles.md, kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/plasma-future-proposals.md | 200 |
| https://develop.kde.org/hig/simple_by_default/ | kde-plasma-ui-ux/references/design-principles.md, kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/plasma-future-proposals.md | 200 |
| https://develop.kde.org/hig/status_changes/ | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://develop.kde.org/hig/text_and_labels/ | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/interaction-patterns.md, kde-plasma-ui-ux/references/qt-qml-kirigami.md, kde-plasma-ui-ux/references/review-checklist.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://doc.qt.io/qt-6/accessible.html | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/qt-qml-kirigami.md, kde-plasma-ui-ux/references/review-checklist.md | 200 |
| https://doc.qt.io/qt-6/highdpi.html | kde-plasma-ui-ux/references/accessibility.md | 200 |
| https://doc.qt.io/qt-6/qaccessible.html | kde-plasma-ui-ux/references/accessibility.md | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-accessible.html | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/qt-qml-kirigami.md, kde-plasma-ui-ux/references/review-checklist.md | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-behavior.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-layoutmirroring.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-text.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qml-qtquick-transition.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qobject.html#connect | kde-plasma-best-practices/references/rules/cpp/signals-slots.md | 200 |
| https://doc.qt.io/qt-6/qtquick-controls-qmlmodule.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qtquick-positioning-layouts.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qtquick-positioning-topic.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://doc.qt.io/qt-6/qtquick-statesanimations-states.html | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://invent.kde.org/frameworks/ki18n/-/blob/master/docs/programmers-guide.md | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://invent.kde.org/frameworks/kirigami/-/raw/v6.8.0/src/platform/units.h | kde-plasma-ui-ux/references/qt-qml-kirigami.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/CMakeLists.txt | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/import/SensorFace.qml | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/SensorFaceController.cpp | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/facepackages/linechart/metadata.json | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/facepackages/linechart/contents/faceproperties | kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/packagestructure/sensorfacepackage.cpp | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/tree/master/faces/facepackages | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/faces/CMakeLists.txt | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/page/FaceLoader.cpp | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/page/FaceControl.qml | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/page/FacesModel.cpp | kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/pages/overview.page | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/plasma-systemmonitor/-/tree/master/src/page | kde-plasma-best-practices/references/plasma-development.md, kde-plasma-ui-ux/references/configurable-views.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/CMakeLists.txt | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/FaceLoader.h | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/SensorFaceController.h | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/SensorFace_p.h | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/libksysguard/-/blob/master/sensors/Sensor.h | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/6.8/applets/systemmonitor/systemmonitor/package/contents/ui/FullRepresentation.qml | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/6.8/applets/systemmonitor/systemmonitor/package/contents/ui/main.qml | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/6.8/applets/systemmonitor/systemmonitor/systemmonitor.cpp | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/6.8/applets/systemmonitor/systemmonitor/systemmonitor.h | kde-plasma-best-practices/references/plasma-development.md | 200 |
| https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html | kde-plasma-ui-ux/references/accessibility.md, kde-plasma-ui-ux/references/visual-consistency.md | 200 |
| https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | kde-plasma-ui-ux/references/accessibility.md | 200 |
