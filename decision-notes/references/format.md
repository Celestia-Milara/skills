# Notes Format and Examples

## Location and Naming

By default, store notes flat in the target project's `.agents/notes/`. Prefer an existing decision-record directory and identify its location in the project's Agent entry point. Create the directory only when there is something to record.

Name files `YYYY-MM-DD-topic.md`: use the actual date the record is first created, and an English kebab-case topic describing the decision, question, or mechanism. Titles and body text default to English unless the project has a consistent language. Status or subsystem renames do not change the path or original record date.

Keep one decision topic per file; it may involve multiple subsystems. Put alternatives genuinely considered and the reasons they were not chosen in the same record; do not create a file for each alternative. Search for duplicates before creating. Handle existing topics under the update and supersession rules. If a genuinely separate decision needs the same date and name, add a meaningful topic term rather than overwriting the existing file. When parallel duplicate records are found, compare their contents rather than overwriting one to make the conflict disappear.

## Fields and Body

| Content | Requirement |
| --- | --- |
| Title | Identify the topic or central conclusion |
| `Status` | `active`, `superseded`, or `retired`; expresses decision validity, not implementation state |
| `Scope` | Use `project-wide` for global decisions; otherwise describe the responsibility area and link to relevant subsystem documentation. List multiple subsystems when applicable. If no page exists yet, describe the question or mechanism instead of creating an empty page. Source paths are supplementary; glob patterns are not required |
| Conclusion | State the choice, scope, and conditions; distinguish an adopted goal from an implementation fact |
| Rationale and trade-offs | Actual constraints, rationale, and important costs; genuine alternatives not chosen and why |
| Reconsideration conditions | Record when these are established, especially conditional rejections and deferrals; do not invent thresholds or conditions |
| Evidence and related sources | Include reproduction conditions, results, limitations, and links to related designs, plans, source code, or tests as needed |

The conclusion and rationale/trade-offs are core sections. Add others as needed; omit empty sections. Do not require a fixed number of alternatives, `Positive`/`Negative` labels, or a particular length. Omit alternatives when none were genuinely considered; no separate note is required merely to link to.

Clearly distinguish user rejection, failed attempts, options not chosen after comparison, deferral, and out-of-scope items. These can coexist; do not force a single choice among four categories. Preserve the conditions and evidence of a failure; it does not automatically become a permanent rejection. An option not chosen after comparison is not forbidden, and a deferral is not an implementation commitment.

If the user did not provide a reason, say so instead of inventing a technical rationale. State when evidence is inaccessible or results are unverified. Do not rely only on links to temporary output that may expire; retain reproduction conditions and results sufficient for future judgment without copying full logs.

Use `Supersedes` and `Superseded-By` only when a supersession relationship exists; see [Status and Supersession](lifecycle.md). Use `Archived` only when archiving; see [Retention and Organization](retention.md).

## Example

The decision, date, and path below are format examples, not actual project constraints.

File: `.agents/notes/2026-10-17-config-sync-strategy.md`

```markdown
# Merge Configuration During Sync; Defer Full Replacement in the First Release

Status: active
Scope: [Configuration Sync](../subsystems/config-sync.md)

## Conclusion

The first release of configuration sync preserves settings unique to other devices and does not provide a full-replacement operation.

## Rationale and Trade-offs

Multiple devices may maintain different settings; full replacement could delete content that is still needed on another device.
Merging means conflict resolution rules need to be defined.

- **Full replacement: deferred.** There is currently no validated recovery path for accidental overwrites.
- **Confirm each difference: considered and not chosen.** It would add interaction cost to the current automatic sync flow.

## Reconsideration Conditions

If the requirement changes to allow manual confirmation, and recovery has been validated,
the full-replacement option can be reconsidered against the original constraints in this record.
```

This example uses the default `.agents/subsystems/` layout. If the project instead uses `docs/subsystems/`, the Scope target from this note is `../../docs/subsystems/config-sync.md`. Calculate and verify paths from the actual note location. The subsystem page links to the rationale source rather than copying it.
