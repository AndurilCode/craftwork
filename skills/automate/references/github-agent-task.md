# GitHub Agent Tasks (`gh agent-task`) — Delegation Reference

Dispatches a task to GitHub's cloud-hosted Copilot coding agent. Async; agent opens a PR. Local CLI is a thin dispatcher.

Differs from local CLIs: runs server-side, artifact is a PR (not stdout), auth is GitHub token (`gh auth`). Preview feature — flags may change. Aliases: `gh agent-tasks`, `gh agent`, `gh agents`.

## The three subcommands

```
gh agent-task create [<description>] [flags]   # dispatch a task
gh agent-task list [flags]                     # list recent tasks
gh agent-task view [<id>] [flags]              # view a task session
```

### `create`

```
-b, --base <branch>             Base branch for the PR (default: repo default)
-a, --custom-agent <name>       Use .github/agents/<name>.md custom agent
    --follow                    Stream agent session logs after creation
-F, --from-file <file>          Read task description from file ("-" = stdin)
-R, --repo <OWNER/REPO>         Target a different repo (you do not need to be inside it)
```

**`-R/--repo` is the orchestration lever.** Dispatch into any accessible repo without a local clone — one dispatcher script can drive a cron, webhook, or ops dashboard across many repos.

Input sources (choose one):
- Positional argument: `gh agent-task create "fix the pagination bug"`
- File: `gh agent-task create -F task.md`
- Stdin: `echo "..." | gh agent-task create -F -`
- Editor: `gh agent-task create` with no args opens `$EDITOR`

### `list`

```
-L, --limit <N>     Max tasks (default: 30)
-w, --web           Open in browser
```

### `view`

```
--follow              Follow session logs live
--log                 Show the log
-R, --repo <OWNER/REPO>
-w, --web             Open in browser
```

Task identifiers accepted: session ID UUID, PR number, PR URL, or `OWNER/REPO#<num>`. **Prefer session IDs for scripts** — the docs explicitly warn that identifying by PR number is ambiguous when multiple tasks exist on the same PR.

## The canonical automation shapes

### Dispatch-and-forget

Fire and move on; a separate watcher handles completion.

```bash
gh agent-task create -F "$TICKET_FILE" --base main
```

### Dispatch-and-watch

`--follow` keeps the process alive and streams logs until the session finishes. Foreground use only.

```bash
gh agent-task create "Add tests for src/billing" --follow --base main
```

### Custom agent

Custom agents live at `.github/agents/<name>.md` in the target repo. Keeps prompts in version control and shortens task descriptions.

```bash
gh agent-task create "Refactor the auth middleware" --custom-agent security-reviewer
```

### Batch dispatch

Fan out N tickets. `create` has no `--json` in preview — capture via `gh agent-task list` or `gh api` against the REST endpoint.

```bash
for ticket in tickets/*.md; do
  gh agent-task create -F "$ticket" --base main
  sleep 1
done
gh agent-task list --limit 100
```

### Cross-repo fleet (`-R` pattern)

Fan one task across every repo matching a filter — no clones needed:

```bash
gh repo list my-org --topic services --json nameWithOwner -L 100 \
  --jq '.[].nameWithOwner' | while read -r repo; do
    gh agent-task create -F tasks/upgrade.md --base main --repo "$repo"
    sleep 2
done
```

Same pattern fits ticket routers (webhook picks the repo) and ops dashboards (platform team dispatches into product-team repos). Dispatcher needs only `gh auth`.

### Pair with local verification

Agent opens the PR; a local CLI reviews before merge.

```bash
gh agent-task create "Implement $FEATURE" --base main
# ... wait for PR (cron / webhook) ...
claude -p "Review PR #$PR for correctness and test coverage" \
  --permission-mode acceptEdits \
  --allowedTools "Bash(gh pr *),Read,Grep,Glob" \
  --output-format json
```

## Authentication

Uses `gh auth` context. In CI: `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` (or a PAT). Agent runs under GitHub's managed identity; your token only authorizes dispatch. Copilot coding agent must be enabled for the org/repo.

## Exit codes

`gh` family exit codes apply (`gh help exit-codes`). `create` returns non-zero on dispatch failures (auth, quota, feature-not-enabled, network). It does NOT fail if the agent later fails — that's visible only via `view` or the PR state.

## Gotchas

- **`create` is async.** Exit 0 means "dispatched successfully," not "agent succeeded." Your script cannot block on agent completion without `--follow`. For true done-detection, watch the PR state.
- **Preview feature.** Flags and behavior may change. Pin `gh` version in CI if this matters.
- **PR-number identifiers are ambiguous.** Multiple tasks can be associated with one PR. In automation, always use the session ID UUID returned at create time.
- **No structured output from `create`.** Capture session IDs by parsing human output or by listing tasks right after create and matching on description/timestamp. If this matters, file a feature request — or use `gh api` against the underlying REST endpoint for JSON.
- **Custom agents are discovered from the repo**, not passed as files at dispatch. If a team wants CI-only agents, they still live at `.github/agents/<name>.md` in the target repo.
- **Base branch defaults to repo default.** Explicitly pass `--base` in scripts to avoid surprises when the default changes.
- **Feature-enabled check.** `gh agent-task create` fails with a permissions-style error if Copilot coding agent isn't enabled on the target repo. Handle in scripts with a clear error, don't retry.
