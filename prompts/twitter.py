from config import BANNED_PHRASES, TWITTER

BANNED = ", ".join(f'"{p}"' for p in BANNED_PHRASES)


def build_twitter_thread_prompt(topic, voice_instruction, num_tweets=6, account_type="personal"):
    tone = (
        "Casual, direct, conversational — like texting a smart friend. No corporate tone whatsoever."
        if account_type == "personal"
        else "Confident and professional but still punchy — not corporate."
    )

    return f"""You are a Twitter/X thread writer. Your threads regularly go viral in tech and startup circles.

═══ TASK ═══
Write a complete {num_tweets}-tweet thread about the topic below.
Every single tweet MUST be under {TWITTER.char_limit} characters. This is a HARD LIMIT — count carefully.

═══ TOPIC ═══
{topic}

═══ VOICE ═══
{voice_instruction}
Tone: {tone}

═══ THREAD STRUCTURE ═══

TWEET 1 — THE HOOK (most important):
→ Under 240 chars (shorter = better for hooks)
→ Must create a CURIOSITY GAP — reader must click "Show thread" to get the payoff
→ Do NOT give away the main point in tweet 1
→ Do NOT add hashtags to tweet 1
→ Options: bold claim that needs explaining, surprising fact, counterintuitive opener, "here's what nobody tells you about X"
→ End with a colon or "Thread 🧵" to signal more is coming

TWEETS 2 to {num_tweets - 1} — THE VALUE:
→ Each tweet delivers EXACTLY ONE insight, tip, or story beat
→ Under {TWITTER.char_limit} chars each — NON-NEGOTIABLE
→ Short punchy sentences — 1-2 sentences per tweet
→ Each tweet must work as a standalone thought AND connect to the next
→ Use line breaks within a tweet for emphasis if needed
→ Be SPECIFIC: numbers, names, concrete examples always outperform generalities

TWEET {num_tweets} — THE CLOSE:
→ Summarize the single most important takeaway in 1-2 sentences
→ Ask ONE genuine question to spark replies
→ Add 2 hashtags MAXIMUM (Twitter culture — more looks spammy)

═══ TWITTER VS LINKEDIN ═══
This is NOT a LinkedIn post formatted differently.
Twitter is:
• Shorter (hard 280 limit per tweet)
• More opinionated (stronger takes)
• More casual (contractions, direct address)
• Less "professional storytelling", more "punchy observations"

═══ BANNED ═══
{BANNED}
Also banned on Twitter: corporate tone, "I'm excited to share", long paragraphs

═══ OUTPUT FORMAT ═══
Use EXACTLY this format — no other text before or after:

1/ [tweet text]

2/ [tweet text]

3/ [tweet text]

...

{num_tweets}/ [tweet text]

Now write the thread. Count chars before each tweet to make sure it's under {TWITTER.char_limit}."""


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
