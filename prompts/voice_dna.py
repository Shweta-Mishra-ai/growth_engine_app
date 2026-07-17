def build_voice_extraction_prompt(samples):
    joined = "\n\n---SAMPLE---\n\n".join(samples)
    return f"""You are a linguistic analyst specializing in writing voice extraction.

Analyze these {len(samples)} writing sample(s) and extract a detailed "Voice DNA" profile.

SAMPLES:
{joined}

Extract ONLY this structure — no preamble:

### SENTENCE RHYTHM
[Short/punchy or long/flowing? Average sentence length? Patterns?]

### VOCABULARY LEVEL
[Simple/everyday or technical/sophisticated? Recurring words or phrases?]

### TONE
[Formal/casual/witty/direct/warm — be precise]

### STRUCTURAL HABITS
[Line breaks? Lists? Questions? Bold openings? How do paragraphs flow?]

### OPENING STYLE
[How do they typically start — question, claim, story, stat?]

### CLOSING STYLE
[How do they typically end — question, reflection, CTA, no formal close?]

### SIGNATURE QUIRKS
[Unique habits: emoji use, punctuation style, self-deprecation, specific phrases they repeat]

### DO NOT COPY
[Personal specifics that shouldn't be reproduced — extract the PATTERN not the content]"""


def build_voice_matched_prompt(voice_dna, new_topic, platform):
    return f"""You are ghostwriting for a specific person. You MUST match their exact writing voice — not generate generic content.

THEIR VOICE DNA:
{voice_dna}

PLATFORM: {platform}
NEW TOPIC: {new_topic}

RULES:
1. Match their EXACT sentence rhythm — if they write short punchy lines, do that
2. Match their vocabulary level — don't make it more or less sophisticated than their samples
3. Replicate their structural habits exactly
4. Open the way THEY typically open
5. Close the way THEY typically close
6. Do NOT copy specific stories or facts from the samples — only the STYLE
7. The result must feel like THEY wrote it about a new topic they haven't covered yet

Write the post now — output only the post, no preamble."""
