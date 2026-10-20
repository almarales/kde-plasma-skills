# Widget lifecycle

## Scope

Use this reference for the ordered path that turns an empty directory into a published Plasma 6 widget. It owns the **order** and the **hand-offs**; it does not restate the rules. Every step links to the reference that states the rules for it, so there is one source of truth per concern.

The authoritative rules live in the other two skills of this bundle: design in `kde-plasma-ui-ux`, engineering in `kde-plasma-best-practices`. This file is the map between them.

Evidence labels are the ones used across the bundle: `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, `[Unknown]`.

## 1. Decide the backend first

`[Recommendation]` The backend decision constrains everything downstream: what the QML can reach, whether the widget needs a build, and how it is tested. Settle it before writing a single line of QML. See `backends.md`.

## 2. Scaffold the package

`[Official]` A Plasma 6 widget is a KPackage with `Plasma/Applet` structure: `metadata.json` plus `contents/` holding `ui/main.qml` and, when configurable, `config/main.xml` and `config/config.qml` (`../kde-plasma-best-practices/references/plasma-development.md`).

`[Recommendation]` Copy `assets/scaffold/` and change three things: `KPlugin.Id` to a reverse-DNS you own, `KPlugin.Name`, and `KPlugin.Icon`. The scaffold is deliberately minimal and passes the bundle's own checker unchanged.

## 3. Declare the metadata

`[Official]` The Plasma 6 porting guide requires `"X-Plasma-API-Minimum-Version": "6.0"`, a top-level `"KPackageStructure": "Plasma/Applet"`, and the removal of `X-Plasma-MainScript` and `X-Plasma-API`. A widget without the minimum-version key is treated as Plasma 5 only and does not appear in the UI (`../kde-plasma-best-practices/references/forward-compatibility.md`, rule `FWD-04`).

`[Recommendation]` Add `KPlugin.License` (an SPDX id), `KPlugin.Website` and `KPlugin.BugReportUrl` while the file is still open. A KDE reviewer reads `metadata.json` first.

## 4. Declare the configuration

`[Official]` Every value in `contents/config/main.xml` is exposed to the configuration page as a top-level `cfg_<entry>` property; declaring one `property alias cfg_<entry>: <widget>.<property>` per key is what gives the page its Apply and Discard transaction. The page reads the current value from `Plasmoid.configuration.<entry>` (`../kde-plasma-best-practices/references/plasma-development.md`).

`[Recommendation]` Keep the schema, the UI and the runtime access separate. A page that assigns to the configuration property directly writes immediately and skips the transaction.

## 5. Implement the representations

`[Official]` The root QML object must be a `PlasmoidItem`, and `compactRepresentation` / `fullRepresentation` are properties of that root; the wrapper properties that lived on the `Plasmoid` attached property in Plasma 5 were removed (porting guide, `FWD-01`).

`[Recommendation]` The compact view is an icon that toggles `root.expanded` and carries an `Accessible.name`; the full view is a `PlasmaExtras.Representation` sized in `Kirigami.Units.gridUnit`. The theme frame paints the surface, so the widget never paints its own (`../kde-plasma-ui-ux/references/official-applet-anatomy.md`).

## 6. Package

`[Official]` There is no packaging subcommand: a `.plasmoid` is a zip whose root holds `metadata.json` and `contents/`. Nesting them one directory deeper breaks installation.

```bash
cd my-plasmoid/package
zip -r ../../my-plasmoid-1.0.0.plasmoid metadata.json contents
unzip -l ../../my-plasmoid-1.0.0.plasmoid      # metadata.json must be at the root
```

## 7. Install

`[Official]` `kpackagetool6` installs, upgrades, removes and lists `Plasma/Applet` packages; `plasma-framework` is Plasma 5 tooling and must not be mixed with it.

```bash
kpackagetool6 -t Plasma/Applet -i my-plasmoid-1.0.0.plasmoid   # install
kpackagetool6 -t Plasma/Applet -u my-plasmoid-1.0.0.plasmoid   # upgrade after a rebuild
kpackagetool6 -t Plasma/Applet -r com.example.my-plasmoid      # remove by KPlugin.Id
kpackagetool6 -t Plasma/Applet -l                              # list installed
```

`[Recommendation]` Install to the user scope, not the system one, while developing. A system install needs root and will shadow the user copy.

## 8. Test

`[Official]` `plasmoidviewer` runs an unpacked package without installing it; `plasmawindowed` needs the widget installed under `~/.local/share/plasma/plasmoids` and preserves configuration changes, so it is the one that proves save and restore.

```bash
plasmoidviewer -a ./package                              # unpacked package
QT_SCALE_FACTOR=2 plasmoidviewer -a ./package            # HiDPI check
plasmawindowed com.example.my-plasmoid                   # installed widget, remembers config
qmllint6 my-plasmoid/package/contents/ui/main.qml        # lint
python3 ../kde-plasma-best-practices/scripts/lint_qml.py my-plasmoid/package
systemctl --user restart plasma-plasmashell.service      # the real shell
```

`[Official]` QML `console.log()` output is hidden by default: enable it with `QT_LOGGING_RULES="qml.debug=true" plasmoidviewer -a ./package`, or persistently with `qml.debug=true` under `[Rules]` in `~/.config/QtProject/qtlogging.ini`. On Plasma 6 use `kwriteconfig6` for that file.

`[Recommendation]` Test in this order and stop at the first failure: lint, then the unpacked package, then the installed widget with a changed setting, then the real shell. Each step rules out a different class of problem, and the cheap ones come first.

## 9. Publish

`[Recommendation]` The KDE Store submission is a packaging and metadata step, not a code step: the same `.plasmoid` archive, the same `metadata.json`, with screenshots and a description added on the store page. Confirm the widget id, name, license and description are the ones you want to be permanent, because they are what users see and what the store indexes.

`[Unknown]` The current store submission requirements, review criteria and review time are not documented in the sources this bundle checked. Read the store's own page before submitting, and treat anything you cannot verify there as unverified.

## What this skill does not decide

- Whether the interface follows the Plasma grammar: `../kde-plasma-ui-ux`.
- Whether the implementation is correct, fast and thread-safe: `../kde-plasma-best-practices`.
- Whether the widget will survive the next Plasma release: `../kde-plasma-best-practices/references/forward-compatibility.md`.

## Sources

- KDE: Porting Plasmoids to KF6 — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial — https://develop.kde.org/docs/plasma/widget/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial, configuration — https://develop.kde.org/docs/plasma/widget/configuration/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial, testing — https://develop.kde.org/docs/plasma/widget/testing/ (accessed 2026-10-20)
- KDE Store — https://store.kde.org/ (accessed 2026-10-20)

## Version notes

- Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The package format, the metadata keys and the tooling change between major releases; re-check them against the branch you target.
- The scaffold in `assets/scaffold/` is a starting point, not a template to publish unchanged: it has no icon of its own, no configuration binding beyond the label, and no tests.
