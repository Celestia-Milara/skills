# Verification and Delivery

## Behavior and Evidence

Before behavior changes, identify what must stay, what may change under the task's authorization, and which effects remain uncertain. Use effective requirements and contracts; current output can be wrong. An unchanged signature does not prove unchanged behavior.

Start with relevant subsystem sources, contracts, and implementation entries. If sources are missing, use available requirements and call paths. Investigate actual dependencies, including shared state, storage, events, and configuration assumptions. Expand when key effects remain unclear. Judge reading, editing, and verification scope separately. Stop when affected interactions and risks have enough evidence for the task; state remaining gaps. Continue authorized changes and independent work without a fixed report or new approval stage.

Behavior tests should use stable, caller-observable interfaces. Derive expectations independently of implementation. For fixes, check the original failure scenario and retain regression coverage when useful. Use [tdd](../tdd/SKILL.md) for test-first work, not every change.

Select project checks by the affected promises. Structure, behavior, and real integration checks provide different evidence; use what the risk needs. Build or mocked-test success does not prove runtime, integration, persistence, or platform behavior. Use real checks when a test double replaces the mechanism at issue.

Confirm that target checks ran against the relevant version; inspect test matches, skips, and covered paths. A zero exit code alone is insufficient. Report performed checks, failures, and gaps. For pending manual acceptance, provide steps and observable outcomes.

## Review and Delivery

Use [review-code](../review-code/SKILL.md) for requested reviews and delivery self-review. The package owns review scope, findings, and the distinction between reporting and fixing.

Deliver this round's results in conversation. Update repository materials that need ongoing maintenance according to [source ownership](collaboration.md#source-ownership); do not create a persistent report for every delivery. Staging and committing follow [Git guidance](git.md).
