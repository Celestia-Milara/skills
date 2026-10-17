---
name: to-docs
description: "Turn brainstorming, requirements discussions, or design interviews into human-readable design documents for review, revision, and future reference. Use when the user asks to preserve a design or organize discussion outcomes, or when a discussion produces design worth retaining. By default, use docs/designs/<topic>.md and prefer updating an existing source. Distinguish settled conclusions, recommendations, assumptions, and open questions. Do not implement automatically or require a plan; work with maintenance-docs to keep a single source of truth."
---

# To Docs

## 1. Determine the scope and sources

When the user explicitly asks, handle the specified topic. You may also use this skill proactively when a discussion has produced design worth retaining; do not ask for permission to save it each time. Do not mechanically create documents for brief Q&A or repeated content with no independent retention value.

First read existing designs and relevant project entry points, requirements and acceptance criteria, subsystem documentation, and long-term decisions. Reuse context that has been verified and still applies. Determine what this discussion should preserve and whether an existing source can hold it; prefer updating an existing source rather than creating a new document for every conversation.

- Faithfully organize what was actually discussed. Do not invent the user's reasons, adopted conclusions, implementation facts, or details that were never discussed.
- When facts can be investigated, verify them selectively and distinguish verified information from assumptions. If a key design conflict is unclear, identify it and ask the user to decide; continue organizing independent material.
- In-depth interviews remain the responsibility of `grilling`. Do not restart an interview or ask for confirmation of an existing decision just to write a document. If using that interview, follow its shared-understanding confirmation without turning every save into an approval step.
- Preserve unresolved items and facts that need recording as they arise. Record important, settled conclusions with long-term value under `decision-notes` promptly; do not wait until final wrap-up.

Use the skill name actually available in the environment. If it cannot be invoked, read the configured source instead; do not claim to have invoked an unavailable skill. Do not repeatedly load companion skills or rescan the same materials in a cycle.

## 2. Choose a location and keep one source of truth

By default, use `docs/designs/<topic>.md` with a clear, stable English kebab-case topic name. Reuse an existing suitable design source or directory when the project has one; do not require migration. Use a topic subdirectory only when multiple documents or images are genuinely needed. Do not pre-create empty directories or a complete file set.

A human-readable design can be the complete design source; there is no need to first write a copy under `.agents/` and then generate a summary. When requirements, acceptance criteria, shared standards, or detailed designs already have an authoritative source, summarize and link to it rather than copying the full text. Not every design needs a companion Agent document.

Follow `maintenance-docs` for source discovery, organization, verification, and ongoing consistency. These principles apply from the moment a design is saved; implementation does not need to have started. Use an engineering change directory, README, task list, or overall Status only when an engineering change record is actually needed. Do not impose these on human-readable designs. Human-readable designs do not need a separate mandatory state machine, and document maturity is not implementation progress.

## 3. Write a design people can evaluate

Read [Design Content and Expression](references/design-content.md) as needed. The document should help people judge whether the design meets their intent and help later Agents identify settled behavior and constraints.

- Use a clear title for the topic and explain why it matters, the goal and scope, key scenarios, and expected behavior.
- Organize the discussed solution, key mechanisms and interface relationships, necessary constraints, acceptance basis, and unresolved questions. Choose depth based on the topic; do not require every section.
- Clearly distinguish settled content, recommendations not yet decided, assumptions, and questions to verify. Finishing the document does not mean every proposal in it is approved; adopting a goal does not mean it has been implemented.
- For visual or interaction design, provide concrete scenarios, examples, sketches, existing components, or style sources as needed. Avoid relying only on vague words such as “modern,” “simple,” or “consistent.” Label examples and explorations so they are not mistaken for confirmed decisions or evidence from a real running system.
- Keep styles unique to this design here. Maintain established cross-feature standards in an appropriate shared source and have designs link to it. Do not require a `design-system.md` without a real need.
- Briefly explain the rationale needed to understand the design. `decision-notes` owns complete long-term rationale, rejected alternatives, and evidence that meet its retention threshold; link to it elsewhere. Unresolved comparisons can remain in the design.

Do not transcribe Q&A turn by turn. Do not default to a code-change checklist, test commands, or execution progress, and do not prewrite a complete plan just to make the design “implementable.” A design can be saved with open questions; identify important gaps honestly.

## 4. Support implementation and ongoing maintenance

When the user references a design and explicitly asks for implementation, verify that it still applies against current source code, project constraints, and relevant notes. Carry forward applicable settled goals, behavior, style, and trade-offs without reopening decisions. Keep recommendations and unresolved items in their existing status. Investigate conflicts that affect implementation or ask the user to decide, while continuing authorized independent work.

An Agent working on an existing task may locate relevant designs without waiting for the user to cite them explicitly. Creating, reading, or merely referencing a design does not add implementation authorization; authorization already granted for the task remains in effect. If the request is only for discussion or design, stay within that scope.

As needed, add engineering approaches, dependencies, verification arrangements, and progress to `.agents/changes/`, referencing the human-readable design rather than copying it in full. After implementation, update affected subsystem descriptions to reflect verified current behavior. When the design changes, update its original source; do not silently overwrite a still-valid human-readable design with an engineering record. Maintain major changes of decision and their historical rationale under `decision-notes`.

## 5. Review and deliver

Review the relevant scope for this task: does the design reflect the actual discussion; are settled and unresolved content, current state, and goals distinguished; are key scenarios and constraints understandable; can sources and materials be found; does each style reference point to the right source; and have duplicate text, unsupported decisions, or unsubstantiated verification claims been introduced?

Use existing, applicable documentation checks to verify links and structure. If no tool is available, review manually. Do not add a toolchain, product tests, or code changes just to save a design. When organizing or maintaining related documents, follow `maintenance-docs` without expanding the review into a repository-wide audit.

Deliver the saved location, main content, and key gaps with a brief explanation and links to the actual files. Update the same source when feedback arrives. Saving a design does not add approval, mean every proposal is approved, prove a feature is complete or verified, or authorize a commit or release. Follow the project's existing commit-confirmation rules; do not commit, push, open a PR, or publish automatically just because a design was written.