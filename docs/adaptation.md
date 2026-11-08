# Source and host adaptation

The official pstack source at `pstack/` must match the complete path and SHA256
inventory in [source-lock.json](../source-lock.json). The current revision is
6b0300214a09fd6029cfb7077043125758cd1fd2. It has 58 top-level skill entrypoints.

The backnotprop mirror is a reference for cross-harness mappings, not the imported
workflow baseline. Its policy edits and Windows patch are not silently merged.

## Ownership

| Content | Owning source |
| --- | --- |
| Official workflows, principles, agents and resources | pstack/ |
| Runtime tools and installation mapping | adapters/ |
| Script platform mappings, pinned inventory and launcher | adapters/platforms/ |
| Projection and metadata generation | scripts/projection.py |
| Complete assembly and hashes | scripts/package.py |
| Ownership, conflicts, staging and rollback | scripts/install.py |
| Optional project integration | docs/composition.md and agent-guidance/ |
| Independent interview and documentation methods | Five root supplement packages |

Generated entries point to a local host adapter before the workflow. Canonical
resources remain in the complete bundle. Relative document links are resolved
against their source file before relocation. Codex invocation metadata is generated
from upstream explicit-only policy. Pi and dsh retain the corresponding native
frontmatter. Claude keeps disable-model-invocation and reads the official adapter
plus the local user-skill override. Named agents have stable installed paths and
omit unsupported Cursor background metadata.

Claude's official marketplace adapter assumes plugin namespaces. The local override
only changes this skill-directory installation to unprefixed skills and agents.
The generator does not translate every workflow paragraph or duplicate a maintained
Claude body. Host mappings must use the live tool and model schema.

## Directory isolation

Codex user installs use ~/.codex instead of shared ~/.agents because Pi and dsh
also read that shared directory. Their generated invocation metadata differs.
Project installs follow each host's documented roots. A project that uses multiple
engines must avoid giving them conflicting same-name entries in shared roots.

Generated staging directories inherit the destination parent's permissions. On
Windows, owner-only temporary-directory ACLs survive a rename and can prevent
Codex sandbox processes from reading installed skills. Host staging and new shared
versions therefore use exclusive UUID directories with normal parent inheritance.
This changes no global ACL and does not grant access beyond the chosen parent.
Staging contains public package files and installation metadata, not credentials.

## Supplements and updates

Clean installs default to 58 official skills. Five supplements can be selected with
--with-supplements. Existing managed supplements are preserved on update and recorded
separately in the manifest. They do not alter the official mode or principles.

A reset first creates a private, verified archive. Cleanup moves only explicitly
owned entries. Other skills, junction targets, account settings and historical
archives stay untouched. Modified generated files are retained in the reset backup;
normal updates still refuse such files.

The source and adapters are portable distribution content. Actual Windows script
execution is scoped by [the execution platform contract](../adapters/platforms/README.md).
The launcher exposes the portable log helper, reduced local worktree audit and
unchanged private check-plan script. Both storage modes generate the same contract
link. WSL fallback and the remaining workflows need separate validation. No
process-tree or model capability claim follows from successful installation.

## Optional Junction storage

The [Junction mode](../README.md#shared-resources-with-junctions) keeps public
versions in a separate content-addressed store. Public resources and ownership
receipts are separate. The host receipt records exact link targets and local entry
hashes. Scripts and cross-skill documents remain private when they cannot safely
share the public path. Known local dependency caches are preserved in backups.

Updates and restores use the same host-local rename rollback mechanism as copy
storage. No shared target is deleted during host cleanup. Immutable version
validation rejects edited public content; store garbage collection is deliberately
not automated. Backups record links and materialize their contents, including the
external receipt required to identify the generated installation.
