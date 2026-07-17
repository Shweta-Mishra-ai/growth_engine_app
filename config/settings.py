from dataclasses import dataclass

MODEL_NAME = "gemini-2.5-flash"
MODEL_FALLBACK = "gemini-2.0-flash-lite"
DEFAULT_TEMPERATURE = 0.8
DEFAULT_MAX_TOKENS = 2048

@dataclass(frozen=True)
class PlatformLimits:
    name: str
    char_limit: int
    ideal_char_count: int
    hashtag_count: tuple

LINKEDIN = PlatformLimits(name="LinkedIn", char_limit=3000, ideal_char_count=1500, hashtag_count=(3, 5))
TWITTER  = PlatformLimits(name="Twitter/X", char_limit=280, ideal_char_count=240, hashtag_count=(1, 2))
INSTAGRAM = PlatformLimits(name="Instagram", char_limit=2200, ideal_char_count=800, hashtag_count=(15, 20))

PLATFORMS = {"linkedin": LINKEDIN, "twitter": TWITTER, "instagram": INSTAGRAM}

BANNED_PHRASES = [
    "game-changer", "game changer", "dive deep", "delve", "landscape",
    "leverage", "paradigm shift", "synergy", "excited to announce",
    "thrilled to share", "in today's world", "unlock the power",
    "elevate your", "revolutionize", "seamless", "robust solution",
]

LINKEDIN_FORMATS = {
    "hook_story_lesson": "Hook → Short Story → Lesson → Ending Question + Hashtags",
    "contrarian_take":   "Bold Contrarian Claim → Evidence → Nuance → Question",
    "listicle":          "Hook → Numbered List (5-7 items) → Takeaway → Question",
    "data_driven":       "Surprising Stat → Context → Implication → Question",
    "case_study":        "Before State → What Changed → After State → Question",
}

MAX_HISTORY_ENTRIES = 50
