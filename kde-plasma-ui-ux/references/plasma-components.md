# Plasma Components and Structures

## Scope

Use this reference to choose a component stack and to structure Plasma widgets, panels, popups, tray items, configuration dialogs, System Settings modules, and Qt Widgets dialogs. It does not enumerate every API. Import paths, property names, and availability differ by release. Exact API and import availability must be checked against the target version and `https://api.kde.org/` before use.

## Selection order

Choose the first option that satisfies the need. A later option requires a recorded reason.

This order is for new surfaces and for new UI inside an already-Qt-Quick surface. It is not a migration mandate. If the surface already exists in Qt Widgets, the existing toolkit comes first: keep its platform style, `QPalette`, and KDE Frameworks integration, and do not migrate toolkits as part of a UI change without an explicit decision and a separate plan.

| Order | Stack | Use when | Evidence |
|---|---|---|---|
| 1 | Kirigami | New application windows, pages, settings forms, dialogs, overlays, list delegates, empty states | [Official] KDE recommends QtQuick with Kirigami for new applications |
| 2 | Plasma-specific: `PlasmaCore`, `PlasmaExtras`, `PlasmaComponents` | The code runs inside a Plasma widget or shell surface and needs Plasma styling or shell integration | [Official] Documented in Plasma's QML API |
| 3 | Qt Quick Controls | A standard control is missing from the higher layers, or a non-Plasma QtQuick application needs a neutral control | [Official] Qt documentation |
| 4 | Custom control | None of the above meets a documented requirement, and the limitation is recorded | [Recommendation] Last resort |
| — | Existing Qt Widgets | The surface is already a Qt Widgets dialog or window; keep its toolkit and platform style | [Recommendation] Consistency with the existing codebase outranks a toolkit migration |

Rules:

- [Recommendation] Do not import Plasma-specific modules into a standalone Kirigami application unless the Plasma plugin dependency is intentional, packaged, and documented.
- [Recommendation] Do not reimplement a control to change its look. Style through the theme, or document why the platform control cannot meet the requirement.
- [Official] `PlasmaComponents 3` extends Qt Quick Controls 2 and keeps the same API, with Plasma-specific defaults such as panel-aware text color. Read the Plasma source for behavior changes.
- [Official] `PlasmaExtras` provides Plasma-consistent types such as `Heading` and `Paragraph`; it requires its own import.
- [Official] `PlasmaCore` provides shell-level primitives; `PlasmaCore.ColorScope` is referenced in Plasma configuration documentation for theme-aware colors.
- [Official] `PlasmaComponents 2` was removed in Plasma 6.0. Do not copy Plasma 5 imports.

## Plasmoid structure

- [Official] A widget package contains `metadata.json` and its QML under `contents/ui/`; the entry point is `contents/ui/main.qml`. Configuration schemas live under `contents/config/`.
- [Official] Importing `org.kde.plasma.plasmoid` (unversioned in Plasma 6) gives the root item a `Plasmoid` property group and a lowercase `plasmoid` context property. Both expose the same values; prefer one style consistently.
- [Official] Documented `Plasmoid` properties include `compactRepresentation`, `fullRepresentation`, `configuration`, `busy`, `backgroundHints`, `icon`, and screen-availability properties. Confirm the full set for the target version.
- [Recommendation] Keep `main.qml` as composition, not as a monolith. Put representations, configuration UI, and reusable delegates in separate files.
- [Recommendation] Declare a compact representation that remains legible at panel size, and a full representation that handles the expanded or popup context.
- [Official] Use `Plasmoid.busy` for shell-level busy indication rather than drawing a second independent spinner over the widget.
- [Recommendation] Root the full representation in `PlasmaExtras.Representation`, not a bare `Item` with a custom background. `Representation` supplies the page surface, margins from the theme background metrics, and `collapseMarginsHint`; a bare `Item` loses all three and reads as a foreign window.
- [Recommendation] Give the full representation a `PlasmaExtras.PlasmoidHeading` header. Official applets put toggles and icon-only actions there; `BasicPlasmoidHeading` auto-hides its title when the containment already draws one.
- [Observed] The system tray merges a third-party applet's header and footer into its own chrome only when the full representation is a `PlasmaComponents3.Page` or `PlasmaExtras.Representation` whose header is a `PlasmoidHeading`. This is the cheapest available native-feel upgrade for a third-party widget.
- [Recommendation] Drive `Plasmoid.status` from real state (`ActiveStatus` only when the widget has something actionable to say) and keep the symbolic icon in sync. Do not leave a monitoring widget permanently `Active`.
- [Official] Test with `plasmawindowed <plugin-id>` during development; test in the actual panel and desktop containment before review.
- [Recommendation] Set the widget id, name, and description in `metadata.json`; remove stale translated names and legacy `metadata.desktop` files when porting.
- [Recommendation] Treat `metadata.json` as part of the UI contract: a reverse-DNS id you own (never `org.kde.*` for a third-party package), real `Website`, `BugReportUrl`, `X-KDE-Keywords`, `Version`, and a `Messages.sh` plus `po/` when the package ships translations. Incomplete metadata is the first thing a KDE reviewer sees.

## Panels

- [Recommendation] Treat panel space as scarce. A panel widget must work at the panel's thickness, in horizontal and vertical orientation, and at the user's scale factor.
- [Recommendation] Do not hardcode width, height, or margins. Derive size from content, `Kirigami.Units`, and layout constraints.
- [Recommendation] The compact representation should communicate state at a glance and open the full representation for detail.
- [Official] `Plasmoid.backgroundHints` controls whether the desktop widget draws a background. Use the default unless the design requires otherwise, and verify the enum for the target version.
- [Recommendation] Avoid focus traps in panel popups. Closing the popup must return focus to the panel item.

## Popups, dialogs, and overlays

- [Official] The HIG says to push a new page when content fills the window or view, use `Kirigami.OverlaySheet` for auxiliary read-only narrow content, and reserve dialogs for focused decisions.
- [Recommendation] Keep popup content sized to its purpose. A popup that scrolls through a full application view should be a page or window instead.
- [Observed] A workable envelope from the official notifications applet: content width `gridUnit * 18` (`gridUnit * 22` when centred), clamped to at most three times that; minimum edge distance `2 * gridUnit`; maximum vertical use `0.8` of the screen; a body-text cap of 8 lines with a scrollbar only when overflowing. Start there and justify deviations.
- [Recommendation] Do not make a panel popup behave like a full application viewport. If the content needs persistent navigation across many destinations, reconsider whether it belongs in a popup at all.
- [Recommendation] Define Escape behavior, the default action, initial focus, and focus return. Do not open a modal dialog for information that can be shown inline.
- [Recommendation] Avoid stacking popups. If a popup needs another popup, reconsider the structure.
- [Official] Kirigami documents `Dialog`, `OverlaySheet`, and dialog types as part of its component set; use them before building custom overlays.
- [Recommendation] Verify that the chosen popup type behaves correctly in a panel, on the desktop, and in a windowed test harness.

## System tray

- [Recommendation] A tray item is a plasmoid with a severely constrained compact representation. Prioritize a recognizable symbolic icon and a single clear state.
- [Observed] In Plasma 6.8, tray discovery is decided by a non-empty `X-Plasma-NotificationAreaCategory` in `metadata.json`; `applets/systemtray/plasmoidregistry.cpp` skips plugins without one. `X-Plasma-NotificationArea` remains documented, so set both, but do not rely on the boolean alone.
- [Observed] The tray's popup title is the string "Status and Notifications". An applet that declares a tray category appears inside that popup; it does not inject content into it.
- [Official] The notifications applet exposes no provider registry or page-injection API. The only supported ways for third-party content to appear in that surface are a real `KNotification` (with a `.notifyrc` event) and the D-Bus `org.kde.JobViewServer` / `org.kde.JobViewV2` progress protocol. Do not design around content injection.
- [Recommendation] Default a tray entry to disabled (`KPlugin.EnabledByDefault: false`) unless the widget's whole purpose is a tray indicator. A duplicate of an existing official indicator is clutter, and the user decides what lives in the tray.
- [Recommendation] Do not rely on hover tooltips for essential status; tray items are frequently scanned without pointer interaction.
- [Recommendation] Expose detail and actions through the expanded representation or context menu.
- [Unknown] Tray-specific status and attention APIs vary by Plasma release. Verify any such property in the target branch and `api.kde.org`; do not infer it from a Plasma 5 example.
- [Recommendation] Test with the tray in a panel of minimum thickness and with a scaled display.

## Context menus

- [Recommendation] Support both right-click and the keyboard Menu key. A context menu that only opens by pointer is an accessibility defect.
- [Recommendation] Group actions by task, use standard actions and shortcuts where they exist, and place destructive actions last with clear separation.
- [Recommendation] Keep the menu short. Move deep or rarely used operations into a settings or secondary surface.
- [Recommendation] Give every action a visible label and an icon consistent with its meaning; do not use icon-only menu items.
- [Unknown] The recommended menu component differs between shell and application contexts. Verify the available type and import for the target version before implementation.

## Configuration dialogs

- [Official] Widget configuration is declared in `contents/config/main.xml` with KConfig types and is exposed at runtime as `plasmoid.configuration.<name>`.
- [Official] Every widget has a configure action by default; the generated dialog includes at least the global shortcut setting.
- [Recommendation] Build the configuration UI with `Kirigami.FormLayout`, grouped by task, with labels that state the effect rather than the mechanism.
- [Official] Apply saved settings immediately; do not require an application restart.
- [Recommendation] Provide defaults and a reset path. A configuration dialog is not a place to hide the primary workflow.
- [Official] For a color setting that should follow the theme, prefer an empty string default resolved to a theme role at render time rather than storing a fixed color in the config file.

## System Settings modules (KCMs)

- [Official] A KCM is a plugin loaded by a settings host; it combines a QML UI module with a C++ library that holds the logic. It can be loaded by `systemsettings`, `plasma-settings`, or `kcmshell6`.
- [Official] New KCMs should be built with QML and Kirigami. Legacy QtWidgets KCMs are not recommended for new modules and cannot load in `plasma-settings`.
- [Official] For managed settings, derive the C++ backend from `KQuickManagedConfigModule` and declare the settings in KConfigXT (`*.kcfg` plus `*.kcfgc`); the generated `KConfigSkeleton` supplies defaults, apply, and reset. Use `KQuickConfigModule` directly only when the module manages its own state.
- [Official] Register the module with `kcmutils_add_qml_kcm()` and export the C++ class through `K_PLUGIN_FACTORY_WITH_JSON` with the module's metadata JSON.
- [Recommendation] Choose one apply model and state it in the module: instant-apply commits each change immediately; Apply/Reset keeps pending values until Apply and restores them on Reset. Do not mix both. In either model, saved settings take effect without an application restart.
- [Recommendation] Keep one module focused on one configuration domain. Use Kirigami pages and form layouts rather than a bespoke window chrome.
- [Recommendation] Make the current value, the pending value, and the apply/reset state visually distinct. Do not silently discard edits.
- [Recommendation] Provide searchable, front-loaded labels and a sensible default view; settings are frequently opened to answer one question.
- [Official] Test the module through each wrapper the product supports: `systemsettings <module>`, `plasma-settings -m <module>`, or `kcmshell6 <module>`. Verify which wrappers exist on the target system.
- [Recommendation] Do not assume the module has a window of its own; it may be embedded in a settings shell with different sizing and navigation.

## Qt Widgets dialogs

- [Recommendation] In an existing QtWidgets application, follow the platform style and KDE Frameworks integration already used by that application. Do not restyle standard dialogs to imitate Kirigami.
- [Recommendation] Use standard dialog roles, default and escape buttons, and standard shortcuts. Preserve the application's existing menu and toolbar conventions.
- [Recommendation] Do not mix QtWidgets and QtQuick surfaces in one dialog without a documented reason and a verified focus/ownership model.
- [Recommendation] New application UI should use QtQuick with Kirigami unless the repository has a documented constraint; for existing QtWidgets code, consistency with that codebase outranks a toolkit migration.

## API verification protocol

1. Identify the exact Plasma, Qt, and KF versions from the repository or the user.
2. Confirm the module, type, property, signal, and enum on `https://api.kde.org/` for that version.
3. Confirm the import URI and major version in current documentation or the target branch.
4. Check whether the type is deprecated, removed, or Plasma-only.
5. If a fact cannot be verified, mark it `[Unknown]` and state what would resolve it. Do not ship an invented API.

## Review checklist

1. The component choice follows the selection order and records any skip.
2. Imports and properties are verified for the target version.
3. Compact and full representations both work in their real containers.
4. Panel, popup, tray, and window contexts were tested where applicable.
5. Focus entry, Escape, default action, and focus return are defined.
6. Context menus work from the keyboard.
7. Configuration applies immediately and has defaults/reset.
8. KCM was tested in every supported wrapper.
9. No Plasma 5 import or removed component remains.
10. Any `[Unknown]` API is resolved or explicitly blocked.
11. The full representation is a `PlasmaExtras.Representation` with a `PlasmoidHeading`, not a bare `Item` with custom chrome.
12. Popup sizing sits inside the documented envelope, or the deviation is recorded with a reason.
13. `Plasmoid.status` and the compact icon reflect real state; the widget is not permanently active.
14. Metadata is complete and the package id does not squat an `org.kde.*` namespace.

## Sources

- Plasma Widget tutorial — https://develop.kde.org/docs/plasma/widget/ — Accessed: 2026-10-20
- Plasma widget setup — https://develop.kde.org/docs/plasma/widget/setup/ — Accessed: 2026-10-20
- Widget properties (`Plasmoid` group) — https://develop.kde.org/docs/plasma/widget/properties/ — Accessed: 2026-10-20
- Plasma's QML API — https://develop.kde.org/docs/plasma/widget/plasma-qml-api/ — Accessed: 2026-10-20
- Widget configuration — https://develop.kde.org/docs/plasma/widget/configuration/ — Accessed: 2026-10-20
- Settings module (KCM) development — https://develop.kde.org/docs/features/configuration/kcm/ — Accessed: 2026-10-20
- Kirigami documentation — https://develop.kde.org/frameworks/kirigami/ — Accessed: 2026-10-20
- Kirigami getting started — https://develop.kde.org/docs/getting-started/kirigami/ — Accessed: 2026-10-20
- Kirigami dialog components — https://develop.kde.org/docs/getting-started/kirigami/components-dialogs/ — Accessed: 2026-10-20
- HIG: displaying content (page, dialog, overlay choice) — https://develop.kde.org/hig/displaying_content/ — Accessed: 2026-10-20
- KDE API reference — https://api.kde.org/ — Accessed: 2026-10-20
- plasma-workspace system tray applet, branch `Plasma/6.8` (discovery filter, popup title, header merging) — https://invent.kde.org/plasma/plasma-workspace/-/tree/Plasma/6.8/applets/systemtray — Accessed: 2026-10-20
- plasma-workspace notifications applet, branch `Plasma/6.8` (popup sizing envelope) — https://invent.kde.org/plasma/plasma-workspace/-/tree/Plasma/6.8/applets/notifications — Accessed: 2026-10-20
- Installed `org.kde.plasma.systemmonitor` and `org.kde.plasma.vault` on Plasma 6.8.0 — local, Accessed: 2026-10-20

## Version notes

Verified against KDE documentation published on 2026-10-20, with a local baseline of Plasma 6.8.0, Qt 6.11.1, and KF6.

- [Official] PlasmaComponents 2 is removed in Plasma 6.0; its import must not appear in new code.
- [Recommendation] Import major versions are not stable across KF majors. Treat every import and property in this document as a name to verify, not a guaranteed signature.
- [Unknown] Tray-specific and shell-specific APIs are the least consistently documented surface. Confirm them in the target branch before design approval, not after implementation.
