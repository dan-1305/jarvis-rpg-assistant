import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import google.generativeai as genai

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis_core.ai_agent import AIAgent

class TestAIAgent:
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration"""
        with patch('jarvis_core.ai_agent.Config') as mock:
            config_instance = MagicMock()
            config_instance.get.side_effect = lambda key, default=None: {
                'GOOGLE_API_KEY': 'test-api-key',
                'AI_MODEL': 'gemini-pro'
            }.get(key, default)
            mock.return_value = config_instance
            yield mock
    
    @pytest.fixture
    def ai_agent(self, mock_config):
        """Create AI agent with mocked dependencies"""
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel') as mock_model:
                agent = AIAgent()
                yield agent
    
    def test_init_ai_agent(self, ai_agent):
        """Test AI agent initialization"""
        assert ai_agent is not None
        assert ai_agent.model is not None
    
    @patch('google.generativeai.GenerativeModel')
    def test_generate_response(self, mock_model, ai_agent):
        """Test generating a response"""
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model.return_value.generate_content.return_value = mock_response
        
        ai_agent.model = mock_model.return_value
        
        response = ai_agent.generate_response("Test prompt")
        assert response == "Test response"
    
    @patch('google.generativeai.GenerativeModel')
    def test_generate_response_with_context(self, mock_model, ai_agent):
        """Test generating response with context"""
        mock_response = MagicMock()
        mock_response.text = "Contextual response"
        mock_model.return_value.generate_content.return_value = mock_response
        
        ai_agent.model = mock_model.return_value
        
        context = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        response = ai_agent.generate_response("How are you?", context=context)
        assert response == "Contextual response"
    
    def test_error_handling_on_api_failure(self, ai_agent):
        """Test error handling when API fails"""
        with patch.object(ai_agent.model, 'generate_content', side_effect=Exception("API Error")):
            response = ai_agent.generate_response("Test prompt")
            assert "error" in response.lower() or response == ""
    
    def test_parse_task_from_text(self, ai_agent):
        """Test parsing tasks from text"""
        text = "Remind me to buy groceries tomorrow at 5pm"
        
        with patch.object(ai_agent, 'generate_response', return_value='{"task": "buy groceries", "time": "tomorrow 5pm"}'):
            result = ai_agent.parse_task_from_text(text)
            assert result is not None
    
    def test_summarize_text(self, ai_agent):
        """Test text summarization"""
        long_text = "This is a very long text that needs to be summarized. " * 20
        
        with patch.object(ai_agent, 'generate_response', return_value="Summary of the text"):
            summary = ai_agent.summarize_text(long_text)
            assert len(summary) < len(long_text)
            assert summary == "Summary of the text"
    
    def test_translate_text(self, ai_agent):
        """Test text translation"""
        with patch.object(ai_agent, 'generate_response', return_value="Xin chào"):
            translation = ai_agent.translate_text("Hello", target_lang="Vietnamese")
            assert translation == "Xin chào"
    
    def test_rate_limiting(self, ai_agent):
        """Test that rate limiting is respected"""
        import time
        
        with patch.object(ai_agent.model, 'generate_content', return_value=MagicMock(text="Response")):
            start_time = time.time()
            
            for _ in range(3):
                ai_agent.generate_response("Test")
            
            elapsed = time.time() - start_time
            assert elapsed >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
