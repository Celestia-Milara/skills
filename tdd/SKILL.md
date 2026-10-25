---
name: tdd
description: "Develop behavior through discriminating failing tests, minimal implementation, and small refactors. Use for requested test-first or red-green-refactor work, or when incremental failure feedback helps; not required for every change or integration-only verification."
---

# Test-Driven Development

## 1. Establish applicability and basis

Use TDD for requested test-first work or behavior that benefits from automated failure feedback. Do not mechanically add tests for small low-value changes or impose TDD on investigation and integration-only verification. Adding tests after implementation does not establish a test-first history.

Locate requirements, acceptance criteria, subsystem documentation, code, tests, and commands through the actual project entry point. Before proposing solutions, settling key trade-offs, or changing related implementation or behavioral tests, search applicable decision history. Reuse verified context and recheck affected areas when premises, sources, or scope change.

Use project terminology and constraints without requiring a plan, CONTEXT.md, another ADR system, or dedicated configuration. Retain documentation and long-term decisions in their owning sources. Use available companion skills, or read configured guidance through the host's mechanism; state inaccessible guidance and do not claim an unavailable invocation or load companions cyclically.

## 2. Choose a behavior and boundary

A **test boundary (seam)** is an interface through which a caller observes behavior: a module API, service entry, command, or UI. It need not be an end-to-end application.

Select a result from settled requirements and acceptance criteria. Identify its entry point, input, observable result or side effect, and conditions. Inspect callers, responsibilities, and historical constraints if the interface is unclear. Choose ordinary test locations and engineering seams autonomously; ask only about unsettled behavior, scope, or key interface trade-offs. Do not require another design skill or approval for every test.

Prioritize critical paths, complex logic, and the change's risks. Do not test everything or conceal behavior and scope changes in test preparation.

## 3. Design a discriminating test

When writing tests, read [Good and Bad Tests](tests.md) for stable boundaries, independent expected values, and valid failure evidence. When choosing test doubles or handling external dependencies and uncontrollable conditions, read [When to Mock](mocking.md).

Test observable contracts through stable interfaces. Derive expectations independently from requirements, verified examples, manual calculation, or reliable independent evidence. Do not reproduce the implementation's algorithm or copy current output into an expected constant. Avoid private-method and internal-call coupling unless the interaction itself is a contract. Do not expand production interfaces merely to inspect results.

Preserve real obligations such as idempotent side effects, event ordering, or persistence formats. Advance one behavior at a time rather than batching speculative tests before all implementation. Several assertions may jointly establish one behavior; do not split by assertion count.

## 4. Run red → green and refactor

1. **Red:** Write or reuse a test for the current behavior. Run it and confirm the input reaches the target and fails for the missing or incorrect behavior. Import failures, setup errors, unrelated crashes, skips, or empty matches are not a valid red; fix prerequisites first.
2. **Green:** Add only the implementation needed now. Run the test and verify it passes. Investigate failures without weakening assertions, skipping tests, or changing expectations without evidence.
3. **Continue:** Choose the next behavior from what was learned. One boundary, one behavioral result, and one small implementation step form a cycle.
4. **Refactor when useful and authorized:** Improve structure while green, preserving behavior and compatibility. Run relevant guard tests after changes; refactoring is neither mandatory each cycle nor restricted to a final stage. Return to the decision process for new behavioral trade-offs.

For a bug fix, test the original trigger before fixing and confirm it passes afterward. Where feasible, verify the test catches the unfixed logic for the original reason. Any temporary reversal must be isolated and preserve others' changes. If this evidence is unavailable or tests were added after the fix, state that limit instead of claiming test-first or verified regression coverage.

## 5. Verify and deliver

Select necessary tests, type checks, builds, and other checks for the actual changes and callers. Broaden only when impact, failures, or unknowns warrant it; reuse still-applicable evidence rather than rerunning the entire suite for every commit or confirmation.

Review this task's actual staged, unstaged, committed, and relevant untracked changes against requirements, constraints, and failures; do not review only HEAD. Use available review capabilities without assuming a similarly named skill is a particular upstream version or requiring a fixed agent count. Correct clear issues within implementation authorization; a standalone review request remains reporting-only by default.

Report implemented behavior, checks actually run, results, evidence scope, and gaps. Tests prove covered conditions; mocks do not verify real services, builds do not prove runtime behavior, and code changes do not complete manual acceptance. Obtain integration, runtime, or platform evidence when needed and state unrun, failed, constrained, or pending checks.

Synchronize affected documents and lasting decisions. Keep related work together. Follow project Git rules: show checked work and ask before committing unless this scope is already authorized. TDD adds no push, PR, or publication permission.
