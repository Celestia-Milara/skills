# Skills Library

This repository maintains reusable personal engineering conventions: standalone skills and project agent guidance.

## Project Sources

- Package responsibilities and installation: [README](README.md).
- Guidance ownership, integration, and source updates: [Agent Guidance Integration](agent-guidance/README.md). Use [AGENTS.template.md](agent-guidance/AGENTS.template.md) for other projects.
- Checks for changes to this library: [Reading and maintenance](README.md#reading-and-maintenance). Existing host-test evidence: [Verified host behavior](README.md#verified-host-behavior).

Local `design/` records, when present, contain earlier discussions and decisions. Consult relevant records for design or scope changes; historical statements may no longer describe the current files. These records are excluded from publication and are not package dependencies.

## Task-Specific Rules

Read the applicable guidance before the activity; links do not load its contents automatically.

| Activity | Guidance |
| --- | --- |
| Propose solutions, decide behavior or scope, change implementation or behavioral tests, or organize project documentation | [Collaboration, decision history, and document ownership](agent-guidance/collaboration.md) |
| Implement, change tests, verify, review, or deliver changes | [Verification and delivery](agent-guidance/verification.md) |
| Edit repository files, coordinate parallel work, or perform Git and publication operations | [Change ownership and Git authorization](agent-guidance/git.md) |

## Library Constraints

- Edit the root English packages; `zh-backup/` is a local backup, not a second maintained edition. Keep installation and publication within the [README's scope](README.md#publication-scope).
- Skills must remain usable without project agent guidance. Keep specialized methods in their packages and common operating rules in `agent-guidance/`; see [ownership](agent-guidance/README.md#ownership).
- Preserve complete package references and applicable license/origin files when distributing skills; see [licensing and sources](README.md#license-and-upstream-sources).
