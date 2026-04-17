# Claude Code — Headless Reference

The Claude Code CLI runs non-interactively with `-p` / `--print`. Everything below assumes a scripting context; defaults differ in interactive mode.

Docs: <https://code.claude.com/docs/en/headless>, <https://code.claude.com/docs/en/cli-reference>.

## The minimum viable invocation

```bash
claude -p "Summarize this project"
```

Prints text to stdout, then exits. No session persistence flag needed — a session is created, its ID is discoverable via `--output-format json`.

## `--bare` mode (a posture, not a default)

`--bare` is a tradeoff: you give up project context in exchange for reproducibility and lower baseline tokens. For agentic work on a codebase where `CLAUDE.md`, project skills, or `.mcp.json` servers are what make the agent competent, **do not use `--bare`** — you'll strip the instructions that tell the agent how to behave on *this* codebase. Use it when (a) the task doesn't need repo context (classification/extraction of a single file), (b) you need identical behavior across machines with different `~/.claude` setups, (c) you're running on untrusted code where a hostile `CLAUDE.md` could change behavior, or (d) you're cost-sensitive and the ~38k cache-creation token baseline from CLAUDE.md auto-load matters.

```bash
claude --bare -p "Summarize this file" --allowedTools "Read"
```

`--bare` skips: hooks, LSP, plugin sync, auto-memory, attribution, background prefetches, keychain reads, and CLAUDE.md auto-discovery. Authentication falls back to `ANTHROPIC_API_KEY` env var or `apiKeyHelper` via `--settings`.

Use `--bare` whenever:
- You're running in CI and need identical behavior across machines.
- You don't want a teammate's `~/.claude/hooks` or a `.mcp.json` in the repo to silently affect the run.
- You want faster startup.

You will still get the Bash, Read, and Edit tools by default. Pass extra context explicitly:

| Load                    | Flag                                                    |
| ----------------------- | ------------------------------------------------------- |
| System prompt additions | `--append-system-prompt`, `--append-system-prompt-file` |
| Settings                | `--settings <file-or-json>`                             |
| MCP servers             | `--mcp-config <file-or-json>`                           |
| Custom agents           | `--agents <json>`                                       |
| A plugin directory      | `--plugin-dir <path>`                                   |

Note from the docs: `--bare` will become the default for `-p` in a future release. Adopt it now.

## Output formats

`--output-format` controls what goes to stdout.

| Format        | When to use                                                                      |
| ------------- | -------------------------------------------------------------------------------- |
| `text` (default) | Human reading stdout. Do not parse with regex — it's prose.                   |
| `json`        | Scripts. Single JSON object with fields: `type`, `subtype`, `is_error`, `api_error_status`, `duration_ms`, `duration_api_ms`, `num_turns`, `result`, `stop_reason`, `session_id`, `total_cost_usd`, `usage`, `modelUsage`, `permission_denials`, `terminal_reason`, `fast_mode_state`, `uuid`. On error, an `errors` array is added. `structured_output` appears only when `--json-schema` was passed. |
| `stream-json` | Live UIs, long runs, progress. Newline-delimited JSON events. Requires `--verbose`; add `--include-partial-messages` to stream individual token deltas. |

### JSON-with-schema (structured output)

Constrain the model's final answer to match a JSON Schema:

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

Schema violations cause the run to fail — the CLI validates before returning. Keep schemas as simple as the downstream consumer actually needs.

### Stream events you'll see

- `system/init` — session metadata. Fields: `model`, `tools`, `mcp_servers`, `plugins`, `plugin_errors`.
- `system/api_retry` — API retry happened. Fields: `attempt`, `max_retries`, `retry_delay_ms`, `error_status`, `error` (category like `rate_limit`, `server_error`).
- `system/plugin_install` — only when `CLAUDE_CODE_SYNC_PLUGIN_INSTALL` is set.
- `stream_event` — partial message chunks when `--include-partial-messages` is on.
- `assistant` / `tool_use` / `tool_result` — the conversation turns.
- A final `result` event with usage, cost, duration.

Filter text deltas with `jq`:

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

`-r` = raw strings, `-j` = no newline between items (so tokens concatenate).

Fail CI if a plugin didn't load:

```bash
claude -p "..." --output-format stream-json --verbose | \
  jq -e 'select(.type == "system" and .subtype == "init") | .plugin_errors // empty | length == 0'
```

## Permissions & tools

Two levers: what tools are available (`--allowedTools` / `--disallowedTools`) and what to do when the model wants to use one (`--permission-mode`).

### `--permission-mode`

| Mode                | Behavior                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| `default`           | **Do not use in scripts.** Prompts for approval — in headless runs this blocks or silently denies. |
| `auto`              | **Do not use in scripts.** Claude decides from context — non-deterministic for automation.        |
| `plan`              | Read-only planning mode. Can't edit or run commands. Good for investigation/review.              |
| `acceptEdits`       | Auto-approves file writes and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`). Other shell commands still need `--allowedTools`. The agentic-dev default for scripts. |
| `dontAsk`           | Denies anything not in `permissions.allow` or the read-only command set. Locked-down CI choice. |
| `bypassPermissions` | Allows everything without asking. Same as `--dangerously-skip-permissions`. Sandboxed envs only. |

**Rule of thumb for automation:** pick `plan`, `acceptEdits`, `dontAsk`, or `bypassPermissions`. If you find yourself reaching for `default` or `auto`, you've picked the wrong tool — those are interactive-mode modes.

### `--allowedTools` rule syntax

Comma- or space-separated list of tool names, optionally scoped with rule expressions.

```bash
--allowedTools "Read,Edit,Bash(git diff *),Bash(git log *)"
```

- `Read` — bare tool name allows the tool for all invocations.
- `Bash(git diff *)` — scoped. Prefix matching with `*`. The space before `*` matters: `Bash(git diff*)` also matches `git diff-index`; `Bash(git diff *)` does not.
- `--disallowedTools` takes the same syntax and overrides `--allowedTools`.

Common allowlist recipes:

| Task                     | Allowlist                                                                   |
| ------------------------ | --------------------------------------------------------------------------- |
| Read-only code review    | `"Read,Grep,Glob"`                                                           |
| Auto-fix lint/tests      | `"Read,Edit,Bash(npm test*),Bash(npm run lint*)"` + `--permission-mode acceptEdits` |
| Auto-commit              | `"Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git add *),Bash(git commit *)"` |
| Just research the repo   | `"Read,Grep,Glob,Bash(rg *)"` + `--permission-mode plan`                    |

### `--tools` (built-in set override)

`--tools` replaces the default built-in tool set (not the same as `--allowedTools`). Values: a comma-separated name list, `"default"`, or `""` (disables all built-ins). Use when you want, e.g., no Bash at all even for read-only commands.

## Sessions & multi-turn

```bash
# Capture session_id
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')

# Continue
claude -p "Focus on database queries" --resume "$session_id"
```

- `--resume <uuid>` — explicit, parallel-safe.
- `-c` / `--continue` — "most recent session in cwd". Convenient for the shell; dangerous in parallel.
- `--fork-session` — when resuming, create a new session ID instead of mutating the original (good for branching investigations).
- `--session-id <uuid>` — use a specific UUID. Useful if your pipeline generates IDs.
- `--no-session-persistence` — don't persist to disk at all. Fire-and-forget single-turn.
- `--from-pr <number|url>` — resume a session linked to a PR.

## Cost & budget

| Flag                      | Effect                                                                    |
| ------------------------- | ------------------------------------------------------------------------- |
| `--max-budget-usd <amt>`  | Hard cap in USD for the run. Aborts the run if exceeded. Unattended scripts should always set this. |
| `--effort <level>`        | `low`, `medium`, `high`, `xhigh`, `max`. Trades cost for quality.         |
| `--model <name>`          | `sonnet`, `opus`, `haiku`, or a full ID. Haiku for bulk/cheap, opus for hard problems. |
| `--fallback-model <name>` | Used when default is overloaded. `-p` only.                               |

The JSON output includes `total_cost_usd` (total), `modelUsage[<model-id>].costUSD` (per-model), and `usage.{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}` for post-run accounting.

**`--max-budget-usd` is advisory, not preventive.** Empirically, a single turn with heavy cache-creation can overshoot a small cap — the budget check happens after each iteration, not before. When exceeded, the run aborts with `subtype: "error_max_budget_usd"`, `is_error: true`, and `errors: ["Reached maximum budget ($X)"]`. Set caps with a 2-5x safety margin over expected cost, and always verify `is_error` / `total_cost_usd` post-run rather than trusting the cap as a hard ceiling.

## Passing context

| Flag                            | Purpose                                                                |
| ------------------------------- | ---------------------------------------------------------------------- |
| `--add-dir <dir...>`            | Grant tool access to additional directories beyond cwd.                |
| `--append-system-prompt <text>` | Add instructions on top of the default system prompt.                  |
| `--append-system-prompt-file <f>` | Same, read from file (avoids quoting hell).                          |
| `--system-prompt <text>`        | Replace the default system prompt entirely. Advanced.                  |
| `--system-prompt-file <f>`      | Same, from file.                                                       |
| `--file <specs>`                | Pre-download file resources: `file_id:relative_path`.                  |
| `--agents <json>`               | Define ad-hoc sub-agents inline: `'{"reviewer":{"description":"...","prompt":"..."}}'`. |
| `--setting-sources user,project,local` | Control which settings files load (in `--bare` you pass settings explicitly). |

### stdin for prompts

`claude -p` reads a prompt as an argument. For large prompts or piped input, use heredocs in the script:

```bash
claude -p "$(cat <<'EOF'
Review this diff for security issues:

$(gh pr diff 1234)
EOF
)" --append-system-prompt "You are a security reviewer."
```

Or put the prompt in a file and `cat` it in.

### stream-json input

```bash
claude -p --input-format stream-json --output-format stream-json --verbose < input.jsonl
```

For programs that want to drive Claude turn-by-turn over a pipe. Rare in shell automation; more common when embedding in another tool. See the Agent SDK docs if you need this.

## Exit codes & errors

- `0` — success.
- Non-zero — error (budget exceeded, schema validation failure, permission denial, API error, etc.). Check stderr; with `--output-format json`, the final JSON may contain error details.

Retry logic: Claude Code retries retryable API errors internally and emits `system/api_retry` events. You don't usually need to retry the whole invocation unless the run aborts — but wrapping unattended calls in a retry loop with exponential backoff is still wise for resilience to transient local issues.

## Authentication (esp. in `--bare`)

In normal mode Claude Code uses OAuth and the macOS keychain. `--bare` skips both. Accepted auth sources in `--bare`:

1. `ANTHROPIC_API_KEY` env var.
2. An `apiKeyHelper` command in a JSON passed to `--settings` (e.g., a small script that fetches from a secrets manager).
3. Provider-specific creds for Bedrock (`AWS_*`), Vertex (`GOOGLE_APPLICATION_CREDENTIALS` + `CLAUDE_CODE_USE_VERTEX=1`), Foundry, etc.

In CI: put the API key in a secret, export it before invoking.

## Gotchas

- **Workspace trust dialog is skipped in `-p` mode.** Only run scripts in directories you trust — a hostile `.claude/` or CLAUDE.md could change behavior.
- **Slash commands and skills aren't callable in `-p` mode** (e.g., `/commit`). Describe the task in the prompt instead.
- **`--output-format json` with a huge response** — the final JSON is a single object; very large `result` fields can be awkward to parse with some `jq` versions. Consider `stream-json` + filtering for long outputs.
- **Permission denials abort the run.** In `dontAsk` mode, a single unscoped Bash call kills the whole task. Allowlist precisely.
- **`--continue` in parallel jobs** resolves to "most recent in cwd" and races. Always use `--resume <id>` for parallelism.
- **Budget resets each invocation.** `--max-budget-usd` is per-run. Running three chained calls with `--max-budget-usd 1.00` caps each individually, not the total.
- **Without `--bare`, CLAUDE.md auto-discovery inflates input tokens.** Empirically a trivial "reply: ok" prompt in a repo with CLAUDE.md consumed ~38k cache-creation tokens before producing any output. If you're in CI or running the same prompt many times, `--bare` is a cost difference, not just a speed one.
- **Error responses still return exit 0 in some cases.** Always check `is_error` / `subtype` in the JSON output, especially when budget caps or schema validation could fail the run.
