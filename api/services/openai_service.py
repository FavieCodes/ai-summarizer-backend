import requests
from .base import BaseAIService

class OpenAIService(BaseAIService):
    def __init__(self):
        super().__init__('OPENAI_API_KEY')
    
    async def _test_connection(self):
        """Test if OpenAI API is working"""
        try:
            url = 'https://api.openai.com/v1/models'
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def call(self, title, content):
        if not self.is_available():
            raise Exception('OpenAI API key not configured')
        
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'model': 'gpt-4o-mini',
            'max_tokens': 1024,
            'temperature': 0.3,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You summarize web pages. Respond only with valid JSON, no markdown or backticks.'
                },
                {
                    'role': 'user',
                    'content': self.build_prompt(title, content)
                }
            ]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                error_detail = response.text[:200]
                raise Exception(f'OpenAI API error ({response.status_code}): {error_detail}')
            
            data = response.json()
            result_text = data['choices'][0]['message']['content']
            return self.parse_response(result_text)
            
        except requests.exceptions.Timeout:
            raise Exception('OpenAI API timeout after 30 seconds')

openai_service = OpenAIService()

def call_openai(title, content):
    return openai_service.call(title, content)