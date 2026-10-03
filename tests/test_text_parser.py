"""
tests/test_text_parser.py — Comprehensive tests for text parsing, clean image prompt, scoring, and markdown export.
"""
import pytest
from services.text_parser import (
    extract_section, split_variations, split_numbered_tweets,
    char_count_status, word_count, score_linkedin_post,
    clean_image_prompt, build_content_markdown, build_content_json,
)


class TestExtractSection:
    def test_hash_heading(self):
        text = "### LINKEDIN\nContent here\n### TWITTER\nOther"
        assert extract_section(text, ["LINKEDIN"]) == "Content here"

    def test_double_hash(self):
        text = "## LINKEDIN\nContent\n## TWITTER\nOther"
        assert extract_section(text, ["LINKEDIN"]) == "Content"

    def test_case_insensitive(self):
        text = "### linkedin\nLowercase content\n### END\nDone"
        assert extract_section(text, ["LINKEDIN"]) == "Lowercase content"

    def test_multiple_markers_tries_all(self):
        text = "### LinkedIn Post\nThe content\n### TWITTER\nOther"
        result = extract_section(text, ["LINKEDIN", "LinkedIn Post"])
        assert "The content" in result

    def test_fallback_returns_full_text(self):
        text = "Just plain text, no headings here"
        assert extract_section(text, ["NONEXISTENT"]) == text.strip()

    def test_fallback_not_empty(self):
        assert extract_section("Some text", ["MISSING"]) != ""

    def test_version_a_extraction(self):
        text = "### CAPTION VERSION A\nCaption text here\n### CAPTION VERSION B\nOther"
        result = extract_section(text, ["CAPTION VERSION A", "VERSION A"])
        assert "Caption text here" in result

    def test_empty_input_returns_empty(self):
        assert extract_section("", ["ANYTHING"]) == ""


class TestSplitVariations:
    def test_splits_two(self):
        text = "Post A\n===VARIATION===\nPost B"
        result = split_variations(text)
        assert result == ["Post A", "Post B"]

    def test_splits_three(self):
        text = "A\n===VARIATION===\nB\n===VARIATION===\nC"
        assert len(split_variations(text)) == 3

    def test_empty_returns_empty_list(self):
        assert split_variations("") == []

    def test_whitespace_returns_empty_list(self):
        assert split_variations("   \n\n  ") == []

    def test_single_no_delimiter(self):
        result = split_variations("Just one post")
        assert result == ["Just one post"]

    def test_strips_whitespace(self):
        text = "  Post A  \n===VARIATION===\n  Post B  "
        result = split_variations(text)
        assert result[0] == "Post A"
        assert result[1] == "Post B"


class TestSplitNumberedTweets:
    def test_basic_split(self):
        text = "1/ First tweet\n2/ Second tweet\n3/ Third"
        result = split_numbered_tweets(text)
        assert len(result) == 3
        assert result[0] == "1/ First tweet"

    def test_empty_returns_empty(self):
        assert split_numbered_tweets("") == []

    def test_no_format_returns_list(self):
        result = split_numbered_tweets("plain text")
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_ignores_empty_segments(self):
        text = "1/ First\n\n\n2/ Second"
        result = split_numbered_tweets(text)
        assert all(t.strip() for t in result)


class TestCharCountStatus:
    def test_under_limit(self):
        r = char_count_status("hello", 280)
        assert r["count"] == 5
        assert r["is_over"] is False

    def test_over_limit(self):
        r = char_count_status("x" * 300, 280)
        assert r["count"] == 300
        assert r["is_over"] is True

    def test_exactly_at_limit(self):
        r = char_count_status("x" * 280, 280)
        assert r["is_over"] is False

    def test_empty_string(self):
        r = char_count_status("", 100)
        assert r["count"] == 0
        assert r["is_over"] is False


class TestWordCount:
    def test_basic(self):
        assert word_count("hello world") == 2

    def test_empty(self):
        assert word_count("") == 0

    def test_whitespace_only(self):
        assert word_count("   ") == 0

    def test_multiline(self):
        assert word_count("hello\nworld\nfoo") == 3


class TestScoreLinkedinPost:
    def _good_post(self):
        return (
            "I failed 3 startups before 30.\n\n"
            "Here is what changed everything for me.\n\n"
            "First, I stopped listening to generic advice.\n\n"
            "Second, I found one problem I cared deeply about.\n\n"
            "Third, I shipped something ugly in week one.\n\n"
            "The results shocked me.\n\n"
            "What mistake did you make that turned out to be your best teacher?\n\n"
            "#startup #founder #entrepreneur"
        )

    def test_returns_dict(self):
        result = score_linkedin_post(self._good_post())
        assert isinstance(result, dict)
        assert "overall" in result
        assert "grade" in result
        assert "feedback" in result

    def test_grade_is_letter(self):
        result = score_linkedin_post(self._good_post())
        assert result["grade"] in ("A", "B", "C", "D")

    def test_overall_is_0_to_100(self):
        result = score_linkedin_post(self._good_post())
        assert 0 <= result["overall"] <= 100

    def test_good_post_scores_well(self):
        result = score_linkedin_post(self._good_post())
        assert result["overall"] >= 60

    def test_bad_hook_penalized(self):
        bad = "I'm excited to share some thoughts on leadership.\n\nHere are my ideas."
        result = score_linkedin_post(bad)
        assert result["scores"]["hook"] < 60

    def test_no_hashtags_penalized(self):
        text = "A solid post without any hashtags at all.\n\nWhat do you think?"
        result = score_linkedin_post(text)
        assert result["scores"]["hashtags"] < 50

    def test_no_question_penalized(self):
        text = "A post with no question at the end. " * 20 + "\n\n#startup"
        result = score_linkedin_post(text)
        assert result["scores"]["cta"] < 60

    def test_banned_phrases_penalized(self):
        text = "This is a game-changer for the landscape. " * 15
        result = score_linkedin_post(text)
        assert result["scores"]["language"] < 60


class TestCleanImagePrompt:
    def test_strips_code_blocks(self):
        raw = "```text\nA beautiful futuristic workspace\n```"
        assert clean_image_prompt(raw) == "A beautiful futuristic workspace"

    def test_strips_common_prefixes(self):
        assert clean_image_prompt("Image prompt: A cyberpunk hacker room") == "A cyberpunk hacker room"
        assert clean_image_prompt("Graphic Prompt: Vibrant tech flat illustration") == "Vibrant tech flat illustration"
        assert clean_image_prompt("Prompt: High contrast product design") == "High contrast product design"

    def test_strips_wrapping_quotes(self):
        assert clean_image_prompt('"A cinematic shot of a mountain"') == "A cinematic shot of a mountain"
        assert clean_image_prompt("'A minimal vector logo'") == "A minimal vector logo"


class TestContentExports:
    def test_markdown_export(self):
        entries = [
            {"type": "LinkedIn Post", "platform": "LinkedIn", "content": "Sample post", "timestamp": "2026-10-04 12:00"},
            {"type": "Twitter Thread", "platform": "Twitter/X", "content": "1/ Tweet", "timestamp": "2026-10-04 12:05"},
        ]
        md = build_content_markdown(entries)
        assert "# Growth Engine AI" in md
        assert "LinkedIn Post" in md
        assert "Twitter Thread" in md

    def test_json_export(self):
        entries = [{"type": "Hooks", "platform": "LinkedIn", "content": "Hook 1"}]
        j = build_content_json(entries)
        assert "Hooks" in j
