# Project Agent Guidance

<!-- When reusing in another project, keep AGENTS.md or use another name recognized by the target tool, such as CLAUDE.md; fill in real project resource locations and remove placeholders. -->
<!-- See agent-guidance/README.md for integrating companion files and skill links. This AGENTS.md is the active entry point for this library. -->

Proceed autonomously with authorized work and do not reconfirm established decisions. If behavior, scope, or a key trade-off is unclear, investigate and resolve it with the user. Assess planning, writing a plan, and approving a plan separately; there is no universal start gate.

Maintain each fact in one place and reference it elsewhere. Creating, reading, or referencing a document does not grant implementation authorization; assess commits and external actions against existing authorization.

## Read Rules as Needed

Links do not load files automatically. Read the relevant guidance before the corresponding activity; reuse content already read if it remains applicable.

| When | Guidance |
| --- | --- |
| Starting a task, or preparing a proposal or a decision about behavior or a key trade-off | [Collaboration, document ownership, and method navigation](agent-guidance/collaboration.md) |
| Implementing, changing tests, verifying or manually accepting work, reviewing, or delivering | [Implementation, verification, and delivery](agent-guidance/verification.md) |
| Changing repository files, collaborating in parallel, or staging, committing, pushing, opening a PR, merging, releasing, or changing history | [Git commits and collaboration](agent-guidance/git.md) |

## Project Resources

<!-- Replace with links to real files or indexes; prefer existing locations and do not create empty pages without a need. -->

When first learning the project, locating responsibility boundaries, or assessing cross-subsystem impact, read the relevant architecture overview and subsystem documentation. Follow links to verify the implementation sources involved in this task; reuse verified content that remains applicable.

- Project overview and running instructions: `<README.md or actual usage documentation>`
- Requirements, acceptance, and human-readable designs: `<actual requirements source; default designs location: docs/designs/>`
- Architecture overview and current subsystems: `<actual overview; default subsystem location: .agents/subsystems/>`
- Current change designs and plans: `<actual documents or index; default location: .agents/changes/>`
- Long-term decisions: `<actual source; default location: .agents/notes/>`
- Coding standards, check commands, and environment: `<actual guidance source>`

## Project-Specific Constraints

`<Record only verified constraints that affect decisions, and link to detailed sources>`
