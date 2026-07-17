def build_engagement_analysis_prompt(content: str, platform: str) -> str:
    return f"""You are a senior social media analytics expert and virality strategist.
Analyze the following post content generated for {platform} and predict its engagement potential.

POST CONTENT:
{content}

Provide an analysis with this EXACT structure:

### ENGAGEMENT RATING
Provide a score out of 100% (e.g. 85%) and 1 sentence explaining this overall prediction.

### CORE METRICS (0-100)
- Hook Strength: [Score] (Why: brief 1 sentence reason)
- Readability & Structure: [Score] (Why)
- Value Delivery: [Score] (Why)
- Call-To-Action (CTA) Strength: [Score] (Why)

### SUGGESTED IMPROVEMENTS
Give 2-3 specific, actionable tweaks to make this post perform even better (e.g. rewrite a line, format change).

### ESTIMATED METRICS
- Estimated Read Time: [X seconds]
- Ideal Post Time: [Best hours/days for this topic/platform]
"""
