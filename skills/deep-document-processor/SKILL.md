---
name: deep-document-processor
description: >
  Apply disciplined multi-pass reading to extract token-efficient, decision-relevant
  context from large documents, codebases, or research papers. Use this skill whenever
  an agent needs to process a document longer than ~2000 tokens and produce a compressed
  context representation — not a summary for humans, but a context artifact optimized
  for downstream agent reasoning. Triggers on: "read this and extract what matters",
  "process this document for context", "what's relevant in this for our task?",
  "distill this", "context-extract", or any situation where a large input must be
  compressed into a smaller, high-signal context window. Also trigger when an agent
  is about to dump an entire document into context — this skill replaces naive
  full-inclusion with structured extraction. Do NOT use for simple summarization
  requests aimed at human readers — this skill optimizes for agent consumption.
---

# Deep Document Processor

Transform large documents into token-efficient context artifacts optimized for
downstream agent reasoning. Goal: **maximum decision-relevant signal per token**, not human-readable summaries.

Naive approaches fail predictably:
- **Full inclusion**: blows budget, buries signal
- **Naive truncation**: loses structure, misses late insights
- **Single-pass summary**: misses cross-references, flattens hierarchy

## The Protocol: Four Passes

### Pass 1 — Structural Survey (≤30 seconds)

Extract the document's skeleton before reading content. Creates a mental map guiding attention in later passes.

**Extract:**
- Document type and purpose (paper? spec? report? guide?)
- Table of contents / section headings / file tree
- Total length estimate (pages, sections, or tokens)
- Key entities mentioned (people, systems, concepts)
- Publication date and freshness signal

**Output format:**
```
STRUCTURE:
- Type: [document type]
- Sections: [numbered list of headings/sections]
- Length: [estimate]
- Key entities: [comma-separated]
- Freshness: [date or "undated"]
```

### Pass 2 — Selective Extraction (The 20% Rule)

Read each section and extract ONLY content meeting one of these criteria:
1. **Decision-relevant**: Would change a downstream choice or recommendation
2. **Constraint-defining**: Sets boundaries on what's possible or allowed
3. **Counter-intuitive**: Contradicts likely assumptions an agent might hold
4. **Dependency-creating**: Other facts depend on this being known

**Hard constraint**: extracted content ≤20% of original tokens. If extracting more, stop and re-evaluate decision-relevant vs. merely interesting.

**Extraction format** — telegram-style, not prose:
```
EXTRACT [Section Name]:
- [fact/constraint/insight in ≤15 words]
- [fact/constraint/insight in ≤15 words]
- COUNTER-INTUITIVE: [thing that contradicts common assumption]
```

### Pass 3 — Cross-Reference and Conflict Scan

Review your Pass 2 extracts and identify:
- **Internal contradictions**: Does section 3 contradict section 7?
- **Cross-references**: Does understanding X require knowing Y from another section?
- **Missing context**: Are there terms, acronyms, or concepts used without definition?
- **Implicit assumptions**: What does the document assume the reader already knows?

**Output format:**
```
CROSS-REFS:
- [Section X] depends on [Section Y]: [why]
- CONFLICT: [Section A] says X, but [Section B] implies Y
- UNDEFINED: [term/concept] used but never defined
- ASSUMES: [implicit knowledge required]
```

### Pass 4 — Context Artifact Assembly

Combine passes 1-3 into a single context artifact for agent consumption.

**Template:**
```
=== CONTEXT: [Document Title] ===
Type: [type] | Freshness: [date] | Compression: [X% of original]

STRUCTURE MAP:
[Pass 1 skeleton — 2-3 lines max]

KEY EXTRACTS:
[Pass 2 content, organized by relevance not document order]

DEPENDENCIES & CONFLICTS:
[Pass 3 findings — only if non-empty]

AGENT NOTES:
- [Any warnings about document quality, bias, or missing info]
- [Suggested follow-up if context is insufficient]
===
```

## Quality Checks

1. **Compression ratio**: ≤20% of input tokens. If not, cut more.
2. **Standalone test**: Could an agent with ONLY this artifact make the same decisions as with the full document? If not, what's missing?
3. **No filler**: Every line passes "would removing this change a decision?". If no — delete.
4. **Telegram density**: cut articles, hedging, qualifiers ruthlessly.

## Anti-Patterns

- **Summarizing for humans**: not a book report. No flowing prose.
- **Preserving document order**: organize by relevance, not appearance.
- **"Interesting but irrelevant"**: if it doesn't affect decisions, cut it.
- **Over-extracting definitions**: only define terms the downstream agent won't know.
- **Hedging**: "The document seems to suggest..." — No. State what it says. Flag uncertainty explicitly if needed, but don't hedge the extraction itself.
