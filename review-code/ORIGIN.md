# Adaptation Notes

The user adopted the seven-part review design and requested a formal package. Runtime guidance is in [review-code/SKILL.md](../review-code/SKILL.md) and its package references. The custom entry is named `review-code` to avoid replacing Claude Code's bundled `/code-review`; the upstream name remains `code-review`. This file records source and adaptation rationale; the package does not depend on it. Other finalized skills are unchanged.

## Upstream Source

Fixed source: [code-review from mattpocock/skills@c55ee46073ed923f86ce59a5eb3b6d895095d1b7](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/code-review/SKILL.md).

The upstream explicitly specifies:

- Independent Standards and Spec review axes, so passing one cannot hide failure on the other.
- A user-provided fixed point and commit diff from merge-base to HEAD; if none is supplied, ask.
- If `docs/agents/issue-tracker.md` is absent, require the author's setup. Search for a spec using issue references in commits, the user's paths, and candidate directories; if there is no source, allow the Spec review to be omitted with an explanation.
- Fixed smell prompts under Standards, with project standards taking precedence; prompts are not hard violations. Skip items already covered by tools.
- Two parallel subagents, each limited to 400 words; report each axis separately, without merging or cross-axis ordering.
- A process ending with the summary report and no specified automatic fixes.

The original text and display metadata were read from fixed raw URLs. The upstream method does not prove model behavior is effective, nor does a same-named `code-review` in the current environment prove it is that version.

## Adopted Seven-Part Adaptation

1. **Responsibility.** Check omissions, partial implementation, incorrect behavior, and scope expansion from requirements and project-standard perspectives. Also investigate correctness relevant to the change: affected interfaces on both sides, failures, resources, concurrency, compatibility, and whether tests can distinguish behavior. Missing complete sources do not block correctness checks supported by evidence; do not expand into a full-project audit.
2. **Target.** Prefer a user-specified PR, commit, scope, or files. For current work, verify related commits, staged and unstaged changes, and untracked files from context; do not omit relevant work or mix in unrelated edits. Choose a comparison suited to the target rather than always using merge-base-to-HEAD. Do not ask for a base when it can be determined, or commit early.
3. **Sources.** Use current requirements and the project entry point to locate acceptance criteria, change designs, subsystem documentation, coding standards, and effective notes; use issue and commit text as clues. Remove author-setup dependencies. State what cannot be judged when sources are missing, but continue correctness review where evidence exists. Old implementation is not automatically the intended requirement; resolve conflicts rather than using old materials to overrule new instructions.
4. **Evidence.** Identify the specific location, basis, triggering conditions, and consequences. Static proof is sufficient when available; do not require dynamic reproduction. Do not substitute severe speculation for an unverified premise. Report defects introduced, worsened, or made current by the change; explain causation when the location is in older code, and separate unrelated legacy issues.
5. **Prompts and tools.** Smells are investigation leads, not violations. Prefer explicit project rules and recommend only changes with concrete value. Bind tool results to the actual object, scope, and output; configuration alone does not prove checks passed. Workspace changes at the same HEAD can still invalidate evidence; rerun relevant checks rather than the entire suite mechanically.
6. **Report.** Check both perspectives independently; after verification, merge items only when they share a root cause and fix, retaining the perspective and its basis. Do not combine different causes based on location. Order confirmed defects and explicit violations by impact; separate maintenance suggestions and open questions. Do not force a count or word limit. Distinguish no findings, checks passed, and requirement conformance.
7. **Authorization.** A standalone review defaults to reporting only. An explicit fix request or implementation self-review may address clear issues within existing authorization. Respect read-only or report-first limits; speculation does not trigger behavior changes. Ask the user about key decisions. Verify changes after fixing. A commit remains subject to current-round confirmation; review does not prove runtime execution or required manual acceptance.

Delegation depends on task, environment, and authorization; two Agents are not mandatory, and delegated reports must be verified rather than pasted directly.

## Package Result

The formal package contains the entry point, references for scope and sources, review criteria, findings and reporting, `ORIGIN`, the MIT LICENSE, and metadata. It retains Matt's attribution and fixed source and documents local changes. The package is self-contained and does not hard-code installation paths for other skills. The Agent template has a short trigger pointing to this package. Static and independent text-review results are recorded in `handoff`; the package has not been installed or behavior-tested with a model.
