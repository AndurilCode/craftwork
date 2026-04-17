# GitHub Agent Tasks (`gh agent-task`) — Delegation Reference

`gh agent-task` dispatches a task to GitHub's cloud-hosted Copilot coding agent. The agent runs asynchronously on GitHub's infrastructure, opens a pull request against the repo, and the local CLI is just a thin client for create/list/view.

**This is a different mental model from the local-agent CLIs** (Claude, Codex, Gemini, Copilot CLI):

| | Local agent CLIs | `gh agent-task` |
|-|-----------------|-----------------|
| Where code runs | Your machine / CI runner | GitHub's cloud infrastructure |
| Execution model | Synchronous process | Asynchronous task, produces a PR |
| Artifact | Stdout / files / optional commit | Pull request |
| Permissions | Local filesystem + shell | GitHub repo permissions |
| Auth | API key / OAuth per CLI | GitHub token (via `gh auth`) |
| Context | Loaded at invocation time | Configured per-repo + optional custom agent |

Preview feature — flags may change. Aliases: `gh agent-tasks`, `gh agent`, `gh agents`.

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

**`-R/--repo` is the orchestration lever.** You can dispatch into any repo you have access to without `cd`-ing into a local clone — the agent runs in GitHub's cloud against the remote repo. This makes the whole thing scriptable from one central location: a cron job, a webhook handler, an ops dashboard. You never need to check out the target repo on the dispatcher.

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

For integrations where a ticket or issue should result in an agent-authored PR. You don't wait; another process watches the PR.

```bash
#!/usr/bin/env bash
# Called from a webhook when a Linear/Jira ticket is marked "ready for agent"
set -euo pipefail
TICKET_FILE="$1"
gh agent-task create -F "$TICKET_FILE" --base main
```

The command exits quickly; the agent continues working in the cloud. A PR will appear on the repo when it's done.

### Dispatch-and-watch

When you want live progress in the current job (CI step, local monitor, etc.).

```bash
gh agent-task create "Add tests for src/billing" --follow --base main
```

`--follow` keeps the process alive and streams logs until the session finishes. Use in an interactive or foreground context; skip in true fire-and-forget automation.

### Dispatch with a custom agent

Custom agents live at `.github/agents/<name>.md` in the repo — a markdown spec of role, constraints, and style. Dispatch with `-a`:

```bash
gh agent-task create "Refactor the auth middleware" --custom-agent security-reviewer
```

If the team has invested in agent prompts for specific kinds of work (security review, test generation, docs), custom agents keep the prompt in version control and make task descriptions short.

### Batch dispatch from a queue

Fan out N tickets into N agent tasks. Collect session IDs for later polling.

```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p dispatched
for ticket in tickets/*.md; do
  base_name=$(basename "$ticket" .md)
  # create returns human-readable output; parse with --jq or capture the session ID via list
  gh agent-task create -F "$ticket" --base main > "dispatched/$base_name.out"
  sleep 1  # avoid rate limits
done

# Later: poll for completion
gh agent-task list --limit 100
```

`gh agent-task create` doesn't have a `--json` output flag in preview. To get structured task data, fall back to `gh agent-task list` or query the GitHub REST API directly with `gh api`.

### Cross-repo / fleet orchestration (the `-R` pattern)

`-R/--repo` makes a single dispatcher script work across many repositories without local clones. Three concrete patterns this enables:

**Fan out one task across a fleet of repos:**

```bash
#!/usr/bin/env bash
# Upgrade a dependency across every repo in an org's "services" topic
set -euo pipefail
task_file="tasks/upgrade-node-20.md"

gh repo list my-org --topic services --json nameWithOwner -L 100 \
  --jq '.[].nameWithOwner' | while read -r repo; do
    echo "dispatching to $repo"
    gh agent-task create -F "$task_file" --base main --repo "$repo"
    sleep 2
done
```

**Ticket router — route each ticket to the repo it belongs to:**

```bash
#!/usr/bin/env bash
# Called from a webhook. Ticket metadata names the target repo.
set -euo pipefail
repo="$1"                     # e.g., my-org/payments-service
ticket_file="$2"              # problem statement
gh agent-task create -F "$ticket_file" --base main --repo "$repo" --follow
```

**Central ops dashboard dispatches into many repos:**

```bash
# From a platform team's scheduler, targeting repos owned by product teams
gh agent-task create "Rotate the deprecated API keys per RUNBOOK.md" \
  --repo my-org/checkout-service --base main
gh agent-task create "Rotate the deprecated API keys per RUNBOOK.md" \
  --repo my-org/billing-service --base main
```

In each case the dispatcher needs only `gh auth` credentials with access to the target repos — no clones, no working trees, no local context. The agent runs on GitHub's side and opens the PR there.

### Pair with local verification

A common pattern: agent opens the PR; a local CLI (Claude/Codex/Gemini/Copilot) reviews it.

```bash
# Step 1: dispatch
gh agent-task create "Implement $FEATURE" --base main

# ... wait for PR to appear (separate cron or webhook) ...

# Step 2 (from a reviewer job): review the PR with a local agent
claude -p "Review PR #$PR for correctness and test coverage" \
  --allowedTools "Bash(gh pr *),Read" \
  --permission-mode plan \
  --output-format json
```

Delegation produces the PR; local agent gates its merge.

## Authentication

`gh agent-task` uses the authenticated `gh` CLI context. In CI:

```yaml
env:
  GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}   # or a PAT with appropriate scopes
```

The agent runs under GitHub's managed identity, not under your token — your token just authorizes dispatch. The Copilot coding agent feature must be enabled for the org/repo.

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
