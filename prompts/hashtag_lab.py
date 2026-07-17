def build_hashtag_research_prompt(topic: str, platform: str, niche: str, count: int) -> str:
    nch = niche or "General"
    return f"""You are a social media SEO expert with deep knowledge of hashtag strategy across platforms.

Content topic: {topic}
Platform(s): {platform}
Niche: {nch}
Total hashtags needed: {count}

Generate a strategic hashtag set organized into 3 tiers:

### TIER 1 — HIGH REACH (5-7 hashtags)
Broad hashtags with 500K–5M+ uses. High competition but maximum visibility.
Format: #Hashtag — Brief note on why/when to use it

### TIER 2 — MEDIUM REACH (8-10 hashtags)  
Niche hashtags with 50K–500K uses. Best engagement-to-competition ratio.
Format: #Hashtag — Brief note

### TIER 3 — TARGETED / COMMUNITY (5-7 hashtags)
Highly specific hashtags with 5K–50K uses. Smaller reach but laser-targeted audience.
Format: #Hashtag — Brief note

### PLATFORM STRATEGY
A 3-4 sentence note on how to use these hashtags differently per platform:
- LinkedIn: [how many, where to place them]
- Twitter/X: [how many, placement strategy]
- Instagram: [how many, comment vs caption strategy]

### READY-TO-COPY SETS
Provide 3 ready-to-paste hashtag sets:
**Set A (LinkedIn — 5 tags):** [5 tags optimized for LinkedIn]
**Set B (Twitter — 3 tags):** [3 tags for X/Twitter]
**Set C (Instagram — 20 tags):** [20 tags for Instagram]

IMPORTANT: Only generate real, commonly used hashtags. Do not invent hashtags.
"""
