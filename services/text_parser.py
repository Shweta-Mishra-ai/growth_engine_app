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


def build_content_markdown(entries: list) -> str:
    md = []
    md.append("# Growth Engine AI — Content Export\n")
    md.append(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
    md.append("---\n")
    
    for i, e in enumerate(entries, 1):
        hdr = f"## {i}. {e.get('type','Content')}" + (f" ({e.get('platform','')})" if e.get('platform') else "")
        md.append(hdr)
        if e.get("timestamp"):
            md.append(f"*Timestamp: {e['timestamp']}*\n")
        md.append(e.get("content",""))
        md.append("\n---\n")
        
    return "\n".join(md)


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
        "prompt:"
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
