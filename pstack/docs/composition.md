# Compose pstack with the local supplements

This file owns routing between pstack and the five local supplements. The named
packages own their methods. Project guidance owns project-specific requirements.
These rules apply without installing project guidance and take precedence over
conflicting defaults in imported playbooks, templates, and companion skills.

## Choose methods when needed

Select the task's pstack playbook or requested leaf skill. Add a supplement only
when its trigger applies. Do not run the table as a sequence of mandatory phases.

| Trigger | Method and handoff |
| --- | --- |
| Before a concrete proposal, behavior change, or key trade-off | Read [decision-notes](../../decision-notes/SKILL.md) and search the relevant history. Give `how`, `why`, and `architect` the applicable findings. Do not repeat a still-valid search. |
| Product behavior or scope needs an in-depth interview | Use [grilling](../../grilling/SKILL.md). [grill-me](../../grill-me/SKILL.md) is an explicit entry to that same method. Observable facts belong in investigation, not interview questions. |
| The user asks to save a discussion, or it has independent design value | Use [to-docs](../../to-docs/SKILL.md). Save settled content and label open questions. Return to the requested task; saving does not start Feature or `architect`. |
| Work changes retained facts, plans, or document relationships | Use [maintenance-docs](../../maintenance-docs/SKILL.md) on the affected sources. Reuse the current design and plan. Small changes do not require new records. |
| A run reveals lasting rationale or a reusable correction | Apply `decision-notes`' recording threshold. A `why` finding, audit row, or `reflect` candidate is evidence, not automatically an adopted decision or new rule. |
| The user authorizes implementation of an agreed design | Route to the matching pstack playbook with the design, acceptance criteria, open constraints, and existing authorization. Reuse the confirmed understanding; do not restart the interview. |

Read companions through supported invocation or their installed files. Reuse
guidance and evidence already read while their scope and premises remain valid.
Do not invoke the caller again from a companion or restart a completed phase.
If a companion is unavailable, state the affected capability, retain necessary
context in the existing source, and continue independent work. Do not claim a
method ran. `grill-me` still requires `grilling`, as its entry specifies.

## Carry authorization across handoffs

Determine the requested outcome from the conversation before choosing actions.
Pass the same scope and limits to delegates and follow-on skills. A file, task
list, saved design, or skill name does not expand that scope.

- Discussion and read-only review end with findings or recommendations. A request
  to save those findings permits the document write, not product implementation.
- For a design-only request, `architect` returns the design and skips implementation.
  For authorized implementation, it can proceed without another approval. Honor
  an explicit checkpoint, unresolved product decision, or scope limit.
- Reuse explicit implementation approval and confirmed understanding from the
  conversation. Ask only about missing authority or unresolved material choices;
  continue work that does not depend on the answer.
- If investigation reveals a behavior change outside the agreed design, keep it
  as an unresolved proposal or preserve the behavior while completing the agreed
  work. A plan or sketch cannot label that change accepted merely because no
  current caller was found. Record the evidence and the decision still needed;
  approval of the original design does not approve the extra change.
- A request to implement does not authorize Git commits, push, PR creation, merge,
  release, messages, deployment, deletion, or paid jobs. Apply existing user,
  project, and tool authorization to each such action. An explicit combined request
  covers its stated operations without repeated confirmation.
- If a playbook says to commit, open a PR, file a backlog item, or publish without
  that authority, omit that action and report the local result. Do not stop safe
  implementation work to ask early. A pause can leave an uncommitted checkpoint.

## Keep Git methods in pstack

[Opening a PR](../skills/poteto-mode/playbooks/opening-a-pr.md) owns worktree,
staging, commit, and PR methods. [Shipping](../skills/poteto-mode/playbooks/shipping.md)
owns merge delivery. Use only the sections needed for the authorized task.
Project guidance retains change protection and authorization boundaries, not a
second commit format, commit-size policy, or branch procedure. A local-only task
can finish with checked, uncommitted changes.

## Keep one source for each fact

Locate the existing owning sources before creating artifacts. Apply the lifecycle
and location rules from the relevant supplement, not a second copy of its method.

| Information | Owning artifact |
| --- | --- |
| Agreed target behavior and acceptance | Existing design or requirement; `architect` adds missing technical detail there or links a distinct sketch |
| Execution steps, progress, and remaining verification | One existing plan or change record; pstack updates it rather than creating a competing plan |
| Verified current behavior and known differences | Existing subsystem documentation |
| Lasting decisions, rationale, and supersession | Decision notes when their recording threshold is met |
| Actions, evidence, and results of this run | `show-me-your-work` trail when triggered; link enduring sources rather than copying their full content |
| Continuation | Resume note with current state and next action, linking the design, plan, and trail |

One file can serve more than one role when the sections remain clear. A separate
design, plan, note, and trail are not a required set. `technical-writing` and
`unslop` improve the owning text; they do not select another destination or create
another version. Optional project guidance can link these methods, not duplicate
this routing table.

## Scale plans and verification to the task

Keep the project's required checks and release gates. Select additional checks
from affected behavior and risk. A missing required tool leaves a gate pending;
it is not a pass or a reason to silently remove the requirement.

Use the full multi-PR program template and `check-plan.mjs` only when the user or
project has adopted that program format. Its ten-lane, unit/live/perf requirements
belong to that format. For an ordinary plan, retain scope, dependencies, observable
acceptance, verification, and open risks in the existing owning source. Do not
invent PRs, screenshots, perf metrics, or agent lanes to satisfy a template.
Do not run the full-program checker against a proportionate ordinary plan.
An explicitly requested program keeps its gates even when the work seems small.
