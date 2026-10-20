# KDE Plasma Engineering Skills

Two independent, complementary skills for AI coding agents and developers working on
KDE Plasma interfaces and implementations.

> **Status:** community engineering resource. These skills are **not** affiliated with,
> endorsed by, or approved by KDE. They summarize public documentation and observed
> practice; they do not define official KDE policy or a Plasma roadmap.

| Skill | Purpose | Protects |
| --- | --- | --- |
| [`kde-plasma-ui-ux`](kde-plasma-ui-ux/SKILL.md) | Design, implement, and review interfaces coherent with Plasma's visual language, interaction patterns, and accessibility expectations. | User experience and consistency |
| [`kde-plasma-best-practices`](kde-plasma-best-practices/SKILL.md) | Audit and improve Qt/C++/QML/Kirigami implementation quality: responsiveness, ownership, bindings, architecture, build, and tests. | Implementation quality and reliability |

## Scope and non-goals

**In scope:** the Plasma desktop shell (panels, widgets/plasmoids, launchers, system tray,
popups), System Settings modules (KCMs), Plasma-native dialogs, Breeze conventions, Qt
Widgets, Qt Quick/QML, Kirigami, Plasma-specific components, accessibility, keyboard/focus
behavior, scaling, localization, theming, visual consistency, and code/design review.

**Out of scope:** generic web dashboards, SaaS layouts, marketing pages, mobile-app
conventions, and framework-agnostic design trends. The UI/UX skill must not import web
fashion into Plasma without a documented, evidence-based justification.

## Why two skills

They answer different questions and must not silently override each other:

- `kde-plasma-ui-ux` decides **what the interface should do and feel like**: hierarchy,
  interaction, states, accessibility, and adherence to KDE conventions.
- `kde-plasma-best-practices` decides **how to implement it well**: thread affinity,
  ownership, bindings, model/delegate cost, build integration, and tests.

Coordination policy:

1. Neither skill overrides repository requirements, supported APIs, or verified platform
   constraints.
2. A performance change must not silently break accessibility or expected behavior.
3. Visual consistency must not justify a technically incorrect implementation.
4. Trade-offs are documented with alternatives, evidence, risks, and validation steps.
5. Detailed guidance is not duplicated: load the other skill or the authoritative source.

## Target versions (assumptions)

Verified on the author's system on **2026-10-20**: Plasma **6.8.0**, Qt **6.11.1**, KF6,
`qmllint6` (Qt 6.11.1; the unversioned `qmllint` on this machine is a Qt 5 wrapper). These are assumptions, not universal requirements. Always
verify component names, imports, and properties against the target branch and
`api.kde.org`; KDE Frameworks and Plasma APIs change between releases.

## Architecture

Each skill uses progressive disclosure. `SKILL.md` is a short runtime contract that tells
an agent when to activate, what is non-negotiable, how to route, and what to return.
Detailed material is loaded on demand.

```text
.                              # this bundle root
├── README.md                  # this file
├── LICENSE                    # Apache-2.0
├── kde-plasma-ui-ux/
│   ├── SKILL.md               # activation, rules, routing, output
│   ├── README.md              # purpose, install, maintenance
│   ├── LICENSE
│   ├── references/            # design principles, visual consistency,
│   │                          # components, QML/Kirigami, interaction,
│   │                          # accessibility, future proposals, review
│   └── assets/                # design-proposal and ui-review templates
└── kde-plasma-best-practices/
    ├── SKILL.md
    ├── README.md
    ├── LICENSE
    └── references/
        ├── rules/             # P0-P3 rule catalog (performance, qml, cpp,
        │                      # architecture, build, testing)
        ├── qt-quick-performance.md
        ├── plasma-development.md
        ├── rule-authoring.md
        └── sources.md
```

## Install and activate

The exact scanned root depends on the agent. Common choices:

**Project scope** (available only in this repository):

```bash
# run from the root of this bundle
mkdir -p .agents/skills
cp -r kde-plasma-ui-ux .agents/skills/
cp -r kde-plasma-best-practices .agents/skills/
gentle-ai skill-registry refresh
```

**User scope** (available in every project for Gentle AI agents):

```bash
# run from the root of this bundle
mkdir -p ~/.config/agents/skills
cp -r kde-plasma-ui-ux ~/.config/agents/skills/
cp -r kde-plasma-best-practices ~/.config/agents/skills/
gentle-ai skill-registry refresh
```

Other agents scan different roots (for example `.claude/skills`, `.kiro/skills`,
`~/.config/opencode/skills`). Copy the skill directory into the root your agent documents;
do not copy only `SKILL.md`, because the reference files are part of the contract.

After installation, the skills appear in the agent's skill list and are selected from
their `description` triggers. Example prompts:

- "Review this plasmoid for Plasma visual and accessibility consistency."
- "Design a System Settings module for these options."
- "Audit this QML for binding overwrites and delegate cost."
- "This panel animation stutters; find the GUI-thread or binding cause."
- "Review this C++/QML boundary for ownership and lifetime bugs."
- "Evaluate this Plasma 7 concept without treating it as official."

## Validation

There is no executable behavior in these skills; validation is structural and editorial.
Run at minimum:

```bash
# Frontmatter, description length, section order, local links, empty files
# run from the root of this bundle
python3 - <<'PY'
from pathlib import Path
import re, sys
root = Path(".")
errors = []
for p in root.rglob("SKILL.md"):
    text = p.read_text()
    if not text.startswith("---"):
        errors.append(f"{p}: missing frontmatter")
        continue
    fm = text.split("---", 2)[1]
    for key in ("name:", "description:", "license:", "metadata:", "author:", "version:"):
        if key not in fm:
            errors.append(f"{p}: missing {key}")
    m = re.search(r'^description:\s*"(.*)"\s*$', fm, re.M)
    if not m:
        errors.append(f"{p}: description must be one quoted line")
    elif len(m.group(1)) > 250:
        errors.append(f"{p}: description {len(m.group(1))} > 250 chars")
    for section in ("Activation Contract", "Hard Rules", "Decision Gates",
                    "Execution Steps", "Output Contract", "References"):
        if f"## {section}" not in text:
            errors.append(f"{p}: missing section {section}")
for p in root.rglob("*"):
    if p.is_file() and p.stat().st_size == 0:
        errors.append(f"{p}: empty file")
print("\n".join(errors) if errors else "OK: structural checks passed")
sys.exit(1 if errors else 0)
PY
```

Then run `skill-improver` on both skills, and verify every cited URL returns HTTP 200.
Documentation-only changes are an explicit exception to test-first implementation: there is
no runnable RED state. Do not claim a check passed without inspecting its output.

## Maintenance

- Every reference states its scope, sources, and the date the sources were accessed.
- Re-verify official links and version-specific APIs when the target Plasma/Qt/KF branch
  changes. Treat deprecations as maintenance work, not as silent edits.
- New rules must follow `kde-plasma-best-practices/references/rules/_template.md` and
  `references/rule-authoring.md`. Merge or discard rules that do not add distinct,
  actionable guidance.
- P0-P3 are this catalog's prioritization convention, not an official KDE taxonomy.
- When documentation and observed code disagree, report both and state which was verified.

## Contributing corrections

Open an issue or pull request that includes: the exact file and section, the observed
problem, the evidence (source URL with access date, code location, screenshot, or command
output), and the proposed correction. Do not submit unverified API names, benchmark
numbers, design tokens, or claims about KDE's future direction. Changes that affect a
rule's impact or scope must update its frontmatter and `_sections.md` together.

## Reporting outdated guidance

Include the skill, file, target version, what changed upstream, and the source that shows
the change. If a recommendation is only valid for an older branch, say so explicitly
rather than deleting the history.

## License

The skill content in this directory is licensed under the **Apache License 2.0** (see
`LICENSE`). The rest of the HyaloNet repository remains under its own GPL-3.0 license.
KDE, Plasma, Kirigami, and Breeze are trademarks or projects of their respective owners;
this bundle claims no affiliation.
