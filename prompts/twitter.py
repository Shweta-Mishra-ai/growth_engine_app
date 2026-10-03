from config import BANNED_PHRASES, TWITTER

BANNED = ", ".join(f'"{p}"' for p in BANNED_PHRASES)

TWITTER_HOOK_PATTERNS = """\
VIRAL HOOK PATTERNS (study the structure):
  • "I analyzed 500 successful startups. Here are 7 patterns that explain why they won:"
  • "The biggest mistake junior developers make isn't writing bad code. It's this:"
  • "How to build a $10k/month micro-SaaS with zero funding (full breakdown):"
  • "Most advice on [topic] is dead wrong. Here's what actually moves the needle:"
"""


def build_twitter_thread_prompt(topic: str, voice_instruction: str, num_tweets: int = 6, account_type: str = "personal") -> str:
    tone = (
        "Casual, direct, razor-sharp, and conversational — like texting a brilliant founder friend. Absolutely no corporate speak."
        if account_type == "personal"
        else "Confident, professional, punchy, and authoritative — concise and high-impact industry thought leader."
    )

    return f"""You are a master Twitter/X ghostwriter. Your threads are read by founders, VCs, and tech leaders, routinely going viral and generating thousands of bookmarks.

{TWITTER_HOOK_PATTERNS}

═══ TASK ═══
Write a complete, high-quality, and highly engaging {num_tweets}-tweet thread about the topic below.
Every single tweet MUST be under {TWITTER.char_limit} characters. This is a HARD limit — count carefully.

═══ TOPIC ═══
{topic}

═══ VOICE & TONE ═══
{voice_instruction}
Tone: {tone}

═══ THREAD STRUCTURE ═══

TWEET 1 — THE HOOK:
→ Must make someone stop mid-scroll. State a high-impact outcome, a contrarian perspective, a shocking stat, or a vulnerable failure.
→ Under 240 chars. Keep it short and punchy.
→ CURIOSITY GAP: Do NOT give away the main lesson in tweet 1. Create an irresistible curiosity gap.
→ NEVER start with introduction filler (e.g., "I wanted to share...", "Here is a thread on...").
→ End with "Thread 🧵" or "A short breakdown:" or a colon to lead into the next tweet.

TWEETS 2 to {num_tweets - 1} — THE BODY & VALUE:
→ Each tweet must deliver exactly ONE specific lesson, case study detail, or action step.
• Bullet points and short lines make it scannable
• Plain text emphasis for punchiness
• Connect each tweet organically to the next (keep reader scrolling)

TWEET {num_tweets} — THE CONCLUSION & CTA:
→ Summarize the core takeaway in 1 punchy sentence.
→ Add a specific, interesting question that invites replies.
→ Place exactly 1 or 2 highly relevant hashtags at the very end of this last tweet (NO hashtags on earlier tweets).

═══ BANNED PHRASES ═══
{BANNED}
Also banned: corporate jargon, emojis at the start of every sentence (use max 1-2 per tweet), generic greetings.

═══ OUTPUT FORMAT ═══
Provide exactly this format, with no preamble:

1/ [tweet text]

2/ [tweet text]

...

{num_tweets}/ [tweet text]

Now write the thread. Ensure every single tweet is under {TWITTER.char_limit} characters."""


def build_single_tweet_prompt(topic: str, voice_instruction: str, variations: int = 5) -> str:
    return f"""Write {variations} distinct standalone tweets about this topic.

TOPIC: {topic}
VOICE: {voice_instruction}

Each tweet:
• Under {TWITTER.char_limit} characters — count carefully
• Takes a DIFFERENT angle (vary: hot take, question, stat, joke, observation)
• Feels native to Twitter — punchy, direct, no corporate tone
• Stands alone (no "thread" references)

Format:
1. [tweet — char count: X]
2. [tweet — char count: X]
..."""
