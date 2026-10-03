from __future__ import annotations
import base64
import urllib.parse
from dataclasses import dataclass
from config import IMAGE_STYLES, PLATFORM_IMAGE_SIZES

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    requests = None
    _HAS_REQUESTS = False


@dataclass
class ImageResult:
    success: bool
    image_bytes: bytes | None = None
    image_url: str | None = None
    provider: str | None = None
    error_message: str | None = None


class ImageService:
    POLLINATIONS_BASE = "https://image.pollinations.ai/prompt/{prompt}"
    GEMINI_MODEL = "gemini-2.5-flash-preview-image-generation"
    GEMINI_URL = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "{model}:generateContent?key={key}"
    )

    def __init__(self, google_api_key: str | None = None):
        self.google_api_key = google_api_key

    def generate(
        self,
        prompt: str,
        platform: str = "Instagram",
        ratio: str = "1:1",
        model: str = "flux",
        nologo: bool = True,
    ) -> ImageResult:
        if not _HAS_REQUESTS:
            return ImageResult(success=False, error_message="requests package is not installed")

        # Resolve dimensions
        width, height = self._resolve_dimensions(platform, ratio)

        # 1. Try Pollinations.ai (Flux)
        poll_res = self._pollinations(prompt, width, height, model, nologo)
        if poll_res.success:
            return poll_res

        # 2. Try Gemini fallback if key available
        if self.google_api_key:
            gem_res = self._gemini(prompt)
            if gem_res.success:
                return gem_res

        return ImageResult(
            success=False,
            error_message=f"Image generation failed. Pollinations error: {poll_res.error_message}",
        )

    def _resolve_dimensions(self, platform: str, ratio: str) -> tuple[int, int]:
        if "4:5" in ratio or ratio == "4:5":
            return 800, 1000
        if "16:9" in ratio or ratio == "16:9":
            return 1280, 720
        if "9:16" in ratio or ratio == "9:16":
            return 720, 1280
        if "1:1" in ratio or ratio == "1:1":
            return 1024, 1024

        if platform in PLATFORM_IMAGE_SIZES:
            s = PLATFORM_IMAGE_SIZES[platform]
            return s["width"], s["height"]

        return 1024, 1024

    def _pollinations(self, prompt: str, width: int, height: int, model: str, nologo: bool) -> ImageResult:
        try:
            clean_model = model.split(" ")[0].strip() if model else "flux"
            encoded = urllib.parse.quote(prompt.strip())
            logo_param = "true" if nologo else "false"
            url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model={clean_model}&nologo={logo_param}&enhance=true"

            headers = {"User-Agent": "GrowthEngineAI/3.1 (SocialVelocityPlatform)"}
            resp = requests.get(url, timeout=45, headers=headers)

            if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("image"):
                return ImageResult(
                    success=True,
                    image_bytes=resp.content,
                    image_url=url,
                    provider="Pollinations.ai (Flux)",
                )
            return ImageResult(success=False, error_message=f"Pollinations HTTP status {resp.status_code}")
        except requests.exceptions.Timeout:
            return ImageResult(success=False, error_message="Pollinations timed out (45s) — server is busy, try again")
        except Exception as e:
            return ImageResult(success=False, error_message=f"Pollinations network error: {e}")

    def _gemini(self, prompt: str) -> ImageResult:
        try:
            url = self.GEMINI_URL.format(model=self.GEMINI_MODEL, key=self.google_api_key)
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
            }
            resp = requests.post(url, json=payload, timeout=45)
            if resp.status_code != 200:
                return ImageResult(success=False, error_message=f"Gemini image endpoint error {resp.status_code}")
            data = resp.json()
            for candidate in data.get("candidates", []):
                for part in candidate.get("content", {}).get("parts", []):
                    if "inlineData" in part:
                        img_bytes = base64.b64decode(part["inlineData"]["data"])
                        return ImageResult(success=True, image_bytes=img_bytes, provider="Google Gemini Image Gen")
            return ImageResult(success=False, error_message="Gemini returned no inline image data")
        except Exception as e:
            return ImageResult(success=False, error_message=f"Gemini fallback error: {e}")


def build_image_prompt(post_content: str, platform: str, style: str = "professional") -> str:
    size_info = PLATFORM_IMAGE_SIZES.get(platform, PLATFORM_IMAGE_SIZES["Instagram"])
    platform_context = {
        "LinkedIn":        f"Professional LinkedIn header graphic, {size_info['desc']}, executive modern corporate aesthetic",
        "Instagram":       f"Eye-catching Instagram post visual, {size_info['desc']}, high-engagement aesthetic",
        "Instagram Story": f"Bold vertical Instagram Story, {size_info['desc']}, mobile-first punchy design",
        "Twitter/X":       f"Clean Twitter/X card image, {size_info['desc']}, minimal high-contrast design",
    }.get(platform, f"Professional social media image, {size_info['desc']}")

    style_desc = IMAGE_STYLES.get(style, IMAGE_STYLES.get("professional", "Clean modern digital art"))
    snippet = post_content[:180].strip().replace("\n", " ") if post_content else "social media thought leadership"

    return (
        f"{platform_context}. "
        f"Visual theme inspired by: {snippet}. "
        f"Style: {style_desc}. "
        f"No text overlays. No watermarks. No logos. "
        f"Ultra high quality. Sharp focus. 4K resolution."
    )
