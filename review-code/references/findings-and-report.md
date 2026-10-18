# Findings, Reporting, and Fixes

## Confirm Findings

At minimum, a correctness defect must state:

- The specific location in the target content and any necessary context.
- The requirement, contract, or provable mechanism constraint that is violated.
- The input, state, or event ordering that triggers the issue in the current code.
- The incorrect result and its impact, not just an abstract risk.

For an explicit standards violation, cite the rule and its conditions of applicability; do not invent a runtime failure to prove it. If the rule is unclear or its applicability is disputed, continue investigating or classify it as a suggestion or an item requiring a decision.

Keep evidence strength separate from impact. A static call chain or state derivation may prove an issue without dynamic reproduction. If a premise is unverified, do not present it as a confirmed defect merely because the potential consequence is severe. Tests, logs, and runtime results prove only the scope they actually cover; do not infer that all requirements are met from green checks.

First try to disprove each candidate: is the entry point reachable, does the caller already guarantee the precondition, is the error handled upstream, does the constraint apply only to another version, or does a valid decision explain this behavior? Do not label an intentional trade-off as an error by default.

## Scope, Deduplication, and Ordering

Prioritize defects introduced or worsened by this change, or made into current problems by it. A finding may point to older code, but explain its causal relationship to the target change. Keep unrelated pre-existing issues out of current findings and do not opportunistically modify them.

Merge findings from multiple perspectives when they share a root cause and the same fix resolves them. Preserve the relevant requirements, standards, or correctness basis and consequences. The same file and line do not make distinct problems one issue; do not mechanically merge different root causes.

Sort confirmed defects and explicit standards violations together by actual impact. List maintenance suggestions separately and state their specific benefits and costs. Mark items requiring investigation with their unresolved premises and evidence gaps; do not treat them as confirmed blockers. Do not force a fixed number or length of findings, pad the report, or speculate to make it look comprehensive.

## Report Contents

Organize the report concisely according to its size:

1. The actual review target and scope, including repository, base, target revision, or workspace state when needed.
2. Verified findings: a brief conclusion, file location, basis or perspective, trigger, and consequence; sorted by impact.
3. Useful maintenance suggestions or items requiring investigation, separate from confirmed findings. Omit this section when there are none.
4. Checks performed or reused, their coverage, and any gaps such as checks not run, restrictions, or missing requirements.

If there are no findings, say plainly: "No confirmed issues were found within the reviewed scope." This does not guarantee there are no bugs, certify security, prove all requirements passed, or mean manual acceptance is complete. Without a requirements source, do not say requirements compliance passed. If there were no changes, state that the comparison found no diff; do not present it as a full review.

If two perspectives were delegated, first verify that both results concern the same target, then check their rationale and counterexamples. Do not paste the two reports together. State the scope of both perspectives and any parts that could not be judged.

## Fixes and Follow-up Actions

A review alone defaults to reporting findings. An explicit request to fix, or a delivery self-review within an implementation task, permits fixes for clear issues within existing authorization. If the current user request limits the work to read-only review, reporting first, or discussion, stay within that scope. A speculative finding does not directly justify a behavioral change. Ask the user to decide when behavior, scope, or a key trade-off must change; do not reconfirm existing decisions.

After fixing, inspect the diff, verify whether the original finding is resolved and whether new issues were introduced, and run relevant checks. Evidence from before the fix does not automatically apply to the changed content. Report accurately whether each item was fixed, still needs verification, or remains unresolved and why.

Long-term decisions and persistent documentation remain the responsibility of `decision-notes` and `maintenance-docs`, respectively; do not create a parallel reporting system. For authorized edits, follow project Git rules and current authorization: by default, show the checked work and ask whether this round is ready for a local commit; if this scope is already explicitly authorized, do not ask again. A review does not automatically authorize committing, pushing, opening a PR, or publishing, and cannot replace real-world execution or necessary manual acceptance.
