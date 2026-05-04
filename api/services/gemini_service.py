import requests
from .base import BaseAIService

class GeminiService(BaseAIService):
    def __init__(self):
        super().__init__('GEMINI_API_KEY')
    
    async def _test_connection(self):
        """Test if Gemini API is working"""
        try:
            url = f'https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}'
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def call(self, title, content):
        if not self.is_available():
            raise Exception('Gemini API key not configured')
        
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}'
        
        payload = {
            'contents': [
                {
                    'parts': [
                        {'text': self.build_prompt(title, content)}
                    ]
                }
            ],
            'generationConfig': {
                'maxOutputTokens': 1024,
                'temperature': 0.3
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code != 200:
                error_detail = response.text[:200]
                raise Exception(f'Gemini API error ({response.status_code}): {error_detail}')
            
            data = response.json()
            text = data['candidates'][0]['content']['parts'][0]['text']
            return self.parse_response(text)
            
        except requests.exceptions.Timeout:
            raise Exception('Gemini API timeout after 30 seconds')

gemini_service = GeminiService()

def call_gemini(title, content):
    return gemini_service.call(title, content)