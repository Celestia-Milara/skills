# Implementation, Verification, and Delivery

Proceed according to settled behavior, scope, and applicable decisions. Handle ordinary engineering details autonomously; investigate or ask the user about unknowns that affect key trade-offs.

Add or adjust tests to verify behavior through stable, caller-observable interfaces, with an independent basis for expected results. For bug fixes, verify the original failure scenario. Preserve regression protection when automation is suitable and has ongoing value; do not mechanically add tests for every small change.

When test-first development is appropriate, use [tdd](../tdd/SKILL.md). That package owns detailed behavior testing and the red → green method; TDD and writing a plan are not prerequisites for every change.

Choose necessary checks based on affected paths and actual project configuration, and expand verification when evidence is insufficient. Run the application when integration, runtime, or platform evidence is needed. Report builds, tests, and real runtime checks separately. Accurately describe checks not run, failures, limitations, and pending manual acceptance; when manual acceptance is needed, give the user steps and observable outcomes.

Before review or delivery, self-review with [code-review](../code-review/SKILL.md) against the correct target and relevant requirements, project conventions, and correctness concerns. Review the intended scope, including staged and unstaged changes, new files, and commits; when a PR or commit is specified, do not automatically include worktree changes. Report supported findings, deduplicate findings with the same root cause, and distinguish maintenance suggestions from questions requiring investigation. The package owns the specific review method.

A review-only request defaults to reporting findings. When fixes are explicitly requested or self-review is part of an implementation task, address clear issues within authorization and run related verification. Respect a read-only or report-first constraint. Finishing a review does not mean the feature, actual runtime behavior, or required manual acceptance has passed.

Deliver this round's results mainly in conversation; put materials requiring ongoing maintenance in the repository. When current behavior or operating instructions change, update their owning documents and have other locations reference them. Keep related code, documentation, and notes together as a pending deliverable.

Before staging, committing, or performing another Git operation, follow [Git Commits and Collaboration](git.md). When integrating this guidance into a project, update skill links to their actual locations and have the project entry point provide navigation to actual check commands, environments, and rules.
