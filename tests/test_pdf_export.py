"""
tests/test_pdf_export.py — Tests PDF generation with ReportLab.
"""
import pytest
from services.pdf_export import build_content_pdf, HAS_REPORTLAB


def _entry(entry_type="LinkedIn Post", platform="LinkedIn", content="Sample content"):
    return {
        "type": entry_type,
        "platform": platform,
        "content": content,
        "timestamp": "2026-10-04 12:00",
    }


class TestPDFGeneration:
    @pytest.mark.skipif(not HAS_REPORTLAB, reason="ReportLab not installed")
    def test_empty_entries_generates_valid_pdf(self):
        pdf = build_content_pdf([])
        assert isinstance(pdf, bytes)
        assert pdf[:4] == b"%PDF"
        assert len(pdf) > 500

    @pytest.mark.skipif(not HAS_REPORTLAB, reason="ReportLab not installed")
    def test_single_entry_pdf(self):
        entries = [_entry("LinkedIn Post", "LinkedIn", "This is a test post.")]
        pdf = build_content_pdf(entries)
        assert pdf[:4] == b"%PDF"
        assert len(pdf) > 1000

    @pytest.mark.skipif(not HAS_REPORTLAB, reason="ReportLab not installed")
    def test_all_platforms_work(self):
        entries = [
            _entry("LinkedIn Post", "LinkedIn", "LinkedIn content"),
            _entry("Twitter Thread", "Twitter/X", "1/ Tweet one\n2/ Tweet two"),
            _entry("Instagram Caption", "Instagram", "IG caption here"),
            _entry("Hooks", "Hooks", "Hook content"),
            _entry("Voice DNA", "Voice DNA", "Voice profile"),
        ]
        pdf = build_content_pdf(entries)
        assert pdf[:4] == b"%PDF"
        assert len(pdf) > 1000
