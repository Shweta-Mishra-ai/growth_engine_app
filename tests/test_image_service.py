"""
tests/test_image_service.py — Tests ImageService and prompt builder with mocked requests.
"""
from unittest.mock import patch, MagicMock
from services.image_service import ImageService, ImageResult, build_image_prompt
from config import PLATFORM_IMAGE_SIZES, IMAGE_STYLES


class TestPlatformSizes:
    def test_linkedin_dimensions(self):
        s = PLATFORM_IMAGE_SIZES["LinkedIn"]
        assert s["width"] == 1200
        assert s["height"] == 628

    def test_instagram_square(self):
        s = PLATFORM_IMAGE_SIZES["Instagram"]
        assert s["width"] == 1024
        assert s["height"] == 1024

    def test_instagram_story_vertical(self):
        s = PLATFORM_IMAGE_SIZES["Instagram Story"]
        assert s["height"] > s["width"]

    def test_twitter_landscape(self):
        s = PLATFORM_IMAGE_SIZES["Twitter/X"]
        assert s["width"] > s["height"]

    def test_all_platforms_defined(self):
        assert len(PLATFORM_IMAGE_SIZES) >= 4


class TestImageServiceInit:
    def test_init_with_key(self):
        svc = ImageService(google_api_key="test_key")
        assert svc.google_api_key == "test_key"

    def test_init_without_key(self):
        svc = ImageService(google_api_key=None)
        assert svc is not None

    def test_has_pollinations_method(self):
        svc = ImageService()
        assert hasattr(svc, "_pollinations")


class TestImageServiceGenerate:
    @patch("services.image_service._HAS_REQUESTS", True)
    @patch("services.image_service.requests.get")
    def test_pollinations_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"content-type": "image/jpeg"}
        mock_resp.content = b"fake_image_bytes"
        mock_get.return_value = mock_resp

        svc = ImageService()
        res = svc.generate("A sunny beach", platform="Instagram")
        assert res.success is True
        assert res.image_bytes == b"fake_image_bytes"
        assert "Pollinations" in res.provider

    @patch("services.image_service._HAS_REQUESTS", True)
    @patch("services.image_service.requests.get")
    def test_pollinations_failure_without_gemini(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp

        svc = ImageService(google_api_key=None)
        res = svc.generate("A sunny beach", platform="Instagram")
        assert res.success is False
        assert "Image generation failed" in res.error_message


class TestBuildImagePrompt:
    def test_contains_platform_context(self):
        p = build_image_prompt("My SaaS startup launch", "LinkedIn", "professional")
        assert "LinkedIn" in p
        assert "No text overlays" in p

    def test_contains_style(self):
        p = build_image_prompt("My SaaS launch", "Twitter/X", "minimal")
        assert "Minimalist" in p or "minimal" in p.lower()
