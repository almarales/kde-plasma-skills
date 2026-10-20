# Future design proposals and experimentation

How to evaluate, document, and label a design idea that is not yet established KDE practice. Use this file before proposing a new interaction model, visual direction, or platform-wide change, and when reviewing someone else's proposal.

## Scope

- In scope: design proposals that depart from current KDE patterns, prototypes of unshipped ideas, and reviews of "what Plasma should do next" arguments.
- Out of scope: implementing an already-established pattern (use the other references), engineering-only refactors, and product roadmap planning for a specific application.
- This file cannot approve anything. No statement here, and no score in the rubric, makes an idea an official KDE decision.

## 1. Classify the proposal before writing it

| Level | Definition | Minimum evidence | Allowed framing |
| --- | --- | --- | --- |
| Level 1 - Established | A documented HIG pattern, or a convention consistently implemented in current KDE software | Citation to the HIG page or to inspected code in the target branch | `[Official]` or `[Observed]`. Implement directly. |
| Level 2 - Proposed improvement | A scoped change to an existing surface that keeps the current interaction model | Before/after evidence, the affected component, and the convention it changes | `[Recommendation]`. "Proposed", "would", "we recommend". |
| Level 3 - Experimental future | A change to the interaction model, visual language, or platform direction, with no established implementation to compare against | The full protocol in section 2 | `Experimental — not an official KDE decision`. Always. |

Classification rules:

- `[Recommendation]` If you cannot name the current behavior with a file, screenshot, or HIG citation, you are not ready to classify the idea. Gather that first.
- `[Recommendation]` A Level 2 proposal that grows to affect unrelated surfaces or the platform's default behavior is a Level 3 proposal. Reclassify it; do not stretch the lighter process.
- `[Official]` The HIG describes itself as a living document and explicitly says it is not an ironclad law code: innovation is expected within the guidelines, and breaking a rule can be appropriate when it produces a superior result. That permission is for evidence-backed deviation, not for declaring new policy.

## 2. Level 3 protocol

Every Level 3 proposal must contain these nine sections, in this order. Missing sections are a hard fail, not a formatting nit.

### 2.1 Problem statement

- State the user problem in one paragraph, without naming the proposed solution.
- Name who experiences it, in which workflow, and how often. "Users" is not an audience.
- Failure mode: a solution in search of a problem, or a problem defined as "the current UI is not like <other platform>".

### 2.2 Evidence

- Separate what you observed from what you infer. Use `[Observed]` only for artifacts you inspected: file paths with line numbers, screenshots with environment details, measurements with method.
- Include current behavior, not only the desired behavior. A proposal that cannot describe today's behavior cannot predict its impact.
- Failure mode: mockups presented as evidence, or claims about user demand with no source.

### 2.3 Affected workflows

- List the workflows that change, the ones that must not change, and the ones you have not checked.
- Include non-pointer input, keyboard-only use, screen readers, and touch where the surface supports it.
- Failure mode: a desktop-only analysis applied to a component shared with Plasma Mobile or a touch-capable device.

### 2.4 Alternatives

- At least three: keep the current behavior, the smallest local fix, and the proposed change. Add a "do nothing and document the limitation" option.
- For each, state cost, reversibility, and who pays the maintenance.
- Failure mode: a single option described as inevitable.

### 2.5 Accessibility impact

- Address keyboard path, focus visibility and order, screen-reader name/role/state, contrast in both color schemes, text scaling, color-independent status, reduced motion, and localization/RTL.
- Mark each as verified, expected, or unknown. Unknown is acceptable at proposal stage; silent omission is not.
- Failure mode: "accessibility will be handled during implementation." That defers a design constraint and usually loses it.

### 2.6 Technical implications

- Name the components, frameworks, and versions affected (Plasma, Qt, KF6 modules), the migration path for existing users and third-party themes/plasmoids, and the fallback when the feature is unavailable.
- State what you verified and what you assume. Do not invent APIs or performance numbers.
- Failure mode: a platform-wide change with no migration story for existing configurations.

### 2.7 Validation plan

- Define the smallest prototype that could falsify the idea, the tasks participants perform, and the signals you will record (completion, errors, time, subjective rating, accessibility findings).
- Include a comparison against the current implementation, not only against the prototype's own goals.
- Failure mode: "we will gather feedback" with no task, sample, or decision rule.

### 2.8 Risks

- Cover user confusion, inconsistency with existing surfaces, maintenance burden, theme/plugin breakage, accessibility regressions, and reversibility cost.
- Give each risk a likelihood and an impact, and name a mitigation or an accepted residual risk.
- Failure mode: risk list that contains only "users may not like change".

### 2.9 Decision status

Use exactly one of these values, with a date and an owner:

| Status | Meaning | Required link |
| --- | --- | --- |
| `Draft` | Being written; not ready for review | None |
| `Under discussion` | Shared with the community for feedback | Discussion or issue URL |
| `Prototype approved for evaluation` | Allowed to build a throwaway prototype; not approved for shipping | Decision comment URL |
| `Rejected` | Considered and declined | Rationale URL or archived document |
| `Superseded` | Replaced by another proposal | Superseding document |
| `Adopted` | Shipped or accepted by the relevant KDE process | Merged change or published decision URL |

- `[Recommendation]` `Adopted` is never self-declared. Without a merged change or a published decision URL, the status stays `Under discussion` at most.
- `[Recommendation]` Every artifact carries the label `Experimental — not an official KDE decision`, plus the date and the target version. This includes the proposal document, mockups, prototype screenshots, issue text, and slide decks. A label only in the appendix does not count.

## 3. Evaluation rubric

Score each criterion from 1 to 5. Record the score and one sentence of justification. Scores are an argument aid, not an approval mechanism.

| Criterion | 1 | 3 | 5 |
| --- | --- | --- | --- |
| User benefit | No identified user problem | Plausible benefit for a defined group | Measured or strongly evidenced benefit for a defined workflow |
| Consistency | Contradicts established patterns without explanation | Fits most surrounding behavior | Extends existing patterns coherently; deviations are explained |
| Accessibility | Regresses a known accessibility behavior | Neutral, with open questions | Improves or preserves every applicable accessibility requirement with evidence |
| Feasibility | Requires unavailable APIs or unknown platform work | Feasible with known work and some uncertainty | Proven in a prototype on the target stack |
| Maintenance cost | New bespoke component with no owner | Moderate, shared with existing code | Reuses existing components and has a clear owner |
| Reversibility | Platform-wide, breaks existing configs or third-party assets | Reversible with user-visible migration | Local, removable without data or config migration |
| Evidence quality | Assertion or mockup only | Some inspected artifacts, gaps acknowledged | Current behavior, alternatives, and validation evidence are all inspectable |

Decision rules:

- `[Recommendation]` Evidence quality of 1 means stop. Do not prototype; gather evidence first.
- `[Recommendation]` Accessibility of 1 or 2 is a blocker for recommending a prototype, regardless of the average.
- `[Recommendation]` An average of 3.5 or higher is the minimum to recommend a prototype. Lower scores can still be documented as `Rejected` or `Under discussion`.
- `[Recommendation]` No score, however high, changes the decision status. Status changes only through the community process in section 5.

## 4. Acceptable and unacceptable framing

| Acceptable | Unacceptable |
| --- | --- |
| "Observed in Plasma 6.8: the panel configuration dialog places Apply at the bottom right. This proposal would move it, because ..." | "Plasma 7 will move the Apply button." |
| "No published decision was found as of 2026-10-20. This is a proposal for discussion." | "KDE has decided to redesign the panel." |
| "The VDG discussion thread proposes X; the linked issue is still open." | "The VDG approved X." |
| "Prototype only. Not shipped, not approved, and not a commitment." | "Coming soon to Plasma." |
| "We have not tested this with a screen reader; impact is unknown." | "This change is accessibility-neutral." (without testing) |
| "This borrows a pattern from mobile; here is why it fits a desktop panel, and here is what we rejected." | "Modern UI conventions require this." |
| "The current implementation is at `file:line`; the deviation is intentional because ..." | "The old design was bad." |
| "This is reversible: the old setting remains and the new path is opt-in." | "Users will adapt." |

Rules:

- `[Recommendation]` Never write "Plasma 7 will ...", "KDE is moving to ...", or any sentence that implies an approved future. Describe proposals in conditional or past-evidence form.
- `[Recommendation]` If you cannot link a decision, describe it as missing evidence rather than inferring it from a mockup, a chat message, or another project's roadmap.
- `[Recommendation]` Attribute borrowed patterns to their source and argue platform fit. Novelty is not a benefit.

## 5. How KDE decisions actually emerge

- `[Official]` The Visual Design Group (VDG) created and maintains the KDE Human Interface Guidelines and the Breeze theme.
- `[Official]` VDG discussions typically begin in the group's real-time chatroom. Once there is general consensus, the conversation moves to a GitLab issue where developers participate. The issue should summarize the discussion, tag participants, and include before/after images or mockups, user benefits, and red flags.
- `[Official]` Scope and details are expected to evolve through developer feedback; proposals should bring solid evidence. When general agreement is reached, the discussion thread is closed, because open discussions block the code change from proceeding.
- `[Official]` Because the shipping implementation matters more than design-toolkit fidelity, low-fidelity wireframes or mockups are recommended over high-fidelity mockups that differ from real components.
- `[Official]` The HIG is a living document; corrections and improvements are contributed through invent.kde.org.

What this means for an agent:

- `[Recommendation]` Cite the specific issue, merge request, or HIG page. "The community wants" is not evidence.
- `[Recommendation]` When no decision exists, say so with the date of the search: "No verified public decision found on 2026-10-20." Then name what would change the conclusion (a merged MR, a closed issue with agreement, a published HIG update).
- `[Unknown]` Any statement about Plasma 7 direction is unverified unless a current public decision is linked. Do not fill that gap with plausible-sounding plans.

## 6. Operational workflow

1. `[Recommendation]` Classify the idea as Level 1, 2, or 3 before writing prose.
2. `[Recommendation]` Collect current-behavior evidence: file paths and line numbers, screenshots with theme/scale/locale, and the HIG or API citation that governs the surface.
3. `[Recommendation]` Write the proposal with [`../assets/design-proposal.md`](../assets/design-proposal.md). Replace every `<placeholder>`; a template with placeholders is not a proposal.
4. `[Recommendation]` Apply the experimental label to every artifact, with date and target version.
5. `[Recommendation]` Score the rubric, including criteria where the proposal is weak. Record dissent instead of averaging it away.
6. `[Recommendation]` Prototype only the smallest falsifiable slice, off by default, in a branch or throwaway build. Do not present prototype behavior in release notes.
7. `[Recommendation]` Validate against the current implementation, including keyboard-only, screen-reader, both color schemes, text scaling, long translations, and RTL.
8. `[Recommendation]` Hand the result to the community process with links. Do not mark `Adopted` yourself.
9. `[Recommendation]` Record the outcome. If adopted, update the HIG or component documentation first, then remove the experimental label and cite the decision.

## 7. Anti-patterns

- `[Recommendation]` Solution-first proposals: the mockup exists before the problem is stated.
- `[Recommendation]` Invented consensus: "the community", "the VDG", or "KDE" used without a link.
- `[Recommendation]` Mockup-only evidence with no states, no error path, and no accessibility pass.
- `[Recommendation]` Borrowed web or mobile patterns with no argument for desktop fit.
- `[Recommendation]` Irreversible platform changes with no migration for existing configs, themes, or third-party plasmoids.
- `[Recommendation]` Treating accessibility, localization, or maintenance as implementation details to settle later.
- `[Recommendation]` Calling a prototype "shipping" or "approved" because it was demonstrated once.

## Sources

- KDE Human Interface Guidelines (living document, innovation and deviation clause): https://develop.kde.org/hig/ (Accessed: 2026-10-20)
- KDE HIG, Accessibility and inclusiveness: https://develop.kde.org/hig/accessibility/ (Accessed: 2026-10-20)
- KDE HIG, Simple by default: https://develop.kde.org/hig/simple_by_default/ (Accessed: 2026-10-20)
- KDE HIG, Powerful when needed: https://develop.kde.org/hig/powerful_when_needed/ (Accessed: 2026-10-20)
- KDE Visual Design Group: https://community.kde.org/KDE_Visual_Design_Group (Accessed: 2026-10-20)
- Plasma Developer Guide: https://community.kde.org/Plasma/DeveloperGuide (Accessed: 2026-10-20)
- KDE Developer documentation: https://develop.kde.org/ (Accessed: 2026-10-20)

## Version notes

- Written against the documentation available on 2026-10-20; no Plasma 7 decision is asserted anywhere in this file.
- The VDG process description reflects the current wiki page on that date. Community process changes without a deprecation notice; re-check the wiki and the linked issue before relying on a step.
- The rubric thresholds are this skill's proposed conventions (`[Recommendation]`), not KDE policy.
