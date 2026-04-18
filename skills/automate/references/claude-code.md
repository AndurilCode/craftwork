# Claude Code — Headless Reference

`claude -p` / `--print`. Docs: <https://code.claude.com/docs/en/headless>, <https://code.claude.com/docs/en/cli-reference>.

## The minimum viable invocation

```bash
claude -p "Summarize this project" --permission-mode acceptEdits --allowedTools "Read"
```

Prints text to stdout, then exits. Session ID is in `--output-format json`.

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
  --permission-mode acceptEdits --allowedTools "Read" \
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
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages \
  --permission-mode acceptEdits --allowedTools "Read" | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

`-r` = raw strings, `-j` = no newline between items (so tokens concatenate).

Fail CI if a plugin didn't load:

```bash
claude -p "..." --output-format stream-json --verbose \
  --permission-mode acceptEdits --allowedTools "Read" | \
  jq -e 'select(.type == "system" and .subtype == "init") | .plugin_errors // empty | length == 0'
```

## Permissions & tools

Two levers: `--allowedTools` / `--disallowedTools` (what's available) and `--permission-mode` (what to do on use). Scope via the allowlist.

### `--permission-mode`

All six modes complete in `-p`. What differs is what the agent *does* on a tool call:

| Mode                | Behavior                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| `default` / `auto`  | Classifier-gated (`claude auto-mode defaults`). Safe actions pass, risky ones denied — verdict depends on transcript heuristics. **Non-reproducible; avoid in scripts.** |
| `plan`              | Agent refuses writes in-turn ("Plan mode is active…") and returns a plan. No action taken. For read-only script work, use `acceptEdits` + `--allowedTools "Read,Grep,Glob"`. |
| `acceptEdits`       | Auto-approves writes and common filesystem commands. Other shell commands need `--allowedTools`. Script default. |
| `dontAsk`           | Denies anything not in `permissions.allow` or the read-only set. Locked-down CI. |
| `bypassPermissions` | Allows everything. Same as `--dangerously-skip-permissions`. Sandboxed envs only. |

**Rule of thumb:** pick `acceptEdits`, `dontAsk`, or `bypassPermissions` — the three deterministic modes, gated by `--allowedTools` + `permissions.allow` you set.

### `--allowedTools` rule syntax

Comma- or space-separated list of tool names, optionally scoped with rule expressions.

```bash
--allowedTools "Read,Edit,Bash(git diff *),Bash(git log *)"
```

- `Read` — bare tool name allows the tool for all invocations.
- `Bash(git diff *)` — scoped. Prefix matching with `*`. The space before `*` matters: `Bash(git diff*)` also matches `git diff-index`; `Bash(git diff *)` does not.
- `--disallowedTools` takes the same syntax and overrides `--allowedTools`.

Common allowlist recipes (all paired with `--permission-mode acceptEdits` unless noted):

| Task                     | Allowlist                                                                   |
| ------------------------ | --------------------------------------------------------------------------- |
| Read-only code review    | `"Read,Grep,Glob"`                                                           |
| Auto-fix lint/tests      | `"Read,Edit,Bash(npm test*),Bash(npm run lint*)"`                          |
| Auto-commit              | `"Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git add *),Bash(git commit *)"` |
| Just research the repo   | `"Read,Grep,Glob,Bash(rg *)"`                                                |

### `--tools` (built-in set override)

`--tools` replaces the default built-in tool set (not the same as `--allowedTools`). Values: a comma-separated name list, `"default"`, or `""` (disables all built-ins). Use when you want, e.g., no Bash at all even for read-only commands.

## Sessions & multi-turn

```bash
# Capture session_id
session_id=$(claude -p "Start a review" --output-format json \
  --permission-mode acceptEdits --allowedTools "Read,Grep,Glob" | jq -r '.session_id')

# Continue
claude -p "Focus on database queries" --resume "$session_id" \
  --permission-mode acceptEdits --allowedTools "Read,Grep,Glob"
```

- `--resume <uuid>` — explicit, parallel-safe.
- `-c` / `--continue` — "most recent session in cwd". Convenient for the shell; dangerous in parallel.
- `--fork-session` — when resuming, create a new session ID instead of mutating the original (good for branching investigations).
- `--session-id <uuid>` — use a specific UUID. Useful if your pipeline generates IDs.
- `--no-session-persistence` — don't persist to disk at all. Fire-and-forget single-turn.
- `--from-pr <number|url>` — resume a session linked to a PR.

## Model & effort

| Flag                      | Effect                                                                    |
| ------------------------- | ------------------------------------------------------------------------- |
| `--effort <level>`        | `low`, `medium`, `high`, `xhigh`, `max`. Trades cost for quality.         |
| `--model <name>`          | `sonnet`, `opus`, `haiku`, or a full ID. Haiku for bulk/cheap, opus for hard problems. |
| `--fallback-model <name>` | Used when default is overloaded. `-p` only.                               |

The JSON output includes `total_cost_usd`, `modelUsage[<model-id>].costUSD`, and `usage.{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}` for post-run accounting. Use wall-clock `timeout <N>s` to cap runaway runs.

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
| `--setting-sources user,project,local` | Control which settings files load.                              |
| `--settings <file-or-json>`     | Load an explicit settings blob (useful for CI reproducibility).        |
| `--mcp-config <file-or-json>`   | Point at a specific MCP server set instead of auto-discovery.          |
| `--plugin-dir <path>`           | Load plugins from a specific directory.                                |

### stdin for prompts

`claude -p` reads a prompt as an argument. For large prompts or piped input, use heredocs in the script:

```bash
claude -p "$(cat <<'EOF'
Review this diff for security issues:

$(gh pr diff 1234)
EOF
)" --append-system-prompt "You are a security reviewer." \
  --permission-mode acceptEdits --allowedTools "Read,Grep,Glob"
```

Or put the prompt in a file and `cat` it in.

### stream-json input

```bash
claude -p --input-format stream-json --output-format stream-json --verbose \
  --permission-mode acceptEdits --allowedTools "Read,Edit" < input.jsonl
```

For programs that want to drive Claude turn-by-turn over a pipe. Rare in shell automation; more common when embedding in another tool. See the Agent SDK docs if you need this.

## Exit codes & errors

- `0` — success.
- Non-zero — error (schema validation failure, permission denial, API error, timeout, etc.). Check stderr; with `--output-format json`, the final JSON may contain error details.

Retryable API errors are handled internally (emits `system/api_retry`). Wrap unattended calls in an outer retry loop only for transient local issues.

## Authentication

Claude Code uses OAuth and the macOS keychain by default. In CI or headless environments without a keychain:

1. `ANTHROPIC_API_KEY` env var.
2. An `apiKeyHelper` command in a JSON passed to `--settings` (e.g., a small script that fetches from a secrets manager).
3. Provider-specific creds for Bedrock (`AWS_*`), Vertex (`GOOGLE_APPLICATION_CREDENTIALS` + `CLAUDE_CODE_USE_VERTEX=1`), Foundry, etc.

In CI: put the API key in a secret, export it before invoking.

## Gotchas

- **Workspace trust dialog is skipped in `-p` mode.** Only run scripts in directories you trust — a hostile `.claude/` or CLAUDE.md could change behavior. For defence-in-depth on adversarial inputs, pass an explicit `--settings`, `--mcp-config`, and a narrow `--allowedTools` list so nothing in the repo can grow the surface.
- **Slash commands and skills aren't callable in `-p` mode** (e.g., `/commit`). Describe the task in the prompt instead.
- **`--output-format json` with a huge response** — the final JSON is a single object; very large `result` fields can be awkward to parse with some `jq` versions. Consider `stream-json` + filtering for long outputs.
- **Permission denials abort the run.** In `dontAsk` mode, a single unscoped Bash call kills the whole task. Allowlist precisely.
- **`--continue` in parallel jobs** resolves to "most recent in cwd" and races. Always use `--resume <id>` for parallelism.
- **CLAUDE.md auto-discovery inflates input tokens.** Empirically a trivial "reply: ok" prompt in a repo with CLAUDE.md consumed ~38k cache-creation tokens before producing any output. In CI, either accept this (context is usually *why* the agent is competent) or feed an explicit `--settings` + `--setting-sources` combo that loads only what the task needs.
- **Error responses still return exit 0 in some cases.** Always check `is_error` / `subtype` in the JSON output, especially when schema validation or tool permissions could fail the run.
