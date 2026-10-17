---
name: grill-me
description: A relentless interview to sharpen a plan or design.
disable-model-invocation: true
---

Load the installed `grilling` skill using the current host's available mechanism: if it provides a `Skill` tool, invoke `grilling`; otherwise locate and read the installed `grilling/SKILL.md` and follow its instructions. The path `../grilling/SKILL.md`, relative to this file, is only a candidate if it exists; do not assume a fixed installation path. If `grilling` is not installed or cannot be accessed, state that it is a required dependency and stop; do not claim it was loaded.
