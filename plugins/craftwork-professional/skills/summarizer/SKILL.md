---
name: summarizer
description: "Apply this skill whenever the user asks to summarize, condense, distill, or compress any content — a document, article, meeting notes, conversation, codebase, book, research paper, video transcript, or any other source material. Triggers on phrases like 'summarize this', 'give me the TL;DR', 'condense this', 'what are the key points?', 'distill this down', 'brief me on this', 'what's the gist?', 'BLUF this', 'executive summary', 'compress this for me', or any request to reduce content while preserving its essential value. Also trigger when the user pastes a long text and implicitly wants it shortened, when they share a link and ask 'what does this say?', or when they ask for meeting notes or action items from a transcript. This skill does NOT apply to 'explain X to me' (use topic-explainer) or 'write a summary section for my doc' (use technical-writing). This skill is for when source material exists and needs to be compressed."
---

# Summarizer

**Core principle**: A summary is lossy compression — what you choose to lose defines whether it's useful or dangerous. The right shape depends on what the reader will *do* with it: decision-makers need the conclusion first, future-self needs retrievability, sharers need self-containment. Produce the smallest artifact that preserves the value the reader needs.

---

## STEP 1 — Analyze the Source (internal only — NEVER show)

Classify silently:
- Type: article / document / transcript / conversation / code / paper / book / multi-source
- Length: short (<1K) / medium (1-5K) / long (5-20K) / very long (20K+) / multi-doc
- Density: sparse / mixed / dense
- Structure: well-structured / loose / unstructured
- Contains: arguments / data / narrative / instructions / mixed

---

## STEP 2 — Recommend Style and Compression

### Summarization Styles

| Style | How it works | Best for | Avoid when |
|-------|-------------|----------|------------|
| **BLUF** | Bottom Line Up Front. Conclusion in first sentence; supporting evidence descending by importance. Reader can stop at any point. | Decision-makers, status updates — "what should we do?" matters more than "what happened?" | Exploratory source with no clear conclusion; reader must form own opinion |
| **Key Points** | Extract N most important claims as a structured list. Each point self-contained. Optimized for scanning. | Meeting notes, papers, long reports, anything needing quick lookup | Narrative/argument where logic between points matters as much as the points |
| **Narrative** | Coherent short-form prose preserving logical flow and argumentation. | Articles, essays, arguments, stories — when *reasoning chain* matters | Data dumps or reference material where flow doesn't matter |
| **Briefing** | Self-contained for people who haven't seen the source. Structure: situation → key findings → implications → recommended actions. | Sharing with teammates, leadership updates, async briefings | Reader has source access and just wants compression |
| **Progressive** | Multi-layer. Layer 1: one sentence. Layer 2: paragraph. Layer 3: full summary. Reader picks depth. | Reference material, notes for future self, knowledge management | One-time summaries the reader won't revisit |
| **Action-Oriented** | Only what requires action: decisions, action items, owners, deadlines, open questions. Discard the rest. | Meeting transcripts, planning sessions, retros | Informational content with no actions (use Key Points) |
| **Comparative** | Synthesize multiple sources highlighting agreements, disagreements, unique contributions. | Literature reviews, competitive analysis, multi-article research | Single source |

### Compression Levels

| Level | Ratio | Output | When |
|-------|-------|--------|------|
| **Headline** | ~98% | 1 sentence | "What is this about?" |
| **Snapshot** | ~90% | 2-4 sentences | Quick orientation |
| **Standard** | ~75% | 1-3 paragraphs | Default |
| **Detailed** | ~50% | Multiple paragraphs | Nuance, evidence, caveats matter |
| **Comprehensive** | ~30% | Structured doc | Long/complex sources |

### Fidelity Mode

| Mode | Means | When |
|------|-------|------|
| **Faithful** | Preserves source language, terminology, attributions, qualifications. Accuracy > fluency. | Legal, medical, scientific, compliance |
| **Rewritten** | Rephrases freely; may restructure. Readability > verbatim accuracy. | General content, articles, blogs, meeting notes |

Default to **Rewritten** unless high-stakes domain or user requests faithfulness.

### Recommendation Logic

```
meeting transcript / conversation  → Action-Oriented + Standard + Rewritten
research paper / technical doc     → Key Points + Detailed + Faithful
article / essay / blog             → Narrative + Standard + Rewritten
"brief my team" / "for leadership" → Briefing + Standard + Rewritten
"TL;DR" / "gist" / "quick"         → BLUF + Snapshot + Rewritten
"action items" / "what to do"      → Action-Oriented + Standard + Rewritten
multiple sources                   → Comparative + Standard + Rewritten
"save for future reference"        → Progressive + Detailed + Rewritten
legal/medical/financial/compliance → Key Points + Detailed + Faithful
```

### Incompatible Combinations

- **Action-Oriented + Headline**: Actions need detail. → Snapshot minimum.
- **Comparative + Headline**: Can't synthesize multi-source in one sentence. → Standard minimum.
- **Progressive + Headline/Snapshot**: Progressive already contains a headline. → Standard or Detailed.
- **Faithful + Headline**: Impossible at 98%. → Snapshot + Faithful.
- **Briefing + Headline**: Briefings need context. → Standard minimum.

---

## STEP 3 — Present Options

```
I'd recommend a [style] summary at [compression] depth, [fidelity].
[1-sentence reason.]

Want me to adjust?
  Style: [recommended] / [alt 1] / [alt 2]
  Depth: Headline / Snapshot / Standard / Detailed / Comprehensive
  Fidelity: Faithful / Rewritten
```

Use ask_user_input if available.

**Speed override**: If user pastes content and says "TL;DR" or "summarize quickly", skip interaction and deliver immediately. 2-4 plain sentences or short bullets — no labels, no template, casual tone matching the request.

---

## STEP 4 — Produce the Summary

#### BLUF

```
BOTTOM LINE: [Conclusion / recommendation in 1-2 sentences]

SUPPORTING DETAIL:
[Most important evidence — 1-2 sentences]
[Second most important — 1-2 sentences]
[Additional if compression allows]

SO WHAT: [Why this matters — 1 sentence]
```

**Check**: Cover all but BOTTOM LINE. Does the reader have what they need to act?

#### Key Points

```
KEY POINTS FROM: [source]

1. [Self-contained claim, not topic label]
2. [...]
... N points (Snapshot=3, Standard=5-7, Detailed=8-12)

NOTABLE OMISSIONS: [What you cut — 1 sentence]
```

**Check**: Each point sensible in isolation? "The authors discussed methodology" is a label — rewrite as "The study used a randomized control trial with 500 participants over 12 months."

#### Narrative

Coherent passage preserving reasoning:
1. Open with core thesis/finding
2. Walk through key supporting arguments in order
3. Note most important caveats/counterarguments
4. Close with implication/conclusion

**Check**: Could someone follow the argument from your summary alone?

#### Briefing

```
BRIEFING: [Title]
Source: [what this summarizes] | Date: [created] | Prepared for: [audience]

SITUATION: [Context — 2-3 sentences]
KEY FINDINGS:
- [Finding 1] [...]
IMPLICATIONS: [What this means — 1-2 sentences]
RECOMMENDED ACTIONS: [If applicable]
OPEN QUESTIONS: [Unresolved]
```

**Check**: Send to someone unfamiliar with the source. Self-contained?

#### Progressive

```
## Layer 1 — One Sentence
[Most important takeaway]

## Layer 2 — One Paragraph
[Core message + 2-3 supporting points]

## Layer 3 — Full Summary
[Detailed; preserve evidence, caveats, nuance. Subheadings if source has sections.]
```

**Check**: Each layer valid alone. Layer 1 doesn't need Layer 2.

#### Action-Oriented

```
DECISIONS MADE:
- [Decision 1 + decider if known]

ACTION ITEMS:
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Specific action] | [Name] | [Date] | Open |

OPEN QUESTIONS:
- [Question — who answers?]

PARKING LOT: [Deferred topics — 1-2 sentences]
```

**Check**: Could someone who missed the meeting know exactly what to do? "Follow up on X" without specifics isn't actionable.

#### Comparative

```
SYNTHESIS: [Sources]

CONSENSUS: [Where all/most agree]
- [Shared finding]

DIVERGENCE: [Where sources disagree]
- [A says X; B says Y — tension is about Z]

UNIQUE CONTRIBUTIONS:
- [Source C uniquely argues...]

GAP: [What none address]
```

**Check**: Each source fairly represented? Distinct contribution visible?

---

## STEP 5 — Offer Follow-up

Pick one based on style:

- **BLUF**: "Want me to expand any supporting detail?"
- **Key Points**: "Want me to elaborate on any point?"
- **Narrative**: "Compress further or expand a section?"
- **Briefing**: "Adjust for a different audience?"
- **Progressive**: "Add a Layer 4 — your executive annotation?"
- **Action-Oriented**: "Draft follow-up messages for any action items?"
- **Comparative**: "Deep-dive into any divergence?"

Skip if user signals completion.

---

## Calibration

1. **Compression is not deletion.** Preserve information density while reducing volume. Did you lose anything the reader would want back?
2. **Flag what you cut.** Standard or above: include "NOTABLE OMISSIONS" so reader knows when to consult the original.
3. **Multi-source requires synthesis, not concatenation.** Never summarize each source independently and stack. The value is in cross-references.
