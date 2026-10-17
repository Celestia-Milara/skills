---
name: maintenance-docs
description: "Create, verify, maintain, continue, and close subsystem documentation, change designs, and plans; verify how human-readable designs relate to engineering materials. Use when the user asks to organize these materials, work requires preserving design and execution context over time, or changes make existing documentation, plans, status, or navigation inaccurate. Check source code, tests, and relevant decisions as needed; distinguish current state, goals, unresolved questions, and actual verification; maintain a single source of truth. This is not a mandatory phase for every development task."
---

# Maintenance Docs

## 1. Clarify responsibilities and the current scope

Use this skill to decide whether to create or reuse records, organize content, verify descriptions, expose gaps, and maintain source relationships, status, and navigation. This requires engineering judgment: investigate actual paths when explaining current mechanisms; do not merely reformat conversation or create false certainty by filling out templates.

- The Agent performing the current task handles technical choices, trade-offs, task breakdown, implementation, debugging, and verification; use these shared rules when outputs need to be retained. Targeted investigation and updates to subsystem documentation are valid tasks and do not require starting a separate design process first.
- Use `to-docs` to create readable design deliverables for people to review, edit, and reference later. A human-readable design can be the complete source; this skill guides document ownership and consistency from the time it is saved. Do not require an engineering record first or create circular calls between skills.
- Use `grilling` to clarify the current topic in depth; `grill-me` is its explicit entry point. Continue from established content without reopening decisions or adding approval gates for each iteration.
- Use `decision-notes` to find, record, supersede, and organize long-term decisions. This skill references its conclusions; it does not establish a separate interview process or decision lifecycle. Search when its trigger conditions apply, even if there is no direct link.
- Use `handoff` as needed to prepare or verify a handoff across sessions or Agents. This skill continues to maintain engineering materials and status; do not create a complete duplicate just because the person executing the task changed, and do not create circular calls between skills.
- Ordinary reading, immediate questions, and small changes that do not affect existing materials do not independently trigger the full maintenance process; still read the materials needed for the task. A documentation-only request does not expand authorization to change product behavior, run unrelated checks, or commit code; existing engineering-task authorization remains in effect.

Use the names actually available in the environment. If a skill cannot be invoked, read the project's configured guidance instead; do not claim to have invoked an unavailable skill. Collaboration must not cause circular loading or duplicate searches.

## 2. Locate sources and decide whether to reuse or create records

Start from the project's actual Agent entry point to locate constraints, requirements and acceptance criteria, relevant subsystems, change records, and notes; verify the scope of the current work. For existing projects, prefer existing locations and names; do not require migration. For cross-subsystem work, cover relevant interfaces and shared constraints.

Reuse context already read and verified for the same task if it still applies. When the scope, a key premise, or a source changes, or a conflict appears, recheck the affected areas. Do not rescan the whole repository or restart an interview simply because the turn or skill changed.

When choosing locations, names, file splits, or navigation, read [Organization and Sources](references/organization.md).

1. First look for existing documentation that still applies to the same change; a similar topic does not necessarily mean the same change. To continue existing work, locate its original record and verify the current state rather than automatically writing a complete handoff document.
2. Create or update records when target designs, migration plans, dependencies, or questions to investigate or verify must be retained for later implementation, acceptance, or cross-session continuation. This also applies during investigation and solution comparison.
3. Small, clear changes completed in the current turn may be delivered in conversation alone, while still maintaining affected existing documentation and notes required by established rules. If the user explicitly asks to save something, record it, preferring an appropriate existing source.
4. Do not mechanically create records based on line count, file count, conversation turns, or commit count. Do not pre-create empty pages or an entire documentation library, and do not ask each time whether to write documentation.

## 3. Verify and maintain materials according to their purpose

| Current work | Read as needed | Information ownership |
| --- | --- | --- |
| Verify ownership and alignment between human-readable designs and engineering materials | [Organization and Sources](references/organization.md) | Human-readable designs retain the complete source for goals, scenarios, and behavior; engineering materials reference and supplement them |
| Describe a current subsystem or correct differences between documentation and implementation | [Subsystem Documentation](references/subsystems.md) | Current responsibilities, mechanisms, contracts, and navigation to source code, tests, and notes |
| Record change goals, designs, tasks, and continuation context | [Change Designs and Plans](references/changes.md) | Current goals, gaps from the existing state, unresolved questions, implementation, and verification plans |
| Update status; complete, pause, cancel, resume, or close records | [Status and Closeout](references/lifecycle.md) | Overall progress, task results, actual verification, and disposition of remaining work |

Maintain each fact in one place; summarize and link to it elsewhere. `docs/designs/<topic>.md` can be the complete human-readable design source. Add engineering details, dependencies, verification, and progress to `.agents/changes/` only as needed; do not duplicate the design. Do not turn an overview of an existing source into a full copy, create a second status or progress record in an index, or maintain long-term rationale outside its notes source.

The engineering change entry point, README, plan, and overall Status rules apply only to work that needs an engineering change record; they are not imposed on human-readable designs. A design's settled or unresolved content is not engineering progress. Do not introduce a mandatory design state machine or create a companion engineering directory for every design.

Distinguish settled conclusions, unresolved recommendations, assumptions, and items to investigate from source-code verification, existing test coverage, and actual runtime verification. Links should explain the mechanism, behavior covered, or decision topic they support. The existence of a test does not mean it has been run successfully. Adopting a goal does not mean it has been implemented or automatically remove transition or compatibility obligations.

When documentation and implementation disagree, check the relevant source code, tests, requirements, applicable notes, and implementation status. Determine whether documentation is stale, implementation diverges from intended behavior, or a transition is incomplete. Correct verified documentation errors; address implementation errors within existing authorization. Do not describe a defect as a normal contract or use old documentation to overrule a new user instruction. If key behavior or trade-offs remain unclear, describe the conflict and ask the user to decide while continuing work that does not depend on that decision.

## 4. Keep materials in sync with substantive changes

- When subsystem responsibilities, boundaries, main paths, interfaces, state, failure behavior, compatibility behavior, or necessary navigation change, update the relevant documentation alongside the verified change rather than waiting for the project to finish. Do not mechanically rewrite descriptions that remain accurate after internal refactoring, but repair broken links.
- Update designs when goals, scope, key choices, or premises clearly change; continue to label unresolved content as unresolved. Update plans when task results, dependencies, blockers, or next steps change in a way that affects execution or continuation. Sync important schedule changes before executing affected steps; do not log every tool operation.
- Handle adjustments within existing authorization autonomously. Documentation updates do not add approval requirements and cannot replace a necessary user decision. Ask the user to decide on behavior, scope, or key trade-off changes that exceed authorization; do not reconfirm settled matters.
- Before delivery, pausing, or handoff, verify that relevant materials requiring ongoing retention let the next Agent identify the current state, gap from the goal, remaining work, and next step. Do not wait until these moments to make the first record.

Handle only the scope relevant to the current task. Keep current facts in subsystem documentation, long-term decisions in `decision-notes`, and have other locations reference them.

## 5. Check and deliver

Check the scope agreed for this task; do not turn it into a repository-wide audit:

1. **Coverage and ownership**: Retain content that needs to persist; reuse appropriate sources without duplicate prose, empty placeholders, or continuation context left only in temporary conversation.
2. **Accuracy**: Make current state, goals, settled and unresolved points, and evidence clear; do not conflate stage progress, code changes, successful verification, and required manual acceptance.
3. **Status and continuation**: If an engineering change record exists, maintain its overall Status only at the change entry point and mark tasks according to actual progress. Make related blockers, gaps, next steps, and remaining work locatable; retain necessary conclusions and evidence in closeout records.
4. **Links and consistency**: Keep relevant requirements and acceptance criteria, designs, plans, subsystems, and notes accurately connected; ensure links work. Reorganizing materials or records must not lose unique information.
5. **Verification scope**: Run applicable existing checks based on the task and project, and review the results; perform a manual review if no dedicated tool exists. Do not impose unrelated checks, a full test suite, or a new toolchain just to complete documentation. Reuse verified results when the content has not changed, and accurately describe unverified or constrained areas.

Completing the current documentation task means that the agreed information is accurate, sources are locatable, unknowns and verification gaps are disclosed, and the materials support continuation. It does not prove the design is sufficient, the implementation is correct, or the feature is complete. Verify completion of the overall change separately using [Status and Closeout](references/lifecycle.md).

Deliver the changes, checks, and necessary gaps from this round with a concise explanation and links to actual files; put results that need ongoing maintenance in the repository. Keep related code, documentation, and notes together as a pending deliverable. Saving documentation does not authorize commit, push, PR, or release; follow the project's existing commit confirmation rules and do not commit early just because documentation was saved.
