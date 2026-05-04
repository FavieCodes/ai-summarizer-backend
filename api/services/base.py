import os
import json
import re
from abc import ABC, abstractmethod

class BaseAIService(ABC):
    """Base class for AI services"""
    
    def __init__(self, api_key_env_var):
        self.api_key_env_var = api_key_env_var
        self.api_key = os.getenv(api_key_env_var)
    
    def is_available(self):
        """Check if API key is configured and looks valid"""
        if not self.api_key:
            return False
        
        # Check for placeholder values
        if self.api_key in ['YOUR_CLAUDE_API_KEY_HERE', 'YOUR_OPENAI_API_KEY_HERE', 
                           'YOUR_GEMINI_API_KEY_HERE', 'YOUR_GROQ_API_KEY_HERE',
                           '[ENCRYPTION_KEY]', '']:
            return False
        
        # Check minimum length for real keys
        if len(self.api_key) < 10:
            return False
            
        return True
    
    async def check_availability(self):
        """Actually test if the API is working by making a small request"""
        if not self.is_available():
            return False
        
        try:
            # Override this method in child classes to test the actual API
            return await self._test_connection()
        except:
            return False
    
    async def _test_connection(self):
        """Override in child classes to test API connection"""
        return False
    
    def get_api_key(self):
        """Return the API key"""
        return self.api_key
    
    @abstractmethod
    def call(self, title, content):
        """Make API call to the provider"""
        pass
    
    def build_prompt(self, title, content):
        """Build the summarization prompt"""
        # Limit content length to 8000 chars (same as original extension)
        if len(content) > 8000:
            content = content[:8000]
        
        # Match the exact prompt from your original extension
        return f"""You are a helpful assistant that summarizes web pages.

Page Title: {title}
Page Content:
{content}

Respond ONLY with a valid JSON object — no markdown, no backticks, no extra text:
{{
  "summary": ["bullet 1", "bullet 2", "bullet 3", "bullet 4", "bullet 5"],
  "keyInsights": ["insight 1", "insight 2", "insight 3"],
  "readingTime": "X min read"
}}"""
    
    def parse_response(self, text):
        """Parse AI response, extracting JSON"""
        # Remove markdown code blocks if present
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Find JSON object
        json_match = re.search(r'\{[\s\S]*\}', text)
        if not json_match:
            raise ValueError('Could not parse AI response as JSON')
        
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError as e:
            raise ValueError(f'Invalid JSON from AI: {str(e)}')