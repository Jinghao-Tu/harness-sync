---
name: codex-worker
description: >-
  Delegate bounded coding, codebase research, and code review tasks to Codex CLI
  (`codex exec`) as an isolated worker subagent using `gpt-6.2-sol` or
  `gpt-6.2-astra`. Use when the primary agent acts as orchestrator and offloads
  implementation, multi-file edits, debugging, or independent verification to
  Codex CLI.
---

# Codex Worker

Delegate self-contained execution tasks to Codex CLI (`codex exec`) while the
primary agent handles user interaction, architectural decisions, and final
verification.

## Model Selection

Choose the worker model and reasoning effort based on task complexity unless the
user explicitly specifies them:

- `gpt-6.2-sol` (default): everyday implementation, refactoring, tests,
  targeted research, and code review. Default effort: `medium` or `high`.
- `gpt-6.2-astra`: complex multi-file changes, difficult debugging, core
  architecture work, or escalation when `gpt-6.2-sol` fails to resolve the root
  cause. Default effort: `high` or `xhigh`.
- Pass reasoning effort via `-c model_reasoning_effort="<level>"` using `low`,
  `medium`, `high`, `xhigh`, or `max`. Avoid `ultra` for single-worker runs
  because it enables automatic task delegation.

## Sandbox and Isolation

Always pass `-s` / `--sandbox` explicitly on every `codex exec` call:

- `-s read-only`: research, codebase inspection, and code review.
- `-s workspace-write`: implementation, file edits, and local checks.
- `-s danger-full-access`: only when the task requires unrestricted access and
  the user has explicitly authorized it.

Keep nested subagents disabled with `-c agents.enabled=false` and
`-c features.multi_agent_v2=false`.

When launching multiple write workers in parallel, assign strictly disjoint file
paths or isolate each worker in a managed Git worktree with `--worktree`.

## Invocation

Invoke `codex exec` non-interactively, passing the prompt via stdin (`-`) to
avoid shell quoting issues and writing the final response to a file (`-o`) to
keep parent context clean.

POSIX shell:

```bash
codex exec \
  -m gpt-6.2-sol \
  -c model_reasoning_effort="medium" \
  -c agents.enabled=false \
  -c features.multi_agent_v2=false \
  -s workspace-write \
  -C <workdir> \
  -o <output_file> \
  - < <prompt_file>
```

PowerShell:

```powershell
Get-Content -Raw <prompt_file> | codex exec `
  -m gpt-6.2-sol `
  -c 'model_reasoning_effort="medium"' `
  -c 'agents.enabled=false' `
  -c 'features.multi_agent_v2=false' `
  -s workspace-write `
  -C <workdir> `
  -o <output_file> `
  -
```

Optional flags:

- `--worktree`: run the task in a new managed Git worktree.
- `--json`: stream JSONL events (useful for capturing the session ID).
- `--ephemeral`: skip persisting session files for disposable one-shot runs
  that will not be resumed.
- `codex exec review`: run a repository code review directly.

To continue the same worker session for targeted fixes, use `resume` (supports
`-m`, `-c`, `-o`, and `-` for stdin; runs in the session's existing workspace):

```bash
codex exec resume <session_id_or_--last> -o <output_file> - < <followup_file>
```

If the host environment runs terminal commands in a network-restricted sandbox
that blocks API access or `~/.codex` credentials, execute `codex` outside the
sandbox.

## Prompt Structure

Codex workers do not see the primary conversation. Make every prompt
self-contained with four concise sections:

1. **Goal**: the exact outcome or behavior to deliver.
2. **Scope**: files or directories allowed to inspect or modify, plus explicit
   boundaries not to touch.
3. **Constraints**: repository conventions, compatibility requirements, and
   non-goals.
4. **Checks**: exact validation commands to run before finishing, and a request
   for a concise final summary (changes made, files touched, checks run, and
   remaining risks).

## Verification and Escalation

1. Never accept a worker's summary on faith. Inspect `git status`, `git diff`,
   and relevant check output before reporting completion to the user.
2. Confirm the worker stayed within its assigned scope and preserved unrelated
   user changes.
3. On failure, retry with concrete error evidence. Escalate from `gpt-6.2-sol`
   to `gpt-6.2-astra` when deeper reasoning is needed.
4. Stop automatic retries after 2 failed attempts on the same task, then report
   the attempted paths, root-cause findings, and next options to the user.
