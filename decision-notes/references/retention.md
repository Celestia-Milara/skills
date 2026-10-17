# Retention, Archiving, Merging, and Deletion

Retain notes by default and organize them according to their future decision value, not their age, length, count, or a cleanup quota. Deferral, lack of implementation, recent inactivity, or no current use are not reasons to delete. Valid rejections and compatibility constraints remain `active` while they apply.

Organize only duplicates, supersessions, or removed subjects directly affected by the current work. A full cleanup must be in scope; do not scan the entire library for cleanup during every delivery.

## Logical Archiving

Consider archiving only records with `superseded` or `retired` status that also meet all of these conditions:

- They have no effective conclusion, transition, or compatibility obligation.
- Reasons for not choosing an option, failure evidence, and reconsideration conditions are no longer the primary current safeguards; any information still needed has a clear current home.
- Current documentation and notes point to the right effective sources and do not depend on reading the old record to discover a missed constraint.
- The record still has historical explanatory value.

Keep the original path, original record date, and Status. Add `Archived: YYYY-MM-DD`, using the actual date, and briefly state the reason for archiving and any necessary links to current records. Do not add an `archived` status or create archive directories.

In routine searches, prefer active records, then consult unarchived history by relevance. Search archived records by topic when tracing evidence, following old links, reconsidering an option, or when current guidance is insufficient. Do not hide all archived records from tool searches or assume that archiving means no history exists.

After archiving, do not keep rewriting the body to follow the current implementation. Corrections supported by evidence, clarification of historical identity, and link repairs are allowed; do not introduce permanent freezing or hash inventories. If the record again needs to serve as routine guidance, the `Archived` marker may be removed, but `superseded` or `retired` does not automatically become `active`. For genuine re-adoption, create a new record under [Status and Supersession](lifecycle.md).

## Merge Records for the Same Decision

Duplicate records of the same decision or rationale scattered across duplicate files may be consolidated into one source of record. Prefer a stable, suitably scoped record rather than creating a new one without reason.

Before merging, migrate each piece of unique information that matters: conclusion and scope, premises, genuine alternatives and reasons for not choosing them, failure conditions and evidence, important trade-offs, reconsideration conditions, and unresolved verification limits. Preserve their conditions and historical context.

Preserve the identities and supersession relationships of genuine changes of decision; do not dismiss them as duplicate cleanup. Similarly, do not merge records merely because their topics are related if their constraints or scopes differ, or one only partially supersedes the other. Reasons still needed may be moved to the current source, but the old record must independently meet the conditions for archiving or deletion.

A redundant file may be removed if its references have been fully migrated and it has no independent historical identity worth preserving. If necessary history or external references cannot be migrated completely, leave a short pointer at the original path linking to the sole source of record and stating that it was a duplicate merged. A pointer to a duplicated effective decision may use `superseded`; do not fabricate renewed validity for history that was already `retired`.

After merging, check scopes, chronology, and supersession chains. Do not create broken links, self-links, or cycles, or make contradictory decisions from different periods appear to have always been the same.

## Deletion Conditions

All of the following must be true:

1. The record is an empty template, an accidental record, a redundant copy after a complete merge, or a record whose subject and obligations have disappeared and which no longer has independent historical, misuse-prevention, or reintroduction value.
2. Valuable unique conclusions, rationale, alternatives, conditions, evidence, and verification limitations have appropriate homes; Git history is not the only copy.
3. References in subsystem documentation, source pointers, designs and plans, other notes, and supersession chains have been migrated or explicitly removed. If a meaningful reference cannot be repaired, leave a short pointer at the original path.

Removing a feature does not automatically meet the deletion conditions. Why it was removed, why alternatives were not chosen, and conditions for restoration may still be valuable and could be carried by the removal decision.

Do not delete because a new approach seems better, the note is inconvenient to maintain, there is no corresponding code, it has not been read for a long time, or Git can restore it. If the unique value or meaning of a reference is uncertain, keep the record and state what is unclear.

## After Organizing

Check unique information, status scope, links, and chains, and briefly explain what was organized and why. Run existing project checks when applicable; otherwise review manually. Do not add a toolchain automatically.

Archiving, merging, and deletion do not authorize a commit; continue to follow the user's confirmation rules for this round's delivery.
