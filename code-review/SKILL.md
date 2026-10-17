---
name: code-review
description: "Review changes against requirements, project standards, and relevant correctness concerns, including related interfaces and failure scenarios. Use when the user requests a review or when reviewing the actual changes before delivery. Identify the correct target and source material, verify findings with evidence, distinguish defects from maintenance suggestions and open questions, and report by impact. A review alone defaults to reporting findings; it does not authorize fixes, commits, or broader audit."
---

# Code Review

## 1. Confirm Authority and Purpose

- Review is read-only by default. A review request authorizes investigation and reporting, not code edits, commits, pushes, PR actions, or release.
- When reviewing your own implementation as part of an already-authorized task, address clear issues within that task's scope and verify the resulting changes. For a standalone review, report only unless the user authorizes fixes.
- Do not make behavior or scope decisions for the user. Investigate, explain material alternatives and consequences, and ask when a key choice remains unclear.
- Use the skills and tools actually available in the environment. A capability's name alone does not establish that it is installed or available.

## 2. Identify the Review Target

Start with the user's specified PR, commit, range, files, or review scope. Otherwise, inspect repository status, branch and base information, recent relevant history, the index, and working-tree changes to identify the current task's changes. Include relevant untracked files and local modifications; do not limit an implementation review to HEAD or silently mix unrelated changes into it.

Choose a comparison suited to the request: PR diff against its base, specified commits or range, a focused file change, or the authorized set of staged, unstaged, committed, and untracked files. Do not always use merge-base-to-HEAD. If the target can be determined from the task and repository, do not ask merely for a base ref. If it cannot be established, state the ambiguity and ask a focused question.

If the target is empty, say so; an empty diff is not evidence of code quality. If the target changes during review, update the scope and recheck affected findings. Do not create a commit just to make review possible.

## 3. Locate Requirements and Sources

Follow the project's actual Agent entry point to relevant requirements, acceptance criteria, change designs, subsystem documentation, coding standards, and effective decision notes. Use issue or commit text as a clue, not as the sole authority for intent. Verify related source and tests for the changed paths and behavior. If a required source is absent, state which conclusions cannot be checked while continuing to assess correctness that has evidence.

When documentation and implementation conflict, investigate the discrepancy. Existing code does not automatically define the requirement, and old documentation does not overrule a new user instruction. See [Review Scope and Sources](references/scope-and-sources.md).

## 4. Review from Independent Perspectives

Check requirements and project standards for omissions, partial implementations, incorrect behavior, and scope expansion. Separately investigate correctness risks related to the actual change, including affected callers and interfaces, failure cases, resources, concurrency, compatibility, and whether tests can distinguish the intended behavior from a faulty implementation.

Neither perspective replaces the other. Missing complete requirements do not excuse skipping correctness analysis supported by evidence; finding no bug does not prove requirements were met.

Apply only relevant rules. Treat maintainability smells as leads to investigate, not automatic violations. Prefer explicit project standards. Suggest a cleanup only when it has a concrete benefit and acceptable cost. See [Review Criteria](references/review-criteria.md).

## 5. Verify Findings and Evidence

For each candidate, establish the relevant location, rule or contract, triggering input/state/event, and concrete impact. Check reachability, caller guarantees, error handling, version scope, applicable decisions, and counterexamples. Static reasoning is enough when it proves the issue; dynamic reproduction is not mandatory. Do not elevate a speculative premise to a confirmed defect because its possible impact sounds severe.

Report issues introduced, worsened, or made current by the target change. A finding may point to existing code if the causal relationship is clear. Keep unrelated pre-existing problems separate; do not mix them into the findings or fix them as part of a review without authorization.

## 6. Report Clearly and by Impact

Verify and deduplicate findings before reporting. Merge items only when they share the same root cause and fix; retain the relevant requirement, standard, or correctness basis. Report confirmed defects and explicit standard violations together, ordered by actual impact. Put maintenance suggestions and questions needing investigation in separate sections, with concrete benefit, cost, or unresolved assumptions. See [Findings and Reporting](references/findings-and-report.md).

State the review target and scope, findings with locations and triggering scenarios, checks run or reused and their coverage, and any missing sources or limitations. If there are no findings, say there were none in the examined scope; do not claim there are no bugs, that all requirements passed, or that manual acceptance is complete. If no target changes exist, say there is no difference under the stated comparison.

If review perspectives are delegated, first confirm that they assessed the same target. Verify their evidence, look for counterexamples, deduplicate the results, and report each perspective's coverage and undecidable areas. Do not paste subreports without checking them.

## 7. Fixes and Follow-up

A standalone review defaults to reporting only. In an implementation task, or after an explicit fix request, handle concrete findings within existing authorization. If the user requested read-only review, reporting first, or discussion, stay within that boundary. Speculation does not authorize a behavior change. Ask the user about changes to behavior, scope, or a key trade-off; do not reconfirm established decisions.

After a fix, inspect the new diff, verify that the finding is resolved and no new issue was introduced, and run relevant checks. Pre-fix evidence does not prove the fixed version. Report accurately what was fixed, remains unverified, or was left untouched and why.

Long-term decisions and ongoing documentation remain owned by `decision-notes` and `maintenance-docs`; do not create a parallel full reporting policy. Follow the project's confirmation rules before committing. Do not automatically commit, push, open a PR, or release. A completed review does not prove real runtime behavior or required manual acceptance.
