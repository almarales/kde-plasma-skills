---
title: "Resources, QML modules, and package layout"
impact: P2
scope: "Build / Qt resources, QML module packaging, KPackage plasmoids, install dirs"
tags: [build, resources, kpackage, plasmoid, install, i18n]
---

# Resources, QML modules, and package layout

## Principle

Ship one artifact per installable unit, with the files it needs inside that unit. QML and images belong in the compiled resource system; a plasmoid belongs in a KPackage directory with JSON metadata and a `contents/` tree; install paths come from `KDEInstallDirs`, never from hard-coded `/usr` prefixes.

## Why it matters

The Qt resource system embeds files in the binary so they load regardless of the working directory or the platform's file-access policy, and `qt_add_qml_module()` handles that embedding plus ahead-of-time compilation of the listed `QML_FILES` `[Official]`. Hand-managed `.qrc` files drift: a file added to disk but not to the manifest is simply absent at run time.

Plasma 6 tightened the package contract. The porting guide states that all plasmoids must use JSON metadata, that the QML root must be a `PlasmoidItem` (or `ContainmentItem` for a containment), and that the entry point is always `ui/main.qml` `[Official]`. Metadata must carry `"X-Plasma-API-Minimum-Version": "6.0"`, must drop `X-Plasma-API` and `X-Plasma-MainScript`, and must replace the old `ServiceTypes` with a top-level `"KPackageStructure": "Plasma/Applet"` `[Official]`.

Installed plasmoids on this machine follow exactly that shape: `/usr/share/plasma/plasmoids/<id>/metadata.json` plus `contents/ui/main.qml`, with `KPlugin.Id`, `KPlugin.Name`, `KPlugin.Icon`, `KPlugin.License`, and `X-Plasma-API-Minimum-Version` present `[Observed]`.

## Incorrect

```text
# Pseudocode: illustrative layout, not a working package.
mywidget/
├── metadata.desktop        # Plasma 5 metadata; ignored by Plasma 6
├── main.qml                # wrong entry point
└── ui/Main.qml
```

## Preferred

```text
# Pseudocode: illustrative layout.
mywidget/
├── metadata.json
└── contents/
    ├── ui/
    │   └── main.qml
    ├── config/
    │   ├── main.xml                 # KConfigXT schema
    │   └── config.qml               # configuration dialog
    └── locale/<lang>/LC_MESSAGES/<domain>.mo
```

```json
// Pseudocode: illustrative only.
{
  "KPackageStructure": "Plasma/Applet",
  "KPlugin": {
    "Id": "org.example.mywidget",
    "Name": "My Widget",
    "License": "GPL-2.0+"
  },
  "X-Plasma-API-Minimum-Version": "6.0"
}
```

- Install with `KDEInstallDirs` variables, for example `${KDE_INSTALL_DATADIR}/plasma/plasmoids/<id>`, so distributions can relocate the prefix `[Recommendation]`.
- During development, install or upgrade from the package directory with `kpackagetool6 --type Plasma/Applet --install <dir>`; the tool is present locally and documents `--type`, `--install`, `--global`, and `--show` `[Observed]`.
- Keep `ui/main.qml` as the single entry point; reference the other QML files relatively.
- Put user-visible strings behind `i18n()` and ship the compiled catalogs under `contents/locale/`; the translation domain for applets follows `plasma_applet_<plugin-id>` in the widget documentation `[Official]`, which is Plasma 5-era — confirm the domain actually used by your build before renaming catalogs.

## Exceptions and trade-offs

- Large, optional assets can stay outside the resource system to keep the binary small, but then their installation path becomes part of the contract and must be resolved at run time.
- Installing to a user prefix (`~/.local/share/plasma/plasmoids`) is right for iteration; release packages should use the distribution prefix.

## Review checklist

- [ ] `metadata.json` exists, is valid JSON, and carries `KPackageStructure` and `X-Plasma-API-Minimum-Version`.
- [ ] `ui/main.qml` is the root and uses `PlasmoidItem`/`ContainmentItem` as appropriate.
- [ ] No `metadata.desktop`, `X-Plasma-MainScript`, or `X-Plasma-API` left over from a Plasma 5 port.
- [ ] QML files and images are declared in the build, not only present on disk.
- [ ] Install destinations use `KDEInstallDirs` variables; translation domain and catalogs match the build output.

## References

- KDE: Porting Plasmoids to KF6 (metadata, `PlasmoidItem`, `ui/main.qml`) — https://develop.kde.org/docs/plasma/widget/porting_kf6/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial — setup — https://develop.kde.org/docs/plasma/widget/setup/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial — translations/i18n — https://develop.kde.org/docs/plasma/widget/translations-i18n/ (accessed 2026-10-20)
- KDE: Plasma Widget tutorial — testing (`plasmoidviewer`, `plasmawindowed`) — https://develop.kde.org/docs/plasma/widget/testing/ (accessed 2026-10-20)
- Qt: Best Practices — bundle application resources — https://doc.qt.io/qt-6/qtquick-bestpractices.html (accessed 2026-10-20)
- Qt: `qt_add_qml_module` — https://doc.qt.io/qt-6/qt-add-qml-module.html (accessed 2026-10-20)
- KDE: `KDEInstallDirs` — https://api.kde.org/ecm/kde-module/KDEInstallDirs6.html (accessed 2026-10-20)

## Version notes

Written against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0), verified 2026-10-20; the installed-package shape and `kpackagetool6` flags were observed on that system. Plasma 5 material using `metadata.desktop`, `kpackagetool5`, and a configurable main script is not applicable to Plasma 6 and must be ported, not copied.
