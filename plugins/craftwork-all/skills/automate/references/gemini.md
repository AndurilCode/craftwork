# Gemini CLI — Headless Reference

`gemini -p`. Plain `gemini` is TUI. Docs: <https://geminicli.com/docs/cli/headless/>, <https://geminicli.com/docs/reference/policy-engine/>.

## The minimum viable invocation

```bash
gemini -p "Summarize this project"
```

If stdin is piped AND `-p` is supplied, stdin is prepended to the prompt:

```bash
cat error.log | gemini -p "Classify the severity of the error above"
```

Headless mode is also triggered automatically when stdin is not a TTY — e.g., inside CI runners.

## JSON output shape

```bash
gemini -p "extract keywords" --output-format json --approval-mode auto_edit
```

Empirically observed top-level fields:

| Field        | Type    | Notes                                                        |
| ------------ | ------- | ------------------------------------------------------------ |
| `session_id` | string  | UUID.                                                        |
| `response`   | string  | The model's final answer. **NOTE: `response`, not `result`.** |
| `stats`      | object  | Aggregated statistics (see below).                           |
| `error`      | object  | Only present on failure.                                     |

`stats.models[<model-id>]` contains per-model usage:
- `api.{totalRequests, totalErrors, totalLatencyMs}`
- `tokens.{input, prompt, candidates, total, cached, thoughts, tool}`
- `roles.main.{...}` — same shape, scoped to the "main" role

`stats.tools` — aggregate tool usage (totalCalls, totalSuccess, totalFail, totalDurationMs, totalDecisions).

`stats.files` — `totalLinesAdded`, `totalLinesRemoved`.

**No native cost field.** Only token counts. Compute cost externally from model pricing if needed.

**Heavy baseline.** A trivial "ok" prompt costs ~6,280 input tokens — Gemini's built-in system prompt is substantial.

## Stream-json events

```
-o, --output-format stream-json
```

Newline-delimited JSON events:

| Event         | Purpose                                                                       |
| ------------- | ----------------------------------------------------------------------------- |
| `init`        | Session metadata including ID and model selection.                            |
| `message`     | User and assistant message chunks.                                            |
| `tool_use`    | Tool call requests with arguments.                                            |
| `tool_result` | Output from executed tools.                                                   |
| `error`       | Non-fatal warnings and system errors.                                         |
| `result`      | Final outcome with aggregated stats and per-model token usage.                |

## Exit codes

Gemini's exit codes are meaningful (unlike Codex):

| Code | Meaning                                  |
| ---- | ---------------------------------------- |
| `0`  | Success                                  |
| `1`  | General error or API failure             |
| `42` | Input error (invalid prompt or args)     |
| `53` | Turn limit exceeded                      |

Use them directly in shell guards. Still parse `stats.error` for details when you need the message.

## Approval modes

```
--approval-mode <default|auto_edit|yolo|plan>
```

| Mode        | Effect                                                                      |
| ----------- | --------------------------------------------------------------------------- |
| `default`   | **Avoid in scripts.** Write tools default to `ask_user`; in headless `ask_user` → deny, so most writes silently fail. |
| `plan`      | **Avoid in scripts.** Read-only planning — yields a plan, not action. Use `auto_edit` + a deny-shell policy for read-only. |
| `auto_edit` | Auto-approves edits; still prompts for shell unless a policy allow rule covers it. Script default. |
| `yolo`      | Auto-approves everything. Same as `-y` / `--yolo`. Sandboxed envs only. |

**Rule:** use `auto_edit` (with a policy allowlist for shell) or `yolo`.

**Naming gotcha.** CLI flag is `auto_edit` (underscore). Policy TOML `modes` field uses `autoEdit` (camelCase).

## Policy Engine (preferred over deprecated `--allowed-tools`)

```
--policy <FILE_OR_DIR>          User-level policy files
--admin-policy <FILE_OR_DIR>    Admin-level policy files (override user)
```

Policy files are **TOML**, located at `~/.gemini/policies/*.toml` by default, or passed via the flags above. They supersede the deprecated `--allowed-tools` list.

### Rule schema

```toml
[[rule]]
toolName = "run_shell_command"        # or a wildcard like "mcp_*", or an array ["write_file","replace"]
commandPrefix = "rm -rf"              # syntactic sugar for shell commands
# commandRegex = "git (commit|push)"
# argsPattern = "..."                 # regex over the JSON-encoded args
decision = "deny"                     # allow | deny | ask_user
priority = 100                        # 0-999
modes = ["autoEdit", "yolo"]          # optional: when does this rule apply?
# mcpName = "my-jira-server"
# subagent = "codebase_investigator"
# interactive = false                 # restrict to headless / interactive
denyMessage = "Deletion is permanent"
# allowRedirection = true
```

### Decision model

- `allow` — tool runs.
- `deny` — tool blocked. For global rules (no `argsPattern`), denied tools are **excluded from the model's memory entirely** — the model won't even attempt them.
- `ask_user` — confirmation prompt. **In headless runs this is treated as `deny`.** So `ask_user` rules are interactive-only.

### Priority tiers

Effective priority = `tier_base + (toml_priority / 1000)`:

| Tier      | Base | Location                          |
| --------- | ---- | --------------------------------- |
| Default   | 1    | Built-in policies                 |
| Extension | 2    | Extension policies                |
| User      | 4    | `~/.gemini/policies/`             |
| Admin     | 5    | OS system dirs (see below)        |

Admin policy locations:
- Linux: `/etc/gemini-cli/policies`
- macOS: `/Library/Application Support/GeminiCli/policies`
- Windows: `C:\ProgramData\gemini-cli\policies`

Within-tier priority dominates tier base: a User rule with `priority: 100` (eff. 4.100) beats an Admin rule with `priority: 50` (eff. 5.050).

### Useful policy examples

```toml
# Block destructive deletes
[[rule]]
toolName = "run_shell_command"
commandPrefix = "rm -rf"
decision = "deny"
priority = 100

# Allow git commit/push in automated modes
[[rule]]
toolName = "run_shell_command"
commandRegex = "git (commit|push)"
decision = "allow"
priority = 150
modes = ["autoEdit", "yolo"]

# Trust one specific MCP server; deny another
[[rule]]
mcpName = "untrusted-server"
decision = "deny"
priority = 500
denyMessage = "This server is not trusted by the admin."
```

## Working directory & scope

| Flag                                  | Effect                                                                  |
| ------------------------------------- | ----------------------------------------------------------------------- |
| `--include-directories <dir,...>`     | Additional directories to include in the workspace.                     |
| `-w, --worktree [name]`               | Start Gemini in a new git worktree. Auto-names if unspecified.          |
| `-s, --sandbox`                       | Run the session in a sandbox.                                           |

## Sessions

```bash
gemini --list-sessions                    # List available sessions
gemini -r latest -p "Continue"            # Resume most recent
gemini -r 5 -p "Pick up where we left off"  # Resume by index
gemini --delete-session 3                  # Delete by index
```

Gemini addresses sessions by index or `"latest"` — there's no UUID-based resume in the CLI flags. For parallel-safe scripting, prefer completing each task in a single invocation rather than chaining via `-r`.

## Extensions, MCP, skills, hooks

| Subcommand / flag               | Purpose                                                             |
| ------------------------------- | ------------------------------------------------------------------- |
| `gemini mcp`                    | Manage MCP servers.                                                 |
| `gemini extensions`             | Manage extensions.                                                  |
| `gemini skills`                 | Manage agent skills.                                                |
| `gemini hooks`                  | Manage CLI hooks.                                                   |
| `-e, --extensions <names>`      | Restrict to a specific set of extensions.                           |
| `--allowed-mcp-server-names`    | Whitelist MCP servers for this run.                                 |

In CI, prefer restricting extensions/MCPs explicitly rather than inheriting whatever is installed globally.

## ACP mode

`--acp` — Agent Control Protocol for embedding Gemini in another agent framework. Rare in shell scripts.

## Model selection

`-m, --model <NAME>`. Falls back to config default.

## Gotchas

- **No `-p` → no headless.** Plain `gemini` with a positional argument still launches the TUI. Always pass `-p`.
- **Gemini crawls cwd at startup.** Empirically confirmed: launching from `/tmp` produced ~100 `[WARN] Skipping unreadable directory` lines on stderr before it ran. Launch from a clean directory, or scope with `--include-directories`. This also means **huge repos pay a walk cost on every invocation**.
- **Heavy baseline input tokens.** ~6,280 input tokens on "ok". Trivial batch jobs can be surprisingly expensive relative to Claude's Haiku.
- **`--allowed-tools` is deprecated.** Use `--policy` or policy files in `~/.gemini/policies/`.
- **`--raw-output` is a security risk** — ANSI escapes from attacker-controlled text can mess with terminals or logs. Don't enable unless you understand the threat model.
- **No native budget flag.** Use `timeout <N>s` and model choice to bound spend; check `stats.models[...].tokens` post-run.
- **Session resume is index-based**, so parallel scripts using `-r latest` race. Prefer single-invocation tasks when parallelizing.
- **`-y` / `--yolo` ≡ `--approval-mode yolo`** — treat both as red flags.
- **`ask_user` in headless = deny.** If your policy relies on prompts for interactive confirmation, it'll silently block in CI.
- **Stderr is chatty.** Don't merge `2>&1` into a pipe that expects clean JSON — you'll get `[WARN]` lines interleaved.
