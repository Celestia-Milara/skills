---
name: review-code
description: "Review changes against requirements, project standards, and relevant correctness risks. Use for a requested review or delivery self-review; verify findings and rank by impact. A standalone review reports by default and does not authorize fixes or a broader audit."
---

# Review Code

## 1. Establish authority and target

A standalone review authorizes investigation and reporting by default. Respect explicit read-only, report-first, and discussion limits. An implementation self-review or explicit fix request permits clear fixes within existing scope. Neither review nor speculation adds commit, push, PR, or release authorization.

Use the requested PR, commit, range, files, or behavior. Otherwise infer this task's changes from repository status, branch and base, recent history, index, working tree, and relevant untracked files. Do not inspect only HEAD, silently include unrelated work, or always use merge-base-to-HEAD. Ask only if material target ambiguity remains; an empty diff is no evidence of quality.

Read [Review Scope and Sources](references/scope-and-sources.md) when choosing the comparison, distinguishing workspace/index versions, or locating requirements and related paths. Recheck affected conclusions if the target changes; do not commit or clean the workspace just to enable review.

## 2. Locate the basis and assess both perspectives

Follow the actual project entry point to applicable requirements, acceptance criteria, designs, subsystem documentation, standards, and decisions. Verify related source, tests, callers, and interfaces. Issue and commit text provide clues; existing code does not automatically establish intent, and old documents do not override new user instructions. State missing-source limits while continuing correctness checks supported by evidence.

Assess requirements and standards for omissions, partial implementation, incorrect behavior, and scope expansion. Separately assess correctness relevant to the change: interfaces, failure paths, resources, concurrency, compatibility, and whether tests discriminate intended behavior. Neither perspective substitutes for the other.

Read [Review Criteria](references/review-criteria.md) for applicable risk prompts and tool-evidence checks. Smells are investigation leads, not automatic violations; prefer explicit project rules and suggest cleanup only for concrete benefit at acceptable cost. Stay within the target's impact.

Use capabilities actually available. If needed companion guidance cannot be invoked, read its configured source through the host's mechanism; state inaccessible guidance without claiming a successful invocation. Do not require a fixed number of agents or repeated loading.

## 3. Verify and report

Read [Findings, Reporting, and Fixes](references/findings-and-report.md) when verifying candidates or preparing the report; it owns detailed evidence, counterexample, causation, deduplication, and reporting rules.

Establish a location, applicable rule or contract, trigger, and concrete impact for each finding. Try to disprove it using reachability, caller guarantees, handling, version limits, and applicable decisions. Static proof can suffice; severity does not turn an unverified premise into a defect. Report problems introduced, worsened, or made current by the target and explain causation for older locations. Keep unrelated legacy issues separate.

Merge findings only when they share root cause and fix. Order confirmed defects and explicit standards violations by impact; separate maintenance suggestions and unresolved questions. Report target, locations, triggers, checks and coverage, missing sources, and limits. No findings means none confirmed within the examined scope, not proof of no bugs, full requirements conformance, or manual acceptance.

If delegating is useful and authorized, verify that perspectives share the same target, examine evidence and counterexamples, and integrate coverage and limitations rather than pasting reports.

## 4. Handle authorized follow-up

For fixes already authorized, inspect the new diff, verify the original issue is resolved, check for new issues, and run relevant checks against the changed version. Pre-fix evidence does not validate the fix. Ask only when behavior, scope, or a key trade-off needs a decision beyond existing authorization; do not reconfirm settled decisions.

Keep long-term decisions and retained documentation in their owning sources rather than duplicating their policies here. After authorized edits, follow project Git rules and current authorization; absent explicit commit authorization for this scope, show the checked work and ask whether the round is ready for a local commit. Honor existing authorization without asking again. Report what changed and what remains unresolved or unverified; review does not prove runtime behavior or required manual acceptance.
