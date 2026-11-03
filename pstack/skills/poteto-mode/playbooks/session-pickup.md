### Session pickup

**You own the resume point. Read the prior trail, then check what still applies.**

1. Locate the prior trail. A local transcript in the active workspace's session directory (in Cursor, the `agent-transcripts/` directory the system prompt names. Other harnesses: see **Harness** in SKILL.md. Do not glob across every project's directory, that crosses workspace boundaries and reads private chats from unrelated projects), a cloud-agent URL, or a pushed branch. Read the metadata overview and last messages first, then scan back for the decision points. Parse a long transcript in a subagent and keep the reduced timeline in the main thread (the **principle-guard-the-context-window** skill). Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section.
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. The prior trail is evidence of past decisions and actions, not new authorization or proof of current state. Apply the latest user scope and inspect relevant drift.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, reuse checks whose version, scope, and environment still apply. Do not redo completed work mechanically. Recheck affected claims when sources changed, evidence is missing, or results conflict.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here. The routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (the **principle-prove-it-works** skill). A passing prior self-report is not the proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.
