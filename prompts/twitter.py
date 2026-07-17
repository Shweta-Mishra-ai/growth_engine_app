from config import BANNED_PHRASES, TWITTER

BANNED = ", ".join(f'"{p}"' for p in BANNED_PHRASES)


def build_twitter_thread_prompt(topic, voice_instruction, num_tweets=6, account_type="personal"):
    tone = (
        "Casual, direct, razor-sharp, and conversational — like texting an industry leader. Absolutely no corporate fluff."
        if account_type == "personal"
        else "Confident, professional, punchy, and authoritative — concise and high-impact."
    )

    return f"""You are a master Twitter/X ghostwriter. Your threads are read by founders, VCs, and tech leaders, routinely going viral and generating thousands of bookmarks.

═══ TASK ═══
Write a complete, high-quality, and highly engaging {num_tweets}-tweet thread about the topic below.
Every single tweet MUST be under {TWITTER.char_limit} characters. This is a HARD limit — count carefully.

═══ TOPIC ═══
{topic}

═══ VOICE ═══
{voice_instruction}
Tone: {tone}

═══ THREAD STRUCTURE ═══

TWEET 1 — THE HOOK:
→ Must make someone stop mid-scroll. State a high-impact outcome, a contrarian perspective, a shocking stat, or a vulnerable failure.
→ Under 240 chars. Keep it short and punchy.
→ Do NOT give away the main lesson in tweet 1. Create a curiosity gap.
→ NEVER start with introduction filler (e.g., "I wanted to share...", "Here is a thread on...").
→ End with "Thread 🧵" or "A short story:" or a colon to lead into the next tweet.

TWEETS 2 to {num_tweets - 1} — THE BODY & VALUE:
→ Each tweet must deliver exactly ONE specific lesson, case study detail, or action step.
→ Use bullet points and lists to make it highly scannable.
→ Bold key phrases (using plain text capitalization or simple formatting syntax) for emphasis.
→ Use short line breaks. Do not write large blocks of text.
→ Connect each tweet organically to the next (keep the reader scrolling).

TWEET {num_tweets} — THE CONCLUSION & CTA:
→ Summarize the core takeaway in 1 punchy sentence.
→ Add a specific, interesting question that invites discussion/replies (avoid generic "What do you think?").
→ Place exactly 1 or 2 highly relevant hashtags at the very end of this last tweet (NO hashtags on earlier tweets).

═══ BANNED PHRASES ═══
{BANNED}
Also banned: corporate jargon, emojis at the start of every sentence (use max 1-2 per tweet), generic greetings.

═══ OUTPUT FORMAT ═══
Provide exactly this format, with no preamble:

1/ [tweet text]

2/ [tweet text]

3/ [tweet text]

...

{num_tweets}/ [tweet text]

Now write the thread. Ensure every single tweet is under {TWITTER.char_limit} characters."""


def build_single_tweet_prompt(topic, voice_instruction, variations=5):
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
