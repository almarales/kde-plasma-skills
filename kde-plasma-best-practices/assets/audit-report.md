<!--
INSTRUCTIONS
Replace every <angle-bracketed> placeholder before sharing this audit.
An audit with no inspected evidence is inconclusive, not a pass.
Use the severity mapping, verdict rules, and evidence discipline from
references/audit-criteria.md, and the rule impact classes from
references/rules/_sections.md.
Delete this comment block before publishing.
-->

# Code audit: <target>

## Scope

Use this template to record one audit of Plasma source code: QML, C++, build files, or their interaction. Record only what was inspected. An audit without inspected evidence is `inconclusive`, never a pass. This is not a bug tracker, and it does not replace the engineering review of visual, interaction, or accessibility decisions, which belongs to `kde-plasma-ui-ux`.

## Target

| Field | Value |
| --- | --- |
| Component / subsystem | <name and repository-relative path> |
| Change under review | <merge request, commit, or diff range> |
| Branch / revision | `<branch>` at `<commit-sha>` |
| Reviewer | <name or agent identifier> |
| Review date | `<YYYY-MM-DD>` |
| Criteria used | `references/audit-criteria.md` |
| Rules loaded | <rule files selected from `references/rules/_sections.md`> |
| Out of scope | <files, components, or questions deliberately not audited> |

## Versions

| Item | Value | How verified |
| --- | --- | --- |
| Plasma | `<version>` | `<command output>` |
| Qt | `<version>` | `<command output>` |
| KF6 / ECM | `<version>` | `<command output>` |
| Build type | `<release / debug>` | `<command or config>` |
| Compiler | `<version>` | `<command output>` |

## Environment

| Dimension | Value |
| --- | --- |
| Build command | `<command>` |
| QML lint | `<qmllint6 --version, or the project's all_qmllint target>` |
| C++ analyzers | `<clazy / clang-tidy present or absent, and how established>` |
| Test command | `<command, or "not run">` |
| Uncommitted changes | `<none, or the list: an audit of a dirty tree is not a review of a revision>` |
| Environment notes | <anything that changes how the results should be read> |

## Evidence captured

| Evidence | Path or URL | Captured in |
| --- | --- | --- |
| Baseline build output | <path or inline block> | <environment row> |
| Candidate build output | <path or inline block> | <environment row> |
| `qmllint6` output | <path or inline block> | <environment row> |
| Test output | <path or inline block> | <environment row> |
| Measurement logs | <path or inline block> | <environment row> |

## Axis outcomes

| Axis | Outcome | Rules applied | Notes |
| --- | --- | --- | --- |
| Correctness | `<pass / fail / inconclusive / unverified>` | <rule files> | <what was inspected> |
| Performance | `<pass / fail / inconclusive / unverified>` | <rule files> | <what was measured or not> |
| Maintainability | `<pass / fail / inconclusive / unverified>` | <rule files> | <what was inspected> |

An axis that was not inspected is `unverified`, never `pass`.

## Findings

Severity: `Blocker | Major | Minor | Nit`, taken from the violated rule's `impact` class. Status: `Fail | Unverified` (a finding is never a pass).

| ID | Status | Severity | Location (`file:line`) | Rule | Observed | Expected | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | `<Fail \| Unverified>` | <severity> | `<path:line>` | `<rules/...md>` | <what happens> | <what should happen> | <command output / file / measurement> |
| F2 | `<Fail \| Unverified>` | <severity> | `<path:line>` | `<rules/...md>` | <what happens> | <what should happen> | <command output / file / measurement> |

Every finding cites a rule that was loaded. A defect no rule covers is an observation, not a finding.

## Observations

Defects outside the rule catalog: no rule loaded condemns them, so they are not findings and are never `Blocker`.

| ID | Severity | Location (`file:line`) | Observed | Why it matters | Candidate rule? |
| --- | --- | --- | --- | --- | --- |
| O1 | `Minor` | `<path:line>` | <what happens> | <consequence> | <yes / no> |

## Checks run

| Check ID | Status | Evidence |
| --- | --- | --- |
| C1 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| C2 | `<Pass / Fail / N/A / Unverified>` | <evidence> |
| C3 | `<Pass / Fail / N/A / Unverified>` | <evidence> |

Add or remove rows to match the checks actually required for the change; see the required-checks table in `references/audit-criteria.md`.

## Checks not run

| Check ID or check | Reason | What evidence would close it |
| --- | --- | --- |
| <ID> | <missing tool, missing environment, out of scope> | <specific evidence> |

## Measurements

Only rows with real numbers. A row without a command and an environment is not a measurement.

| Metric | Command | Before | After | Environment |
| --- | --- | --- | --- | --- |
| <metric> | `<command>` | <value> | <value> | <machine, build type, version> |

## Accepted risks

Findings that were reviewed and consciously accepted, with an owner. An accepted finding is still open until it is fixed; it is not a pass.

| Finding ID | Accepted by | Reason | Review date |
| --- | --- | --- | --- |
| F1 | <name> | <why the risk is accepted> | `<YYYY-MM-DD>` |

## Verdict

| Field | Value |
| --- | --- |
| Verdict | `<pass \| fail \| inconclusive>` |
| Open blockers | <count and IDs, or `none`> |
| Open major findings | <count and IDs, or `none`> |
| Unverified items | <count and IDs, or `none`> |
| Accepted risks | <finding IDs, or `none`> |
| Delivery decision | `<left to the repository's own policy>` |

Verdict rules:

- `pass`: every applicable check is `Pass` with evidence, and no blocker or major finding is open.
- `fail`: at least one blocker or major finding is open.
- `inconclusive`: any required evidence is missing, or any applicable check is `Unverified`. An audit without inspected evidence is always `inconclusive`.

The verdict describes the audited revision only. It does not authorize delivery, and it does not judge the author.

## Sources

- Rule index and impact classes — `references/rules/_sections.md`
- Audit criteria — `references/audit-criteria.md`
- Sources consulted for this audit — <URL and access date, one per line>

## Version notes

- Template version 1.0, 2026-10-20. The authority for severities, statuses, and verdicts is `references/audit-criteria.md`; this template only records the outcome.
- The severity classes and the verdict rules are this skill's proposed conventions (`[Recommendation]`), not official KDE policy.
- The verdict vocabulary is shared with `kde-plasma-ui-ux`'s UI review on purpose: one vocabulary for the bundle.
