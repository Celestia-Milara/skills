# Sources and Local Adaptation

This directory draws on Matt Pocock's handoff method and reorganizes it around this collection's approved handoff and documentation-maintenance boundaries. It is not an unmodified upstream copy.

- Repository: [mattpocock/skills](https://github.com/mattpocock/skills)
- Pinned commit: `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`
- Original entry point: [skills/productivity/handoff/SKILL.md](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/handoff/SKILL.md)
- Guide: [docs/productivity/handoff.md](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/docs/productivity/handoff.md)
- Copyright: Copyright (c) 2026 Matt Pocock. The complete [MIT LICENSE](LICENSE) is retained with this package.

## Methods retained

Select context for the next task; reference existing specifications, plans, decisions, and code changes rather than copying them. A handoff transfers context; it does not replace handling every phase boundary. Remove sensitive information before transferring.

## Local changes

- Rewrote the entry point and references in English, covering both preparing a handoff and verifying the context when taking over, rather than only generating a session summary.
- Support both explicit requests and genuine need for transfer. Do not set the upstream `disable-model-invocation`; actual discovery and invocation still depend on the target framework and installation.
- Removed the requirement to write to a system temporary directory. Prefer a user-specified location, an existing task record, or a minimal handoff message. Create a separate file as needed and verify accessibility from the receiving environment.
- Added targeted handling of session-specific constraints, authorization basis, workspace ownership, evidence applicability, temporary resources, open questions, and next actions, without a fixed required form.
- When taking over, verify the current task, sources, and working context; reuse valid conclusions and evidence. A reported handoff does not expand authorization, prompt redundant approvals, or drive canceled or invalid work.
- `maintenance-docs` owns engineering materials and status, `decision-notes` owns long-term rationale, and `to-docs` organizes human-readable designs. This package does not copy their detailed rules or hard-code their installation paths.
- Do not require a handoff at the end of every turn or automatically start or end sessions, assign people, send messages, or perform Git operations.

Also compared the former `engineering_skills` handoff-work as a local requirements source; it was not adopted wholesale, and its fixed directories and cross-package path dependencies were not restored. Architecture navigation belongs to project entry points and `maintenance-docs`, not to handoff as an extra responsibility.

Runtime rules depend only on references inside this package. Source review used local text reading and a pinned commit, with relevant file differences checked. Upstream code was not executed and no model behavior evaluation was performed.