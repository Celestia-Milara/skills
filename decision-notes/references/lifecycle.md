# Status, Updates, and Supersession

## Status and Applicability

| Status | Meaning |
| --- | --- |
| `active` | Explicitly adopted and still applicable within its stated scope; valid rejections, deferrals, and scope restrictions are also active |
| `superseded` | The entire scope of the original decision has been replaced by one or more new decisions |
| `retired` | Nothing remains in effect and no new decision fully takes it over, for example because the subject was removed, the constraint was canceled, or a partially superseded remainder was canceled |

Status does not express implementation progress or whether a candidate is feasible. Unsettled proposals do not belong in notes. A long-term goal that has been adopted and begins to constrain work may be recorded, but must be distinguished from actual implementation. If it is explicitly set to take effect in the future, it cannot supersede the current decision early. Design and plan documents track implementation progress; subsystem documentation records current behavior and verifies it against code.

Do not supersede or retire a record automatically because one experiment failed, premises might change, implementation has not begun, or a file is temporarily missing. Reassess when evidence is no longer valid. Change the decision's effect only when the user explicitly changes it or a clear change is made within delegated authority. Recording does not add an approval step.

## Update in Place or Create a New Record

| Change | Action |
| --- | --- |
| Name, path, link, wording, or typo changes, with the decision unchanged | Revise in place; preserve the filename and original record date |
| Evidence is supplemented, corrected, or limited without changing the current choice or effective scope | Update the rationale and explain conditions or limitations; do not invent a new decision |
| A core choice or key constraint changes clearly, or a decision is made again based on materially different core evidence | Create a new record and explain why the old decision held and why it is changing now |
| Only part of the scope changes | Create a record for the changed part; retain the remaining constraints in the old record |
| The subject or constraint clearly disappears without a successor decision | Set to `retired`; explain why and provide evidence |

Correcting a false record and making a genuine change of decision are different. If evidence shows that the note was wrong and the actual decision never changed, correct the original. If the decision was genuinely made at the time and is now changing, create a new record. Do not erase real history under the label “correction.”

## Full Supersession

The new record states which conclusion and scope it takes over and why they changed. Preserve the old conclusion, rationale, alternatives, and evidence; mark the old record `superseded` and link to the successor. The relationship must be traceable in both directions.

The following snippets demonstrate fields only. An actual note still needs a Scope and body:

```markdown
Status: superseded
Superseded-By: [New decision](./2026-10-18-new-decision.md)
```

```markdown
Status: active
Supersedes: [Old decision](./2026-10-17-old-decision.md)
```

When multiple new decisions collectively replace the entire scope, list all successors and their respective scopes; do not force a link to just one. Supersession relationships must have no self-links, cycles, or broken links. Follow the branch relevant to the conclusion and scope being queried, not an arbitrary chain endpoint.

The end of a chain may be `active`, or `retired` after its subject disappears. The absence of a current constraint does not automatically restore an ancestor decision. Update subsystem documentation and Agent navigation to point to the current source; historical links remain explainable through old records.

## Partial Supersession and Migration

When only part of a decision is superseded, keep the old record `active`, narrow its Scope and current conclusion to the remaining area, and briefly describe its original coverage, the portion handed over, and the link to the new record. Preserve necessary historical rationale. The new record clearly states which portion it takes over. Do not add a partial-supersession status or delete the old rationale outright.

For example, if “do not cache any requests” changes to “static assets may be cached,” the old record continues to govern other requests and the new one governs static assets. Only when the remaining scope is later superseded should the old record become `superseded`, with links to all successors. If the remainder is canceled without being fully taken over, mark it `retired`, preserving existing successor links and scope explanations.

For staged migrations, state the target constraint, stage conditions, and compatibility obligations that remain in effect. Adopting a new goal does not mean old data or interface obligations have been removed. Residual old implementation does not automatically extend the old decision's validity. There must not be conflicting active conclusions for the same scope and conditions; investigate the decisions rather than choosing one arbitrarily.

A new record must retain still-relevant reasons for not choosing alternatives, premises, and necessary evidence so they do not get lost through supersession. Do not copy detailed implementation steps into notes.

## Cancellation and Re-adoption

When nothing remains in effect and no successor fully takes over, mark the record `retired` and explain why the subject was canceled or disappeared. If cancellation itself creates a new decision worth preserving long term, create a new record and supersede the old one rather than using `retired` to omit the new rationale.

If an old option is genuinely adopted again after a change of decision, create a new `active` record, link to the historical rationale, explain the new conditions and trade-offs, and supersede the currently relevant decision. Do not change the status of the historical record back to `active`. If only the status was marked incorrectly, correct it based on the facts without inventing a new decision.

Retain `superseded` and `retired` records by default. Before archiving, merging, or deleting, read [Retention and Organization](retention.md). Status updates do not authorize a commit.
