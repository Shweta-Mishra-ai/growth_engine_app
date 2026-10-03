import json
import re
from datetime import datetime


def extract_section(text: str, markers: list) -> str:
    for marker in markers:
        pattern = rf"(?:#+\s*{re.escape(marker)}\s*\n)(.*?)(?=\n#+\s*[A-Z]|\Z)"
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m and m.group(1).strip():
            return m.group(1).strip()
        pattern2 = rf"\*?\*?{re.escape(marker)}\*?\*?\s*:?\s*\n(.*?)(?=\n\*?\*?[A-Z]{{3,}}|\Z)"
        m2 = re.search(pattern2, text, re.IGNORECASE | re.DOTALL)
        if m2 and m2.group(1).strip():
            return m2.group(1).strip()
    return text.strip()


def split_variations(text: str, delimiter: str = "===VARIATION===") -> list:
    if not text or not text.strip():
        return []
    parts = [p.strip() for p in text.split(delimiter) if p.strip()]
    return parts if parts else [text.strip()]


def split_numbered_tweets(text: str) -> list:
    tweets = re.split(r'\n(?=\d+/)', text)
    return [t.strip() for t in tweets if t.strip()]


def char_count_status(text: str, limit: int) -> dict:
    count = len(text)
    return {"count": count, "limit": limit, "is_over": count > limit}


def word_count(text: str) -> int:
    return len(text.split()) if text and text.strip() else 0


def score_linkedin_post(text: str) -> dict:
    """
    Score a LinkedIn post on key algorithmic quality dimensions.
    Returns scores 0-100 and actionable feedback items.
    """
    scores = {}
    feedback = []

    # 1. Length score
    words = word_count(text)
    if words >= 200:
        scores["length"] = 100
    elif words >= 150:
        scores["length"] = 75
        feedback.append(f"Post is {words} words — aim for 200+ for higher dwell time and reach")
    elif words >= 100:
        scores["length"] = 50
        feedback.append(f"Post is only {words} words — too brief for maximum LinkedIn value")
    else:
        scores["length"] = 20
        feedback.append(f"Post is only {words} words — significantly too short")

    # 2. Hook quality (first line)
    first_line = text.split("\n")[0].strip() if text else ""
    hook_score = 50
    if len(first_line) <= 80:
        hook_score += 20  # punchy and visible before "see more" cutoff
    if any(c.isdigit() for c in first_line):
        hook_score += 15  # has credible number or stat
    bad_starts = ["i'm excited", "great news", "i wanted to", "today i", "i am happy", "thrilled"]
    if any(first_line.lower().startswith(s) for s in bad_starts):
        hook_score -= 30
        feedback.append("Hook starts with a generic opening cliché — rewrite first sentence")
    if first_line.endswith("?"):
        hook_score += 10
    scores["hook"] = min(100, max(0, hook_score))

    # 3. Spacing & Mobile Readability
    lines = text.split("\n")
    blank_lines = sum(1 for l in lines if l.strip() == "")
    if blank_lines >= 4:
        scores["readability"] = 100
    elif blank_lines >= 2:
        scores["readability"] = 70
        feedback.append("Add blank lines between short paragraphs for mobile formatting")
    else:
        scores["readability"] = 30
        feedback.append("Wall of text detected — separate paragraphs with empty lines")

    # 4. Comment Question / CTA
    has_question = "?" in text[-300:]
    scores["cta"] = 90 if has_question else 40
    if not has_question:
        feedback.append("No closing question found — ending questions boost comment replies")

    # 5. Hashtag Strategy
    hashtag_count = text.count("#")
    if 3 <= hashtag_count <= 5:
        scores["hashtags"] = 100
    elif hashtag_count > 0:
        scores["hashtags"] = 60
        feedback.append(f"Found {hashtag_count} hashtags — 3 to 5 targeted tags is optimal")
    else:
        scores["hashtags"] = 20
        feedback.append("No hashtags found — add 3-5 relevant tags at the end")

    # 6. Corporate Cliches & AI Buzzwords
    banned = [
        "game-changer", "dive deep", "delve", "synergy", "paradigm shift",
        "excited to announce", "thrilled to share", "in today's world", "leverage"
    ]
    found_banned = [p for p in banned if p.lower() in text.lower()]
    if found_banned:
        scores["language"] = 40
        feedback.append(f"Remove corporate clichés: {', '.join(found_banned)}")
    else:
        scores["language"] = 100

    overall = int(sum(scores.values()) / len(scores))
    grade = "A" if overall >= 85 else "B" if overall >= 70 else "C" if overall >= 55 else "D"

    return {
        "overall": overall,
        "scores": scores,
        "feedback": feedback,
        "grade": grade,
    }


def clean_image_prompt(prompt_text: str) -> str:
    text = prompt_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    cleaned = text
    while cleaned and cleaned[0] in "*# \t\n":
        cleaned = cleaned[1:]

    prefixes = [
        "image generation prompt:",
        "image prompt:",
        "graphic prompt:",
        "visual prompt:",
        "here is the prompt:",
        "here is the image generation prompt:",
        "prompt:",
    ]

    lower_cleaned = cleaned.lower()
    for prefix in prefixes:
        if lower_cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            lower_cleaned = cleaned.lower()

    while cleaned and cleaned[0] in " \t:-*#\n":
        cleaned = cleaned[1:]

    if cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1].strip()
    if cleaned.startswith("'") and cleaned.endswith("'"):
        cleaned = cleaned[1:-1].strip()

    return cleaned.strip()


def build_content_markdown(entries: list) -> str:
    md = [
        "# Growth Engine AI — Content Export\n",
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n",
        "---\n",
    ]

    for i, e in enumerate(entries, 1):
        hdr = f"## {i}. {e.get('type', 'Content')}" + (f" ({e.get('platform', '')})" if e.get('platform') else "")
        md.append(hdr)
        if e.get("timestamp"):
            md.append(f"*Timestamp: {e['timestamp']}*\n")
        md.append(e.get("content", ""))
        md.append("\n---\n")

    return "\n".join(md)


def build_content_json(entries: list) -> str:
    return json.dumps(entries, indent=4, ensure_ascii=False)
