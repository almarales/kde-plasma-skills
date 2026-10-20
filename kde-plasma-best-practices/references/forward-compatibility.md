# Forward compatibility

## Scope

Use this reference when the question is not "is this code correct?" but "**will this widget still work in the next Plasma release?**" It states the rules that keep a widget on the public, supported surface, and it is the basis the checker in `scripts/lint_qml.py` enforces.

It does not restate the rule catalog: performance, lifetime, threading and testing live in `rules/`. What lives here is the compatibility contract — the part that decides whether your widget survives a major release or becomes a maintenance liability.

Target assumptions: Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The rules below are version-sensitive; re-check them against the branch you target.

Evidence labels are the ones used across this skill: `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, `[Unknown]`.

## The contract in one line

`[Recommendation]` A widget is forward compatible when everything it depends on is **public API that the distribution documents**, and nothing it depends on is **removed, renamed, versioned, or private** between major releases.

## Plasma 5 APIs removed

`[Official]` The Plasma 6 porting guide states that "all the wrapper properties and methods from `AppletInterface` to `Applet` … have been removed", that the root object must now be a `PlasmoidItem`, and that QML module imports must be un-versioned because "this is unnecessary in Qt6 and can cause bugs" (`https://develop.kde.org/docs/plasma/widget/porting_kf6/`, accessed 2026-10-20; quoted in `plasma-development.md`).

`[Official]` The same migration moved theming and metrics to Kirigami: `Kirigami.Theme.colorSet` replaces the Plasma 5 `PlasmaCore.ColorScope.colorGroup`, and `Kirigami.Theme.inherit` replaces `PlasmaCore.ColorScope.inherit` (`kde-plasma-ui-ux/references/qt-qml-kirigami.md`).

`[Recommendation]` The following are gone in Plasma 6 and must not appear in new code:

| Removed | Replacement |
| --- | --- |
| `PlasmaCore.Theme` | `Kirigami.Theme` |
| `PlasmaCore.Units` | `Kirigami.Units` |
| `PlasmaCore.IconItem` | `Kirigami.Icon` |
| `PlasmaCore.ColorScope` | `Kirigami.Theme.colorSet` |
| `plasmoid.compactRepresentation` / `plasmoid.fullRepresentation` | properties on the root `PlasmoidItem` |

`[Observation]` The lowercase `plasmoid` context property still exists in Plasma 6 and is now an instance of the underlying `Applet`; what moved to the root `PlasmoidItem` are the wrapper properties (`compactRepresentation`, `fullRepresentation`, `switchWidth`, `switchHeight`, `toolTip*`, `hideOnWindowDeactivate`).

## Imports are unversioned

`[Official]` "Un-version your QML module imports. This is unnecessary in Qt6 and can cause bugs" (porting guide, accessed 2026-10-20).

`[Recommendation]` Write `import QtQuick` and `import org.kde.kirigami as Kirigami`. A versioned import pins the module to a version the target distribution may not ship, and the failure appears on someone else's machine.

## Private modules are not API

`[Recommendation]` A module under a `private` path, or any symbol documented only in the source tree, is not part of the public contract. It can be renamed, moved, or removed between releases without a deprecation cycle, so a widget that depends on it breaks on a routine upgrade rather than on a major one.

`[Official]` KDE's binary compatibility policy constrains exported classes and their virtuals, so an accidental dependency on an internal symbol is not a local mistake you can fix later (`rules/architecture/kde-api-compatibility.md`).

`[Recommendation]` If a public API does not exist for what you need, file it upstream instead of reaching into a private module. If you must use one temporarily, isolate it behind a single component, record the upstream issue, and give it a removal condition.

## metadata.json requirements

`[Official]` The porting guide requires, for Plasma 6 (accessed 2026-10-20):

- `"X-Plasma-API-Minimum-Version": "6.0"` must be present. Without it the widget is treated as Plasma 5 only and does not appear in the UI.
- `X-Plasma-MainScript` must be removed: `ui/main.qml` is always the entry point.
- `X-Plasma-API` must be removed.
- `ServiceTypes` must be replaced by a top-level `"KPackageStructure": "Plasma/Applet"`.
- All widgets use JSON metadata; a legacy `.desktop` file is converted with `desktoptojson`.

`[Recommendation]` A third-party widget must use a reverse-DNS id it owns. `org.kde.*` is reserved for KDE contributions, and a third-party package that takes one is indistinguishable from an official one (`kde-plasma-ui-ux/references/plasma-components.md`). Declare an SPDX license id as well: it is what a packager and a user read before installing.

## Compatibility layers are a waypoint

`[Official]` `org.kde.plasma.plasma5support` is "a migration aid, not a destination" (`plasma-development.md`).

`[Recommendation]` Isolate any compatibility import behind one component, so that removing it later is a single-file change instead of a sweep through the widget.

## Running the checker

`[Observed]` The checker lives in this skill and enforces the machine-checkable subset of the rules above plus the native-surface rules stated in `kde-plasma-ui-ux`:

```bash
# from the bundle root
python3 kde-plasma-best-practices/scripts/lint_qml.py path/to/plasmoid
python3 kde-plasma-best-practices/scripts/lint_qml.py path/to/plasmoid --json
python3 kde-plasma-best-practices/scripts/lint_qml.py --list-checks
```

`[Observed]` It exits 1 when a finding of the configured severity exists, which is what a CI job needs; `--fail-on warning` widens it, `--fail-on never` makes it report-only.

`[Recommendation]` Run it in CI on the same schedule as the build, and compare against the previous run rather than requiring a clean tree: a warning that is already there is debt, a warning the change introduced is the change's to own (`rules/build/static-analysis.md`).

## What the checker does not prove

`[Recommendation]` A clean run is a floor, not a verdict. It cannot see layout, contrast, keyboard flow, RTL behaviour, focus order, or whether a decision was the right one — the same limits `qmllint` has, and the reason the review checklist still exists. It proves the widget is on the public surface; it does not prove the widget is good.

`[Recommendation]` The checker cannot know your allowlist. A `Qt.rgba` derived from theme role channels is reported as informational, not as an error, because only your project knows whether that surface is documented as allowed.

## Sources

- KDE: Porting Plasmoids to KF6 — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial, properties — https://develop.kde.org/docs/plasma/widget/properties/ (accessed 2026-10-20)
- KDE: API documentation — https://api.kde.org/ (accessed 2026-10-20)
- KDE: Binary compatibility issues — https://community.kde.org/Policies/Binary_Compatibility_Issues_With_C%2B%2B (accessed 2026-10-20)

## Version notes

- Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20. The rules here are tied to the Plasma 6 porting guide; a Plasma 7 porting guide will change them, and this file must change with it.
- The checker implements the checks listed in `scripts/lint_qml.py --list-checks`. Each check cites the section of this file or of the UI/UX skill that states the rule, so a finding can always be traced to a rule rather than to a tool's opinion.
