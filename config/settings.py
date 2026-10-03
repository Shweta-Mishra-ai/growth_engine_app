from dataclasses import dataclass

MODEL_NAME = "gemini-2.5-flash"
MODEL_FALLBACK = "gemini-2.0-flash-lite"
DEFAULT_TEMPERATURE = 0.82
DEFAULT_MAX_TOKENS = 2500


@dataclass(frozen=True)
class PlatformLimits:
    name: str
    char_limit: int
    ideal_char_count: int
    ideal_words: tuple  # (min, max) word count
    hashtag_count: tuple  # (min, max)


LINKEDIN = PlatformLimits(name="LinkedIn", char_limit=3000, ideal_char_count=1500, ideal_words=(180, 300), hashtag_count=(3, 5))
TWITTER = PlatformLimits(name="Twitter/X", char_limit=280, ideal_char_count=240, ideal_words=(15, 50), hashtag_count=(1, 2))
INSTAGRAM = PlatformLimits(name="Instagram", char_limit=2200, ideal_char_count=800, ideal_words=(80, 250), hashtag_count=(15, 20))

PLATFORMS = {"linkedin": LINKEDIN, "twitter": TWITTER, "instagram": INSTAGRAM}

BANNED_PHRASES = [
    "game-changer", "game changer", "dive deep", "delve", "landscape",
    "leverage", "paradigm shift", "synergy", "excited to announce",
    "thrilled to share", "in today's world", "unlock the power",
    "elevate your", "revolutionize", "seamless", "robust solution",
    "cutting-edge", "state-of-the-art", "best-in-class", "holistic",
]

LINKEDIN_FORMATS = {
    "hook_story_lesson": "Hook → Personal Story → Lesson Learned → Question + Hashtags",
    "contrarian_take":   "Bold Contrarian Claim → Evidence → Nuance → Question",
    "listicle":          "Hook → Numbered List (5-7 items) → Takeaway → Question",
    "data_driven":       "Surprising Stat → Context → Why It Matters → Question",
    "case_study":        "Before State → The Turning Point → After State → Question",
    "carousel":          "Carousel (multi-slide) Slide Deck — Slide-by-slide structure",
}

IMAGE_STYLES = {
    "professional": "Corporate photography, clean polished background, business professional, natural lighting",
    "creative":     "Creative digital art, vibrant colors, modern illustration, artistic composition",
    "minimal":      "Minimalist design, abundant white space, clean lines, simple elegant composition",
    "cinematic":    "Cinematic photography, dramatic moody lighting, film-grade color grading, atmospheric",
    "editorial":    "Editorial magazine style, high fashion photography, sophisticated composition",
    "3d_render":    "Professional 3D clay render, smooth lighting, modern tech aesthetic",
}

PLATFORM_IMAGE_SIZES = {
    "LinkedIn":        {"width": 1200, "height": 628,  "desc": "Landscape banner"},
    "Instagram":       {"width": 1024, "height": 1024, "desc": "Square post"},
    "Instagram Story": {"width": 768,  "height": 1344, "desc": "Vertical story"},
    "Twitter/X":       {"width": 1200, "height": 675,  "desc": "16:9 card"},
}

MAX_HISTORY_ENTRIES = 100
APP_VERSION = "3.1.0"
