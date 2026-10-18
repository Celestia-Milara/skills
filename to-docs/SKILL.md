---
name: to-docs
description: "Turn brainstorming, requirements discussions, and design interviews into readable designs for review and later reference. Use when asked to preserve a design or when a discussion yields design worth retaining; saving it does not authorize implementation."
---

# To Docs

## 1. Establish scope and sources

Handle the requested topic, or proactively preserve a discussion with independent design value. Do not document brief Q&A or repeated content mechanically. Read relevant existing designs, project entry points, requirements, acceptance criteria, subsystem documentation, and decisions; reuse verified context and prefer updating a suitable source.

Organize what was actually discussed. Verify discoverable facts selectively; distinguish settled conclusions, recommendations, assumptions, and open questions. Do not invent user rationale, decisions, or implementation facts. Ask about unresolved key conflicts while saving independent material.

Use `grilling` for an in-depth interview without restarting settled questions. Its shared-understanding confirmation applies before implementing the resulting design, not before saving settled content and open items. Promptly preserve settled rationale through `decision-notes` when it meets the long-term retention threshold.

Use companion skills when available; otherwise read their configured guidance through the host's supported mechanism. If required guidance is inaccessible, state the gap and continue independent work. Do not claim an unavailable invocation, repeatedly load companions, or introduce circular calls.

## 2. Choose one owning source

Default to `docs/designs/<topic>.md` with a stable English kebab-case topic. Prefer existing project locations without migration. Use a topic directory only for genuinely separate documents or images; do not pre-create empty directories or a complete file set.

A readable design may be the complete source. Link to existing requirements, acceptance criteria, shared standards, and detailed sources rather than copying them or first creating an Agent version. Not every design needs companion engineering documentation, a README, a plan, or an overall Status. Document maturity is distinct from implementation progress.

Maintain specific styles with the design; link to established cross-feature standards in their owning source. Do not require a new design system. Use `maintenance-docs` when source organization or ongoing engineering records need attention, preserving these ownership boundaries even before implementation starts.

## 3. Write a design people can evaluate

When drafting or substantially revising a design, read [Design Content and Expression](references/design-content.md) for content choices, examples, and handling later feedback.

Explain the problem, goal, scope, key scenarios, expected behavior, relevant mechanisms and interfaces, constraints, acceptance basis, and unresolved questions at the depth this topic needs. No fixed section template is required. Make visual and interaction choices concrete with scenarios, components, sketches, or style sources; label explorations and examples accurately.

Include concise rationale needed to understand the design. Link to complete long-term rationale and rejected alternatives only when they meet the notes retention threshold; unresolved comparisons remain here. Do not transcribe Q&A, replace behavior with a code-change checklist, or require a complete implementation plan. A design may be saved with honest gaps.

## 4. Support later implementation

Reading, writing, or referencing a design adds no implementation authorization. Carry forward existing task authorization; a discussion-only request stays within discussion. Before authorized implementation, verify the actual design against current code, constraints, and related decisions. Preserve settled behavior and style without reopening them, and keep recommendations unresolved until decided. Investigate material conflicts or ask for a decision while continuing independent work.

Add engineering approaches, dependencies, verification, and progress to `.agents/changes/` only when continuity needs them, referencing the design. Update affected subsystem documentation after verified implementation. Revise the original design when it changes; do not silently replace it with an engineering record. Preserve genuine long-term changes of decision under `decision-notes`.

## 5. Check and deliver

Check fidelity to the discussion, distinction between goals and current facts, key scenarios and constraints, source links, style ownership, duplication, and unsupported conclusions. Run applicable existing documentation checks, or review manually; saving a design does not justify adding a toolchain, product tests, or code changes. Keep review within the task.

Deliver the actual saved location, main content, and key gaps with links; apply feedback to the same source. Saving does not approve every proposal, prove completion or verification, or authorize external operations. Follow project Git rules and current authorization. Without explicit commit authorization for this scope, show the checked work and ask whether the round is ready for a local commit; do not repeat an authorization already given. Saving alone authorizes no push, PR, or publication.
