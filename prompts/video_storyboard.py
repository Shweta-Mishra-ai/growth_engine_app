def build_video_storyboard_prompt(topic: str, voice_instruction: str, duration_seconds: int = 30) -> str:
    return f"""You are a professional short-form video creator, scriptwriter, and video editor for Instagram Reels, TikTok, and YouTube Shorts.
Create a high-impact, engaging storyboard and video script based on the topic below.

TOPIC: {topic}
VOICE/TONE: {voice_instruction}
DURATION: {duration_seconds} seconds

Provide a complete storyboard formatted exactly as follows:

### VIDEO CONCEPT
Describe the visual hook, overall aesthetic, and key music/audio vibe.

### STORYBOARD SEQUENCE
Create a table or bulleted list showing a second-by-second breakdown of the video:
- [0-3s] Hook: Visual scene description | Voiceover script | On-screen text (caption overlay) | Camera movement/cut
- [3-10s] Problem/Story: Visual scene description | Voiceover script | On-screen text | Camera movement
- [10-25s] Solution/Tips: Visual scene description | Voiceover script | On-screen text | Camera movement
- [25-30s] Call to Action: Visual scene description | Voiceover script | On-screen text | Camera movement

### EDITOR INSTRUCTIONS
- Visual pacing: (e.g. fast cuts, zoom-ins, transitions)
- Sound design: (e.g. sound effects to use, voice modulation)
- B-Roll ideas: (what to film)
"""
