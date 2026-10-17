---
name: tdd
description: "Test-driven development: Use when the user requests test-first or red-green-refactor, or when the current work is well served by incremental implementation driven by a failing behavioral test. Advance through red → green with observable interfaces, independent expected values, and discriminating failures; refactor in small steps as needed. Do not force every change into test-first development, add approval steps for ordinary test boundaries, or require a plan first."
---

# Test-Driven Development

## 1. Decide whether TDD applies and locate the basis

Use TDD when the user explicitly requests test-first work, or when behavior can be expressed in automated tests and failure feedback will help with the implementation. Ordinary investigation, implementation, and verification remain core Agent capabilities; do not require TDD for every task or mechanically add tests for low-value small changes. If the request is only for integration verification, do not force a test-first process. Adding tests to existing implementation does not count as a complete red → green history.

Use the project's actual Agent entry point to locate requirements and acceptance criteria, relevant subsystem documentation, source code, tests, and commands. Before proposing a solution, settling a key trade-off, or changing related implementation or behavioral tests, use `decision-notes` to look for applicable decisions. Reuse context already verified and still applicable. Recheck affected areas when the scope, premises, sources, or conflicts change; do not rescan everything just because this skill was invoked.

Use the project's terminology and applicable decisions. Do not require a new CONTEXT.md, another ADR system, a plan, or dedicated configuration. When information needs to persist, follow `maintenance-docs` rather than copying its directory, status, or lifecycle scheme. Use skill names actually available in the environment; do not claim to invoke an unavailable skill.

## 2. Choose behavior and test boundaries

A **test boundary (seam)** is the point where a caller can observe behavior through an interface. A public interface can be a module API, service entry point, command, or UI; it is not limited to end-to-end UI.

- Select the result to protect from settled behavior and acceptance criteria. Identify a callable entry point, input, observable output or side effect, and necessary conditions.
- Choose ordinary test locations based on the existing structure without asking the user to approve every boundary or test. Investigate and ask only when the choice involves unclear behavior, scope, or a key interface trade-off; do not reconfirm existing decisions.
- If the interface shape is unclear, inspect actual callers, module responsibilities, and long-term constraints, then make a concrete recommendation. Do not require another domain-modeling or design skill, or a complete plan before starting investigation.
- Prioritize critical paths, complex logic, and this change's risks. Do not test everything. Handle pure engineering changes to expose interfaces within existing authorization; do not hide behavior or scope changes in test preparation.

## 3. Write tests worth keeping

Test behavior through stable interfaces visible to callers. Base expectations on requirements, known examples, manual derivation, or other independent reliable evidence. Tests should act as behavioral specifications and should not need frequent changes when internal structure is refactored without changing the contract.

When writing tests, read the positive and negative examples in [tests.md](tests.md). For test doubles, external dependencies, or uncontrollable conditions, read [mocking.md](mocking.md).

Avoid three anti-patterns:

- **Implementation coupling:** testing only private methods, mocking internal collaborators, checking call counts or ordering outside the contract, or bypassing the boundary under test to observe results.
- **Circular reasoning:** recalculating expected results with the same algorithm as the implementation, asserting a value equals itself, or deriving a baseline from current output without independent verification. The test and implementation could share the same error.
- **Cross-cutting batches:** writing a complete set of speculative tests first, then implementing all behavior at once. Advance one behavior at a time so each round can incorporate real feedback.

When side effects, call order, or storage formats are themselves part of the contract, test those obligations directly. Do not omit a real obligation to comply with “public interface only,” or expand the product interface just to make testing easier. Exceptions should have a concrete basis.

## 4. One result at a time: red → green

1. **Red.** Write a test for one current behavior, run it, and confirm that it fails because of the target behavior. Import errors, missing environment setup, or unrelated crashes are not a valid red; resolve test prerequisites first. Reuse an existing failing test that already catches the behavior instead of duplicating it.
2. **Green.** Add only the implementation needed for this behavior; do not prebuild future functionality. Run the test and confirm it passes. If it fails, adjust based on evidence rather than weakening assertions, skipping the test, or changing expectations without support.
3. **Continue or refactor.** One boundary, one behavioral test, and one small implementation step form a cycle. Choose the next behavior based on what was learned. A behavior may need multiple assertions that jointly establish the result; do not split mechanically by assertion count.
4. **Small refactors.** When useful and already authorized, improve structure while green, preserving behavior and compatibility constraints. Run the relevant guard tests each time. Refactoring need not wait for a single review stage, and is not required every cycle. If a new behavior trade-off emerges, return to the relevant decision process.

For a bug fix, first make a test catch the original failure scenario, then fix it and confirm it passes. When relevant and feasible, verify the test fails against the unfixed logic because of the original defect. If temporarily reverting a fix is needed to verify this, isolate that operation and do not overwrite others' changes; explain the evidence limitation if safe verification is not possible. If a test is added after the code already works and its failure was not verified, say so rather than claiming test-first completion.

## 5. Verify, review, and deliver

Use fast, relevant feedback during the cycle. Before delivery, select applicable and necessary tests, type checks, builds, or other checks based on the actual changes, callers, and project configuration. Expand coverage when impact, failures, or unknowns show that local checks are insufficient. Do not require a complete test suite every time, or mechanically rerun unaffected checks because a commit is pending or confirmation is awaited.

Passing tests prove only the conditions they cover. Obtain integration, real-runtime, or platform evidence when needed. A successful build does not prove the program ran correctly; passing with mocks does not verify an external service. Report what was not run, failed, constrained, or left for manual verification. Do not infer verification merely from the existence of tests.

Before delivery, review the actual changes in this round against requirements, project constraints, and relevant failure scenarios. Include relevant staged, unstaged, and committed changes in scope; do not inspect only HEAD. Use review capabilities available in the environment. Do not assume the installed `review-code` skill is the upstream `code-review` version, and do not require a fixed number of sub-agents. Fix clear issues within existing authorization and add relevant verification. A review-only request does not expand authorization to modify.

Briefly report behavior implemented, checks actually run and their results, evidence scope, and remaining gaps. Synchronize documents and long-term decisions according to their own rules. Keep the project's commit-confirmation process: complete, verify, and show the work before asking about a commit. Do not commit after each red → green cycle or automatically commit, push, open a PR, or publish.