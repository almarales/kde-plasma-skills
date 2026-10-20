# KDE Plasma Builder Skill

A workflow skill for turning an empty directory into a published KDE Plasma 6 widget: choosing a backend, scaffolding the package, declaring metadata and configuration, packaging, installing, testing, and publishing.

## Purpose and audience

`SKILL.md` is a runtime contract: when to activate, which constraints are non-negotiable, how to route a build task, and what a finished widget must contain. This README explains the bundle for humans: what it covers, how to install it, and how to keep it honest.

Written for Plasma widget authors, contributors porting a Plasma 5 widget, and AI coding agents working on their behalf. It is not official KDE policy, and it does not replace the target repository or maintainer judgment.

## Scope

In scope:

- Choosing the backend: pure QML, a C++ applet, or an external process.
- The package layout, `metadata.json`, `contents/config/main.xml` and `config.qml`.
- Packaging, installing, testing, and publishing a widget.
- The order of the path and the hand-off points, not the rules themselves.

Non-goals:

- Interface design, theme roles, and accessibility: `kde-plasma-ui-ux`.
- Threading, lifetime, bindings, build integration, and tests: `kde-plasma-best-practices`.
- Approving a widget without inspecting it, or claiming a command that was not run.

## Structure

| Path | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Activation contract, hard rules, decision gates, workflow, output contract |
| [`references/lifecycle.md`](references/lifecycle.md) | The ordered path from scaffold to store |
| [`references/backends.md`](references/backends.md) | The backend decision, and why a Python object cannot serve a plasmoid |
| [`assets/scaffold/`](assets/scaffold/) | Copy-paste starting point: `metadata.json`, `contents/ui/main.qml`, `contents/config/main.xml`, `contents/config/config.qml` |

## Install and activation

Install the whole bundle from its root. The installer replaces any previous copy, so an update never mixes two versions of a skill:

```bash
/path/to/kde-plasma-skills/install.sh           # user scope
/path/to/kde-plasma-skills/install.sh --scope project
```

To install only this skill, copy its directory into the root your agent scans (`~/.agents/skills` for Gentle AI agents), **replacing** the destination rather than merging into it, then refresh the registry:

```bash
mkdir -p ~/.agents/skills
rm -rf ~/.agents/skills/kde-plasma-builder
cp -r /path/to/kde-plasma-builder ~/.agents/skills/
gentle-ai skill-registry refresh
```

Copy the whole directory, including `references/` and `assets/`: the scaffold is part of the contract, and `SKILL.md` links to it locally.

Install into one root only. The registry keeps one entry per skill name, so a copy in two roots means one of them silently shadows the other; `install.sh check` reports it.

## Relationship to the other skills

The three skills are independent and complementary:

- `kde-plasma-ui-ux` sets interface goals, visual consistency, interaction, and accessibility.
- `kde-plasma-best-practices` sets implementation quality: responsiveness, bindings, ownership, threading, architecture, build integration, and tests.
- `kde-plasma-builder` sets the path from nothing to a published widget, and routes each step to the skill that owns the rules for it.

None of them overrides repository requirements or verified platform constraints. The builder never restates a rule: it links to the skill that states it, so there is one source of truth per concern.

## Version assumptions

Verified on 2026-10-20 against Plasma 6.8.0, Qt 6.11.1, KF6 (ECM 6.31.0). The package format, the metadata keys and the tooling change between major releases: confirm the target branch before relying on a command.

## Validation and maintenance

Validation is structural and editorial, plus one functional check: the scaffold in `assets/scaffold/` must produce zero findings when run through `kde-plasma-best-practices/scripts/lint_qml.py`.

```bash
python3 ../kde-plasma-best-practices/scripts/lint_qml.py assets/scaffold/
```

Maintenance: re-verify the commands and the metadata keys when the target Plasma branch changes, and keep the scaffold passing the checker. Treat a deprecation as maintenance work, not as a silent edit.

## Proposing corrections

Open an issue or a pull request including the exact file and section, the observed problem, the evidence (source URL with access date, command output, or a reproduction), and the proposed correction. Do not submit unverified API names or commands.

## License

The skill text is licensed under the **GNU General Public License, version 3 or later**. See `LICENSE` in this directory.

The copyleft terms apply to this skill's text, its references and its scaffold: anyone who redistributes a modified copy must publish it under the same terms, with the license and the changes marked.

KDE, Plasma, Kirigami, and Breeze are trademarks or project names of their respective owners. This skill is an independent community resource: it is **not affiliated with, endorsed by, or approved by KDE**.
