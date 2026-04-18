# Introspection — Discovering Tools, MCP Servers, Skills, and Models

Two paths:
1. **Static** — subcommands that list *registered* servers/skills/plugins.
2. **Runtime** — first events in a `-p` / `exec` run tell you what *actually loaded* (can differ from registration when a server fails to start or CLI flags override defaults).

For automation, trust runtime over static — a server can be configured but fail to start.

## Claude Code

### Static

```bash
claude mcp list                   # all configured MCP servers (project + user)
claude mcp get <name>             # details on one server
claude agents                     # list configured agents (respects --setting-sources)
claude plugin list                # installed plugins
```

### Runtime

Emit the session-init event and parse it:

```bash
claude -p "noop" \
  --output-format stream-json --verbose \
  --permission-mode acceptEdits --allowedTools "Read" \
  | jq -c 'select(.type == "system" and .subtype == "init")' | head -1
```

The `system/init` event contains:
- `model` — the specific model this session will use
- `tools` — the tool names available to the model
- `mcp_servers` — servers that loaded successfully
- `plugins` — plugins that loaded (each with `name` and `path`)
- `plugin_errors` — plugins that failed to load (each with `plugin`, `type`, `message`). Omitted when empty.

Fail CI if a load-bearing MCP/plugin didn't come up:

```bash
init=$(claude -p "noop" --output-format stream-json --verbose \
  --permission-mode acceptEdits --allowedTools "Read" \
  | jq -c 'select(.type == "system" and .subtype == "init")' | head -1)

echo "$init" | jq -e '.mcp_servers | map(.name) | index("my-required-server")' >/dev/null \
  || { echo "required MCP server missing" >&2; exit 1; }

echo "$init" | jq -e '(.plugin_errors // []) | length == 0' >/dev/null \
  || { echo "plugin errors at load time" >&2; exit 1; }
```

### Models

No `--list-models` flag. Pass aliases (`sonnet`, `opus`, `haiku`) or full IDs (`claude-sonnet-4-6`, `claude-haiku-4-5-20251001`, `claude-opus-4-7`) via `--model`. The `model` field in `system/init` confirms which one was actually selected — useful when `--fallback-model` is in play.

## Codex

### Static

```bash
codex mcp list                    # configured MCP servers
codex mcp get <name>              # details on one server
codex features list               # feature flags and their effective state
```

### Runtime

`codex exec --json` surfaces tool use as `item.*` events, no tool-list event. Prefer `codex mcp list` for pre-flight; probe prompt as fallback:

```bash
codex exec "List the tools you have available. Reply in JSON." \
  --sandbox read-only --skip-git-repo-check \
  --output-schema tools-schema.json -o tools.json
```

### Models

No `--list-models` flag. Pass any OpenAI model ID via `-m` / `--model` or override the default in config:

```bash
codex exec "..." -m o4-mini
codex exec "..." -c model=gpt-5.1
```

Default and fallback models live in `~/.codex/config.toml` (or a profile via `-p`).

## Gemini CLI

### Static

```bash
gemini mcp list                           # MCP servers
gemini skills list [--all]                # skills discovered (--all = include disabled)
gemini extensions list                    # installed extensions
gemini -l                                 # equivalent: --list-extensions, prints and exits
```

### Runtime

`stream-json` emits an `init` event with session metadata, followed by `message`, `tool_use`, `tool_result`, `error`, `result`. The final `result` event's `stats.models[<name>]` confirms which model actually served each request — useful when the CLI picked a different model from your default.

JSON output (non-stream) carries `stats.models` too, so a cheap introspection call:

```bash
gemini -p "ok" --output-format json --approval-mode auto_edit 2>/dev/null \
  | jq -r '.stats.models | keys[]'     # models that served requests
```

Policy-driven tool availability is inspected via policy files (see `references/gemini.md`), not a subcommand — there's no `gemini policy list`.

### Models

No `--list-models` flag. Set via `-m` / `--model` or config default. `stats.models` in the result JSON confirms what was actually used.

## GitHub Copilot CLI

### Static

```bash
copilot mcp list                   # MCP servers (user + workspace + plugin)
copilot mcp get <name>             # details on one server
copilot plugin list                # installed plugins
copilot plugin marketplace browse <name>   # discover more
```

### Runtime

Copilot emits the richest startup-time introspection — every load step becomes a JSONL event:

| Event                                 | What you learn                                            |
| ------------------------------------- | --------------------------------------------------------- |
| `session.mcp_server_status_changed`   | Per-server connection state as servers come up            |
| `session.mcp_servers_loaded`          | Final roster: `{name, status, source, error?}` per server |
| `session.skills_loaded`               | Skill registry loaded, including description + path       |
| `session.tools_updated`               | Current tool list the model will see                      |

Parse with:

```bash
copilot -p "noop" --allow-all-tools --autopilot --output-format json -s 2>/dev/null \
  | jq -c 'select(.type == "session.mcp_servers_loaded") | .data.servers' | head -1
```

Detect a failed MCP load (Copilot does not abort when an MCP server fails):

```bash
copilot -p "noop" --allow-all-tools --autopilot --output-format json -s 2>/dev/null \
  | jq -e 'select(.type == "session.mcp_servers_loaded") | .data.servers[] | select(.status == "failed")' \
  && echo "at least one MCP server failed to load" >&2
```

### Models

No `--list-models` flag. Set via `--model <name>`. The effective model is not emitted in a dedicated event; capture it from `result.usage` or the session ID and query GitHub's Copilot API if you need it.

## gh agent-task (delegated cloud agent)

Agent runs server-side; local introspection is about repo config, not the CLI.

### Static

```bash
# Custom agents are markdown files in the target repo
gh api repos/<owner>/<repo>/contents/.github/agents --jq '.[].name'

# Previous tasks and their state
gh agent-task list --limit 50
```

### Runtime

```bash
gh agent-task view <session-id> --log          # session transcript
gh agent-task view <session-id> --follow       # tail live
```

Model selection is managed server-side by GitHub's Copilot coding-agent infrastructure; there's no client-side model flag. Custom agent prompts (`.github/agents/<name>.md`) shape behavior instead.

## Cross-CLI summary

| Question                       | Claude                         | Codex                 | Gemini                  | Copilot                             |
| ------------------------------ | ------------------------------ | --------------------- | ----------------------- | ----------------------------------- |
| List MCP servers (config)      | `claude mcp list`              | `codex mcp list`      | `gemini mcp list`       | `copilot mcp list`                  |
| List MCP servers (runtime)     | `system/init.mcp_servers`      | probe prompt          | `init` event            | `session.mcp_servers_loaded`        |
| List tools (runtime)           | `system/init.tools`            | `item.*` as used      | inferred from policy    | `session.tools_updated`             |
| List skills / plugins          | `claude plugin list`           | n/a                   | `gemini skills list`    | `copilot plugin list`               |
| List custom agents             | `claude agents`                | agent concept differs | extensions via `list`   | plugin concept                      |
| `--list-models` flag           | none — use init event's `model`| none — pass via `-m`  | none — stats confirms   | none — passed via `--model`         |
| Pre-flight fail-fast on load  | parse `plugin_errors`          | `codex mcp list`      | `gemini mcp list`       | parse `session.mcp_servers_loaded`  |

**Rule:** if a script depends on a specific MCP server/tool, check the runtime init/session event — not just `mcp list`.
