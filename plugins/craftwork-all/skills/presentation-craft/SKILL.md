---
name: presentation-craft
description: "Apply this skill whenever the user needs to create, plan, structure, or improve a presentation, talk, pitch, keynote, or slide deck. Triggers on phrases like 'make a presentation about', 'I have a talk on', 'help me structure my deck', 'create slides for', 'pitch deck for', 'I'm presenting at', 'conference talk', 'prepare a keynote', 'workshop slides', or any request that involves communicating ideas to an audience via slides and spoken delivery. Also trigger when the user has existing slides and wants to improve the narrative flow, when they need speaker notes, or when they want to rehearse timing. This skill does NOT produce .pptx files directly (use the pptx skill for file creation). This skill produces the presentation SCRIPT — the narrative blueprint that determines what each slide says, shows, and how long the presenter spends on it."
---

# Presentation Craft

A presentation is a performance with a narrative arc moving the audience from where they are to where you need them to be. Great talks oscillate between "what is" and "what could be," building tension that resolves in a call to action. Design that arc before touching a slide.

Deliverable: a **Presentation Script** — narrative arc, each slide's visual, presenter notes, and time allocation per slide and overall.

---

## STEP 1 — Gather Context

Establish these parameters. Some come from the request; ask for the rest.

```
PRESENTATION CONTEXT
Topic: [what it's about]
Core message: [the ONE thing they should remember]
Audience type: [see classification]
Audience size: [intimate <15 / room 15-100 / auditorium 100+ / virtual]
Time slot: [total minutes, including Q&A]
Setting: [conference / internal meeting / pitch / workshop / lecture / lightning]
Constraints: [template, branding, language, accessibility]
Desired outcome: [what should they DO after?]
```

#### Audience Classification

| Audience | Characteristics | Implications |
|----------|----------------|--------------|
| **Technical Peers** | Deep knowledge, skeptical of hand-waving | Less context, more depth. Jargon OK. Evidence + trade-offs. Denser slides. |
| **Technical Mixed** | Varying expertise | Layer: accessible surface, technical depth available. Visual > text. |
| **Leadership / Executives** | Time-poor, decision-focused | BLUF. Lead with "so what." Outcomes over process. One idea per slide. |
| **Cross-functional** | Product, design, eng, business mixed | No single team's jargon. Problem/solution frame. Visuals + examples. |
| **External / Conference** | Don't know you, came for the topic | Earn attention in 60s. Strong hook. No assumed context. Story > data. |
| **Investors / Pitch** | Evaluating opportunity, risk, team, market | Pitch deck conventions. Numbers matter. Address risks. Clear ask. |
| **Workshop / Training** | Came to learn and practice | Interactive beats. Exercises between theory. Slides scaffold, not content. |
| **General / Non-technical** | No domain expertise | Analogies > abstractions. One idea per slide. Emotional > logical. |

---

## STEP 2 — Ask the User

Present inferred context and confirm in one interaction.

```
Here's what I'm working with:

Topic: [inferred]
Core message: [inferred or "Tell me the ONE thing they should remember"]
Audience: [classified]
Time: [inferred or "How long is your slot?"]
Outcome: [inferred or "What should they DO after?"]

Adjust anything? Which narrative style fits best:
```

| Arc | Structure | Best for |
|-----|-----------|----------|
| **Sparkline** (Duarte) | Oscillate "what is" vs "what could be." Build tension via contrast. End with "new bliss." | Conference talks, keynotes, persuasive, change proposals |
| **Situation → Complication → Resolution** | World as is, problem, solution. Linked by "but" and "therefore." | Consulting, B2B pitches, internal proposals, technical recs |
| **Hook → Meat → Payoff** | Grab attention, deliver substance, memorable close. | Lightning talks, short presentations, internal updates |
| **Explanation Journey** | Meet them where they are, lay roadmap, walk through, arrive at understanding. | Workshops, training, technical deep-dives, education |
| **Hero's Journey** | Status quo → call → trials → transformation → return with elixir. AUDIENCE is the hero. | Inspirational talks, case studies, transformation stories |
| **Problem → Evidence → Solution → Ask** | State problem, show data, present solution, make ask. | Pitch decks, funding, resource requests |

**Recommendation logic:**

```
IF conference/keynote → Sparkline
IF internal proposal → Situation-Complication-Resolution
IF lightning talk (<10 min) → Hook-Meat-Payoff
IF workshop/training → Explanation Journey
IF pitch/investors → Problem-Evidence-Solution-Ask
IF case study/retrospective → Hero's Journey
```

---

## STEP 3 — Design the Narrative Spine

Write the spine before any slides. Strong spine + mediocre slides beats beautiful slides + no spine.

```
NARRATIVE SPINE

Opening hook: [first words — question, stat, story, provocation]

Act 1 — Setup: [where are we now? what does the audience know/feel?]
  Key emotion: [curiosity / concern / recognition / frustration]

Tension point: [the "but..." — what's broken, missing, at risk?]

Act 2 — Confrontation: [explore problem, build understanding, show evidence]
  Key emotion: [urgency / insight / surprise]

Turn: [the "therefore..." — shift toward resolution]

Act 3 — Resolution: [solution, vision, path forward]
  Key emotion: [hope / confidence / clarity]

Closing: [call to action — what should they DO?]
  Last words: [final sentence they'll remember. Write it now.]

Narrative thread: [the metaphor, story, or throughline connecting everything.
  e.g., "Bridges vs. walls" / recurring case study developing across the talk]
```

The **narrative thread** separates a presentation from a slide deck. Without it: collection of slides. With it: a story.

---

## STEP 4 — Produce the Presentation Script

Each slide entry:

```
═══════════════════════════════════════════════════════════
SLIDE [N] of [TOTAL]                           ⏱ [M:SS]
Arc position: [Act 1 / Tension / Act 2 / Turn / Act 3]
═══════════════════════════════════════════════════════════

SLIDE TITLE: [as it appears]

VISUAL DESCRIPTION:
[What the slide LOOKS like. Visual design, not content.
 e.g., "Full-bleed photo of busy airport terminal. Single stat
 overlaid in white: '4.2 billion passengers/year.' No other text."]

CONTENT ON SLIDE:
[Actual text, data, or diagram description. Minimal —
 paragraphs on a slide = writing a document, not a presentation.]

PRESENTER NOTES:
[What the presenter SAYS. Natural speech, not bullets. Include:
 - Transition from previous ("So now that we've seen X...")
 - Key point on this slide
 - Bridge to next ("Which brings us to...")
 - Audience interaction cues ("Show of hands — how many of you...")
 - Emotional beats ("Pause here. Let this sink in.")]

NARRATIVE FUNCTION:
[Hook / Context / Evidence / Tension / Insight / Solution /
 Example / Transition / Callback / Call to Action / Closing]
───────────────────────────────────────────────────────────
```

#### Timing Guidelines

| Slide type | Duration | Notes |
|------------|----------|-------|
| Title / Opening | 0:30 - 1:00 | Introduce, set the stage |
| Hook slide | 0:30 - 1:30 | Grab attention — don't linger |
| Context / Setup | 1:00 - 2:00 | Establish shared understanding |
| Data / Evidence | 1:00 - 2:00 | Let data speak — don't over-explain |
| Key Insight | 1:00 - 2:00 | Let it land — don't rush |
| Story / Anecdote | 1:30 - 3:00 | Stories need breathing room |
| Demo / Example | 2:00 - 4:00 | Show, don't tell |
| Transition | 0:15 - 0:30 | Brief connective tissue |
| Interactive / Question | 1:00 - 3:00 | Allow response time |
| Solution / Proposal | 1:30 - 2:30 | Clear and concrete |
| Call to Action | 0:30 - 1:00 | Crisp and memorable |
| Closing | 0:30 - 1:00 | Last words matter most |

**Slide count**: ~1 slide per 1.5-2 min. 30-min talk = 15-20 slides. 10-min lightning = 5-8. Adjust for density.

#### Script Footer

```
═══════════════════════════════════════════════════════════
TIMING SUMMARY
═══════════════════════════════════════════════════════════
Total slides: [N]
Total speaking time: [M:SS]
Buffer for Q&A: [M:SS]
Slot duration: [M:SS]

Pacing check:
- Fastest section: [Act/section] at [slides/min]
- Slowest section: [Act/section] at [slides/min]
- Risk: [section that might run long or feel rushed]

Rehearsal note: First rehearsal will likely run 15-20% over.
Cut from Act 2 (the middle) first — never cut opening or closing.
```

---

## STEP 5 — Review and Strengthen

- **Mute Test**: Look at only visuals, no notes. Does the visual sequence tell a story? Would silent flip-through convey the gist?
- **Bar Test**: Can you explain the core message in one sentence to someone at a bar? If not, too many things.
- **So What Test**: After each slide, would they think "so what?" Either the slide doesn't earn its place, or notes don't connect it to what they care about.
- **Callback Test**: Does the closing connect back to the opening? Strongest presentations create a loop.
- **Timing Test**: Total within slot? Leave 10-15% buffer — talks always run long, never short.
- **One-Idea-Per-Slide Test**: Any slide making two points? Split it. Audience listens AND reads simultaneously.

---

## Calibration Rules

1. **Audience is the hero, not the presenter.** Frame everything in terms of their problems, opportunities, world. You're the guide.
2. **Complexity kills.** If a slide needs 3 min of explanation, it's too complex. Simplify, split, or move to appendix.
3. **Every slide must earn its place.** Ask: "What happens if I delete this?" If nothing — delete.
4. **Open with a hook, not an agenda.** "Today I'll cover three topics..." is an anti-hook. Open with a question, stat, claim, or story. Agenda goes on slide 2 if at all.
5. **Close with the call to action, not "Questions?"** Last slide should reinforce core message — not generic Q&A or Thank You.
6. **Presenter notes are speech, not bullets.** Bullet notes produce bullet delivery.
7. **Design for the back row.** Unreadable text = too small. Chart not understood in 5s = too complex. Applies to virtual too.
8. **Adapt the arc, don't skip it.** Even a 5-min lightning talk has beginning, middle, end. The arc scales down — it doesn't disappear.

---

## Thinking Triggers

- *"If they remember only ONE thing, what must it be?"*
- *"What do they believe RIGHT NOW, and what do I need them to believe AFTER?"*
- *"Where is the tension? No tension = no story."*
- *"Am I telling or showing? Can I replace this bullet with a visual, demo, or story?"*
- *"Would I pay attention to this slide at 3pm after lunch?"*
- *"Does my closing circle back to my opening? Does the last sentence land?"*
