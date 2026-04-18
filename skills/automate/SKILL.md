---
name: automate
description: Build automation scripts and pipelines that use coding-agent CLIs (Claude Code, Codex, Gemini CLI, GitHub Copilot CLI) in headless/non-interactive mode as the AI engine, or delegate work to cloud agents (`gh agent-task`) that open pull requests asynchronously. Use this skill whenever the user wants to write a shell script, CI job, cron task, batch processor, webhook handler, or any automation that shells out to `claude`, `codex`, `gemini`, `copilot`, or `gh agent-task` — single-turn prompts, multi-turn agentic loops, parallel fan-out across files/folders, structured JSON outputs consumed by downstream tools, or cloud-delegated tasks that produce PRs. Trigger on phrases like "script that uses Claude", "automate with Claude Code", "headless Claude", "batch process files with an LLM", "pipeline with codex exec", "gemini -p", "copilot --autopilot", "gh agent-task create", "GitHub Action that calls Claude", "cron job to review PRs", "agent loop in bash", "dispatch an agent task to open a PR", "fleet-wide agent-task across repos", or any request to integrate a coding agent CLI into an automated workflow. Also trigger when the user describes the shape of a pipeline (fan-out, map-reduce, review-then-fix, extract-then-summarize, ticket-to-PR, scheduled fleet upgrade) and AI is the engine, even if they don't name the CLI explicitly.
---

# Coding-Agent CLI Automation

## Two categories

Pick the category before the tool:

1. **Local execution** — agent runs on your machine or CI runner against cwd. Synchronous, output to stdout, you decide what happens. For anything that produces artifacts other than PRs (reports, JSON, edits, batch transforms).
2. **Delegated cloud execution** — dispatch to a cloud agent that works asynchronously and opens a PR. For ticket/issue/webhook-triggered "implement this and open a PR" workflows.

| CLI | Headless invocation | Reference |
|-----|--------------------|-----------|
| Claude Code | `claude -p "<prompt>"` | `references/claude-code.md` |
| Codex | `codex exec "<prompt>"` | `references/codex.md` |
| Gemini CLI | `gemini -p "<prompt>"` | `references/gemini.md` |
| GitHub Copilot CLI | `copilot -p "<prompt>" --allow-all-tools --autopilot` | `references/copilot.md` |
| `gh agent-task` (cloud) | `gh agent-task create "<description>" --base main` | `references/github-agent-task.md` |

The two can be combined — `gh agent-task` opens the PR, a local CLI reviews it (see cookbook). **Default to Claude Code** unless the user names another. Load the relevant reference when you commit to a CLI.

## Non-negotiable flags (the checklist)

**Local execution (`claude` / `codex` / `gemini` / `copilot`):**

- [ ] **Deterministic auto mode.** Claude: `acceptEdits` / `dontAsk` / `bypassPermissions`. Codex: `--sandbox <read-only|workspace-write|danger-full-access>`. Gemini: `--approval-mode auto_edit` or `yolo`. Copilot: `--autopilot` + `--allow-all-tools` + `--no-ask-user`. See the auto-mode menu below for the full comparison.
- [ ] **`--allowedTools` narrow allowlist — the real safety boundary.** Auto mode means "don't pause for approval"; the allowlist defines what the agent can do. Read-only? `"Read,Grep,Glob"`. Dev? `"Read,Edit,Bash(npm test*)"`.
- [ ] **`--output-format json`** when the next step is a shell pipeline. Never parse `text` with regex/grep/sed.
- [ ] **Structured-output constraint** (`--json-schema` for Claude, `--output-schema` for Codex) when output feeds downstream code. Stops the model from drifting into prose / invalid enums so your `jq` pipeline can't silently break.
- [ ] **Verify success in the JSON** (`is_error`, `subtype`, `errors[]`, `permission_denials[]`), not just exit code. All four CLIs can exit 0 on recoverable failures.

**Delegated cloud execution (`gh agent-task`):**

- [ ] **Explicit `--base <branch>`.** A PR opened against `develop` when you meant `main` wastes a review cycle.
- [ ] **`create` exit 0 = "dispatched," not "succeeded" and not "merged."** The agent runs after the command returns. Pair dispatch with a completion watcher (`gh pr list`, `pull_request.opened` webhook, or `--follow` in the foreground).
- [ ] **`--repo <owner/name>`** when targeting another repo. One dispatcher can address any repo you have access to without cloning.
- [ ] **Long ticket bodies via `-F <file>` / stdin**, never inlined as argv. Avoids quoting bugs and arg-length limits.

## The five canonical shapes

Shapes 1-4 are local execution; shape 5 is cloud delegation.

### 1. Single-turn, extract to JSON

Classification, extraction, summarization, triage. Script gets a structured answer it can parse.

```bash
result=$(claude -p "Classify the severity of this error: $(cat error.log)" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"severity":{"type":"string","enum":["low","medium","high","critical"]},"reason":{"type":"string"}},"required":["severity","reason"]}' \
  --permission-mode acceptEdits \
  --allowedTools "Read")

severity=$(echo "$result" | jq -r '.structured_output.severity')
```

No edit tool in the allowlist ⇒ no writes happen, regardless of permission mode. That's how you scope "read-only" in a script.

### 2. Agentic loop on a codebase

"Review and fix," "refactor," "add tests." Model needs file access + command execution.

```bash
cd /path/to/repo
claude -p "Run the test suite and fix any failures. Report which tests you changed." \
  --allowedTools "Bash,Read,Edit" \
  --permission-mode acceptEdits \
  --output-format json > run.json
```

`acceptEdits` auto-approves writes. `dontAsk` is stricter (deny-by-default) — better for locked-down CI. The real scope control is still the allowlist.

### 3. Multi-turn agentic (chained calls sharing state)

Discrete steps with checkpoints — review, decide, act — each seeing prior context.

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

Same operation against N files/PRs/tickets. Fan out via `xargs -P` or background jobs; collect into a directory, then reduce.

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

Bound parallelism (`-P 4`) to dodge rate limits. `timeout` per worker stops one runaway from stalling the batch.

### 5. Delegate to a cloud agent (async PR)

Output = a pull request, no synchronous control needed. Local CLI is a dispatcher.

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

- **Auto-mode menu** — tool restriction, not a plan mode, is how you scope capability in a script:

  | CLI | Auto + read-only (via tools) | Auto + edits | Auto + unrestricted | Never use in scripts |
  |-----|-----------------------------|--------------|---------------------|----------------------|
  | Claude | `acceptEdits` + `--allowedTools "Read,Grep,Glob"` | `acceptEdits` / `dontAsk` + edit allowlist | `bypassPermissions` | `plan` / `default` / `auto` |
  | Codex | `--sandbox read-only` | `--full-auto` / `--sandbox workspace-write` | `--sandbox danger-full-access` | — (the flag is the posture) |
  | Gemini | `--approval-mode auto_edit` + read-only policy | `--approval-mode auto_edit` | `--approval-mode yolo` | `plan` / `default` |
  | Copilot | `--autopilot` + narrow `--allow-tool` list | `--autopilot` + `--allow-all-tools` + `--no-ask-user` | `--yolo` / `--allow-all` | `--plan` / `--mode interactive` |

- **Repo context auto-loads** (CLAUDE.md, AGENTS.md, skills, MCP) — usually *why* the agent is competent here, so keep it. Strip via per-CLI config overrides + minimal `--allowedTools` only for reproducibility or adversarial input. Per-CLI details in the references.

- **Capture session IDs for chained calls.** Claude/Gemini: `.session_id`; Codex: `.thread_id` (in `thread.started` when `--json` is on). Stash it early — `--continue` / `--last` / `-r latest` break under shared cwd or parallelism.

- **Stream for progress, JSON to parse.** `--output-format stream-json --verbose --include-partial-messages` for live feedback; plain `json` for `jq`.

- **Don't mix stdout channels.** If the CLI writes JSON to stdout, send progress to stderr (`>&2`). Gemini writes `[WARN]` to stderr on unreadable subdirs — don't `2>&1` into a pure-JSON pipe.

- **Quote prompts aggressively.** `$`, backticks, quotes, newlines. Heredocs (`<<'EOF'`) or `--append-system-prompt-file` avoid shell-expansion bugs.

- **Hygiene wrappers.** `trap 'git stash -u' ERR` to rescue a partial agentic run; `timeout <N>s ...` around every unattended invocation to cap infinite loops, network stalls, or agents that won't stop.

## Anti-patterns

- **Untrusted input straight into `-p`.** Prompt-injection surface. Wrap user-controlled content in clearly-delimited blocks (`<user_input>...</user_input>`) with instructions to treat it as data.
- **`--continue` in parallel jobs.** Races itself — resolves to "most recent session in this cwd." Use explicit session IDs.
- **One script targeting every CLI.** The headless models differ meaningfully. Pick one, commit to its idioms; only abstract if runtime provider choice is a real requirement.

## When to load what

| Scenario | Reference |
|---|---|
| Writing a Claude Code script (flags, output schemas, permissions) | `references/claude-code.md` |
| Writing a Codex script (sandbox modes, `--output-schema`, resume) | `references/codex.md` |
| Writing a Gemini script (approval modes, policy engine, sessions) | `references/gemini.md` |
| Writing a Copilot script (mode flags, `--allow-all-tools` / `--no-ask-user`, output formats) | `references/copilot.md` |
| Ticket/issue → PR pipelines, fleet dispatch, dispatch-then-review | `references/github-agent-task.md` |
| Detecting MCP / skills / models at runtime (fail-fast in CI) | `references/introspection.md` |
| A pipeline shape you haven't built (GH Action, cron PR review, batch translate, review-then-fix) | `references/cookbook.md` |

## Delivering the script

Include a header with: usage + required env vars; permission posture (read-only / edits / shell) and the `--allowedTools` list that enforces it; tunable flags (model, dir, timeout).
