# Codex CLI — Headless Reference

`codex exec`. Plain `codex` is TUI. Docs: <https://developers.openai.com/codex/noninteractive>.

## The minimum viable invocation

```bash
codex exec "Summarize this project"
```

Streams progress to **stderr** and writes only the final agent message to **stdout**. This split makes piping cleanly: `codex exec "..." | tee result.md` captures just the answer.

If a prompt argument is provided AND stdin is piped, stdin is appended to the prompt as a `<stdin>` block — useful for feeding diffs or test output into a templated prompt:

```bash
npm test 2>&1 | codex exec "Summarize failures and suggest fixes"
```

If the prompt is `-` or omitted with piped stdin, stdin is the full prompt:

```bash
cat prompt.txt | codex exec -
```

## Sandbox modes (critical safety lever)

```
-s, --sandbox <read-only|workspace-write|danger-full-access>
```

| Mode                  | What the model can do                                                       |
| --------------------- | --------------------------------------------------------------------------- |
| `read-only`           | Run only read-only commands. Default and safe starting point.               |
| `workspace-write`     | Write inside the workspace. Cannot touch other dirs. Good for agentic edits. |
| `danger-full-access`  | No sandboxing. Equivalent to giving the model root. Do not use casually.    |

Shortcuts:
- `--full-auto` — alias for `--sandbox workspace-write`. Low-friction agentic default.
- `--dangerously-bypass-approvals-and-sandbox` — skip approvals AND sandbox. Externally sandboxed environments only (Docker, microVM, etc.).

## Working directory & scope

| Flag                   | Effect                                                                  |
| ---------------------- | ----------------------------------------------------------------------- |
| `-C, --cd <DIR>`       | Tell the agent to use `<DIR>` as its working root.                      |
| `--add-dir <DIR>`      | Additional writable directory alongside the workspace.                  |
| `--skip-git-repo-check` | Allow running outside a Git repo (by default Codex refuses).            |
| `--ephemeral`          | Don't persist session files to disk. Fire-and-forget.                  |

## Output formats

```
--json                         Emit JSONL events to stdout
--output-schema <FILE>         Constrain the final response to a JSON Schema
-o, --output-last-message <F>  Write just the final assistant message to <F>
```

- `--json` streams events, one JSON object per line.
- `--output-schema` takes a *file path* to a JSON Schema (unlike Claude's inline `--json-schema`). The final response is validated against it.
- `-o` / `--output-last-message` is the quickest way to capture the final answer. The file is written at the end; piping stdout still works for human reading.

### `--json` event types (empirically observed)

| Event type          | Purpose                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| `thread.started`    | First event. Contains `thread_id` (UUID). **NOTE: `thread_id`, not `session_id`.** |
| `turn.started`      | A model turn begins.                                                    |
| `turn.completed`    | Turn finished successfully. Contains aggregated usage.                  |
| `turn.failed`       | Turn aborted. Contains `error.message`.                                 |
| `item.*` (e.g., `item.completed`) | Individual items produced during a turn: agent messages, reasoning, command executions, file changes, MCP calls, web searches, plan updates. |
| `error`             | Non-fatal error or notice.                                              |

Example events from a run that hit a rate limit:

```json
{"type":"thread.started","thread_id":"019d9c8a-0c38-7cb1-8dd0-4a6bf1a852d1"}
{"type":"turn.started"}
{"type":"error","message":"You've hit your usage limit. ..."}
{"type":"turn.failed","error":{"message":"You've hit your usage limit. ..."}}
```

Detect failure in a script:

```bash
codex exec "task" --json 2>/dev/null | jq -e 'select(.type == "turn.failed") | .error.message' >/dev/null \
  && echo "turn failed" >&2
```

### Typical recipes

```bash
# Parseable final answer, written to file
codex exec "Extract TODO comments as JSON" \
  --sandbox read-only \
  --output-schema todos.schema.json \
  -o final.json \
  --cd /repo

# Watch events in real time
codex exec "Refactor the billing module" --full-auto --json | jq '.'
```

## Model & configuration

| Flag                              | Effect                                                                 |
| --------------------------------- | ---------------------------------------------------------------------- |
| `-m, --model <MODEL>`             | Model selection.                                                       |
| `--oss`                           | Use the local OSS provider (LM Studio or Ollama).                     |
| `--local-provider <lmstudio\|ollama>` | Pick the OSS backend explicitly.                                   |
| `-p, --profile <NAME>`            | Load a named profile from `~/.codex/config.toml`.                      |
| `-c, --config <key=value>`        | Override a single config value (TOML syntax). Dotted paths for nesting. |
| `--enable <FEATURE>` / `--disable <FEATURE>` | Toggle feature flags (repeatable).                          |
| `-i, --image <FILE>`              | Attach image(s) to the initial prompt.                                 |

Config overrides via `-c`:
```bash
codex exec "Ship this task" \
  -c model=o4-mini \
  -c 'sandbox_permissions=["disk-full-read-access"]' \
  -c shell_environment_policy.inherit=all
```

Values parse as TOML first, falling back to raw string.

## Authentication

Two supported auth paths:

1. **`CODEX_API_KEY` env var** — recommended for CI. Set as a secret and export before invoking.
   ```bash
   CODEX_API_KEY="$OPENAI_API_KEY" codex exec --json "task"
   ```
2. **`~/.codex/auth.json`** — for ChatGPT-managed accounts. Must be seeded on the runner via secure storage. Treat as a password; Codex refreshes tokens in place between runs.

In GitHub Actions, the dedicated `openai/codex-action@v1` wraps installation and auth:

```yaml
- uses: actions/checkout@v5
- uses: openai/codex-action@v1
  with:
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    prompt-file: .codex/review.md
    sandbox: workspace-write
    safety-strategy: drop-sudo     # default; also unprivileged-user, unsafe
    output-file: codex-result.md
```

The action exposes the final message as a step output: `${{ steps.run_codex.outputs.final-message }}`.

## Resuming sessions

```bash
# Resume most recent (this cwd)
codex exec resume --last "follow-up work"

# Resume by thread/session ID
codex exec resume <UUID> "Continue with the changes"
```

`--all` shows sessions across directories. For parallel pipelines, capture the `thread_id` from the first `thread.started` event and feed it back explicitly.

## Review mode

`codex review` — specialized non-interactive subcommand for code review. Tuned defaults; prefer over hand-rolling.

## MCP & plugins

- `codex mcp` — list/add/remove MCP servers.
- `codex mcp-server` — run Codex itself as an MCP server over stdio.
- **`required = true` MCP servers abort `codex exec` on init failure.** In CI, prefer `-c mcp_servers...` over `~/.codex/config.toml` and set `required = false` unless load-bearing.

## Exit codes

**Exit code 0 even on API errors.** Empirically confirmed: a run that hits `usage limit` emits `turn.failed` in the event stream but the process exits 0. Scripts MUST parse JSON (or check `-o` file size / content) to detect failure, not rely on `$?`.

Safe wrapper:

```bash
out=$(codex exec "task" --json --sandbox read-only 2>/dev/null)
if echo "$out" | jq -e 'select(.type == "turn.failed")' >/dev/null; then
  echo "codex failed" >&2
  exit 1
fi
echo "$out" | jq -rn '[inputs | select(.type=="item.completed" and .item.type=="agent_message") | .item.text] | last'
```

## Gotchas

- **Must be inside a git repo** unless you pass `--skip-git-repo-check`. Codex will refuse to run otherwise.
- **`--full-auto` is `workspace-write`, not unrestricted.** The model can still be blocked when trying to touch files outside the workspace.
- **No native budget flag.** Wrap unattended runs with `timeout <N>s codex exec ...` (requires GNU coreutils on macOS, available as `gtimeout` via Homebrew).
- **`--dangerously-bypass-approvals-and-sandbox`** is an intentionally long flag name. Treat it as a red flag in any PR.
- **`--output-schema` takes a file path**, not an inline JSON string. Keep your schemas alongside the script.
- **Images via `-i` only attach to the initial prompt.** Resuming a session can't add images.
- **`codex exec` always prints "Reading additional input from stdin..."** when stdin is attached, even with an argument prompt. That message goes to stderr; don't let it scare you.
- **Progress streams to stderr, answer to stdout.** If you merge `2>&1` expecting one clean stream, you'll corrupt any downstream JSON parser. Keep them separate.
