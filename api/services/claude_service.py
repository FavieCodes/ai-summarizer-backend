import requests
from .base import BaseAIService

class ClaudeService(BaseAIService):
    def __init__(self):
        super().__init__('CLAUDE_API_KEY')
    
    async def _test_connection(self):
        """Test if Claude API is working"""
        try:
            url = 'https://api.anthropic.com/v1/messages'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01'
            }
            payload = {
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 5,
                'messages': [{'role': 'user', 'content': 'Hi'}]
            }
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def call(self, title, content):
        if not self.is_available():
            raise Exception('Claude API key not configured')
        
        url = 'https://api.anthropic.com/v1/messages'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-3-sonnet-20240229',
            'max_tokens': 1024,
            'messages': [
                {'role': 'user', 'content': self.build_prompt(title, content)}
            ]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code != 200:
                error_detail = response.text[:200]
                raise Exception(f'Claude API error ({response.status_code}): {error_detail}')
            
            data = response.json()
            return self.parse_response(data['content'][0]['text'])
            
        except requests.exceptions.Timeout:
            raise Exception('Claude API timeout after 30 seconds')

claude_service = ClaudeService()

def call_claude(title, content):
    return claude_service.call(title, content)