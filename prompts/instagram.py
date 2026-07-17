from config import INSTAGRAM


def build_instagram_caption_prompt(topic, voice_instruction, content_type, vibe, cta_type, length):
    return f"""You are a top Instagram content strategist. You write captions that drive saves and shares — the signals that boost reach the most.

═══ TASK ═══
Write a complete, high-quality Instagram caption about the topic below.

═══ TOPIC ═══
{topic}

═══ SETTINGS ═══
Content type: {content_type}
Vibe: {vibe}
CTA goal: {cta_type}
Length: {length}
Voice: {voice_instruction}

═══ INSTAGRAM CONTEXT ═══
• Saves + shares matter more than likes for algorithm reach
• First 1-2 lines show before "...more" cutoff — MUST hook immediately
• Line breaks between thoughts — Instagram renders them (unlike most platforms)
• 15-20 hashtags is NORMAL here (unlike Twitter where 1-2 is the limit)
• 5-6 emojis max — use them strategically, not scattered everywhere

═══ STRUCTURE ═══

LINE 1-2 (HOOK — before "more" cutoff):
→ Must stop them from scrolling BEFORE they tap "more"
→ Never start with "I'm excited", "Check this out", or "So excited to share"
→ Options: surprising fact, bold statement, relatable frustration, question they've been asking

BODY:
→ Deliver the value/story/emotion based on the vibe
→ Short paragraphs with line breaks — NOT a wall of text
→ Be specific and real — vague inspiration doesn't save well

CTA:
→ End with: {cta_type}
→ Make it feel natural and earned, not tacked on

HASHTAGS (after a blank line):
→ 15-20 hashtags mixing: 3-4 broad (1M+ posts), 8-10 niche (50K-500K posts), 3-4 micro (under 50K)

═══ OUTPUT FORMAT ═══
Provide exactly:

### CAPTION VERSION A
[full caption including hashtags]

### CAPTION VERSION B
[completely different hook and angle, same topic, with hashtags]

### STORY TEASER
[one short punchy line for an Instagram Story to drive traffic to this post]"""


def build_instagram_image_prompt_brief(topic, vibe):
    return f"""Create a detailed text-to-image prompt for an Instagram post visual.

Post topic: {topic}
Vibe: {vibe}

Write ONE specific image generation prompt covering: composition, lighting, color palette, mood, style (photorealistic / illustration / flat design / etc), and any key visual elements.

Output ONLY the image prompt — nothing else."""
