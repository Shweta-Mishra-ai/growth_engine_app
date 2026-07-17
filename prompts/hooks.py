from config import PLATFORMS

HOOK_FRAMEWORKS = [
    ("Curiosity Gap",    "Make them NEED to know what comes next — tease without revealing"),
    ("Bold Claim",       "An audacious statement they'll strongly agree or argue with"),
    ("Empathy Hook",     "Speak directly to a pain or desire they feel but rarely admit"),
    ("Number Hook",      "Lead with a specific surprising stat or concrete number"),
    ("Story Opener",     "Drop them in the middle of the action — present tense, vivid detail"),
    ("Counterintuitive", "Say the opposite of what everyone expects — then justify it"),
    ("Direct Question",  "The question they've been afraid to ask or haven't articulated yet"),
    ("Social Proof",     "What X people/companies discovered about Y — borrow authority"),
    ("Confession",       "Vulnerable admission that earns immediate trust and relatability"),
    ("Provocation",      "A hot take that splits the room — some will love it, some will argue"),
]


def build_hook_rewrite_prompt(original_line, context, platform, num_hooks=7):
    platform_key = platform.lower().replace("/x", "").replace("twitter", "twitter").replace("x", "twitter")
    platform_info = PLATFORMS.get(platform_key)
    char_note = f"under {platform_info.ideal_char_count} characters" if platform_info else "concise and punchy"
    ctx = f"Post context: {context}" if context and context.strip() else ""
    frameworks = "\n".join(f"{i+1}. **{n}** — {d}" for i, (n, d) in enumerate(HOOK_FRAMEWORKS[:num_hooks]))

    return f"""You are the world's best copywriter for social media hooks.

ORIGINAL (weak) opening: "{original_line}"
{ctx}
Platform: {platform}

Rewrite into {num_hooks} genuinely different hook variations using these frameworks:

{frameworks}

For EACH hook:
• Name the framework used
• Write the hook ({char_note})
• One sentence explaining the psychological mechanism

FORMAT (follow exactly):
**[Number]. [FRAMEWORK NAME]**
Hook: [the hook text]
Why it works: [psychology note]

RULES:
• Never start with an em-dash, "In today's world", or "I'm"
• Each hook must feel GENUINELY different — not just reworded
• Be specific — vague hooks don't stop scrolls

Write all {num_hooks} hooks now."""
