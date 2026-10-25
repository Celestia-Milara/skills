# Reusable Lessons from Corrections and Rework

Use this method when an event could prevent a meaningful repeat failure. It does not require a lesson for every correction or task.

## Classify and retain what matters

Distinguish an implementation or verification error from a changed requirement, changed environment, local exception, or one-time preference. A user correction is a reason to investigate, not proof of a general rule. Normal failing tests during TDD are not mistakes to record individually.

Retain information only when it can help later work and existing facts do not already explain it. Reuse a related change record, subsystem page, or verification record. If no suitable source exists, save a small task evidence record only when its future value warrants one, following project locations. Do not create an empty lessons directory or require a global `lessons.md`.

Keep observations separate from explanations. Preserve the relevant conditions, observed failure or rework, evidence, known cause, and remaining uncertainty. Add a possible prevention action and reconsideration conditions only when supported. Do not invent occurrence counts, time costs, or causation.

A candidate remains an investigation item in its owning source. It does not receive an `active` decision status. When a settled failure result or choice meets the entry point's recording threshold, update a suitable note or create one. Keep current facts in subsystem documentation and progress in the change record; link rather than copy full bodies.

## Verify cause and choose prevention

Repetition across tasks or one high-consequence event can justify review; neither a fixed count nor elapsed rework time automatically creates a rule. Check:

- Does source inspection, a reproduction, or other evidence support the cause? Could the symptom have a different cause?
- Which environment, version, interface, or task conditions make the lesson applicable? Which exceptions remain?
- Would the proposed action detect or prevent this failure? Would it cause false alarms or cost more to maintain than it saves?
- Do existing rules or checks already cover the event? If so, repair execution or retrieval rather than adding a duplicate rule.

Choose the target by the mechanism. Use a regression test or automated check when it detects the failure reliably at reasonable cost. Use subsystem or operating guidance for local conditions. Put a rule in the project entry only when it applies across tasks and needs to be present at session start. A link and a clear reading trigger are enough for conditional material.

Recording evidence adds no authority to change code, run real services, or change project policy. Continue actions already authorized for this scope. If prevention needs an unsettled policy or behavior decision, propose its concrete scope, benefit, and impact before the dependent action. Do not add approval for every factual correction or documentation update.

## Retrieve, reassess, and exit

Make retained evidence findable from the related subsystem, change, or existing project navigation. At the next relevant task, use [history retrieval](retrieval.md) and verify the conditions against the current source. An unrelated task need not load all experience records. Missing history permits continuation; inaccessible history is an evidence gap; still-valid results from this task can be reused.

Correct an unsupported lesson when new evidence disproves it. If only the evidence or facts change, update the owning source. A genuine decision reversal follows the entry point's supersession rules. Changed conditions may justify a new attempt; a failed attempt does not create a permanent blacklist. Record established reconsideration conditions and state when none are known.

After prevention is adopted, remove duplicate summaries only after necessary conditions, rationale, and evidence have a durable home or link. Keep the connection from the failure to its prevention. For decision records, follow [retention rules](retention.md). Do not remove unique history because it was promoted or exceeded a line budget.

## Check reuse across sessions

For a new mechanism or substantial change, use fresh-context tasks when available and authorized. Retain the input, target package version or snapshot, loaded sources, actual output, and relevant artifacts. Verify that a later task retrieves the evidence and changes its behavior under the original conditions. Creating a lesson file alone does not demonstrate reuse.

Include a changed-premise case that should permit a new attempt, an unrelated task that should avoid loading lessons, and missing or inaccessible history. Check both standalone and project-guidance use when affected. Verify host loading separately: a Markdown link does not prove that the host or model read its target. State whether evidence is static inspection, a scenario walkthrough, a model run, or a real host check; one successful run does not establish general reliability.

## Example: verification missed durable storage

This is an illustrative progression, not a reported test run or mandatory format.

An existing task record says a save test passed with a fake store, but a fresh connection could not read the result. Preserve the test boundary, connection conditions, and observed result. Until the transaction path is inspected, keep “commit was missing” as a hypothesis.

If inspection confirms that the fake returned before a commit, assess a check through the shipped storage interface with a fresh connection. A later task on the same storage path should find the evidence and verify durable visibility. An in-memory store with an explicitly different contract does not inherit that requirement. A changed storage contract requires reassessment, not an automatic ban on fakes.
