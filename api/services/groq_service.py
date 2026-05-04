import requests
from .base import BaseAIService

class GroqService(BaseAIService):
    def __init__(self):
        super().__init__('GROQ_API_KEY')
    
    async def _test_connection(self):
        """Test if Groq API is working"""
        try:
            url = 'https://api.groq.com/openai/v1/chat/completions'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            payload = {
                'model': 'llama-3.3-70b-versatile',
                'max_tokens': 5,
                'messages': [{'role': 'user', 'content': 'Hi'}]
            }
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def call(self, title, content):
        if not self.is_available():
            raise Exception(f'Groq API key not configured or invalid')
        
        url = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            'model': 'llama-3.3-70b-versatile',
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
                raise Exception(f'Groq API error ({response.status_code}): {error_detail}')
            
            data = response.json()
            result_text = data['choices'][0]['message']['content']
            return self.parse_response(result_text)
            
        except requests.exceptions.Timeout:
            raise Exception('Groq API timeout after 30 seconds')
        except requests.exceptions.ConnectionError:
            raise Exception('Cannot connect to Groq API')

groq_service = GroqService()

def call_groq(title, content):
    return groq_service.call(title, content)