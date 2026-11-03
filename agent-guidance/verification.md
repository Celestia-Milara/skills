# Verification and Delivery

## Behavior and Evidence

Before behavior changes, identify what must stay, what may change under the task's authorization, and which effects remain uncertain. Use effective requirements and contracts; current output can be wrong. An unchanged signature does not prove unchanged behavior.

Start with relevant subsystem sources, contracts, and implementation entries. If sources are missing, use available requirements and call paths. Investigate actual dependencies, including shared state, storage, events, and configuration assumptions. Expand when key effects remain unclear. Judge reading, editing, and verification scope separately. Stop when affected interactions and risks have enough evidence for the task; state remaining gaps. Continue authorized changes and independent work without a fixed report or new approval stage.

Behavior tests should use stable, caller-observable interfaces. Derive expectations independently of implementation. For fixes, check the original failure scenario and retain regression coverage when useful. Use pstack's [tdd](../pstack/skills/tdd/SKILL.md) for a practical test-first path, not every change.

Select project checks by the affected promises. Structure, behavior, and real integration checks provide different evidence; use what the risk needs. Build or mocked-test success does not prove runtime, integration, persistence, or platform behavior. Use real checks when a test double replaces the mechanism at issue.

Before checks that use real services, check the environment, account, data scope, and expected side effects against existing authorization. Implementation or verification authorization alone does not permit production deployment, real charges, notifications to real users, or changes to production data. If these effects lack authorization, explain the target and impact and obtain authorization before proceeding. Reuse existing authorization for the same scope without asking again.

Confirm that target checks ran against the relevant version; inspect test matches, skips, and covered paths. A zero exit code alone is insufficient. Report performed checks, failures, and gaps. For pending manual acceptance, provide steps and observable outcomes.

## Review and Delivery

Use pstack's [interrogate](../pstack/skills/interrogate/SKILL.md) for executable
adversarial review when its tools are available. It keeps run-proven findings.
Also assess requirements, project constraints, and statically provable defects;
those checks are not replaced by an empty executable-review result. Keep their
evidence distinct. Follow the [host adapter](../pstack/skills/poteto-mode/references/host.md)
for missing delegation or model diversity. A standalone review reports findings;
fixes require applicable implementation authorization.

Deliver this round's results in conversation. Update repository materials that need ongoing maintenance according to [source ownership](collaboration.md#source-ownership); do not create a persistent report for every delivery. Staging and committing follow [Git guidance](git.md).
