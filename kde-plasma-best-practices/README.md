# KDE Plasma Engineering Best Practices

A community rule catalog for reviewing and improving Qt/C++/QML code in KDE Plasma projects with an AI agent.

## Purpose and audience

`SKILL.md` is a runtime contract: when to activate, which constraints are non-negotiable, how to route a code change to the rules that apply, and what a reviewable result must contain. This README explains the bundle for humans: what it covers, how to install it, and how to keep it honest over time.

Written for KDE contributors, Plasma widget and KCM authors, Qt/QML developers, maintainers reviewing performance and lifetime bugs, and AI coding agents working on their behalf. It is not official KDE policy, and it does not replace the target repository, upstream documentation, or maintainer judgment.

## Scope and non-goals

In scope:

- GUI-thread responsiveness, asynchronous work, shutdown, and cancellation.
- Profiling before optimization; startup cost and deferred creation.
- Declarative QML bindings, binding overwrites, models, delegates, and component reuse.
- QObject ownership and lifetime, signals/slots and connection cleanup, thread affinity.
- QML/C++ boundaries, plugin and module boundaries, API and version compatibility.
- CMake, resources, KPackage packaging, static analysis, unit/integration/regression testing.

Non-goals:

- Non-Qt codebases and framework-agnostic performance advice.
- Visual, interaction, and accessibility decisions, which belong to `kde-plasma-ui-ux`.
- Approving a change without inspecting it, or asserting speed-ups that were not measured.
- Replacing repository requirements or verified platform constraints with catalog preferences.

## Structure

| Path | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Activation contract, hard rules, decision gates, workflow, output contract |
| [`references/rules/_sections.md`](references/rules/_sections.md) | Rule index by area, impact, tags, and status |
| [`references/rules/_template.md`](references/rules/_template.md) | Required rule format for new entries |
| `references/rules/performance/` | Blocking GUI thread, async work, profiling, startup cost |
| `references/rules/qml/` | Bindings, binding overwrites, models/delegates, Loader, reuse |
| `references/rules/cpp/` | Ownership/lifetime, signals/slots, threading, QML/C++ boundaries |
| `references/rules/architecture/` | Module boundaries, KDE API compatibility |
| `references/rules/build/` | CMake/ECM, resources and packaging, static analysis |
| `references/rules/testing/` | Unit, integration, and regression tests |
| [`references/qt-quick-performance.md`](references/qt-quick-performance.md) | Labelled synthesis of Qt's Qt Quick performance guidance |
| [`references/plasma-development.md`](references/plasma-development.md) | Plasma 6 architecture, imports, `metadata.json`, version matrix, pluggable view packages |
| [`references/rule-authoring.md`](references/rule-authoring.md) | Eligibility test, evidence labels, merge/split/discard policy |
| [`references/audit-criteria.md`](references/audit-criteria.md) | Audit scope, severity derivation, required checks, verdict rules |
| [`references/forward-compatibility.md`](references/forward-compatibility.md) | The public-surface contract: removed APIs, un-versioned imports, private modules, `metadata.json` |
| [`references/sources.md`](references/sources.md) | Every cited URL with status and access date, plus local observations |
| [`assets/audit-report.md`](assets/audit-report.md) | Template for a written audit with a verdict |
| [`scripts/lint_qml.py`](scripts/lint_qml.py) | Heuristic checker for the machine-checkable subset of the rules |

## Rule catalog at a glance

22 rules across six areas. Load only the rules the change touches; `_sections.md` maps signals in a diff to file paths.

| Area | Rules | Impact |
|---|---|---|
| Performance | `blocking-gui-thread`, `async-work`, `profiling-first`, `startup-cost` | P0, P1, P1, P2 |
| QML | `declarative-bindings`, `binding-overwrites`, `model-delegates`, `loader-usage`, `component-reuse`, `timer-lifecycle`, `representation-composition` | P1, P1, P1, P2, P2, P2, P2 |
| C++ | `ownership-lifetime`, `signals-slots`, `threading`, `qml-cpp-boundaries` | P0, P1, P0, P1 |
| Architecture | `module-boundaries`, `kde-api-compatibility` | P1, P1 |
| Build | `cmake`, `resources-packaging`, `static-analysis` | P2, P2, P2 |
| Testing | `unit-tests`, `integration-tests`, `regression-tests` | P1, P1, P1 |

**Priority caveat:** P0–P3 are this catalog's prioritization convention, not an official KDE taxonomy. P0 means a responsiveness, correctness, or resource-safety break in normal use; P1 a major architectural, lifecycle, or performance concern; P2 a recurring inefficiency or maintainability issue with a local fix; P3 low-impact consistency or cleanup. No rule currently uses P3. Assign by expected impact, not by how alarming the example looks.

Every rule follows the same nine-section shape (`Principle`, `Why it matters`, `Incorrect`, `Preferred`, `Exceptions and trade-offs`, `Review checklist`, `References`, `Version notes`, plus the title) and stays within 40–90 lines. Code blocks are pseudocode unless they quote a build that was actually run.

## Formal audits

The skill produces two kinds of output. A **review** is a conversational answer: the rules that applied, the findings, the measurements, the accepted trade-offs. An **audit** is a written document with a verdict, for a change that needs a reviewable record.

An audit follows `references/audit-criteria.md` and is written with `assets/audit-report.md`:

- It is scoped to an exact revision and file set, and says what was out of scope.
- It states an outcome on three axes — correctness, performance, maintainability — and marks an axis that was not inspected as `Unverified`.
- Every finding cites a rule from the catalog, and its severity **is** that rule's `impact` class: `P0` is a `Blocker`, `P1` a `Major`, `P2` a `Minor`, `P3` a `Nit`. A defect no rule covers is an observation, not a finding.
- Every executed check reports the exact command and its observed result; the checks that could not run are listed with the evidence that would close them.
- The verdict is `pass`, `fail`, or `inconclusive`, using the same vocabulary as the UI review skill. An audit without inspected evidence is always `inconclusive`.

The verdict describes the audited revision. It does not authorize delivery, and it does not judge the author.

## Install and activation

Install the whole bundle from its root. The installer replaces any previous copy, so an update never mixes two versions of a skill:

```bash
/path/to/kde-plasma-skills/install.sh           # user scope
/path/to/kde-plasma-skills/install.sh --scope project
```

To install only this skill, copy its directory into the root your agent scans (`~/.agents/skills` for Gentle AI agents), **replacing** the destination rather than merging into it, then refresh the registry:

```bash
mkdir -p ~/.agents/skills
rm -rf ~/.agents/skills/kde-plasma-best-practices
cp -r /path/to/kde-plasma-best-practices ~/.agents/skills/
gentle-ai skill-registry refresh
```

- Copy the whole directory, including `references/`, `assets/` and `scripts/`, because `SKILL.md` links to those files locally.
- Install into one root only. The registry keeps one entry per skill name, so a copy in two roots means one of them silently shadows the other; `install.sh check` reports it.
- If your agent scans a different skills root, copy the directory there instead and refresh the registry.
- Start a new agent session if skill discovery is cached at startup.
- The skill activates on QML performance, GUI-thread stalls, ownership/lifetime, signals and threading, CMake/KF6 integration, and test-related tasks. It needs no slash command.

## Relationship to `kde-plasma-ui-ux`

The two skills are independent and complementary:

- `kde-plasma-ui-ux` sets interface goals, visual consistency, interaction behavior, and accessibility expectations.
- `kde-plasma-best-practices` sets implementation quality: responsiveness, bindings, ownership, threading, architecture, build integration, and tests.
- Neither silently overrides repository requirements or verified platform constraints.
- A performance change must not break accessibility or expected behavior; visual consistency must not justify a technically incorrect implementation.
- When the two pull in different directions, document alternatives, evidence, risks, and validation.

Do not copy design rules into this skill. Link to `../kde-plasma-ui-ux/SKILL.md` and its `references/` instead.

## Version assumptions

Verified on 2026-10-20 against a local baseline of:

- KDE Plasma 6.8.0
- Qt 6.11.1
- KDE Frameworks 6, ECM 6.31.0
- `qmllint6` (Qt 6.11.1), `kpackagetool6`, `plasmoidviewer`, `plasmawindowed` available; the unversioned `qmllint` is a Qt 5 wrapper

These are assumptions, not universal requirements. `api.kde.org` serves the newest framework documentation, and Plasma/Qt imports, properties, and defaults change between releases: confirm version-sensitive guidance against the target branch before applying it. `clazy` and `clang-tidy` were not installed on the verification machine, so the static-analysis rule describes configuration without claiming observed analyzer output.

Substantive claims are labelled `[Official]`, `[Observed]`, `[Recommendation]`, `[Experimental]`, or `[Unknown]` so readers can see how strongly each statement is supported.

## Validation and maintenance

Validation is structural and editorial, with one executable exception: `scripts/lint_qml.py` is validated by running it. It enforces the machine-checkable subset of the rules and cites, for every finding, the reference that states the rule it enforces.

1. Parse each rule's YAML frontmatter; confirm `title`, `impact` in P0–P3, `scope`, and `tags`.
2. Confirm all nine sections are present in order and the file is 40–90 lines.
3. Confirm every code block is marked pseudocode and every substantive claim is labelled.
4. Resolve every relative link in `SKILL.md`, this README, and each reference.
5. Re-check every URL in `references/sources.md`:

```bash
curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 <url>
```

6. Check rule rows in `_sections.md` match the files and their `impact` values.
7. Run the `skill-improver` audit before publishing changes.

Maintenance:

- Re-verify cited URLs and version-sensitive API names when the target Plasma, Qt, or KF branch changes, and at least once per Plasma major release.
- Treat deprecations as maintenance work, not silent edits. Update `## Version notes` and keep the history.
- Keep `SKILL.md` short. New mechanism detail belongs in a reference or a rule.
- Do not keep a rule for coverage. If the evidence no longer supports it, merge or discard it and update `_sections.md`.

## Proposing corrections

Open an issue or pull request in the repository that distributes this skill. Include:

- The exact file and section.
- The current text and the proposed text.
- The evidence: official URL with access date, repository path with branch, command output, or test result.
- The affected versions and platforms.
- Whether the change is a correction, a new rule, or an experiment.

New rules must pass the four eligibility tests in `references/rule-authoring.md` (recurring, actionable, non-duplicative, evidence-backed) and follow `_template.md`. Corrections that add or reclassify a rule must update its frontmatter and `_sections.md` in the same change. Unsourced preferences are treated as proposals, not corrections.

## Reporting outdated or version-specific guidance

Report outdated guidance with the same evidence standard:

- Which Plasma, Qt, or KF version the guidance fails on.
- What current documentation or implementation says instead, with a URL or repository reference.
- Whether the guidance was wrong when written or became wrong after a release.
- A minimal reproduction for behavioral claims.

Do not silently widen a rule to cover a new release. State the supported versions and let maintainers decide whether to update, split, or replace it.

## License

The skill text is licensed under the **GNU General Public License, version 3 or later**. See `LICENSE` in this directory.

The copyleft terms apply to this skill's text, its references, its templates and `scripts/lint_qml.py`: anyone who redistributes a modified copy must publish it under the same terms, with the license and the changes marked. Application code in the surrounding repository is not relicensed by this file.

`scripts/lint_qml.py` was developed in the `kde-plasma-design` project under LGPL-2.0-or-later and was relicensed by the copyright holder to this bundle's license, so that the whole bundle ships under a single license. The file header records that history.

KDE, Plasma, Kirigami, and Breeze are trademarks or project names of their respective owners. This skill is an independent community resource: it is **not affiliated with, endorsed by, or approved by KDE**.
