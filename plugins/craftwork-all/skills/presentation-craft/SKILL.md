---
name: presentation-craft
description: "Apply this skill whenever the user needs to create, plan, structure, or improve a presentation, talk, pitch, keynote, or slide deck. Triggers on phrases like 'make a presentation about', 'I have a talk on', 'help me structure my deck', 'create slides for', 'pitch deck for', 'I'm presenting at', 'conference talk', 'prepare a keynote', 'workshop slides', or any request that involves communicating ideas to an audience via slides and spoken delivery. Also trigger when the user has existing slides and wants to improve the narrative flow, when they need speaker notes, or when they want to rehearse timing. This skill does NOT produce .pptx files directly (use the pptx skill for file creation). This skill produces the presentation SCRIPT — the narrative blueprint that determines what each slide says, shows, and how long the presenter spends on it."
---

# Presentation Craft

**Core principle**: A presentation is not a document read aloud. It is a performance with a narrative arc that takes the audience from where they are to where you need them to be. Every great presentation — from Steve Jobs' iPhone launch to Martin Luther King's "I Have a Dream" — follows the same structural pattern: oscillating between "what is" (the current reality) and "what could be" (the future you're proposing), building tension that resolves in a call to action. This skill designs that arc before touching a single slide.

The deliverable is a **Presentation Script** — a complete blueprint containing: the narrative arc, each slide's visual description, presenter notes with what to say, and time allocation per slide and overall.

---

## How to Execute This Skill

### STEP 1 — Gather Context

Before designing anything, establish these parameters. Some will come from the user's request; others must be asked.

```
PRESENTATION CONTEXT
Topic: [what the presentation is about]
Core message: [the ONE thing the audience should remember]
Audience type: [see audience classification below]
Audience size: [intimate (<15) / room (15-100) / auditorium (100+) / virtual]
Time slot: [total minutes available, including Q&A if applicable]
Setting: [conference talk / internal meeting / pitch / workshop / lecture / lightning talk]
Constraints: [template requirements, corporate branding, language, accessibility needs]
Desired outcome: [what should the audience DO after this presentation?]
```

#### Audience Classification

The audience type determines language level, assumed knowledge, narrative style, and slide density. Classify into one of these:

| Audience | Characteristics | Implications |
|----------|----------------|--------------|
| **Technical Peers** | Deep domain knowledge, skeptical of hand-waving, value precision | Less context-setting, more depth. Can use jargon. Prioritize evidence and trade-offs. Slides can be denser. |
| **Technical Mixed** | Varying expertise levels in the room | Layer the explanation: accessible surface, technical depth available. Visual > text-heavy. |
| **Leadership / Executives** | Time-poor, decision-focused, care about impact and cost | BLUF structure. Lead with "so what." Minimize process, maximize outcomes. One idea per slide. |
| **Cross-functional** | Product, design, engineering, business together | Avoid any single team's jargon. Use the problem/solution frame everyone shares. Heavy on visuals and examples. |
| **External / Conference** | Don't know you or your company, came for the topic | Must earn attention in first 60 seconds. Strong hook. No assumed context. Story-driven over data-driven. |
| **Investors / Pitch** | Evaluating opportunity, risk, team, and market | Follow pitch deck conventions. Numbers matter. Address risks proactively. Clear ask at the end. |
| **Workshop / Training** | Came to learn and practice, not just listen | Interactive beats. Exercises between theory. Slides are scaffolding, not the content. |
| **General / Non-technical** | No domain expertise, want to understand the "why" | Analogies over abstractions. One idea per slide. Emotional resonance over logical proof. |

---

### STEP 2 — Ask the User

Present the context you've inferred and ask for confirmation or adjustment in a single interaction.

```
Here's what I'm working with:

Topic: [inferred]
Core message: [inferred or "I need you to tell me the ONE thing they should remember"]
Audience: [classified]
Time: [inferred or "How long is your slot?"]
Outcome: [inferred or "What should they DO after your talk?"]

Adjust anything? And which narrative style fits best:
```

Offer narrative arc options based on the setting:

| Arc | Structure | Best for |
|-----|-----------|----------|
| **Sparkline** (Duarte) | Oscillate between "what is" and "what could be" throughout. Build tension through contrast. End with the "new bliss" — the future state if the audience acts. | Conference talks, keynotes, persuasive presentations, change proposals |
| **Situation → Complication → Resolution** | Establish the world as it is. Introduce the problem. Present the solution. Linked by "but" and "therefore." | Consulting presentations, B2B pitches, internal proposals, technical recommendations |
| **Hook → Meat → Payoff** | Open with something that grabs attention (question, stat, story). Deliver the substance. Close with a clear, memorable payoff. | Lightning talks, short presentations, internal updates |
| **Explanation Journey** | Meet the audience where they are. Lay out the roadmap. Walk through step by step. Arrive at understanding. | Workshops, training sessions, technical deep-dives, educational talks |
| **Hero's Journey** | Status quo → Call to adventure (opportunity/problem) → Trials (challenges faced) → Transformation → Return with the elixir (lessons/solution). The AUDIENCE is the hero, not the presenter. | Inspirational talks, case studies, transformation stories |
| **Problem → Evidence → Solution → Ask** | State the problem. Show the data. Present the solution. Make the ask. | Pitch decks, funding presentations, resource requests |

**Recommendation logic:**

```
IF conference/keynote → Sparkline (most engaging for earned attention)
IF internal proposal/recommendation → Situation-Complication-Resolution
IF lightning talk / short slot (<10 min) → Hook-Meat-Payoff
IF workshop/training → Explanation Journey
IF pitch/investors → Problem-Evidence-Solution-Ask
IF case study/retrospective → Hero's Journey
```

---

### STEP 3 — Design the Narrative Spine

Before writing any slides, write the narrative spine — the story backbone that every slide will hang from. This is the most important step. A presentation with a strong spine and mediocre slides will outperform a presentation with beautiful slides and no spine.

```
NARRATIVE SPINE

Opening hook: [First words out of your mouth — question, stat, story, provocation]

Act 1 — Setup: [Where are we now? What does the audience already know/feel?]
  Key emotion: [curiosity / concern / recognition / frustration]

Tension point: [The "but..." — what's broken, missing, or at risk?]

Act 2 — Confrontation: [Explore the problem. Build understanding. Show evidence.]
  Key emotion: [urgency / insight / surprise]

Turn: [The "therefore..." — the shift toward resolution]

Act 3 — Resolution: [The solution, the vision, the path forward]
  Key emotion: [hope / confidence / clarity]

Closing: [Call to action — what should the audience DO?]
  Last words: [The final sentence they'll remember. Write it now.]

Narrative thread: [The metaphor, story, or throughline that connects everything.
  e.g., "Building bridges vs. building walls" / "The map is not the territory" /
  A recurring character or case study that develops across the talk]
```

The **narrative thread** is what separates a presentation from a slide deck. It's the recurring element — a metaphor, a character, a case study, a visual motif — that weaves through the entire talk and gives it coherence. Without it, you have a collection of slides. With it, you have a story.

---

### STEP 4 — Produce the Presentation Script

Now produce the slide-by-slide script. Each slide entry follows this format:

```
═══════════════════════════════════════════════════════════
SLIDE [N] of [TOTAL]                           ⏱ [M:SS]
Arc position: [Act 1 / Tension / Act 2 / Turn / Act 3]
═══════════════════════════════════════════════════════════

SLIDE TITLE: [Title text as it appears on the slide]

VISUAL DESCRIPTION:
[What the slide LOOKS like. Not the content — the visual design.
 e.g., "Full-bleed photo of a busy airport terminal. Single stat
 overlaid in white: '4.2 billion passengers/year.' No other text."
 or "Two-column comparison. Left: current architecture diagram.
 Right: proposed architecture. Differences highlighted in orange."
 or "Black slide. Single sentence centered in large white type."]

CONTENT ON SLIDE:
[The actual text, data points, or diagram descriptions that appear.
 Keep it minimal — if you're putting paragraphs on a slide,
 you're writing a document, not a presentation.]

PRESENTER NOTES:
[What the presenter SAYS while this slide is showing.
 Written in natural speech, not bullets.
 Include:
 - The transition from the previous slide ("So now that we've seen X...")
 - The key point to make on this slide
 - The bridge to the next slide ("Which brings us to...")
 - Any audience interaction cues ("Show of hands — how many of you...")
 - Emotional beats ("Pause here. Let this sink in.")]

NARRATIVE FUNCTION:
[What this slide DOES in the story. One of:
 Hook / Context / Evidence / Tension / Insight / Solution /
 Example / Transition / Callback / Call to Action / Closing]
───────────────────────────────────────────────────────────
```

#### Timing Guidelines

Use these benchmarks for time estimation per slide:

| Slide type | Typical duration | Notes |
|------------|-----------------|-------|
| Title / Opening | 0:30 - 1:00 | Introduce yourself, set the stage |
| Hook slide | 0:30 - 1:30 | Grab attention — don't linger |
| Context / Setup | 1:00 - 2:00 | Establish shared understanding |
| Data / Evidence | 1:00 - 2:00 | Let the data speak — don't over-explain |
| Key Insight | 1:00 - 2:00 | Let the idea land — don't rush |
| Story / Anecdote | 1:30 - 3:00 | Stories need breathing room |
| Demo / Example | 2:00 - 4:00 | Show, don't tell — takes longer |
| Transition | 0:15 - 0:30 | Brief connective tissue |
| Interactive / Question | 1:00 - 3:00 | Allow audience response time |
| Solution / Proposal | 1:30 - 2:30 | Clear and concrete |
| Call to Action | 0:30 - 1:00 | Crisp and memorable |
| Closing | 0:30 - 1:00 | Last words matter most |

**Slide count heuristic**: Plan for approximately 1 slide per 1.5-2 minutes of speaking time. A 30-minute talk = 15-20 slides. A 10-minute lightning talk = 5-8 slides. Adjust for slide density — data-heavy slides take longer, visual-only slides are faster.

#### Script Footer

End every script with a timing summary:

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
- Risk: [Any section that might run long or feel rushed]

Rehearsal note: [First rehearsal will likely run 15-20% over.
Cut from Act 2 (the middle) first — never cut the opening or closing.]
```

---

### STEP 5 — Review and Strengthen

After producing the script, apply these checks:

**The Mute Test**: Look at only the slide visuals with no presenter notes. Does the visual sequence tell a story on its own? If someone flipped through the slides silently, would they get the gist?

**The Bar Test**: Can you explain the core message in one sentence to someone at a bar? If not, the presentation is trying to say too many things.

**The "So What" Test**: After each slide, would the audience think "so what?" If yes, either the slide doesn't earn its place, or the presenter notes aren't connecting it to something the audience cares about.

**The Callback Test**: Does the closing connect back to the opening? The strongest presentations create a loop — the last slide echoes or resolves the first.

**The Timing Test**: Add up all slide times. Is the total within the slot? Leave 10-15% buffer — presentations almost always run long, never short.

**The One-Idea-Per-Slide Test**: Does any slide try to make two points? Split it. Cognitive load per slide should be minimal — the audience is listening to you AND reading the slide simultaneously.

---

## Calibration Rules

**1. The audience is the hero, not the presenter.** Your talk is not about you. It's about taking the audience on a journey from their current understanding to a new one. Frame everything in terms of their problems, their opportunities, their world. You are the guide, not the protagonist.

**2. Complexity kills presentations.** If a slide needs 3 minutes of explanation, it's too complex. Simplify the visual, split it into two slides, or move the complexity to an appendix slide. The audience can't process dense information while simultaneously listening to you speak.

**3. Every slide must earn its place.** Ask of each slide: "What happens to the presentation if I delete this?" If the answer is "nothing changes" — delete it. Ruthless curation is the difference between a good talk and a great one.

**4. Open with a hook, not an agenda.** "Today I'll cover three topics..." is an anti-hook. It tells the audience to settle back and wait. Instead, open with a question, a surprising statistic, a bold claim, or a short story that makes them lean forward. The agenda can appear on slide 2 if it must exist at all.

**5. Close with the call to action, not "Questions?"** The last slide the audience sees should reinforce your core message or call to action — not a generic "Q&A" or "Thank you" slide. If there's Q&A, it happens after the closing, not instead of it.

**6. Presenter notes are speech, not bullets.** Write the notes as you would actually speak — full sentences, natural transitions, emotional cues. Bullet-point notes produce bullet-point delivery. Conversational notes produce conversational delivery.

**7. Design for the back row.** If text can't be read from the back of the room, it's too small. If a chart can't be understood in 5 seconds, it's too complex. If the visual requires squinting, it fails. This applies even for virtual presentations — assume a small screen.

**8. Adapt the narrative arc, don't skip it.** Even a 5-minute lightning talk has a beginning, middle, and end. Even an internal status update can have a hook. The arc scales down — it doesn't disappear. A presentation without a narrative is a slide deck, and slide decks are documents that got lost.

---

## Thinking Triggers

- *"If the audience remembers only ONE thing from this talk, what must it be?"*
- *"What does the audience believe RIGHT NOW, and what do I need them to believe AFTER?"*
- *"Where is the tension in this story? If there's no tension, there's no story."*
- *"Am I telling them or showing them? Can I replace this bullet slide with a visual, a demo, or a story?"*
- *"Would I pay attention to this slide if I were in the audience at 3pm after lunch?"*
- *"Does my closing circle back to my opening? Does the last sentence land?"*
