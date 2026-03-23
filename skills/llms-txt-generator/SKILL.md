---
name: llms-txt-generator
description: "Generate llms.txt-style context documents — token-budgeted, section-per-concept Markdown optimized for LLM and RAG consumption. Use this skill whenever someone asks to generate an llms.txt, create LLM-friendly documentation, produce a context document for a library or codebase, build a RAG-ready reference, make docs 'agent-readable', create a developer quick-reference, or says anything like 'generate context for X', 'make an llms.txt for this repo', 'create a reference doc for NotebookLM', 'turn these docs into something an LLM can use', 'context document', 'developer cheatsheet from docs'. Also trigger when someone provides a GitHub repo URL and asks for documentation synthesis, or when working inside a codebase and asked to produce a self-contained reference of how it works. This is the context engineer's doc generation tool — it turns sprawling documentation into precise, structured, token-efficient context."
---

# llms.txt Generator

**What this produces**: A single, self-contained Markdown document following the `llms.txt` convention — the same format pioneered by Context7. Each section covers one concept with a 1-3 sentence explanation and one annotated, copy-pasteable code example. The whole document stays within a token budget and ends with a Summary section that ties concepts together. The output is immediately usable as a RAG source (NotebookLM, vector DBs, agent context windows) or as a standalone developer reference.

**Why this format works for RAG**: Each H2 section is an independent retrieval unit — self-explanatory without surrounding context, small enough for clean chunking, and dense enough to answer questions without filler.

---

## Execution Flow

Two modes, detected automatically:

| Signal | Mode | Source |
|--------|------|--------|
| User provides a GitHub URL or `org/repo` identifier | **Remote** | Fetch docs via GitHub raw content |
| No URL, but agent is inside a codebase | **Local** | Scan the current working directory for docs |

If ambiguous, ask.

---

## PHASE 1 — Source Discovery

The goal is to find all documentation files that describe the library/codebase's concepts, API surface, and usage patterns.

### Remote mode (GitHub repo)

1. Determine the org, repo, and optionally a version tag from the user's input.
2. Fetch the repo's directory tree to locate documentation:

```bash
# Clone only the docs — shallow, sparse
git clone --depth 1 --filter=blob:none --sparse https://github.com/{org}/{repo}.git /tmp/llms-gen-{repo}
cd /tmp/llms-gen-{repo}
git sparse-checkout set docs/ README.md CHANGELOG.md
# If a specific tag is needed:
# git fetch --depth 1 origin tag {version} && git checkout {version}
```

3. If the repo has no `docs/` directory, fall back to: `README.md`, `wiki/`, `pages/`, `content/`, `src/` (for inline JSDoc/docstrings), or any directory that smells like documentation.
4. List all `.md`, `.mdx`, `.rst`, `.txt` files found. Discard changelogs, contribution guides, and CI/CD docs unless specifically requested.

### Local mode (current codebase)

1. From the current working directory, scan for documentation:

```bash
# Find doc-like files, excluding node_modules, vendor, dist, build
find . -type f \( -name "*.md" -o -name "*.mdx" -o -name "*.rst" \) \
  ! -path "*/node_modules/*" ! -path "*/vendor/*" ! -path "*/.git/*" \
  ! -path "*/dist/*" ! -path "*/build/*" | head -100
```

2. Also scan for: README files at any depth, inline documentation in source (JSDoc, docstrings, doc comments), and any `docs/` or `documentation/` directories.
3. Identify the project name from `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or the root directory name.
4. Identify the version from the same manifest file or from git tags.

**Output of Phase 1**: A list of documentation file paths ranked by likely relevance (README first, then guides, then API reference, then examples).

---

## PHASE 2 — Topic Extraction

Scan the discovered docs to build a **concept list** — the H2 sections that will appear in the final document.

### How to extract topics

1. **From doc file structure**: Each top-level doc file or major H2 heading is a candidate topic. Sidebar navigation files (`_sidebar.md`, `_meta.json`, `mkdocs.yml`, `docusaurus.config.js`, etc.) are gold — they give the author's intended topic hierarchy.

2. **From README structure**: H2 headings in the README often map directly to the library's core concepts.

3. **From source code** (when docs are thin): Exported module names, class names, CLI command names, route definitions — these represent the public API surface and each is a candidate topic.

### Topic selection criteria

Not every topic makes the cut. Filter by:

- **Is this a core concept a user encounters in the first week?** → Include
- **Is this an advanced/niche feature?** → Include only if token budget allows
- **Is this about installation/setup?** → Include only if setup is non-trivial
- **Is this deprecated?** → Exclude
- **Is this internal/implementation detail?** → Exclude

### Topic ordering

Order topics by dependency and learning path:
1. What the library/project IS (overview)
2. Getting started / installation (only if non-trivial)
3. Core concepts in order of dependency (e.g., routing before middleware)
4. Data flow / state management
5. Integration points
6. Advanced patterns
7. Configuration reference

**Output of Phase 2**: An ordered list of 8-25 topic names, each with a pointer to the source doc chunk(s) that cover it.

---

## PHASE 3 — Per-Section Synthesis

This is the core generation step. For each topic, produce a single Markdown section.

### Section format (strict)

```markdown
## {Topic Name}

{1-3 sentences: what it is, when you'd use it, one key thing to know.}

```{language}
// Annotated code example — complete enough to copy-paste
// Inline comments only for non-obvious lines
```

```{language}
// OPTIONAL second code block — only when the concept spans two
// languages or distinct usage contexts (e.g., .env file + tsx usage,
// reading cookies vs. writing cookies in separate server contexts)
```
```

### Synthesis rules

For each topic, read the relevant source doc chunk(s) and produce the section following these constraints:

1. **Explanation**: 1-3 sentences. First sentence says what it is. Following sentences say when/why you'd use it or what the most important gotcha is. No fluff, no "In this section we'll explore..."

2. **Code example**: One primary fenced code block per section, with an optional second block when the concept genuinely spans two languages or distinct usage contexts (e.g., a `.env` file + TypeScript usage, or reading vs. writing cookies in different server contexts). Don't split into two blocks what could be one.
   - **Complete**: Include enough code that a developer can copy-paste it into a project and understand the concept. Don't strip context to the point of being cryptic — but don't add boilerplate either.
   - **Annotated**: Add inline comments only for non-obvious lines (don't comment `import React from 'react'`)
   - **Runnable where possible**: If the snippet can be copy-pasted and run, it should be. If it's illustrative (e.g., a component), it should be self-contained enough to drop into a project.
   - **Current**: Use the APIs from the pinned version, not deprecated ones
   - **Idiomatic**: Follow the library's own conventions and style

3. **What to exclude from each section**:
   - Installation steps (unless the topic IS setup)
   - More than two code blocks per section
   - Prose explanations beyond 3 sentences
   - Links to external resources
   - Deprecated APIs or patterns
   - Type definitions unless they're the concept being explained

### Token budgeting per section

Given a total token budget `T` and `N` sections:
- Header + overview: ~300 tokens (two paragraphs for complex frameworks)
- Summary section: ~200 tokens
- Each topic section gets roughly `(T - 500) / N` tokens
- Code-heavy sections (API reference, config) can borrow from prose-light sections
- If a section can't be meaningfully covered in its budget, combine it with a related section or drop it

---

## PHASE 4 — Assembly

Combine all sections into the final document.

### Document structure

```markdown
# {Library/Project Name}

{Overview paragraph 1: what it is, its core paradigm/architecture, and the most important thing about the current version.}

{Overview paragraph 2 (optional, for complex frameworks): additional context on capabilities, rendering model, or developer experience that helps an LLM answer questions accurately.}

## {Topic 1}

{explanation + code}

## {Topic 2}

{explanation + code}

...

## Summary

{1-2 paragraphs tying the concepts together: how the pieces compose into a typical application architecture, which APIs to reach for in common scenarios, and key integration patterns. This section acts as a RAG anchor — it gives the retriever a "how these pieces fit together" chunk that individual topic sections can't provide.}
```

### Assembly rules

1. The H1 is the library/project name — nothing else in H1.
2. The overview is 2-3 sentences for simple libraries, or two short paragraphs for complex frameworks. It should answer: "If I know nothing about this, what is it and why does it matter?"
3. Sections are separated by a single blank line (no horizontal rules, no extra spacing).
4. No table of contents — the H2 headings ARE the table of contents for RAG chunking.
5. No metadata, frontmatter, or preamble — the document starts with `# Name`.
6. The final `## Summary` section is required. It connects the dots between individual sections: which concept to use when, how they compose, and common architecture patterns. Keep it to 1-2 paragraphs.
7. The final document should feel like it was written by a senior developer who uses this library daily and wants to save a colleague time.

### Token budget enforcement

After assembly, estimate the total token count (rough: `word_count * 1.3`). If over budget:
1. First: trim code comments that explain obvious things
2. Second: shorten explanations to 1 sentence per section
3. Third: drop lowest-priority sections from the bottom
4. Last resort: merge related sections

---

## PHASE 5 — Output

Save the assembled document to disk.

### File naming

- If the user specified a name: use it
- Default for a library: `{library-name}.llms.txt` (e.g., `next-js.llms.txt`)
- Default for a local codebase: `llms.txt` at the repo root
- Alternative: `{name}.context.md` if the user prefers `.md` extension

### Save location

- If in a codebase: save to the repo root (or a `docs/` directory if one exists)
- If generating for external use: save to `/home/claude/` and present to user
- Always copy final output to `/mnt/user-data/outputs/` for download

---

## Parameters

The user can control these. Use sensible defaults if not specified.

| Parameter | Default | Description |
|-----------|---------|-------------|
| Token budget | 10,000 | Total output size. 5K for focused topics, 10K for standard, 20K for comprehensive |
| Version | latest | Git tag, branch, or `latest` |
| Language | auto-detect | Primary language for code examples |
| Topic filter | all | Comma-separated list of topics to include (e.g., "routing, data-fetching, auth") |
| Code density | balanced | `code-heavy` = more/longer snippets, `info-heavy` = more prose, less code |

If the user says something like "make it short" → use 5K budget. "Give me everything" → use 20K. "Focus on routing and auth" → topic filter.

---

## Quality Checklist (Self-Review Before Output)

Before saving, verify:

- [ ] Every H2 section has one primary code block (and at most one optional second block justified by language/context split)
- [ ] No section explanation exceeds 3 sentences
- [ ] Code examples are in the correct language and use current APIs
- [ ] Code examples are complete enough to copy-paste — not stripped to the point of being cryptic
- [ ] No deprecated patterns or APIs
- [ ] The overview accurately describes what the library/project is (2-3 sentences or two short paragraphs)
- [ ] A `## Summary` section exists at the end, tying concepts together into architecture guidance
- [ ] Total token count is within budget (±10%)
- [ ] Sections are ordered by dependency (earlier concepts don't reference later ones)
- [ ] The document is self-contained — no broken references to other sections
- [ ] No installation instructions unless setup IS the concept
- [ ] Each section is independently useful as a retrieval unit

---

## Examples

### Example: User provides a GitHub URL

**User**: "Generate an llms.txt for https://github.com/supabase/supabase"

**Action**: Remote mode → sparse clone → discover docs in `apps/docs/` → extract topics (Auth, Database, Storage, Realtime, Edge Functions, etc.) → synthesize each → assemble at 10K tokens → save as `supabase.llms.txt`

### Example: User is inside a codebase

**User**: "Create an LLM-friendly reference for this project"

**Action**: Local mode → scan for docs and source → identify project name from `package.json` → extract topics from README H2s + source module structure → synthesize → assemble → save as `llms.txt` at repo root

### Example: User wants focused output

**User**: "Generate context docs for Next.js, just routing and data fetching, keep it under 5K tokens"

**Action**: Remote mode → fetch Next.js docs → filter to routing + data fetching topics only → synthesize with 5K budget → save as `next-js.llms.txt`

---

## Edge Cases

- **No docs found**: Fall back to README + source code analysis. Generate sections from exported APIs, CLI commands, or class structures. Warn the user that output quality depends on source code comments.
- **Docs are auto-generated API reference only**: Synthesize from the API reference but group related endpoints/methods into conceptual sections rather than listing every method.
- **Monorepo**: Ask which package/app to target, or generate separate documents per package.
- **Non-English docs**: Generate in the language of the source docs unless the user specifies otherwise.
- **Token budget too small for topic count**: Prioritize core concepts, drop advanced topics, and tell the user what was excluded.
