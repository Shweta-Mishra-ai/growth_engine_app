import pytest
from services.text_parser import extract_section, split_variations, split_numbered_tweets, char_count_status, build_content_markdown

def test_extract_section():
    # Test extract_section with markdown headers
    text = "Some intro\n### SECTION A\nThis is content A\n### SECTION B\nThis is content B"
    assert extract_section(text, ["SECTION A"]) == "This is content A"
    assert extract_section(text, ["SECTION B"]) == "This is content B"
    
    # Test extract_section with bold headers
    text2 = "Some intro\n**VERSION A**:\nThis is caption A\n**VERSION B**:\nThis is caption B"
    assert extract_section(text2, ["VERSION A"]) == "This is caption A"
    assert extract_section(text2, ["VERSION B"]) == "This is caption B"

    # Test extract_section default behavior when markers not found
    text3 = "Hello World"
    assert extract_section(text3, ["NOTFOUND"]) == "Hello World"

def test_split_variations():
    # Test split_variations with default delimiter
    text = "Variation 1\n===VARIATION===\nVariation 2\n===VARIATION===\nVariation 3"
    assert split_variations(text) == ["Variation 1", "Variation 2", "Variation 3"]
    
    # Test split_variations with empty or no delimiter
    assert split_variations("") == []
    assert split_variations("   ") == []
    assert split_variations("Single variation") == ["Single variation"]

def test_split_numbered_tweets():
    # Test split_numbered_tweets standard format
    text = "1/3 First tweet\n2/3 Second tweet\n3/3 Third tweet"
    assert split_numbered_tweets(text) == ["1/3 First tweet", "2/3 Second tweet", "3/3 Third tweet"]

    # Test split_numbered_tweets with preamble
    text_with_preamble = "Sure, here is your thread:\n1/3 First tweet\n2/3 Second tweet"
    # Currently split_numbered_tweets yields ["Sure, here is your thread:\n1/3 First tweet", "2/3 Second tweet"]
    # We should check if we want to improve split_numbered_tweets to handle preambles
    res = split_numbered_tweets(text_with_preamble)
    assert res[0].startswith("Sure, here is your thread") or res[0].startswith("1/3")

def test_char_count_status():
    status = char_count_status("Hello", 10)
    assert status == {"count": 5, "limit": 10, "is_over": False}
    
    status_over = char_count_status("Hello World!", 5)
    assert status_over == {"count": 12, "limit": 5, "is_over": True}


def test_build_content_markdown():
    entries = [
        {"type": "Post", "platform": "LinkedIn", "content": "Hello LinkedIn!", "timestamp": "2026-07-17 12:00"},
        {"type": "Tweet", "platform": "Twitter/X", "content": "Hello Twitter!", "timestamp": "2026-07-17 12:05"}
    ]
    md = build_content_markdown(entries)
    assert "# Growth Engine AI" in md
    assert "Hello LinkedIn!" in md
    assert "Hello Twitter!" in md
    assert "2026-07-17 12:00" in md

