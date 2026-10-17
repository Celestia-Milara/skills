---
name: decision-notes
description: "Search and maintain long-term decision memory to prevent old proposals from being raised again, repeated failed attempts, or loss of non-obvious constraints. Use before proposing a concrete solution, deciding behavior or key trade-offs, changing related implementation or behavioral tests, and writing decision records; also use to look up historical decisions, resolve conflicts, supersede decisions, or organize notes. Coordinate with subsystem documentation and record settled conclusions, rationale, scope, and genuine alternatives that were not chosen."
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

Locate and assess records in this order:

1. Use the project's Agent entry point to find the actual notes location and applicable global constraints. Use subsystem documentation to locate current responsibilities, contracts, source code, tests, and related notes. A subsystem may span packages or repositories, and one note may relate to multiple subsystems.
2. Follow links, then search by question, mechanism, solution name, and constraint as needed. The absence of a link, corresponding code, or matching name does not prove that there is no relevant history. If no subsystem page exists, locate relevant context from available materials and the task topic; do not create an empty document in advance.
3. Start with the title, `Status`, `Scope`, and conclusion; read rationale, alternatives, and evidence when relevant. Prefer currently effective records, then trace history according to relevance. Search archived records directly when reconsidering an old option or when current guidance is insufficient. Trace supersession according to the scope in question; do not follow an arbitrary chain to its end.
4. Confirm the record's applicability and current facts. If the directory truly does not exist, continue; create it only when a record is first needed. A failed read or search with no matches does not prove there is no history.

Within the same task, reuse results already verified and still applicable. Recheck affected parts when scope, a key premise, or a related record changes, or when a conflict appears. Do not rescan everything just because the turn or skill changed.

Proactively raise an old option again only when its premises have clearly changed, explaining why it was not chosen before, which conditions changed, and the impact. If the user explicitly changes an earlier decision, follow the new instruction without requesting approval again. General implementation authorization does not automatically cancel an existing rejection or scope restriction.

## 2. Decide Whether to Create a Record

A new record should meet all of these conditions:

1. **The conclusion is settled.** It has been adopted, rejected, deferred, or limited in scope, or there is a failed result and conditions worth retaining long term. Unresolved proposals and assumptions awaiting verification belong in design documents and plans.
2. **It has lasting value.** Without the rationale, a future Agent could raise an old option again, repeat a meaningful failed attempt, or accidentally change an important constraint. Merely restating current behavior does not meet this threshold.
3. **It needs a separate record.** Related history has been searched, and the information cannot be captured by updating facts, adding evidence, or clarifying scope. A genuine change of decision requires a new record under the supersession rules. Do not create records mechanically by date, delivery count, or number of alternatives.

Typical subjects include non-obvious subsystem boundaries, interfaces, or persistence and compatibility choices; important selections and reasons for not choosing alternatives; reasons for deliberately avoiding caching or automatic retries; significant rejections or deferrals that might be raised again; and evidence-backed long-term failure conclusions or cross-task policies.

Usually, do not create notes for formatting, mechanical renames, ordinary implementation or fixes understandable from code and tests, routine dependency upgrades, general troubleshooting attempts, logs, TODOs, or progress. Size is not the criterion. Maintain an existing note if the work makes it inaccurate, and record a new decision if the work produces one that meets the threshold.

If there is no distinct long-term value to preserve, do not create a record just to fill a template. If the user explicitly asks to preserve an important decision, reuse or create an appropriate source; do not silently discard it.

## 3. Record Real Conclusions Promptly

Record an important conclusion promptly once it is clear; do not wait for completion, the end of a session, or commit approval. A decision may come from the user or from an Agent making a choice within delegated authority. Recording does not add an approval step, and a trade-off still awaiting the user's decision cannot be settled by writing a note.

Before writing, read [Format and Examples](references/format.md). The default location is `.agents/notes/YYYY-MM-DD-topic.md` in the target project; prefer an existing project location. Keep one decision topic per file and a stable path. Do not organize notes into directories by status or subsystem.

- Keep a title, `Status`, and `Scope`. Center the body on the conclusion and rationale and trade-offs; add other sections as needed. Body text defaults to English unless the project has a consistent language. Do not invent alternatives, require a fixed count, or force positive/negative consequence labels.
- State the scope and conditions of each conclusion. Do not describe an adopted but unimplemented goal as current implementation, migration, or deployment fact. Design and plan documents own implementation progress.
- If rationale is missing, say it was not provided or recorded. For a failure, retain its conditions, result, and necessary evidence or evidence gap; do not infer permanent infeasibility. Do not rely only on chat or temporary output that a later session cannot access.

## 4. Update, Supersede, and Organize

| Status | Meaning |
| --- | --- |
| `active` | Explicitly adopted and still applicable within its stated scope; valid rejections and deferrals also use this status |
| `superseded` | The entire scope has been replaced by one or more new decisions |
| `retired` | Nothing remains in effect, and no new decision fully takes it over |

Status does not indicate implementation progress or disposition of a candidate solution. If facts, names, paths, or evidence change but the decision does not, update the existing record. Create a new record when a core choice or constraint clearly changes. Reassess when evidence becomes invalid; do not change the decision automatically.

Before changing status, superseding a decision, handling partial supersession, or restoring an old option, read [Status and Supersession](references/lifecycle.md). Cross-link old and new records by scope; preserve remaining constraints after partial supersession. If an old option is adopted again, create a new record rather than erasing the intervening decisions.

Before archiving, merging, or deleting, read [Retention and Organization](references/retention.md). Retain records by default. Logical archiving does not move paths; merging must not erase genuine changes of decision; before deletion, migrate unique information and update references. Organize only records affected by the current task; a full cleanup must be in scope.

## 5. Check Before Delivery

Check records and related scope relevant to this work. Even if no new note was created, check whether the changes made an existing note inaccurate.

1. **Omissions and duplication:** Have important conclusions and long-term rationale been saved? Are they only in conversation? Is an existing record already sufficient?
2. **Truth and evidence:** Do not present a recommendation as a decision, a goal as current state, a failure as permanent rejection, an unchosen option as forbidden, or a deferral as an implementation commitment. State unknown, unprovided, and unverified information accurately.
3. **Status and scope:** Are scope and conditions accurate? Does partial supersession retain remaining obligations? Are there conflicting effective conclusions for the same scope and conditions? Does archiving hide a current constraint?
4. **Document ownership:** Update affected subsystem documentation, designs, plans, and notes; each source owns its information, and other locations link to it.
5. **Links and supersession chain:** Can necessary sources be located? Can conclusions be traced by scope without self-links, broken links, or cycles? Did organization preserve unique rationale, evidence, and meaningful historical references?
6. **Verification:** Run relevant checks already available in the project and review their results. If none are configured, check manually. Do not automatically add dependencies, scripts, CI, or format migrations. Correct real problems found; do not fabricate content. Reuse successful results when the relevant content has not changed.

Passing a format check does not prove that rationale is correct, retrieval is complete, or implementation follows the decision. If current facts conflict with a record, distinguish transition arrangements, stale documentation, incomplete implementation, and actual conflict. Correct verified errors. If a key judgment remains unclear, explain the conflict and ask for a decision; do not override a new user instruction or claim completion. Continue work that does not depend on the answer.

When adding, substantially updating, superseding, or organizing notes, briefly explain what changed, why, and any gaps, with links. Do not emit a fixed “no notes added” message when nothing relevant changed.

Keep code, related documentation, and notes together as one pending deliverable. After completing this round's changes and checks and showing the results, ask whether the work is complete and whether a local commit may be created. If the user gives more feedback, continue editing. Saving or validating notes does not authorize a commit, push, or publication, and does not require committing notes early.
