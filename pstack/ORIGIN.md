# Source and local adaptation

This is the complete pstack 0.15.36 distribution, imported through the portable
[backnotprop mirror](https://github.com/backnotprop/pstack/tree/6c75f4e67546c2ddbf9634734c1e3ebbea34861a).

- Original: [cursor/plugins, pstack](https://github.com/cursor/plugins/tree/ae5650febf4320793844c12c4adaa937f417f8da/pstack).
- Mirror commit: `6c75f4e67546c2ddbf9634734c1e3ebbea34861a`.
- Original version: `0.15.36`. Import date: 2026-11-03.
- License: [MIT, Copyright (c) 2026 Lauren Tan](LICENSE).

All 573 original file paths and all 582 tracked mirror files are retained.
The mirror supplies host-neutral workflows and the conservative Comment Sicko
fix described in its README. Local additions supply host adapters, their reading
triggers, Codex invocation metadata, Windows helpers, and source records.

[source-lock.json](source-lock.json) records original and mirror file hashes.
Hashes use Git blob bytes before checkout line-ending conversion.
Its `local_changes` list identifies changes from the mirror. New files are local
unless recorded as source files. The root library supplies packaging, checks,
and five separately maintained supplementary skills.

For updates, compare the old source, new source, and local files. Preserve local
adapters and intentional mirror fixes. Check completeness and both hosts before
updating the lock. Do not run the mirror's branch/push recipe in this repository.
