def build_autopsy_prompt(post_text, performance_note, platform):
    perf = f"Performance context: {performance_note}" if performance_note and performance_note.strip() else ""
    return f"""You are a content performance analyst who reverse-engineers why posts succeed.

PLATFORM: {platform}
{perf}

POST TO ANALYZE:
\"\"\"{post_text}\"\"\"

Analyze and provide:

### HOOK ANALYSIS
What specifically makes the opening work? Name the exact psychological mechanism.

### STRUCTURE BREAKDOWN
Map the structural pattern — paragraph lengths, pacing, how it builds.

### ENGAGEMENT TRIGGERS
What specific elements drove comments vs just likes? Be specific.

### REPLICABLE PATTERN
Extract the underlying TEMPLATE stripped of its specific content — something reusable for any topic.

### WHAT TO AVOID COPYING
Note personal specifics that shouldn't be force-replicated."""


def build_apply_pattern_prompt(extracted_pattern, new_topic, voice_instruction):
    return f"""You are ghostwriting using a PROVEN content pattern that has already performed well.

PROVEN PATTERN:
{extracted_pattern}

VOICE: {voice_instruction}
NEW TOPIC: {new_topic}

Write a new post that follows the SAME structural pattern and engagement mechanics.
Apply the PATTERN — do not copy specific phrases or stories from the original.
Output only the post."""
