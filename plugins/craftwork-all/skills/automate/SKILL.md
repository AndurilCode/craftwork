---
name: automate
description: Build automation scripts and pipelines that use coding-agent CLIs (Claude Code, Codex, Gemini CLI, GitHub Copilot CLI) in headless/non-interactive mode as the AI engine, or delegate work to cloud agents (`gh agent-task`) that open pull requests asynchronously. Use this skill whenever the user wants to write a shell script, CI job, cron task, batch processor, webhook handler, or any automation that shells out to `claude`, `codex`, `gemini`, `copilot`, or `gh agent-task` — single-turn prompts, multi-turn agentic loops, parallel fan-out across files/folders, structured JSON outputs consumed by downstream tools, or cloud-delegated tasks that produce PRs. Trigger on phrases like "script that uses Claude", "automate with Claude Code", "headless Claude", "batch process files with an LLM", "pipeline with codex exec", "gemini -p", "copilot --autopilot", "gh agent-task create", "GitHub Action that calls Claude", "cron job to review PRs", "agent loop in bash", "dispatch an agent task to open a PR", "fleet-wide agent-task across repos", or any request to integrate a coding agent CLI into an automated workflow. Also trigger when the user describes the shape of a pipeline (fan-out, map-reduce, review-then-fix, extract-then-summarize, ticket-to-PR, scheduled fleet upgrade) and AI is the engine, even if they don't name the CLI explicitly.
---

# Coding-Agent CLI Automation

## Method — step-by-step

Run these nine steps in order for every new automation. The sections below are the toolbox; this list is the procedure.

1. **Discover runtime.** Which CLIs, skills, MCPs, and models are available on the host? Fail fast when a dependency is missing. See `references/introspection.md`.
2. **Pick category** — local execution or cloud-delegated PR (§Two categories, five CLIs).
3. **Pick CLI, then load its reference BEFORE writing any invocation.** Default to Claude Code; use another only if the user named it. For non-Claude targets, loading `references/{codex,gemini,copilot,github-agent-task}.md` is mandatory — examples in this file are Claude-syntax. See §Do not transliterate.
4. **Define the I/O contract** — inputs (positional args, env vars, stdin) and outputs (stdout JSON, exit codes, artifact files). Everything a caller needs to re-run the script lives here (§Reusability & observability).
5. **Pick shape** — single-turn extract, agentic loop, multi-turn, parallel fan-out, or cloud delegation (§The five canonical shapes).
6. **Apply non-negotiable flags** — auto mode + `--allowedTools` + `--output-format json` + schema + success verification (§Non-negotiable flags).
7. **Wire reusability** — parameterize every path, model, timeout; no hardcoded constants (§Reusability & observability).
8. **Wire observability** — capture session ID, cost, live progress, structured exit codes (§Reusability & observability).
9. **Deliver** — header block documenting usage, env, permission posture, tunables.

## Two categories, five CLIs

- **Local execution** (rows 1–4) — agent runs on your machine or CI, synchronous, stdout output. For artifacts that aren't PRs.
- **Delegated cloud** (row 5) — dispatch a cloud agent that opens a PR asynchronously. For ticket/webhook→PR flows.

| CLI | Headless invocation | Reference |
|-----|--------------------|-----------|
| Claude Code | `claude -p "<prompt>"` | `references/claude-code.md` |
| Codex | `codex exec "<prompt>"` | `references/codex.md` |
| Gemini CLI | `gemini -p "<prompt>"` | `references/gemini.md` |
| GitHub Copilot CLI | `copilot -p "<prompt>" --allow-all-tools --autopilot` | `references/copilot.md` |
| `gh agent-task` (cloud) | `gh agent-task create "<description>" --base main` | `references/github-agent-task.md` |

Combinable — `gh agent-task` opens the PR, a local CLI reviews it (see cookbook).

### Do not transliterate across CLIs

Examples throughout this file are Claude-syntax. Swapping `claude`→`codex`/`gemini`/`copilot` with the same flags hallucinates. Key divergences:

| Concern | Claude | Codex | Gemini | Copilot |
|---|---|---|---|---|
| Auto mode | `--permission-mode acceptEdits` | `--sandbox <mode>` / `--full-auto` | `--approval-mode auto_edit` | `--autopilot` + `--allow-all-tools` + `--no-ask-user` |
| Tool scope | `--allowedTools "Read,Edit,..."` | `--sandbox read-only\|workspace-write\|danger-full-access` | `--policy <file>` | `--allow-tool "<name>"` |
| Structured output | `--json-schema '<inline JSON>'` | `--output-schema <file>` | (policy / post-parse) | (post-parse) |
| JSON result field | `.result` / `.structured_output` | `--output-last-message <file>` | `.response` | JSONL events |
| Session resume | `--resume <id>` | `codex exec resume --last` | `-r <id>` / `-r latest` | (n/a) |
| Session ID path | `.session_id` | `.thread_id` (in `thread.started`) | `.session_id` | per-event `session_id` |

## Non-negotiable flags (the checklist)

**Local execution (`claude` / `codex` / `gemini` / `copilot`):**

- [ ] **Deterministic auto mode** — per-CLI flag in §Do not transliterate. Never `plan`/`default`/`interactive` in a script; they pause for a human.
- [ ] **`--allowedTools` narrow allowlist — the real safety boundary.** Auto mode = "don't pause for approval"; the allowlist defines what the agent *can* do. Read-only: `"Read,Grep,Glob"`. Dev: `"Read,Edit,Bash(npm test*)"`.
- [ ] **`--output-format json`** when the next step is a shell pipeline. Never parse `text` with regex/grep/sed.
- [ ] **Structured-output constraint** (`--json-schema` Claude, `--output-schema` Codex) when output feeds downstream code. Stops drift into prose/invalid enums so `jq` can't silently break.
- [ ] **Verify success in the JSON** (`is_error`, `subtype`, `errors[]`, `permission_denials[]`), not just exit code. All four CLIs can exit 0 on recoverable failures.

**Delegated cloud execution (`gh agent-task`):**

- [ ] **Explicit `--base <branch>`.** A PR against `develop` when you meant `main` wastes a review cycle.
- [ ] **`create` exit 0 = "dispatched," not "succeeded" and not "merged."** The agent runs after the command returns. Pair with a completion watcher (`gh pr list`, `pull_request.opened` webhook, or `--follow`).
- [ ] **`--repo <owner/name>`** when targeting another repo. One dispatcher addresses any accessible repo without cloning.
- [ ] **Long ticket bodies via `-F <file>` / stdin**, never inlined as argv. Avoids quoting bugs and arg-length limits.

## The five canonical shapes

Shapes 1-4 are local execution; shape 5 is cloud delegation.

### 1. Single-turn, extract to JSON

Classification, extraction, summarization, triage. Script gets a parseable structured answer.

```bash
result=$(claude -p "Classify the severity of this error: $(cat error.log)" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"severity":{"type":"string","enum":["low","medium","high","critical"]},"reason":{"type":"string"}},"required":["severity","reason"]}' \
  --permission-mode acceptEdits \
  --allowedTools "Read")

severity=$(echo "$result" | jq -r '.structured_output.severity')
```

No edit tool in the allowlist ⇒ no writes happen, regardless of permission mode. That's how you scope "read-only."

### 2. Agentic loop on a codebase

"Review and fix," "refactor," "add tests." Model needs file access + command execution.

```bash
cd /path/to/repo
claude -p "Run the test suite and fix any failures. Report which tests you changed." \
  --allowedTools "Bash,Read,Edit" \
  --permission-mode acceptEdits \
  --output-format json > run.json
```

`acceptEdits` auto-approves writes. `dontAsk` is stricter (deny-by-default) — better for locked-down CI. Real scope control is still the allowlist.

### 3. Multi-turn agentic (chained calls sharing state)

Discrete checkpointed steps — review, decide, act — each seeing prior context.

```bash
session_id=$(claude -p "Audit the auth module for security issues" \
  --output-format json --permission-mode acceptEdits \
  --allowedTools "Read,Grep,Glob" | jq -r '.session_id')

claude -p "Now prioritize the issues you found by severity" \
  --resume "$session_id" --output-format json \
  --permission-mode acceptEdits --allowedTools "Read,Grep,Glob" > prioritized.json

claude -p "Fix the critical issues only" \
  --resume "$session_id" --permission-mode acceptEdits --allowedTools "Read,Edit"
```

First two steps are read-only via narrow tools. `--resume <id>` is explicit and parallel-safe; `--continue` (most-recent-in-cwd) races.

### 4. Parallel fan-out

Same operation across N files/PRs/tickets. Fan out via `xargs -P` or background jobs; collect into a directory, then reduce.

```bash
mkdir -p out
find . -name '*.py' -print0 | xargs -0 -P 4 -I {} bash -c '
  f="$1"
  timeout 60s claude -p "Summarize $(cat "$f") in one sentence" \
    --output-format json --permission-mode acceptEdits \
    --allowedTools "Read" \
    > "out/$(basename "$f").json"
' _ {}

jq -s 'map({file: .session_id, summary: .result})' out/*.json > summary.json
```

Bound parallelism (`-P 4`) to dodge rate limits. Per-worker `timeout` stops one runaway from stalling the batch.

### 5. Delegate to a cloud agent (async PR)

Output = a PR, no synchronous control needed. Local CLI is a dispatcher.

```bash
# Dispatch into current repo
gh agent-task create "Implement the spec in docs/rfc-042.md" --base main

# Dispatch into ANOTHER repo from outside it — no clone
gh agent-task create -F ticket.md --repo my-org/payments-service --base main

# Fan out across a fleet
gh repo list my-org --topic services --json nameWithOwner --jq '.[].nameWithOwner' | \
  while read -r repo; do
    gh agent-task create -F upgrade.md --repo "$repo" --base main
    sleep 2
  done

# Dispatch and follow logs in the foreground
gh agent-task create -F ticket.md --base main --follow
```

`--repo` is the orchestration lever — one dispatcher addresses any accessible repo. Pair with a local-execution CLI for review-gating: agent opens the PR, Claude/Codex/Gemini/Copilot reviews before merge. See `references/github-agent-task.md` for preview-status, PR-number-ambiguity, and no-JSON-from-create pitfalls.

## Principles that save you later

- **Tool restriction scopes capability, not plan mode.** Auto mode says "don't pause"; the allowlist (Claude `--allowedTools`, Codex `--sandbox`, Gemini `--policy`, Copilot `--allow-tool`) says what the agent *can* do. Read-only = narrow allowlist, not a different mode.
- **Repo context auto-loads** (CLAUDE.md, AGENTS.md, skills, MCP) — usually *why* the agent is competent here. Keep it. Strip via per-CLI config + minimal `--allowedTools` only for reproducibility or adversarial input.
- **Quote prompts aggressively.** `$`, backticks, quotes, newlines. Heredocs (`<<'EOF'`) or `--append-system-prompt-file` avoid shell-expansion bugs.

## Anti-patterns

- **Untrusted input straight into `-p`.** Prompt-injection surface. Wrap user-controlled content in delimited blocks (`<user_input>...</user_input>`) with instructions to treat as data.
- **`--continue` in parallel jobs.** Races itself — resolves to "most recent session in this cwd." Use explicit session IDs.
- **One script targeting every CLI.** Headless models differ meaningfully. Pick one, commit to its idioms; only abstract if runtime provider choice is a real requirement.

## When to load what

- **CLI-specific script** — the matching reference from the §Two categories table.
- **Detecting MCP / skills / models at runtime** (fail-fast in CI) — `references/introspection.md`.
- **Pipeline shape not covered above** (GH Action, cron PR review, batch translate, review-then-fix) — `references/cookbook.md`.

## Reusability & observability

Every automation has to be re-runnable by someone who didn't write it and auditable after the fact.

**Reusability:**

- `set -euo pipefail` at the top. Non-negotiable.
- Every path, model, timeout, parallelism bound is an arg or env var with a default: `MODEL="${MODEL:-sonnet}"`, `TIMEOUT="${TIMEOUT:-600}"`, `FILE="${1:?path required}"`. No hardcoded constants.
- Require secrets explicitly: `: "${ANTHROPIC_API_KEY:?set it}"`.
- Take an explicit `--dir` or `TARGET="${1:?}"` and `cd "$TARGET"` inside the script. Don't rely on the caller's cwd.
- Idempotent when plausible: skip if the output artifact exists unless `--force` (or env `FORCE=1`).
- Prompt text lives in a heredoc or `--append-system-prompt-file`, not inlined — swap prompts without editing shell logic.

**Observability:**

- **Stdout = machine (JSON), stderr = human (progress).** Never `2>&1` into a pipe that feeds `jq`. Progress messages go `>&2`.
- **Persist the session ID** to a file (`echo "$session_id" > .session`) — Claude/Gemini `.session_id`, Codex `.thread_id` (in `thread.started` when `--json` is on). `--continue`/`--last`/`-r latest` race under shared cwd or parallelism; always pass an explicit ID.
- **Track cost** via `.total_cost_usd` on every call; sum across a batch before you report done.
- **Live progress** on long agentic runs: `--output-format stream-json --verbose --include-partial-messages | tee progress.log`.
- **Exit-code taxonomy**: `0` success, `2` usage/input error, `3` agent reported failure (`is_error:true` or `permission_denials[]` non-empty), `124` `timeout` fired, `130` interrupted. Downstream tools branch on codes, not on stdout text.
- **Error trap** to capture state before unwinding: `trap 'git stash -u || true; cp progress.log "progress.$(date +%s).log" 2>/dev/null || true' ERR`.

## Delivering the script

Every script opens with a header a stranger can run from:

```bash
#!/usr/bin/env bash
# <name>.sh — one-line purpose
# Usage: ./<name>.sh <args> [flags]
# Env:   ANTHROPIC_API_KEY (required), MODEL (default: sonnet), TIMEOUT (default: 600)
# Posture: read-only | edits | shell  (enforced by --allowedTools "<list>")
# Output: stdout JSON; exits 0/2/3/124 — see README for taxonomy
set -euo pipefail
```
