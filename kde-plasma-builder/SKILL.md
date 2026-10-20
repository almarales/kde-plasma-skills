---
name: kde-plasma-builder
description: "Trigger: build, scaffold, package, install, test or publish a KDE Plasma 6 widget. From an empty directory to a .plasmoid in the store."
license: Apache-2.0
metadata:
  author: "Javier Reinaldo Almarales"
  version: "1.0"
---

## Activation Contract

Use for the path from nothing to a shipped Plasma 6 widget: choosing a backend, scaffolding the package, declaring metadata and configuration, packaging, installing, testing, and publishing. This skill owns the **order** and the decisions on that path. It does not own the design rules (`kde-plasma-ui-ux`) or the engineering rules (`kde-plasma-best-practices`).

Not for reviewing an existing widget's design or implementation: load the other two instead.

## Hard Rules

- Copy `assets/scaffold/`; do not retype a package layout from memory.
- The root QML object is `PlasmoidItem`, and `compactRepresentation` / `fullRepresentation` are set on it, not on the `Plasmoid` attached property.
- QML imports are un-versioned. `PlasmaCore.Theme`, `PlasmaCore.Units` and `PlasmaCore.IconItem` do not exist in Plasma 6.
- `metadata.json` declares `"KPackageStructure": "Plasma/Applet"` and `"X-Plasma-API-Minimum-Version": "6.0"`, and the id is a reverse-DNS you own.
- The `.plasmoid` archive holds `metadata.json` and `contents/` at its root; a nested directory does not install.
- A configuration page declares one `cfg_` alias per key; assigning to the configuration property directly skips Apply and Discard.
- Never claim a build, an install, or a test you did not run: name the command and its output.
- These are community conventions, not KDE policy or endorsement.

## Decision Gates

| Need | Read |
|---|---|
| The ordered path, from scaffold to store | `references/lifecycle.md` |
| What can provide the data: pure QML, a C++ applet, or an external process | `references/backends.md` |
| Copy-paste starting point | `assets/scaffold/` |
| Package format, metadata keys, install and test commands | `../kde-plasma-best-practices/references/plasma-development.md` |
| Staying on the public surface across Plasma releases | `../kde-plasma-best-practices/references/forward-compatibility.md` |
| Interface goals, theme roles, accessibility | `../kde-plasma-ui-ux/SKILL.md` |
| Threading, lifetime, bindings, build, tests | `../kde-plasma-best-practices/SKILL.md` |

## Execution Steps

1. Decide the backend before writing UI: `references/backends.md`.
2. Copy `assets/scaffold/`, then rename the id, the name and the icon.
3. Declare the configuration: `contents/config/main.xml` plus a `cfg_` alias per key in `config.qml`.
4. Implement the compact and full representations with theme roles and Kirigami units.
5. Package: zip `metadata.json` and `contents/` at the archive root.
6. Install: `kpackagetool6 -t Plasma/Applet -i <file>.plasmoid`.
7. Test: lint, then `plasmawindowed` against the installed widget.
8. Publish: KDE Store submission, with every unverified step labelled.

## Output Contract

Return: the package layout produced; the backend chosen and why; the commands run with their observed output; the metadata keys declared; the checks still unverified; the next action.

## References

- `references/lifecycle.md` — the ordered path from scaffold to store.
- `references/backends.md` — the backend decision and the Python trap.
- `assets/scaffold/` — copy-paste starting point.
- `../kde-plasma-best-practices/SKILL.md` — engineering rules.
- `../kde-plasma-ui-ux/SKILL.md` — design rules.
