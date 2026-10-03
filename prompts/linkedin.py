from config import BANNED_PHRASES, LINKEDIN_FORMATS

BANNED = ", ".join(f'"{p}"' for p in BANNED_PHRASES)

HOOK_EXAMPLES = """\
PROVEN / GOOD HOOKS (study the PATTERN, not the words):
  ✅ "I got fired 3 times before 30. Best thing that ever happened."
  ✅ "We hit $50k MRR in 6 months. Zero ads. Here's the exact playbook:"
  ✅ "I spent $47,000 on a mistake most founders make in month 2."
  ✅ "99% of productivity advice is wrong. Here's what actually works."
  ✅ "Nobody talks about the 6 months before success. I will."
  ✅ "I almost quit on a Tuesday. This is what changed my mind."

WHAT MAKES THEM WORK:
  → Specific numbers create instant credibility ($47k, 6 months, 99%)
  → Tension or contradiction makes people need to know more
  → Personal vulnerability earns trust before asking for attention
  → Promise of insight the reader hasn't seen before

HOOKS TO NEVER WRITE:
  ❌ "I'm excited to share some thoughts on leadership today."
  ❌ "In today's rapidly evolving business landscape..."
  ❌ "I wanted to take a moment to discuss something important."
  ❌ "As a professional with X years of experience..."
  ❌ "Great news! We've just launched..."
"""


def build_linkedin_prompt(
    topic: str,
    voice_instruction: str,
    audience: str,
    format_style: str,
    num_variations: int = 1,
    include_cta: bool = True,
) -> str:
    fmt = LINKEDIN_FORMATS.get(format_style, LINKEDIN_FORMATS["hook_story_lesson"])
    aud = f"Target audience: {audience}" if audience and audience.strip() else "Target audience: professionals, founders, and builders on LinkedIn"
    cta = (
        "End with a specific, genuine question that makes readers want to share their own experience. "
        "NOT 'What do you think?' — something like 'What's the lesson you wish someone had told you earlier?' "
        "or 'Which of these would you add?'"
    ) if include_cta else "No CTA needed."

    variation_block = ""
    if num_variations > 1:
        variation_block = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENERATE {num_variations} COMPLETELY DIFFERENT VARIATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Each variation MUST:
• Use a DIFFERENT hook style (story hook ≠ stat hook ≠ contrarian hook)
• Take a DIFFERENT angle on the topic
• Feel like it was written by the same person on a different day
• NOT be a reword of another variation — genuinely distinct content

Separate variations with EXACTLY this line (nothing else on that line):
===VARIATION===
"""

    return f"""You are a world-class LinkedIn ghostwriter. Your posts regularly generate 500+ comments and go viral in professional feeds.

{HOOK_EXAMPLES}

═══ TASK ═══
Write a HIGH-QUALITY, COMPLETE LinkedIn post about the topic below.
The post must be LONG ENOUGH to deliver real value — minimum 180 words, ideally 200-300 words.
A short post that doesn't deliver value is WORSE than no post.

═══ TOPIC ═══
{topic}

═══ FORMAT TO FOLLOW ═══
{fmt}

═══ VOICE & TONE ═══
{voice_instruction}

═══ AUDIENCE ═══
{aud}

═══ CTA ═══
{cta}

═══ ALGORITHMIC RULES FOR HIGH REACH ═══
• Line 1-2 MUST be a scroll-stopping hook (see Proven / Good Hooks above)
• Blank line between EVERY 1-2 sentences for mobile readability
• Cut ALL corporate fluff and jargon (game-changer, synergy, etc.)
• Specific numbers always beat generalities ($47k, 6 months, 99%)
• Emojis: 0-2 MAXIMUM, only if they genuinely add meaning (not decoration)
• End with a genuine question to trigger comment velocity
• Include 3-5 relevant hashtags on the final line only

═══ BANNED PHRASES (NEVER USE) ═══
{BANNED}

{variation_block}

Write the post(s) now. Output ONLY the post content — zero preamble, zero explanation, zero meta-commentary."""


def build_linkedin_carousel_prompt(topic: str, voice_instruction: str, num_slides: int = 6) -> str:
    return f"""You are a LinkedIn carousel strategist. Document posts get 39% more reach than standard posts.

TOPIC: {topic}
VOICE: {voice_instruction}
SLIDES: {num_slides}

Write content for a {num_slides}-slide LinkedIn carousel:
• Slide 1 — TITLE: The most compelling, curiosity-driving headline possible
• Slides 2 to {num_slides - 1} — ONE clear point per slide, max 2 sentences, scannable in 3 seconds
• Final slide — SUMMARY + question that drives comments

Format:
SLIDE 1: [headline]
SLIDE 2: [headline] / [1-2 sentence content]
...
SLIDE {num_slides}: [summary] / [question]"""
