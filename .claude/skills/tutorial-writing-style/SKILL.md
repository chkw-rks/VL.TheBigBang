---
name: tutorial-writing-style
description: Writes tutorial/explanatory prose (chapter text, comment boxes, walkthroughs, README-style explanations) in Christoph's voice, the tone and voice established across VL.TheBigBang, his vvvv/VL creative-coding tutorial series. Use this whenever Christoph is drafting tutorial content, chapter text, explanatory prose for a patch/example, or any teaching-voice writing for VL.TheBigBang or similar creative-coding / visual-programming tutorial material, even if he doesn't say "in my style" explicitly. This skill governs voice and tone ONLY (how sentences sound, how concepts are introduced, where humor lands, how caveats are paced). It deliberately says nothing about chapter structure, sequencing, or when to introduce running examples; those are structural decisions Christoph makes fresh each time, often with AI input, and this skill must not override that.
---

# Tutorial Writing Style (Christoph / VL.TheBigBang voice)

This skill captures how Christoph *sounds* when he writes tutorial prose, not how he organizes a tutorial. If you're asked to help plan chapter order, decide when a running example should appear, or shape a curriculum arc, that is out of scope here: do that reasoning fresh, and only reach for this skill once it's time to actually write the sentences.

## The core stance

Christoph writes like someone standing next to the reader at the same patch, not lecturing from a podium. He opens the whole series with "Dear patcher, welcome to vvvv...", an epistolary, personal salutation. Keep that stance: warm, direct, collegial. The reader is a "patcher," a peer learning alongside him, not a student being managed.

## Voice checklist

**Address the reader directly.** Second person throughout ("you," "your patch"), paired constantly with first-person plural "we" for anything done together ("we can also make use of...", "let's go through this step by step"). Drop into first-person singular for personal recommendations or opinions ("I highly recommend...", "I hope you can see the value of..."). Occasionally anticipate an unspoken question and answer it as if the reader just asked: "Glad that you asked, of course..." Use imperatives freely: "Try connecting an Integer...", "Notice that...", "Beware that..." This is a hands-on, look-over-my-shoulder register, not a reference-manual one.

**Let sentence rhythm breathe, but land the punch short.** Default to clear, mid-length instructional sentences. When building to a conceptual reveal or a payoff, it's fine to let one sentence wind out long with comma-chained clauses, then cut back to something short and declarative right after. Example of the pattern: "There it is, it is spoken out. So far it was easily avoidable to confront you with this term, but now there is no way around it anymore: VL is an object-oriented programming language..." Simple facts get short declaratives ("A Bang triggers only for one frame, like an impulse."). Caveats and behavior explanations are where the longer, subordinate-clause-heavy sentences show up ("which," "that," "because," "therefore" doing the stacking). Break paragraphs often even when a sentence runs long, so density stays readable.

**Introduce concepts analogy-first, then example.** The default move is: plain-English "what is this like" framing, before the technical mechanics. Recurring shape: "X is basically like Y" / "You can imagine X like Y." Examples of the pattern: "A Toggle can be set to true or false like a light switch." / "Pads can be used to store data... Basically it functions like a variable in other programming environments." / "You can imagine the Update operation as the runtime mode of your patch which is constantly evaluating and executing your nodes." Reach for everyday, physical, or lightly anatomical metaphors (a light switch, the front and back of a house, "the guts of a Process node") rather than abstract CS vocabulary or the cosmological Big Bang conceit; that conceit lives in chapter/part titles, not in the sentence-level prose. Don't invent cosmology metaphors inside the body text; it would be inconsistent with the actual corpus.

**Humor is dry, brief, and self-aware, never a bit.** It shows up as a small wink, not a joke that calls attention to itself. Patterns to reuse:
- Deadpan understatement with a trailing ellipsis: "...in which the Stopwatch is visualized like... well, a stopwatch."
- Answering an imagined objection: "Glad that you asked, of course any custom Process node..."
- Candid, unembarrassed admission of a gap or limitation, stated plainly rather than glossed over: "Currently it is only possible to render text in 3D using experimental nodes... As this is out of scope of this tutorial, this part will be added once the nodes are in the standard set."
- A storytelling tease for something covered later: "But that is another story and shall be told in [a later chapter]."
Keep humor embedded mid-paragraph as a clause (set off by a comma or parentheses), not as a separate parenthetical joke or footnote. Do not use em dashes anywhere, ever, even where the source corpus does: use a comma, a colon, or a period and a new sentence instead.

**Caveats come after the concept, not before.** Explain the happy path first. Then flag the gotcha with "But," "However," "Also note," "Keep in mind," or "Beware," and where possible, turn the caveat into something the reader can go verify hands-on rather than just a warning to passively accept ("Create some values... and observe this behaviour."). Don't front-load warnings before the reader has a foothold on the base concept.

**Reassure by naming the confusion, then narrowing scope.** When material is conceptually heavy, don't hedge around the difficulty. Name it directly, then immediately shrink what the reader actually needs to worry about right now. Pattern: "[Topic] can be confusing when starting out. But as a beginner you have in fact only to care about [narrow thing]." Or: "That might sound complicated, but..." If there's a deeper rabbit hole for the curious, offer it as an optional escape hatch, not a requirement: "If you want to deep dive into this topic right now, I highly recommend..."

**Favor these recurring connective tics** (use naturally, don't force all of them into one passage):
- "Also..." as a paragraph-opening connective
- "Note, that..." / "Notice that..." to direct attention
- "In fact..." to introduce a slightly deeper or more surprising truth
- "Basically..." as a plain-English simplifier
- "So far..." to summarize progress before pivoting
- "Let's..." for shared-action transitions
- "As mentioned/described [above / in the last chapter]" for tight callbacks to earlier material
- "so-called" to flag a piece of jargon right before defining it
- A colon or a short standalone sentence for a quick clarifying beat (not an em dash)

**Register: casual-professional, never stiff.** Technically precise but conversational. Contractions are fine and expected ("don't," "won't," "it's"). Avoid academic throat-clearing. There's a light German-tinged warmth to the phrasing (a certain earnestness and directness) but the English itself should stay clean and idiomatic. Don't manufacture broken English or literal German constructions.

**Endings invite, they don't interrogate.** Close sections warmly and often with an actual invitation or forward pointer ("And now let's jump right in! Have fun with the tutorial patches, and if something is not clear enough, let me know on GitHub!"), not with a rhetorical question aimed at the reader. Do not end a passage on a question. Avoid filler hedges like "honestly" or "to be fair"; Christoph doesn't use them and they read as an off-note.

## What this skill does not cover

Chapter sequencing, when to introduce a running/carrying example, how many sub-sections a topic needs, and overall pacing across a whole part are structural decisions, not voice decisions. Make those calls fresh for the task at hand (ask Christoph or reason it out). Don't let this skill's examples pull you toward copying VL.TheBigBang's existing chapter shapes wholesale.

## Quick self-check before finishing a passage

Read it back and ask: does this sound like someone talking to a patcher sitting next to them, admitting the confusing bits honestly, cracking one dry aside, and never talking down? If it reads like a manual or a lecture, tighten the direct address, add a "you can imagine it like..." framing, and cut anything that sounds like corporate hedging.
