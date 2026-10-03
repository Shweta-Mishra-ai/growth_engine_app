from config import INSTAGRAM

INSTAGRAM_HOOK_PATTERNS = """\
GREAT OPENING HOOKS (study why they work):
  • "Nobody tells you this about building an audience in 2026..."
  • "Stop making this one mistake on your product launch."
  • "Here's the harsh truth I had to learn the hard way:"
  • "Save this if you want to double your creative output:"
"""


def build_instagram_caption_prompt(topic: str, voice_instruction: str, content_type: str, vibe: str, cta_type: str, length: str) -> str:
    # Adjust emoji guidance and word count guidance based on vibe and length
    emoji_note = (
        "Keep emojis minimal (1-2 total) to preserve raw authenticity and vulnerability."
        if "raw" in vibe.lower() or "vulnerable" in vibe.lower()
        else "Use 4-6 vibrant, relevant emojis to maximize energy and entertainment."
        if "funny" in vibe.lower() or "entertaining" in vibe.lower()
        else "3-5 emojis used strategically to break up sections."
    )

    word_note = (
        "Short length (<100 words): Extremely concise, punchy, high-impact."
        if "short" in length.lower()
        else "Long length (200-300 words): In-depth mini-blog post, rich storytelling."
        if "long" in length.lower()
        else "Medium length (100-200 words): Balanced pacing with key lessons."
    )

    return f"""You are a top Instagram content strategist. You write captions that drive saves and shares — the primary signals that maximize algorithmic reach.

{INSTAGRAM_HOOK_PATTERNS}

═══ TASK ═══
Write a complete, high-converting Instagram caption about the topic below.

═══ TOPIC ═══
{topic}

═══ SETTINGS ═══
Content type: {content_type}
Vibe: {vibe}
CTA goal: {cta_type}
Length: {length} ({word_note})
Voice: {voice_instruction}
Emoji style: {emoji_note}

═══ ALGORITHM RULES ═══
• Saves + shares matter more than likes for feed distribution
• First 1-2 lines show before "...more" cutoff — MUST hook immediately
• Line breaks between thoughts — keep it scannable
• 15-20 hashtags is recommended: mix broad (1M+), niche (50K-500K), and targeted micro tags

═══ STRUCTURE ═══

LINE 1-2 (HOOK):
→ Must stop them from scrolling BEFORE they tap "more"
→ Never start with "I'm excited" or "Check this out"
→ Use proven openings like "Nobody tells you..." or a bold relatable contrast

BODY:
→ Deliver value/story based on the specified vibe: {vibe}
→ Short paragraphs with clean line breaks
→ {word_note}

CTA:
→ Natural call-to-action: {cta_type}

HASHTAGS:
→ Include 15-20 categorized hashtags at the very bottom

═══ OUTPUT FORMAT ═══
Provide exactly this format:

### CAPTION VERSION A
[full caption including hashtags]

### CAPTION VERSION B
[completely different hook and angle, same topic, with hashtags]

### STORY TEASER
[one short punchy line for an Instagram Story to drive traffic to this post]"""


def build_instagram_image_prompt_brief(topic: str, vibe: str) -> str:
    return f"""Create a detailed text-to-image prompt for an Instagram post visual.

Post topic: {topic}
Vibe: {vibe}

Write ONE specific image generation prompt covering: composition, lighting, color palette, mood, style (photorealistic / illustration / flat design / etc), and any key visual elements.

Output ONLY the image prompt — nothing else."""
