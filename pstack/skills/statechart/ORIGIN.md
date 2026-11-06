# Origin

From pstack 0.15.36 by Lauren Tan (MIT), through backnotprop/pstack
commit `6c75f4e67546c2ddbf9634734c1e3ebbea34861a`.
Local changes add the host adapter reading trigger and Codex invocation metadata.
On Windows, `scripts/run.ts` and `scripts/statechart.ts` stop the TLC process tree
with `taskkill`, clean up through a Node janitor instead of `/bin/sh`, and read
TLC's CRLF output.
Install the full pstack tree to retain sibling methods and shared adapters.
