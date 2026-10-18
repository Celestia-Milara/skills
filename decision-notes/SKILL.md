---
name: decision-notes
description: "Search decision history before proposing solutions, settling behavior or key trade-offs, or changing related implementation or behavioral tests. Maintain lasting conclusions, rationale, and genuine alternatives; use for historical lookup, conflicts, supersession, and notes organization."
---

# Decision Notes

Distinguish clearly between user rejection, failed attempts, options not chosen after comparison, deferred items, and out-of-scope items. Do not treat them all as permanently infeasible.

Notes are not for unresolved proposals, complete requirements, implementation steps, task progress, or troubleshooting logs. Keep proposals and implementation plans in design and plan documents; maintain current behavior in the owning subsystem documentation and verify it against source code. Maintain long-term rationale in notes; summarize and link to it elsewhere.

## 1. Search Before Decisions and Changes

Before starting the following work, consult applicable project-level constraints, relevant subsystem documentation, and related notes:

- Propose a concrete solution, settle behavior, or make a key design trade-off.
- Change related implementation or behavioral tests; for cross-subsystem work, cover related interfaces and shared constraints.
- Create or change a decision record; first search for existing conclusions on the same topic.

When the user asks about history, a decision pointer is found, or a conflict appears, read the relevant record directly. Pure spelling, formatting, and status updates do not require a new search when they do not involve established constraints.

When locating or assessing history, read [Finding Applicable Decision History](references/retrieval.md). It covers project entry points, topic searches, archived records, applicability, and missing or inaccessible sources. Search by decision scope, not just matching filenames or existing links.

Within the same task, reuse results already verified and still applicable. Recheck affected parts when scope, a key premise, or a related record changes, or when a conflict appears. Do not rescan everything just because the turn or skill changed.

Proactively raise an old option again only when its premises have clearly changed, explaining why it was not chosen before, which conditions changed, and the impact. If the user explicitly changes an earlier decision, follow the new instruction without requesting approval again. General implementation authorization does not automatically cancel an existing rejection or scope restriction.

## 2. Decide Whether to Create a Record

A new record should meet all of these conditions:

1. **The conclusion is settled.** It has been adopted, rejected, deferred, or limited in scope, or there is a failed result and conditions worth retaining long term. Unresolved proposals and assumptions awaiting verification belong in design documents and plans.
2. **It has lasting value.** Without the rationale, a future Agent could raise an old option again, repeat a meaningful failed attempt, or accidentally change an important constraint. Merely restating current behavior does not meet this threshold.
3. **It needs a separate record.** Related history has been searched, and the information cannot be captured by updating facts, adding evidence, or clarifying scope. A genuine change of decision requires a new record under the supersession rules. Do not create records mechanically by date, delivery count, or number of alternatives.

Apply the threshold to ordinary fixes, formatting, renames, upgrades, troubleshooting, and progress too: they rarely need a new record merely to restate code or tests. Maintain affected existing records. If the user explicitly asks to preserve an important decision, reuse or create an appropriate source rather than silently discarding it.

## 3. Record Real Conclusions Promptly

Record an important conclusion promptly once it is clear; do not wait for completion, the end of a session, or commit approval. A decision may come from the user or from an Agent making a choice within delegated authority. Recording does not add an approval step, and a trade-off still awaiting the user's decision cannot be settled by writing a note.

Before writing, read [Format and Examples](references/format.md). The default location is `.agents/notes/YYYY-MM-DD-topic.md` in the target project; prefer an existing project location. Keep one decision topic per file and a stable path. Do not organize notes into directories by status or subsystem.

- Keep a title, `Status`, and `Scope`. Center the body on the conclusion and rationale and trade-offs; add other sections as needed. Body text defaults to English unless the project has a consistent language. Do not invent alternatives, require a fixed count, or force positive/negative consequence labels.
- State the scope and conditions of each conclusion. Do not describe an adopted but unimplemented goal as current implementation, migration, or deployment fact. Design and plan documents own implementation progress.
- If rationale is missing, say it was not provided or recorded. For a failure, retain its conditions, result, and necessary evidence or evidence gap; do not infer permanent infeasibility. Do not rely only on chat or temporary output that a later session cannot access.

## 4. Update, Supersede, and Organize

If facts, names, paths, or evidence change but the decision does not, update the existing record. Create a new record when a core choice or constraint clearly changes. Status describes applicability, not implementation progress or a candidate's feasibility; [Status and Supersession](references/lifecycle.md) owns the status definitions and transition rules. Reassess invalid evidence without automatically changing a decision.

Before changing status, superseding a decision, handling partial supersession, or restoring an old option, read [Status and Supersession](references/lifecycle.md). Cross-link old and new records by scope; preserve remaining constraints after partial supersession. If an old option is adopted again, create a new record rather than erasing the intervening decisions.

Before archiving, merging, or deleting, read [Retention and Organization](references/retention.md). Retain records by default. Logical archiving does not move paths; merging must not erase genuine changes of decision; before deletion, migrate unique information and update references. Organize only records affected by the current task; a full cleanup must be in scope.

## 5. Check Before Delivery

Check relevant records even when no new note was created:

- Preserve important lasting rationale without duplication or content left only in chat. Distinguish recommendations from decisions, goals from current facts, failures from rejections, unchosen options from prohibitions, and deferrals from commitments.
- Verify status, scope, conditions, and supersession chains against [Status and Supersession](references/lifecycle.md) when they change. Preserve remaining obligations and avoid conflicting effective conclusions, cycles, self-links, or broken links.
- Synchronize affected subsystem, design, plan, and notes sources without duplicating their owned content. After organization, check that unique evidence and meaningful historical references survived.
- Run relevant existing checks and inspect results, or review manually. Do not automatically add dependencies, scripts, CI, or format migrations; reuse applicable successful evidence. State unknown, inaccessible, and unverified information honestly.

Passing a format check does not prove that rationale is correct, retrieval is complete, or implementation follows the decision. If current facts conflict with a record, distinguish transition arrangements, stale documentation, incomplete implementation, and actual conflict. Correct verified errors. If a key judgment remains unclear, explain the conflict and ask for a decision; do not override a new user instruction or claim completion. Continue work that does not depend on the answer.

When adding, substantially updating, superseding, or organizing notes, briefly explain what changed, why, and any gaps, with links. Do not emit a fixed “no notes added” message when nothing relevant changed.

Keep code, related documentation, and notes together as one pending deliverable. Follow the project's Git rules and current authorization. By default, after completing checks and showing the results, ask whether this round is complete and ready for a local commit; continue editing if feedback arrives. If the user already explicitly authorized a commit for this scope, check and commit without asking again. Saving or validating notes adds no commit, push, PR, or publication authorization and does not require committing notes early.
