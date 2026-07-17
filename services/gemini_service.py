from __future__ import annotations
from dataclasses import dataclass
from config import MODEL_NAME, MODEL_FALLBACK, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS

try:
    from google import genai
    from google.genai import types as genai_types
    _NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    genai_types = None
    _NEW_SDK = False


@dataclass
class GenerationResult:
    success: bool
    text: str | None = None
    error_type: str | None = None
    error_message: str | None = None


class GeminiService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key required")
        self._new_sdk = _NEW_SDK
        if _NEW_SDK:
            self._client = genai.Client(api_key=api_key)
            self._legacy_model = None
        else:
            genai.configure(api_key=api_key)
            self._client = None
            self._legacy_model = genai.GenerativeModel(MODEL_NAME)

    def generate(self, prompt: str, max_tokens: int = DEFAULT_MAX_TOKENS, temperature: float = DEFAULT_TEMPERATURE) -> GenerationResult:
        result = self._call(prompt, max_tokens, temperature, MODEL_NAME)
        if not result.success and result.error_type == "unavailable":
            result = self._call(prompt, max_tokens, temperature, MODEL_FALLBACK)
        return result

    def _call(self, prompt: str, max_tokens: int, temperature: float, model_name: str) -> GenerationResult:
        try:
            if self._new_sdk:
                response = self._client.models.generate_content(
                    model=model_name, contents=prompt,
                    config=genai_types.GenerateContentConfig(max_output_tokens=max_tokens, temperature=temperature)
                )
            else:
                response = self._legacy_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens, temperature=temperature)
                )
            text = response.text
            if not text or not text.strip():
                return GenerationResult(success=False, error_type="empty_response",
                    error_message="AI returned empty response — safety filter or token limit. Try rephrasing your topic.")
            return GenerationResult(success=True, text=text)
        except Exception as e:
            return GenerationResult(success=False, **self._classify_error(e))

    @staticmethod
    def _classify_error(e: Exception) -> dict:
        err = str(e)
        if "429" in err or "quota" in err.lower() or "RESOURCE_EXHAUSTED" in err:
            return {"error_type": "quota", "error_message": "API Quota Exceeded — try again after midnight GMT or create a new Google AI Studio key."}
        if "401" in err or "API key not valid" in err:
            return {"error_type": "auth", "error_message": "Invalid API Key — check your Streamlit secrets."}
        if "503" in err or "UNAVAILABLE" in err or "overloaded" in err.lower():
            return {"error_type": "unavailable", "error_message": "Model overloaded — retrying with fallback."}
        if "quick accessor" in err.lower() or "no parts" in err.lower() or "safety" in err.lower():
            return {"error_type": "empty_response", "error_message": "Safety filter blocked this request. Try rephrasing your topic."}
        return {"error_type": "unknown", "error_message": f"API Error: {err}"}
