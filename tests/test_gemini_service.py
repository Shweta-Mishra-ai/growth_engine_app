import pytest
from unittest.mock import MagicMock, patch
import sys
from services import GeminiService, GenerationResult

def test_gemini_service_init_missing_key():
    with pytest.raises(ValueError, match="API key required"):
        GeminiService(api_key="")

@patch("services.gemini_service._NEW_SDK", True)
@patch("services.gemini_service.genai")
def test_gemini_service_generate_success_new_sdk(mock_genai_module):
    mock_client = MagicMock()
    mock_genai_module.Client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = "Mocked Response Text"
    mock_client.models.generate_content.return_value = mock_response
    
    service = GeminiService(api_key="test_api_key")
    result = service.generate("Hello")
    
    assert result.success is True
    assert result.text == "Mocked Response Text"
    mock_client.models.generate_content.assert_called_once()

@patch("services.gemini_service._NEW_SDK", False)
@patch("services.gemini_service.genai")
def test_gemini_service_generate_success_legacy_sdk(mock_genai_module):
    mock_model = MagicMock()
    mock_genai_module.GenerativeModel.return_value = mock_model
    
    mock_response = MagicMock()
    mock_response.text = "Legacy Mocked Response Text"
    mock_model.generate_content.return_value = mock_response
    
    service = GeminiService(api_key="test_api_key")
    result = service.generate("Hello")
    
    assert result.success is True
    assert result.text == "Legacy Mocked Response Text"
    mock_genai_module.configure.assert_called_once_with(api_key="test_api_key")
    mock_model.generate_content.assert_called_once()

@patch("services.gemini_service._NEW_SDK", True)
@patch("services.gemini_service.genai")
def test_gemini_service_generate_empty_response(mock_genai_module):
    mock_client = MagicMock()
    mock_genai_module.Client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.text = ""  # empty response
    mock_client.models.generate_content.return_value = mock_response
    
    service = GeminiService(api_key="test_api_key")
    result = service.generate("Hello")
    
    assert result.success is False
    assert result.error_type == "empty_response"
    assert "safety filter" in result.error_message.lower()

@patch("services.gemini_service._NEW_SDK", True)
@patch("services.gemini_service.genai")
def test_gemini_service_generate_quota_error(mock_genai_module):
    mock_client = MagicMock()
    mock_genai_module.Client.return_value = mock_client
    
    mock_client.models.generate_content.side_effect = Exception("RESOURCE_EXHAUSTED: Quota exceeded")
    
    service = GeminiService(api_key="test_api_key")
    result = service.generate("Hello")
    
    assert result.success is False
    assert result.error_type == "quota"
    assert "quota exceeded" in result.error_message.lower()
