"""
tests/test_prompts.py — Validates prompt construction, platform differentiation, and hook frameworks.
"""
import pytest
from prompts.linkedin import build_linkedin_prompt, build_linkedin_carousel_prompt
from prompts.twitter import build_twitter_thread_prompt, build_single_tweet_prompt
from prompts.instagram import build_instagram_caption_prompt
from prompts.hooks import build_hook_rewrite_prompt
from prompts.voice_dna import build_voice_extraction_prompt, build_voice_matched_prompt
from prompts.post_autopsy import build_autopsy_prompt, build_apply_pattern_prompt
from prompts.graphics import build_graphic_prompt
from prompts.profile_auditor import build_profile_audit_prompt
from prompts.hashtag_lab import build_hashtag_research_prompt
from prompts.engagement import build_engagement_analysis_prompt
from prompts.video_storyboard import build_video_storyboard_prompt


class TestLinkedInPrompt:
    def _build(self, **kw):
        defaults = dict(
            topic="AI tools", voice_instruction="casual",
            audience="founders", format_style="hook_story_lesson",
        )
        return build_linkedin_prompt(**{**defaults, **kw})

    def test_generates_content(self):
        assert len(self._build()) > 500

    def test_has_hook_examples(self):
        p = self._build()
        assert "GOOD HOOKS" in p or "Proven" in p or "PROVEN" in p

    def test_has_minimum_word_count(self):
        assert "180" in self._build()

    def test_has_banned_phrases(self):
        assert "game-changer" in self._build()

    def test_single_no_variation_delimiter(self):
        assert "===VARIATION===" not in self._build(num_variations=1)

    def test_multi_has_variation_delimiter(self):
        assert "===VARIATION===" in self._build(num_variations=3)

    def test_all_formats_work(self):
        from config import LINKEDIN_FORMATS
        for fmt in LINKEDIN_FORMATS:
            p = self._build(format_style=fmt)
            assert len(p) > 400

    def test_has_emoji_guidance(self):
        assert "emoji" in self._build().lower() or "Emoji" in self._build()

    def test_cta_present_when_enabled(self):
        assert "question" in self._build(include_cta=True).lower()

    def test_carousel_prompt(self):
        p = build_linkedin_carousel_prompt("AI Strategy", "casual", 6)
        assert "carousel" in p.lower()
        assert "SLIDE 1" in p


class TestTwitterPrompt:
    def _build(self, **kw):
        defaults = dict(topic="AI tools", voice_instruction="casual", num_tweets=6)
        return build_twitter_thread_prompt(**{**defaults, **kw})

    def test_has_char_limit(self):
        assert "280" in self._build()

    def test_has_curiosity_gap(self):
        assert "CURIOSITY GAP" in self._build()

    def test_has_hook_examples(self):
        p = self._build()
        assert "VIRAL" in p or "HOOK" in p or "Thread" in p

    def test_output_format_specified(self):
        assert "1/ [tweet" in self._build() or "1/" in self._build()

    def test_personal_vs_pro_different(self):
        p = build_twitter_thread_prompt("topic", "voice", account_type="personal")
        pro = build_twitter_thread_prompt("topic", "voice", account_type="professional")
        assert p != pro

    def test_num_tweets_reflected(self):
        p = build_twitter_thread_prompt("topic", "voice", num_tweets=8)
        assert "8/" in p or "8-tweet" in p or "8 tweets" in p.lower()

    def test_single_tweet_prompt(self):
        p = build_single_tweet_prompt("Growth hacking", "casual", variations=5)
        assert "280" in p
        assert "5" in p


class TestInstagramPrompt:
    def _build(self, **kw):
        defaults = dict(
            topic="Startup life", voice_instruction="casual",
            content_type="Reel / short video",
            vibe="Educational / informational",
            cta_type="Save this post",
            length="Medium (100-200 words)",
        )
        return build_instagram_caption_prompt(**{**defaults, **kw})

    def test_has_version_a(self):
        assert "### CAPTION VERSION A" in self._build()

    def test_has_version_b(self):
        assert "### CAPTION VERSION B" in self._build()

    def test_has_story_teaser(self):
        assert "### STORY TEASER" in self._build()

    def test_has_hashtag_guidance(self):
        p = self._build()
        assert "15" in p or "hashtag" in p.lower()

    def test_vibe_affects_emoji_guidance(self):
        raw = self._build(vibe="Raw & authentic / vulnerable")
        fun = self._build(vibe="Funny & entertaining")
        assert raw != fun

    def test_length_affects_word_guidance(self):
        short = self._build(length="Short (<100 words)")
        long_ = self._build(length="Long (200-300 words)")
        assert short != long_

    def test_hook_examples_present(self):
        p = self._build()
        assert "GREAT OPENING" in p or "Nobody tells" in p


class TestPlatformDifferentiation:
    def test_linkedin_twitter_different(self):
        li = build_linkedin_prompt("AI", "casual", "founders", "hook_story_lesson")
        tw = build_twitter_thread_prompt("AI", "casual")
        assert li != tw

    def test_linkedin_instagram_different(self):
        li = build_linkedin_prompt("AI", "casual", "founders", "hook_story_lesson")
        ig = build_instagram_caption_prompt("AI", "casual", "Reel", "Educational / informational", "Save this post", "Medium (100-200 words)")
        assert li != ig

    def test_twitter_instagram_different(self):
        tw = build_twitter_thread_prompt("AI", "casual")
        ig = build_instagram_caption_prompt("AI", "casual", "Reel", "Educational / informational", "Save this post", "Medium (100-200 words)")
        assert tw != ig

    def test_linkedin_does_not_mention_280(self):
        li = build_linkedin_prompt("AI", "casual", "founders", "hook_story_lesson")
        assert "280" not in li

    def test_twitter_mentions_280(self):
        tw = build_twitter_thread_prompt("AI", "casual")
        assert "280" in tw

    def test_instagram_mentions_hashtag_volume(self):
        ig = build_instagram_caption_prompt("AI", "casual", "Reel", "Educational / informational", "Save this post", "Medium (100-200 words)")
        assert "15" in ig or "20" in ig


class TestHookPrompt:
    def test_generates_content(self):
        p = build_hook_rewrite_prompt("boring line", "context", "LinkedIn", 7)
        assert len(p) > 200

    def test_includes_original_line(self):
        p = build_hook_rewrite_prompt("my boring opener", "ctx", "LinkedIn", 5)
        assert "my boring opener" in p

    def test_framework_count_in_prompt(self):
        p = build_hook_rewrite_prompt("line", "ctx", "Twitter/X", 5)
        assert "5" in p


class TestVoiceDNA:
    def test_extraction_includes_all_samples(self):
        samples = ["Sample one text here.", "Sample two text here.", "Sample three."]
        p = build_voice_extraction_prompt(samples)
        for s in samples:
            assert s in p

    def test_extraction_has_required_sections(self):
        p = build_voice_extraction_prompt(["Sample text"])
        assert "SENTENCE RHYTHM" in p
        assert "TONE" in p
        assert "CLOSING STYLE" in p

    def test_matched_prompt_has_dna_and_topic(self):
        p = build_voice_matched_prompt("DNA profile text", "new topic", "LinkedIn")
        assert "DNA profile text" in p
        assert "new topic" in p
        assert "LinkedIn" in p

    def test_matched_warns_against_copying(self):
        p = build_voice_matched_prompt("dna", "topic", "Twitter/X")
        assert "do not copy" in p.lower() or "not copy" in p.lower()


class TestPostAutopsy:
    def test_generates_analysis(self):
        p = build_autopsy_prompt("viral post text here", "300 comments", "LinkedIn")
        assert "HOOK ANALYSIS" in p
        assert "REPLICABLE PATTERN" in p

    def test_includes_performance_context(self):
        p = build_autopsy_prompt("post", "300 comments", "LinkedIn")
        assert "300 comments" in p

    def test_apply_pattern_uses_pattern(self):
        p = build_apply_pattern_prompt("extracted pattern", "new topic", "casual voice")
        assert "extracted pattern" in p
        assert "new topic" in p


class TestAdditionalPrompts:
    def test_profile_auditor_prompt(self):
        p = build_profile_audit_prompt("Software Dev @ ABC", "Recruiters", "LinkedIn", "Get hired", "casual")
        assert "Software Dev @ ABC" in p
        assert "SCORE" in p

    def test_hashtag_research_prompt(self):
        p = build_hashtag_research_prompt("SaaS growth", "LinkedIn", "B2B Tech", 20)
        assert "SaaS growth" in p
        assert "20" in p

    def test_engagement_analysis_prompt(self):
        p = build_engagement_analysis_prompt("Post content here", "LinkedIn")
        assert "Post content here" in p

    def test_video_storyboard_prompt(self):
        p = build_video_storyboard_prompt("Script idea", "casual", 30)
        assert "30" in p
        assert "Scene" in p or "SCENE" in p or "second" in p.lower()

    def test_graphic_prompt(self):
        p = build_graphic_prompt("A post about developer flow", "LinkedIn", "Modern Illustration")
        assert "Modern Illustration" in p
        assert "NO text" in p or "no text" in p.lower()
