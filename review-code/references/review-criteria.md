# Review Criteria

## Requirements and Project Standards

Check the target against the applicable requirements, acceptance criteria, interface contracts, project conventions, and verified decisions. Look for omissions, partial implementation, incorrect behavior, and scope expansion. Use standards from the actual project rather than generic preferences. A missing or stale document is a source limitation to investigate, not permission to invent expected behavior.

## Related Correctness

For changed logic, interfaces, and data, follow relevant paths through actual callers and collaborators. Consider applicable cases such as:

- Empty, invalid, boundary, duplicate, or unusually large inputs.
- Missing, stale, conflicting, or partially persisted state.
- Errors, retries, cancellation, timeouts, cleanup, and recovery.
- Ordering, concurrency, idempotency, and repeated events.
- Resource limits, security boundaries, and sensitive information.
- Existing data, versions, clients, or integrations and their compatibility.

These are prompts for relevant investigation, not a mandatory checklist. Stay within the change's impact; do not turn review into an audit of the entire project. Test coverage must distinguish the intended behavior from plausible faulty behavior, but missing tests alone are not necessarily a defect.

## Maintenance Smells as Leads

Use a smell only to ask whether a concrete problem exists. It is not automatically a violation or a reason to request a refactor. Investigate, for example, tightly coupled responsibilities, unnecessary indirection, duplicated logic that can diverge, large functions or modules, hidden side effects, swallowed errors, misleading names, or brittle tests. Recommend changes only when a specific future cost or risk justifies them and outweighs the cost of change. Prefer established project conventions and consider whether the code is actually in the target scope.

## Tool and Test Evidence

Choose checks appropriate to the actual target and impact. Confirm that a check examined the relevant staged, unstaged, committed, or untracked version; note when the working tree differs from the requested commit or PR target. A configured command or green status alone is not proof that relevant paths were covered. Read the output and tie conclusions to its actual scope.

Re-run checks when target changes or earlier evidence no longer applies. Do not mechanically run every tool or the entire suite when relevant validated evidence is current. Static reasoning can be sufficient for a demonstrable defect; dynamic tests may be needed to establish behavior that cannot be inferred. State checks that were unavailable, not run, or constrained.
