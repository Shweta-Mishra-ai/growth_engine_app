import re


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
