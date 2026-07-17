from config import BANNED_PHRASES, LINKEDIN_FORMATS

BANNED = ", ".join(f'"{p}"' for p in BANNED_PHRASES)


def build_linkedin_prompt(topic, voice_instruction, audience, format_style, num_variations=1, include_cta=True):
    fmt = LINKEDIN_FORMATS.get(format_style, LINKEDIN_FORMATS["hook_story_lesson"])
    cta = "End with a genuine question that invites comments — make it feel natural, not forced." if include_cta else "No CTA needed."
    aud = f"Target audience: {audience}" if audience and audience.strip() else "Target audience: professionals and builders on LinkedIn"

    variation_block = ""
    if num_variations > 1:
        variation_block = f"""
---
Generate {num_variations} COMPLETELY DIFFERENT variations of this post.
Each variation MUST:
- Use a DIFFERENT opening hook (different psychological approach each time)
- Take a DIFFERENT angle on the same topic
- Have a DIFFERENT structure or format
- NOT be a minor reword of another variation — genuinely distinct

Separate each variation with this exact line (nothing else on that line):
===VARIATION===
---"""

    return f"""You are a world-class LinkedIn ghostwriter. You write for founders, executives, and builders whose posts regularly get 500+ comments and go viral.

═══ TASK ═══
Write a HIGH-QUALITY, COMPLETE LinkedIn post about the topic below.
The post must be LONG ENOUGH to deliver real value — minimum 150 words, ideally 200-300 words.
A short post that doesn't deliver value is WORSE than no post.

═══ TOPIC ═══
{topic}

═══ FORMAT TO FOLLOW ═══
{fmt}

═══ VOICE ═══
{voice_instruction}

═══ AUDIENCE ═══
{aud}

═══ CTA ═══
{cta}

═══ LINKEDIN ALGORITHM — APPLY THIS ═══
• First 2 lines are EVERYTHING — they show before "see more" cutoff on mobile
• Line breaks between every 1-2 sentences — this is how LinkedIn renders on mobile
• Specific numbers and concrete details ALWAYS outperform vague generalities
• Personal story/vulnerability earns 3x more comments than generic advice
• A strong question at the end = comments = algorithm boost

═══ STRUCTURE (follow this exactly) ═══

LINE 1-2: SCROLL-STOPPING HOOK
→ Must make someone stop mid-scroll
→ Options: bold claim, surprising stat, vulnerable admission, tension/conflict, counterintuitive statement
→ NEVER start with: "I'm excited", "Great news", "I'm happy to share", "Today I want to"

[blank line]

BODY (5-8 short paragraphs):
→ Each paragraph: 1-3 sentences MAX
→ Blank line between EVERY paragraph
→ Tell the story / share the insight / break down the list
→ Be SPECIFIC: name real numbers, real situations, real outcomes
→ Build to a clear takeaway or lesson

[blank line]

CLOSING LINE:
→ Summarize the core lesson in 1 punchy sentence

[blank line]

QUESTION FOR COMMENTS:
→ One genuine question that makes readers want to share their experience
→ NOT "What do you think?" — something specific and interesting

[blank line]

HASHTAGS:
→ 3-5 relevant hashtags on the LAST line only

═══ BANNED PHRASES (never use these) ═══
{BANNED}

═══ QUALITY CHECK ═══
Before writing, ask yourself:
• Is the hook genuinely scroll-stopping?
• Does the body deliver REAL value or just filler?
• Is it specific enough (names, numbers, concrete details)?
• Would I personally share this post?

{variation_block}

Now write the post(s). Output ONLY the post content — zero preamble, zero meta-commentary."""


def build_linkedin_carousel_prompt(topic, voice_instruction, num_slides=6):
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
