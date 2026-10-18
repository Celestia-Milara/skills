# Verification and Delivery

## Behavior and Evidence

Behavior tests should exercise stable, caller-observable interfaces and derive expected results independently of the implementation. For bug fixes, check the original failure scenario; retain automated regression coverage when it has ongoing value. Use [tdd](../tdd/SKILL.md) for test-first work, not as a prerequisite for every change.

Select checks from the project's actual commands and affected behavior. Build or mocked-test success does not establish real runtime, integration, or platform behavior; verify those where the change requires that evidence. Report the checks performed, failures, and remaining gaps. For pending manual acceptance, provide steps and observable outcomes.

## Review and Delivery

Use [review-code](../review-code/SKILL.md) for requested reviews and delivery self-review. The package owns review scope, findings, and the distinction between reporting and fixing.

Deliver this round's results in conversation. Update repository materials that need ongoing maintenance according to [source ownership](collaboration.md#source-ownership); do not create a persistent report for every delivery. Staging and committing follow [Git guidance](git.md).
