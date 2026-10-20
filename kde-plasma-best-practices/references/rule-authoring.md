# Authoring and maintaining a rule

Scope: the process this skill uses for adding, merging, splitting, or discarding a rule. It exists so the catalog stays a set of evidence-backed, testable statements instead of a growing pile of preferences.

Audience: contributors proposing a rule, and reviewers deciding whether to accept one.

## 1. Does the candidate deserve to be a rule?

A rule earns its place when all four hold:

1. **Recurring.** The problem appears in more than one component, or in code a reviewer keeps having to correct. A single incident is a bug report, not a rule.
2. **Actionable.** A reviewer can look at a diff and say yes or no. "Write maintainable code" fails; "a QObject returned from a `Q_INVOKABLE` is parented or marked `CppOwnership`" passes.
3. **Non-duplicative.** No existing rule already covers it. If one nearly does, extend that rule instead of adding a neighbour.
4. **Evidence-backed.** Either documented behaviour whose source can be linked, or observable behaviour that can be reproduced. A preference with neither is not a rule.

A candidate that fails (1) or (4) is discarded. A candidate that fails (2) is rewritten until it is checkable, or discarded. A candidate that fails (3) is merged.

Do not translate a rule from another ecosystem mechanically. A React rule about re-render cost has no direct Qt analogue; the Qt analogue is binding re-evaluation and cross-boundary property access, and it must be justified from Qt's own documentation. If the mechanism differs, the rule differs.

## 2. Anatomy of a rule file

Path: `references/rules/<area>/<slug>.md`, where `<area>` is one of `qml`, `cpp`, `architecture`, `build`, `testing`, and `<slug>` is a short kebab-case noun phrase.

```yaml
---
title: "Short imperative title"
impact: P0            # one of P0, P1, P2, P3
scope: "Area / what it governs"
tags: [area, technology, concept]
---
```

Required sections, in this order:

| Section | Content |
| --- | --- |
| `# Title` | Matches or closely tracks the frontmatter title |
| `## Principle` | The rule in one or two sentences, stating the contract |
| `## Why it matters` | Mechanism and consequence, with labelled evidence |
| `## Incorrect` | A short counter-example, clearly marked as pseudocode |
| `## Preferred` | The replacement shape, plus a few checkable bullets |
| `## Exceptions and trade-offs` | When the rule does not apply, and what it costs |
| `## Review checklist` | Four to six binary checks a reviewer can run on a diff |
| `## References` | Verified URLs only, one per line |
| `## Version notes` | Target versions, what changed, what to re-verify |

Length target: 40–90 lines. A rule that needs more is usually two rules.

Every code block is pseudocode unless it is quoted from a build that was actually run. Say so inside the block, in the first comment line. Never present a placeholder as a production-ready implementation.

## 3. Impact classification

The classes are this skill's convention, not an official KDE taxonomy. State that in the README so nobody cites them as policy.

| Class | Meaning | Typical examples |
| --- | --- | --- |
| **P0** | Breaks responsiveness, correctness, or resource safety in normal use | Blocking the GUI thread; a dangling QObject pointer; double ownership of an engine-owned object |
| **P1** | Major architectural, lifecycle, or performance concern that will be expensive later | Wide QML/C++ boundary; no shutdown path for a worker thread; missing regression coverage for a fixed bug |
| **P2** | Recurring inefficiency or maintainability issue with a local fix | Globbed sources; hand-managed `.qrc`; warning regressions |
| **P3** | Consistency, tooling, and cleanup with low individual impact | Naming, formatting, catalog hygiene |

Assign by expected impact under normal use, not by how alarming the example looks. When two classes seem plausible, choose the lower one and say in the rule why it is not higher. A catalog where everything is P0 trains readers to ignore the labels.

## 4. Evidence standard

Use exactly these labels on substantive claims:

- `[Official]` — stated in the linked Qt or KDE documentation, a KDE policy page, or the platform's own source documentation.
- `[Observed]` — reproduced on the verification machine, or visible in an installed package; state the version and date.
- `[Recommendation]` — this skill's engineering judgement, derived from the mechanism but not itself documented.
- `[Experimental]` — a proposal under evaluation; must not be presented as guidance to follow.
- `[Unknown]` — explicitly unverified. Prefer this over a plausible guess.

Rules for evidence:

- Every substantive claim carries a label. A paragraph of unlabelled assertions is a defect.
- Every URL is re-checked before publishing: `curl -s -o /dev/null -w '%{http_code}' -L --max-time 15 <url>`, expecting 200. Record the access date.
- A URL that returns a directory listing or an error page is not a source, even when the status is 200.
- No invented benchmarks, APIs, test results, design tokens, or roadmap decisions. If a number was not measured, it does not appear.
- Prefer primary sources: Qt's documentation for Qt behaviour, `api.kde.org` and KDE's own docs for KDE behaviour, the target repository for what the code actually does.
- `api.kde.org` serves the newest framework documentation. When writing about a versioned branch, say which branch the claim came from, and verify symbols against installed headers where possible.

## 5. Merge, split, discard

- **Merge** when two candidates share a mechanism and a review checklist. Signals and slots plus connection cleanup belong together; ownership plus lifetime belong together.
- **Split** when the exceptions of one half contradict the other, or when the checklist would exceed six items. A rule whose title needs an "and" is a candidate for splitting.
- **Discard** when the evidence is a preference, when the mechanism is already covered by a linked document, or when the recommendation cannot be checked on a diff. Deleting a weak rule improves the catalog.
- **Do not** keep a rule for coverage. S6 in the originating feature document lists candidate topics precisely so that the evidence, not the list, decides the final shape.

## 6. Review process

1. Propose: state the mechanism, the label for the evidence, and the checklist item the rule would add.
2. Check duplication against the existing catalog by mechanism, not by filename.
3. Verify every URL and record the access date.
4. Confirm the file matches the section order and the length budget.
5. Read the `Incorrect` example and ask whether it would actually compile or run in the target version. An example that cannot occur teaches nothing.
6. Confirm the rule does not contradict a repository requirement or a verified platform constraint. If it does, the repository wins; record the trade-off in the rule.
7. Land the change with the update to `references/sources.md` when a new source was introduced.

## 7. Recording version applicability

Every rule states its target in `## Version notes`:

- The versions it was written against (for this catalog: Plasma 6.8.0, Qt 6.11.1, KF6 / ECM 6.31.0).
- The verification date.
- What specifically must be re-checked on a different branch — API names, metadata keys, tool names, defaults.
- Whether the guidance is stable across the major version or tied to one release.

When a rule becomes wrong for a newer target, do not delete the history: update the rule, adjust `## Version notes`, and note the change in the catalog changelog or the repository's task record.

## Checklist for a rule change

- [ ] Four eligibility tests passed (recurring, actionable, non-duplicative, evidence-backed).
- [ ] Frontmatter complete: `title`, `impact` in P0–P3, `scope`, `tags`.
- [ ] All nine sections present, in order.
- [ ] 40–90 lines.
- [ ] Each code block marked pseudocode.
- [ ] Every claim labelled.
- [ ] Every URL re-checked with a recorded status and date.
- [ ] Exceptions section states a real trade-off, not a disclaimer.
- [ ] Checklist items are binary and observable on a diff.
- [ ] Contradictions with repository or platform constraints resolved in favour of the constraint.

## Sources

- Qt: Performance considerations and suggestions (example of a primary source with explicit claims) — https://doc.qt.io/qt-6/qtquick-performance.html
- Qt: QML Coding Conventions — https://doc.qt.io/qt-6/qml-codingconventions.html
- KDE: API documentation — https://api.kde.org/
- KDE: KDE Human Interface Guidelines — https://develop.kde.org/hig/
- Vercel: Introducing React Best Practices (organisational model only) — https://vercel.com/blog/introducing-react-best-practices

Accessed: 2026-10-20. All URLs returned HTTP 200 on that date.
