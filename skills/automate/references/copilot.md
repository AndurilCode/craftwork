# GitHub Copilot CLI — Headless Reference

GitHub's Copilot CLI runs non-interactively with `-p` / `--prompt`. Without `-p` it launches the TUI.

Official: run `copilot help commands`, `copilot help environment`, `copilot help permissions` for the authoritative local reference.

## The minimum viable invocation

```bash
copilot -p "Summarize this project" --allow-all-tools
```

**`--allow-all-tools` is required for non-interactive mode.** This is explicit in the `--help` text — without it, Copilot has no way to proceed when a tool needs permission and there's no human to ask.

For clean output suitable for piping:

```bash
copilot -p "Summarize this project" --allow-all-tools -s
```

`-s` / `--silent` suppresses stats and ancillary lines, leaving only the agent's response on stdout.

## Mode selection

```
--mode <interactive|plan|autopilot>
--autopilot            # alias for --mode autopilot
--plan                 # alias for --mode plan
```

| Mode          | Behavior                                                                     |
| ------------- | ---------------------------------------------------------------------------- |
| `interactive` | **Do not use in scripts.** Prompts for every tool action.                    |
| `plan`        | Read-only planning. Good for investigation/review in scripts.                |
| `autopilot`   | Autonomous execution; agent continues turns without asking. The script default for agentic work. |

Cap autonomous runs:
```
--max-autopilot-continues <N>   # limit continuation messages (default: unlimited)
--no-ask-user                   # disable the ask_user tool entirely
```

`--no-ask-user` is important in autopilot: without it, the agent can still pause to ask a clarifying question mid-run — fine interactively, hanging in a script.

## Output formats

```
--output-format <text|json>     # json = JSONL (one event per line)
-s, --silent                    # text mode: suppress stats
--stream <on|off>               # streaming deltas
```

### JSONL event types (empirically observed)

| Event type                          | Purpose                                                         |
| ----------------------------------- | --------------------------------------------------------------- |
| `session.mcp_server_status_changed` | MCP server connection state changes.                            |
| `session.mcp_servers_loaded`        | Final MCP load summary (successes + failures).                  |
| `session.skills_loaded`             | Skills registry loaded (includes each skill's metadata).        |
| `session.tools_updated`             | Available tool list updated.                                    |
| `user.message`                      | The user turn that initiated the exchange.                      |
| `assistant.turn_start`              | A model turn begins.                                            |
| `assistant.message_delta`           | Streaming token chunks (when `--stream on`).                    |
| `assistant.message`                 | Complete assistant message.                                     |
| `assistant.turn_end`                | Turn finished.                                                  |
| `result`                            | Final event. See shape below.                                   |

### Final `result` event

```json
{
  "type": "result",
  "timestamp": "2026-04-17T17:54:04.209Z",
  "sessionId": "992440ff-d268-4198-95fb-992eb96cbf0c",
  "exitCode": 0,
  "usage": {
    "premiumRequests": 3,
    "totalApiDurationMs": 3198,
    "sessionDurationMs": 7422,
    "codeChanges": {
      "linesAdded": 0,
      "linesRemoved": 0,
      "filesModified": []
    }
  }
}
```

- **`sessionId`** (camelCase) — not `session_id` like Claude/Gemini, not `thread_id` like Codex.
- **`exitCode`** is reported in the event; also reflected in the process exit code.
- **`usage.premiumRequests`** — Copilot bills in "premium requests," not tokens. No `total_cost_usd` field. Budget control is about request count, not token spend.
- **`usage.codeChanges`** — useful for auditing what the run actually modified.

Extract the final answer and session ID:

```bash
out=$(copilot -p "task" --allow-all-tools --autopilot --output-format json 2>/dev/null)
result=$(echo "$out" | jq -c 'select(.type == "result")')
session_id=$(echo "$result" | jq -r '.sessionId')
exit_code=$(echo "$result" | jq -r '.exitCode')
answer=$(echo "$out" | jq -sr 'map(select(.type == "assistant.message")) | last | .data.content // .content // empty')
```

## Permissions & tools

Copilot's permission system is fine-grained. Three axes: tools, file paths, URLs.

### Tools

```
--allow-all-tools           # required for non-interactive (also env COPILOT_ALLOW_ALL)
--allow-tool='<spec>'       # allow a specific tool or pattern
--deny-tool='<spec>'        # deny a specific tool or pattern (precedence over allow)
--available-tools=<list>    # restrict the universe of tools the model sees
--excluded-tools=<list>     # remove specific tools from availability
```

Rule syntax for `--allow-tool` / `--deny-tool` (per `--help` examples):
- `write` — the file-writing tool.
- `shell(git:*)` — any `git` subcommand.
- `shell(git push)` — exactly `git push` (combine with `--deny-tool` to subtract from a broader allow).

Recipe: allow all git EXCEPT push:
```bash
copilot -p "commit the staged changes" \
  --autopilot \
  --allow-tool='shell(git:*)' \
  --deny-tool='shell(git push)'
```

### File paths

```
--add-dir <dir>             # add a directory to the allowed list (repeatable)
--allow-all-paths           # disable path verification (dangerous)
--disallow-temp-dir         # revoke the auto-allowed temp dir
```

### URLs

```
--allow-url=<url-or-domain>
--deny-url=<url-or-domain>  # precedence over --allow-url
--allow-all-urls
```

### The nuclear options

```
--allow-all         # = --allow-all-tools --allow-all-paths --allow-all-urls
--yolo              # alias for --allow-all
```

Use only in sandboxed environments. Treat as a red flag in any PR.

**Rule of thumb for automation:** `--autopilot --allow-all-tools --no-ask-user` + specific `--allow-tool` / `--add-dir` rules for what the task actually needs. Reach for `--yolo` only when the environment itself is the sandbox.

## Working directory & scope

| Flag                | Effect                                                              |
| ------------------- | ------------------------------------------------------------------- |
| `--add-dir <dir>`   | Allow file access to an additional directory (repeatable).          |
| `--config-dir <dir>` | Override `~/.copilot` config location for this run.                |

Copilot runs against cwd by default; add other dirs explicitly.

## Context posture (AGENTS.md, skills, MCP)

Copilot auto-loads:
- `AGENTS.md` and related custom instruction files
- User skills from `~/.copilot/` or equivalent (surfaced via the `session.skills_loaded` event)
- MCP servers from `~/.copilot/mcp-config.json`
- Plugins

```
--no-custom-instructions          # disable AGENTS.md and related — the "--bare" equivalent
--disable-builtin-mcps            # disable built-in MCPs (currently github-mcp-server)
--disable-mcp-server <name>       # disable a specific MCP server (repeatable)
--additional-mcp-config <json>    # add MCPs for this session (JSON string or @file)
--plugin-dir <dir>                # load a plugin from a local dir (repeatable)
```

**Same posture decision as the other CLIs:** agentic work on a codebase usually wants `AGENTS.md` and project skills loaded — they encode the conventions that make the agent competent. Strip context (`--no-custom-instructions` + `--disable-builtin-mcps`) only for reproducible CI, cost-sensitive batch jobs on a single file, or adversarial/untrusted runs.

### GitHub MCP server control

Copilot ships with a built-in GitHub MCP server. Tune which tools it exposes:

```
--add-github-mcp-tool <tool>        # enable a specific tool (repeatable; "*" = all)
--add-github-mcp-toolset <toolset>  # enable a toolset (repeatable; "all" = all)
--enable-all-github-mcp-tools       # full firehose
```

By default it's a curated subset. Expand deliberately — full toolset access is a big authority grant.

## Sessions

```bash
copilot --continue                              # resume most recent
copilot --resume                                # interactive picker
copilot --resume=<session-id>                   # specific session
copilot --resume=0cb916db-26aa-40f2-86b5-1ba81b225fd2 "follow-up"
```

Session IDs are UUIDs; capture `.sessionId` from the `result` event and reuse it for parallel-safe chaining (don't rely on `--continue`, which is "most recent in context").

## Model & reasoning

```
--model <model>                         # e.g., gpt-5.2
--effort / --reasoning-effort <low|medium|high|xhigh>
--enable-reasoning-summaries            # request reasoning summaries for OpenAI models
--agent <agent>                         # use a custom agent
```

## Authentication

```bash
copilot login
```

Uses GitHub OAuth. Requires a GitHub Copilot subscription. For CI, seed the auth file as a secret (check `copilot help environment` for the exact variable — Copilot's auth state lives in its config dir, not a simple `API_KEY` env var).

The `COPILOT_ALLOW_ALL` env var is equivalent to `--allow-all-tools`; prefer the flag in CI so intent is explicit in the workflow file.

## Output sharing

```
--share[=path]       # write a markdown transcript after completion
--share-gist         # publish to a secret GitHub gist
```

`--share` is helpful for PR-review automation: write the transcript to the workflow's artifact dir and link it from the PR comment.

## Security

```
--secret-env-vars=<vars>   # strip these env vars from shell/MCP environments and redact from output
--no-remote                # disable remote control from GitHub web/mobile
```

For CI: always use `--secret-env-vars` to name any secrets the runner has set, so they don't leak into tool output or MCP logs.

## Gotchas

- **`--allow-all-tools` is mandatory for `-p` mode.** Forgetting it means the run stalls on the first tool permission request. This is by design but the error message isn't obvious.
- **Exit code IS meaningful** (unlike Codex). `exitCode` in the `result` event matches the process exit. Safe to use `$?` for quick success checks.
- **Billing is in "premium requests," not tokens.** No direct dollar figure in the output. For budget control, cap turns with `--max-autopilot-continues` and wrap with `timeout`.
- **Auto-loads your personal skills and MCP servers.** In a fresh `/tmp` dir a trivial run surfaced every skill registered on the machine via `session.skills_loaded`. Use `--no-custom-instructions`, `--disable-builtin-mcps`, or explicit `--disable-mcp-server` in CI to get reproducible behavior.
- **Notion/GitHub MCP auth failures are silent** — they appear as `session.mcp_servers_loaded` with `status: "failed"` but the run continues. Parse that event if a specific MCP server is load-bearing for your task.
- **`interactive` is still the default mode.** Without `--autopilot` or `--plan`, the agent will try to prompt. `-p` + `--allow-all-tools` isn't enough by itself — pair with `--autopilot` for non-interactive execution.
- **No `cwd` flag.** Unlike Codex's `-C` or Claude's explicit `--add-dir`, you `cd` into the target dir before invoking. Confirm cwd in your script to avoid subtle scope bugs.
