---
name: llms-txt-generator
description: "Generate llms.txt-style context documents — token-budgeted, section-per-concept Markdown optimized for LLM and RAG consumption. Use this skill whenever someone asks to generate an llms.txt, create LLM-friendly documentation, produce a context document for a library or codebase, build a RAG-ready reference, make docs 'agent-readable', create a developer quick-reference, or says anything like 'generate context for X', 'make an llms.txt for this repo', 'create a reference doc for NotebookLM', 'turn these docs into something an LLM can use', 'context document', 'developer cheatsheet from docs'. Also trigger when someone provides a GitHub repo URL and asks for documentation synthesis, or when working inside a codebase and asked to produce a self-contained reference of how it works. This is the context engineer's doc generation tool — it turns sprawling documentation into precise, structured, token-efficient context."
---

# llms.txt Generator

Produces a single self-contained Markdown doc following the `llms.txt` convention: H2 per concept, 1-3 sentence explanation + one annotated code example, token-budgeted, ending with a Summary. Each H2 is an independent retrieval unit — usable as RAG source (NotebookLM, vector DBs, agent context) or standalone reference.

---

## Execution Flow

| Signal | Mode | Source |
|--------|------|--------|
| GitHub URL or `org/repo` | **Remote** | Fetch via GitHub raw |
| No URL, agent in codebase | **Local** | Scan cwd for docs |

If ambiguous, ask.

---

## PHASE 1 — Source Discovery

Find docs describing the library/codebase concepts, API surface, usage patterns.

### Remote mode

1. Determine org, repo, optional version tag.
2. Sparse-clone docs:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/{org}/{repo}.git /tmp/llms-gen-{repo}
cd /tmp/llms-gen-{repo}
git sparse-checkout set docs/ README.md CHANGELOG.md
# For specific tag: git fetch --depth 1 origin tag {version} && git checkout {version}
```

3. If no `docs/`, fall back to: `README.md`, `wiki/`, `pages/`, `content/`, `src/` (inline JSDoc/docstrings), or any doc-like dir.
4. List all `.md`, `.mdx`, `.rst`, `.txt`. Discard changelogs, contribution guides, CI docs unless requested.

### Local mode

1. Scan cwd:

```bash
find . -type f \( -name "*.md" -o -name "*.mdx" -o -name "*.rst" \) \
  ! -path "*/node_modules/*" ! -path "*/vendor/*" ! -path "*/.git/*" \
  ! -path "*/dist/*" ! -path "*/build/*" | head -100
```

2. Also scan: README at any depth, inline source docs (JSDoc, docstrings), `docs/` or `documentation/` dirs.
3. Identify project name from `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or root dir name.
4. Identify version from same manifest or git tags.

**Output**: doc file paths ranked by relevance (README → guides → API reference → examples).

---

## PHASE 2 — Topic Extraction

Build the concept list — the H2 sections.

### How to extract

1. **Doc structure**: Each top-level doc file or major H2 is a candidate. Sidebar/nav files (`_sidebar.md`, `_meta.json`, `mkdocs.yml`, `docusaurus.config.js`) give author's intended hierarchy — gold.
2. **README structure**: H2s often map to core concepts.
3. **Source code** (when docs thin): exported modules, classes, CLI commands, route definitions.

### Selection criteria

- Core concept user hits in week one → Include
- Advanced/niche → Include only if budget allows
- Installation/setup → Include only if non-trivial
- Deprecated → Exclude
- Internal/implementation → Exclude

### Ordering

1. What it IS (overview)
2. Getting started / installation (if non-trivial)
3. Core concepts in dependency order (routing before middleware)
4. Data flow / state
5. Integration points
6. Advanced patterns
7. Configuration reference

**Output**: ordered list of 8-25 topics, each with pointer to source chunk(s).

---

## PHASE 3 — Per-Section Synthesis

For each topic, produce one Markdown section.

### Section format (strict)

```markdown
## {Topic Name}

{1-3 sentences: what it is, when to use it, one key thing to know.}

```{language}
// Annotated code — complete enough to copy-paste
// Inline comments only for non-obvious lines
```

```{language}
// OPTIONAL second block — only when concept genuinely spans two
// languages or distinct contexts (.env file + tsx usage; reading
// vs. writing cookies in separate server contexts)
```
```

### Synthesis rules

1. **Explanation**: 1-3 sentences. First says what it is. Following say when/why or key gotcha. No "In this section we'll explore..."
2. **Code example**: One primary fenced block. Optional second only when concept genuinely spans two languages or contexts.
   - **Complete**: copy-pastable, not cryptic, no boilerplate
   - **Annotated**: inline comments only on non-obvious lines (don't comment `import React from 'react'`)
   - **Runnable** where possible
   - **Current**: pinned-version APIs, no deprecated
   - **Idiomatic**: follow library's own conventions
3. **Exclude per section**:
   - Installation steps (unless topic IS setup)
   - More than two code blocks
   - Prose beyond 3 sentences
   - External links
   - Deprecated APIs
   - Type definitions unless they ARE the concept

### Token budget per section

Given total `T` and `N` sections:
- Header + overview: ~300 tokens (two paragraphs for complex frameworks)
- Summary: ~200 tokens
- Each topic: ~`(T - 500) / N`
- Code-heavy sections borrow from prose-light
- If a section can't be meaningful in budget, combine or drop

---

## PHASE 4 — Assembly

### Document structure

```markdown
# {Library/Project Name}

{Overview para 1: what it is, core paradigm/architecture, most important thing about current version.}

{Overview para 2 (optional, complex frameworks): capabilities, rendering model, or DX context.}

## {Topic 1}

{explanation + code}

## {Topic 2}

{explanation + code}

...

## Summary

{1-2 paragraphs tying concepts: how pieces compose into typical architecture, which APIs for common scenarios, key integration patterns. RAG anchor — gives retriever a "how pieces fit" chunk.}
```

### Assembly rules

1. H1 = library/project name, nothing else.
2. Overview = 2-3 sentences for simple libs, two short paragraphs for complex frameworks. Answers: "What is it and why does it matter?"
3. Sections separated by single blank line. No HRs, no extra spacing.
4. No TOC — H2s ARE the TOC for RAG chunking.
5. No metadata, frontmatter, preamble. Doc starts with `# Name`.
6. Final `## Summary` required. 1-2 paragraphs.
7. Should feel written by a senior dev who uses the library daily.

### Budget enforcement

Estimate tokens (`word_count * 1.3`). If over:
1. Trim obvious code comments
2. Shorten explanations to 1 sentence
3. Drop lowest-priority sections from bottom
4. Last resort: merge related sections

---

## PHASE 5 — Output

### File naming

- User-specified: use it
- Library default: `{library-name}.llms.txt` (e.g., `next-js.llms.txt`)
- Local codebase default: `llms.txt` at repo root
- Alt: `{name}.context.md` if user prefers `.md`

### Save location

- In a codebase: repo root (or `docs/` if exists)
- External use: save to `/home/claude/` and present to user
- Always copy final to `/mnt/user-data/outputs/` for download

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Token budget | 10,000 | 5K focused / 10K standard / 20K comprehensive |
| Version | latest | Git tag, branch, or `latest` |
| Language | auto-detect | Primary code language |
| Topic filter | all | Comma-separated topics (e.g., "routing, data-fetching, auth") |
| Code density | balanced | `code-heavy` / `info-heavy` |

"make it short" → 5K. "Give me everything" → 20K. "Focus on routing and auth" → topic filter.

---

## Quality Checklist

- [ ] Every H2 has one primary code block (and at most one justified second)
- [ ] No explanation > 3 sentences
- [ ] Code uses current APIs in correct language
- [ ] Code is copy-pastable — not cryptic
- [ ] No deprecated patterns
- [ ] Overview accurately describes the project (2-3 sentences or two short paragraphs)
- [ ] `## Summary` present, ties to architecture
- [ ] Total tokens within ±10% of budget
- [ ] Sections in dependency order (no forward references)
- [ ] Self-contained — no broken cross-references
- [ ] No installation unless setup IS the concept
- [ ] Each section independently useful as retrieval unit

---

## Examples

**GitHub URL**: "Generate an llms.txt for https://github.com/supabase/supabase"
→ Remote → sparse clone → docs in `apps/docs/` → topics (Auth, Database, Storage, Realtime, Edge Functions) → synthesize → 10K → `supabase.llms.txt`

**Inside codebase**: "Create an LLM-friendly reference for this project"
→ Local → scan docs + source → project name from `package.json` → topics from README H2s + source modules → synthesize → `llms.txt` at repo root

**Focused output**: "Generate context docs for Next.js, just routing and data fetching, under 5K"
→ Remote → fetch Next.js docs → filter → 5K budget → `next-js.llms.txt`

---

## Edge Cases

- **No docs**: Fall back to README + source. Generate sections from exported APIs, CLI commands, classes. Warn user about source-comment dependence.
- **Auto-generated API reference only**: Group related endpoints/methods into conceptual sections rather than listing every method.
- **Monorepo**: Ask which package, or generate one doc per package.
- **Non-English docs**: Generate in source language unless user specifies.
- **Budget too small for topic count**: Prioritize core, drop advanced, tell user what was excluded.
