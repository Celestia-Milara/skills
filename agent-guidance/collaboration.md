# Collaboration and Use of Project Materials

Before starting a task, read the project's actual constraints, requirements, relevant source code, and tests; compare documentation with actual behavior. If behavior, scope, or a key trade-off is unclear, investigate, make a recommendation, and resolve it with the user. Do not reconfirm established decisions. Handle ordinary engineering details autonomously; leave important or hard-to-reverse choices to the user.

Assess planning, writing a plan, and approving a plan separately. There is no universal stage that requires writing a plan first or getting approval before work starts. Proceed autonomously with authorized work. Near-term plans need only be actionable; refine later work as evidence emerges. Investigation itself is execution.

Use only skill names actually available in the environment. If a skill cannot be invoked, read the project's configured guidance instead; do not claim to have invoked unavailable capabilities. When changing skills, reuse verified context that remains applicable. Recheck when the scope, premise, or source changes, or when there is a conflict; do not repeatedly reload materials or rescan the entire repository.

## Source Ownership

Maintain each fact in one place; summarize and reference it elsewhere. `README.md` and `docs/` support understanding the project, requirements and acceptance, and human-readable designs. `.agents/` holds detailed engineering maintenance materials. Divide materials by purpose and level of detail, not by reader; do not create a complete human-facing copy of every Agent document.

A human-readable design can be a complete source. Engineering records reference it and add details as needed; do not require companion directories or impose engineering status on designs. Existing tasks can read relevant designs as needed. Creating, reading, or referencing a design does not add implementation authorization; existing authorization remains in effect.

Ordinary files in `.agents/` do not load automatically because of their directory name; link to them from the project's actual Agent entry point. Use the entry point recognized by the tool, such as `AGENTS.md` or `CLAUDE.md`; do not assume a singular `AGENT.md` loads automatically. Do not create empty documents without a need.

## Methods and Sources

Use the relevant guidance below for the task. When integrating into a project, update the links to the actual installed or configured locations.

| Purpose | Guidance |
| --- | --- |
| In-depth discussion of the current topic | [grilling](../grilling/SKILL.md), with [grill-me](../grill-me/SKILL.md) as an explicit entry point |
| Create designs for people to read, edit, and reference later | [to-docs](../to-docs/SKILL.md) |
| Organize and maintain subsystem documentation, change designs, and plans | [maintenance-docs](../maintenance-docs/SKILL.md) |
| Find and maintain long-term decisions and their lifecycle | [decision-notes](../decision-notes/SKILL.md) |
| Prepare a real handoff or continue from handoff materials | [handoff](../handoff/SKILL.md) |

Before proposing a concrete solution, deciding behavior or a key trade-off, changing related implementation or behavioral tests, or writing a decision record, search the history according to `decision-notes`. Start with project constraints and subsystem documentation, then follow links and search by issue or mechanism. For cross-system work, cover relevant interfaces and shared decisions. Missing links or differing names do not prove there is no history. Pure formatting or status updates that do not involve constraints do not require a new search.

Record important settled conclusions promptly and let the user know; do not wait for a commit or ask separately whether to save each one. Propose an old option again only when a premise has clearly changed, and explain the impact. Follow the user's new instruction when they change a decision. Detailed thresholds and status definitions belong to their respective skills and are not duplicated here.

Current facts belong in subsystem documentation; target behavior belongs in the human-readable design or existing design source; engineering details and progress belong in change designs and plans; long-term rationale belongs in notes. Keep them in sync with verified substantive changes. Check them before delivery or handoff rather than waiting until the project ends. Complete documentation does not prove implementation or acceptance is complete, and documenting work does not add approval requirements.

When materials conflict with implementation, investigate and correct verified errors. Do not describe a defect as a normal contract or use old materials to override a new instruction. If a key decision remains unclear, ask the user while continuing work that does not depend on it.
