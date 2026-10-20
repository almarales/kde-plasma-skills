# Configurable views

## Scope

Use this reference when an application must let the user choose **how a datum is presented** — a line chart, a pie chart, a table, a text row — and keep that choice across sessions. The evidence base is the System Monitor (`plasma-systemmonitor`) and the face library it shares with `libksysguard`: the first-party Plasma surface where a rendered item is a separately installable plugin.

This file covers the **design contract**: what the app owns, what the pluggable view owns, what the user is offered, and what the user must never be shown. The plugin plumbing (KPackage structures, C++ instantiation, config groups) is in `../kde-plasma-best-practices/references/plasma-development.md`; the visual grammar the views must obey is in `official-applet-anatomy.md`.

Evidence base, inspected on 2026-10-20 against upstream `master` (Plasma 6.8 era). Upstream code is cited as `repository/path → symbol`; line numbers were not captured in this pass, so re-open the file before quoting a line.

## The one rule that explains the rest

**The app owns the data and the frame; the pluggable view owns the rendering of one item, and nothing else.**

`SensorFaceController` returns a `QQuickItem` (`fullRepresentation()`, `compactRepresentation()`) that the host places inside its own layout. The view never owns the page, the page never re-implements the rendering, and the two never negotiate through shared mutable state `[Official]` (`libksysguard/faces/SensorFaceController.cpp → SensorFaceController::fullRepresentation`, `plasma-systemmonitor/src/page/FaceControl.qml`).

[Official] The host-to-view contract is small and explicit, and both sides speak it through the `org.kde.ksysguard.faces` QML module:

- The view's shared base is `Faces.AbstractSensorFace`, which exposes the app-owned `controller` (sensor ids, colours, labels) to the view's QML (`libksysguard/faces/import/SensorFace.qml`).
- The host tells the view **how much space it has** before showing it: `loader.controller.fullRepresentation.formFactor = Faces.SensorFace.Constrained` (`plasma-systemmonitor/src/page/FaceControl.qml → FaceControl.updateContentItem`).
- The host replaces the view in place by reassigning its content item: `control.contentItem = loader.controller.fullRepresentation`, re-run on `faceIdChanged` (`FaceControl.qml → FaceControl.updateContentItem`).

Consequences for design:

- A change to one view must not require a change in the app. The app's contract with a view is narrow: *render these sensors, in this space, with this title*.
- Two views of the same datum must be **visually indistinguishable in context**: same frame, same spacing, same typography ladder, same theme roles. Otherwise the user is not choosing a visualization, they are choosing a different application.
- A view that cannot honour the app's contract is a bug in the view, not a special case to branch around in the app.

## What the user is offered

[Official] The picker is populated by listing installed packages and showing each one's **display name**, never its identifier: `FacesModel::reload()` calls `KPackage::PackageLoader::self()->listPackages("KSysguard/SensorFace")` and stores `plugin.name()` as the display role and `plugin.pluginId()` as the id role (`libksysguard/faces/SensorFaceController.cpp → FacesModel::reload`).

[Official] The list ends with an explicit **"No Chart"** entry, which maps to a null face: `FacesModel::rowCount()` returns `m_faceLoaders.size() + 1` and the extra row resolves to `nullptr` (`plasma-systemmonitor/src/page/FacesModel.cpp → FacesModel::data`, `FacesModel::faceAtIndex`).

[Recommendation] Two unrelated classes are named `FacesModel` here — the library's lists the views available on the system, the application's lists the views placed on the current page plus the empty option. When you read either file, check which side you are on before concluding that the lists are the same.

[Recommendation] Offer the empty choice deliberately. A user who wants a metric gone must be able to say so, and "off" must be a first-class value in the model, not an empty string in a text field.

[Recommendation] Never show a view that cannot accept the datum it is offered for. The System Monitor solves this with per-view capability declarations (below) rather than with a hardcoded compatibility table.

## Capability negotiation instead of hardcoded branches

[Official] Every view declares what it can do in a `faceproperties` KConfig file, read as the `Config` group (`libksysguard/faces/SensorFaceController.cpp → SensorFaceController::supportsSensorsColors`, `supportsTotalSensors`, `supportsLowPrioritySensors`, `maxTotalSensors`). The shipped line chart declares `SupportsSensorsColors=true`, `SupportsTotalSensors=false`, `SupportsLowPrioritySensors=true` (`libksysguard/faces/facepackages/linechart/contents/faceproperties`):

| Key | Meaning when absent |
| --- | --- |
| `SupportsSensors` | Defaults to `true`; when `false` the app hides the sensor-selection page |
| `SupportsTotalSensors` | Defaults to `false`; without it the view cannot show a total beside the live value |
| `MaxTotalSensors` | Defaults to `1`; caps how many totals the view can render |
| `SupportsSensorsColors` | Defaults to `false`; without it the per-series colour editor is hidden |
| `SupportsLowPrioritySensors` | Defaults to `false`; without it the low-priority sensor list is hidden |

[Recommendation] This is the pattern to copy: **the view declares its capabilities, the app renders the options it can honour.** The alternative — the app hardcoding "if the view is a pie chart, hide X" — is a coupling that breaks the moment a third-party view appears.

## Configuration ownership

[Official] Two separate owners, and the boundary is clean:

- **The view owns its own configuration UI**: `SensorFaceController::faceConfigUi()` loads `ui/Config.qml` from the view package and hosts it in the app's configuration dialog (`libksysguard/faces/SensorFaceController.cpp → SensorFaceController::faceConfigUi`). A view with nothing to configure simply ships no `Config.qml`.
- **The app owns the per-item appearance**: title, `showTitle`, sensor colours, sensor labels, and the update-rate limit live in the app's own config group, not in the view's (`SensorFaceController` reads them from the `Appearance`, `SensorColors`, and `SensorLabels` groups).

[Official] Per-view settings are namespaced by the view's own identifier: in a shipped page preset, one item reads `[Face-106123380916688][org.kde.ksysguard.piechart][General] showLegend=false`, so the `piechart` view's own keys never collide with another view's (`plasma-systemmonitor/src/pages/overview.page`).

[Recommendation] A view that needs structured settings declares a schema (`mainconfigxml`) so the app can expose them generically; the app must not open the view's config file directly.

## The datum is addressed by path, and the view says what to emphasize

[Official] Sensors are referenced by path (`cpu/all/usage`, `memory/physical/used`, `network/(?!all).*/download`), and each item declares three ordered lists: `totalSensors`, `highPrioritySensorIds`, and `lowPrioritySensorIds` (`plasma-systemmonitor/src/pages/overview.page`, `[Face-…][Sensors]`).

[Official] The app resolves them asynchronously through `KSysGuard::SensorQuery` and reports the ones that do not resolve: `SensorResolver` collects `missing` ids and the controller exposes `missingSensors` (`libksysguard/faces/SensorFaceController.cpp → SensorResolver::execute`).

[Official] The application surfaces that state in the interface: `MissingSensorsDialog.qml` in the System Monitor (`plasma-systemmonitor/src/page/MissingSensorsDialog.qml`).

[Recommendation] Two rules follow. First, **resolution failure is a visible state, never a blank cell** — a user must be able to tell "this sensor is gone" from "this sensor is idle". Second, **the view decides emphasis, the app decides availability**: the app resolves and validates the sensors, the view chooses which of them are headline, secondary, or absent.

## The layout is data, and it is shareable

[Official] The page layout is a tree of KConfig groups, not a hardcoded QML hierarchy: `[page]`, `[page][row-0]`, `[page][row-0][column-0]`, `[page][row-0][column-0][section-0]`, with each section pointing at a face instance by `face=Face-<id>` (`plasma-systemmonitor/src/pages/overview.page`).

[Official] A saved layout is a **Plasma applet package**: `savePreset()` writes a `Plasma/Applet` `metadata.json` with `X-Plasma-RootPath: org.kde.plasma.systemmonitor` and installs it with `KPackage::PackageJob::install`; `PresetsModel::reload()` finds them again by scanning `Plasma/Applet` packages with that root path (`libksysguard/faces/SensorFaceController.cpp → SensorFaceController::savePreset`, `PresetsModel::reload`).

[Recommendation] A layout the user assembled is worth more than the default, and a user who invested in one expects to keep it, move it, and hand it to someone else. Treat "save this arrangement" and "load someone else's arrangement" as first-class features of any configurable dashboard, and make the artefact an installable package so it survives upgrades.

## Editing is a state of the same tree

[Official] The editor operates on the same page tree the renderer uses, in dedicated components: `PageEditor.qml`, `EditorToolBar.qml`, `RowControl.qml`, `ColumnControl.qml`, `SectionControl.qml`, `MoveButton.qml`, and the dialogs `PageSortDialog.qml`, `PageDialog.qml`, `LoadPresetDialog.qml` (`plasma-systemmonitor/src/page/`).

[Recommendation] Keep editing a **mode of the same data model**, not a parallel editor model. When the editor and the renderer own separate structures, they drift, and the drift only shows up in a layout the user built by hand — the case nobody tests.

## Testable rules

1. Every pluggable view is reachable by display name; no identifier string reaches the interface.
2. A "none"/off option exists and maps to a null selection, not to an empty string.
3. Options the selected view cannot honour are not rendered. No `if (view === "piechart")` branches in the app.
4. No view ships an absolute colour, font, or spacing literal; it uses the same theme roles as the rest of the app (`official-applet-anatomy.md`).
5. Every view provides a title that fits the same type ramp as any other view.
6. A sensor that fails to resolve produces a visible state, not an empty rendering.
7. The app owns the frame, the layout, and the data; the view owns pixels for one item only.
8. A user-assembled layout can be saved, reloaded, and shared as an installable package.
9. The editor and the renderer read the same structure; no parallel editor-only model exists.

## Sources

- plasma-systemmonitor, `src/page/` (page tree, editor, face control) — https://invent.kde.org/plasma/plasma-systemmonitor/-/tree/master/src/page — Accessed: 2026-10-20
- plasma-systemmonitor, `src/pages/overview.page` (shipped layout preset, KConfig group tree) — https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/pages/overview.page — Accessed: 2026-10-20
- plasma-systemmonitor, `src/faces/CMakeLists.txt` (faces shipped by the app itself) — https://invent.kde.org/plasma/plasma-systemmonitor/-/blob/master/src/faces/CMakeLists.txt — Accessed: 2026-10-20
- libksysguard, `faces/SensorFaceController.cpp` (discovery, capabilities, presets, missing sensors) — https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/SensorFaceController.cpp — Accessed: 2026-10-20
- libksysguard, `faces/facepackages/linechart/metadata.json` (view plugin declaration) — https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/facepackages/linechart/metadata.json — Accessed: 2026-10-20
- libksysguard, `faces/facepackages/` (the seven chart views) — https://invent.kde.org/plasma/libksysguard/-/tree/master/faces/facepackages — Accessed: 2026-10-20
- libksysguard, `faces/packagestructure/sensorfacepackage.cpp` (required and optional files of a view package) — https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/packagestructure/sensorfacepackage.cpp — Accessed: 2026-10-20
- libksysguard, `faces/facepackages/linechart/contents/faceproperties` (capability declaration) — https://invent.kde.org/plasma/libksysguard/-/blob/master/faces/facepackages/linechart/contents/faceproperties — Accessed: 2026-10-20

## Version notes

- Verified against upstream `master` on 2026-10-20. The face architecture has been stable across Plasma 6, but the plugin id prefix, the package structure name, and the capability keys are project conventions, not a published API contract: re-read them before relying on them.
- [Unknown] The edit-mode entry point (`applicationWindow.editing`-style state) was not verified in this pass; the editor components are cited directly instead.
- [Recommendation] The System Monitor is an application, not a widget. Its layout, preset, and face mechanisms do not transfer to a plasmoid unchanged; a plasmoid that wants per-item visualizations should stay inside one package unless it has a reason to ship plugins.
