# Review Criteria

## Requirements and Project Standards

Check the target against applicable requirements, acceptance criteria, contracts, project conventions, and verified decisions. Look for omissions, partial implementation, incorrect behavior, and scope expansion. Use the project's standards, not generic preferences. Investigate missing or stale sources; do not invent expected behavior.

## Related Correctness

For changed logic, interfaces, and data, follow relevant paths through actual callers and collaborators. Consider applicable cases such as:

- Empty, invalid, boundary, duplicate, or unusually large inputs.
- Missing, stale, conflicting, or partially persisted state.
- Errors, retries, cancellation, timeouts, cleanup, and recovery.
- Ordering, concurrency, idempotency, and repeated events.
- Resource limits, security boundaries, and sensitive information.
- Existing data, versions, clients, or integrations and their compatibility.

These prompts guide relevant investigation; they are not a mandatory checklist. Stay within the change's impact rather than auditing the whole project. Tests must distinguish intended behavior from plausible faults; missing tests alone do not establish a defect.

Check for new dependencies on another module's internal implementation, owned state, storage, or undefined event and configuration semantics. Check whether unchanged callers still meet their conditions and receive the promised behavior. An unchanged signature alone does not establish compatibility.

Apply boundary rules defined by the project. Without such a rule, report a defect only when evidence establishes incorrect behavior. Keep future maintenance concerns and uncertain dependencies separate from confirmed findings.

## Maintenance Smells as Leads

Use smells to investigate concrete problems, not to declare violations or require refactoring. Examples include tight coupling, unnecessary indirection, divergent copies, large modules, hidden effects, swallowed errors, misleading names, and brittle tests. Recommend changes only when a specific benefit outweighs their cost. Apply project conventions and stay within scope.

## Tool and Test Evidence

Choose checks for the actual target and impact. Confirm the relevant staged, unstaged, committed, or untracked version was checked. State differences between the working tree and requested commit or PR. Read the output for matched tests, skips, and relevant paths. A configured command, zero exit code, or green status alone does not prove coverage.

When implementation and verification material both change, check the basis for changed assertions, snapshots, selectors, contracts, and test doubles. Refactoring must preserve valid behavioral obligations. A fix can replace a faulty expectation; an authorized contract change can alter obligations. Require an independent basis for either change. Check that revised tests still distinguish relevant faults; a focused counterexample can resolve a specific doubt.

Check whether a test double replaces the property being verified. Fake success alone cannot establish real persistence, transaction timing, or integration behavior. Obtain relevant real evidence when needed, or state the gap.

Repeat checks when the target changes or prior evidence no longer applies. Reuse current evidence instead of running every tool or the full suite mechanically. Static proof can establish a defect; use runtime checks when necessary facts cannot be inferred. State checks that were unavailable, not run, or constrained.
