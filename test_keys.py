import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_claude():
    key = os.getenv('CLAUDE_API_KEY')
    if not key:
        print("❌ Claude: No API key found")
        return False
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': key,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 100,
                'messages': [{'role': 'user', 'content': 'Say "test"'}]
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Claude: API key works")
            return True
        else:
            print(f"❌ Claude: Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Claude: Error - {e}")
        return False

def test_openai():
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        print("❌ OpenAI: No API key found")
        return False
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {key}'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'max_tokens': 100,
                'messages': [{'role': 'user', 'content': 'Say "test"'}]
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ OpenAI: API key works")
            return True
        else:
            print(f"❌ OpenAI: Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ OpenAI: Error - {e}")
        return False

def test_gemini():
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        print("❌ Gemini: No API key found")
        return False
    
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}',
            json={
                'contents': [{'parts': [{'text': 'Say "test"'}]}]
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Gemini: API key works")
            return True
        else:
            print(f"❌ Gemini: Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Gemini: Error - {e}")
        return False

def test_groq():
    key = os.getenv('GROQ_API_KEY')
    if not key:
        print("❌ Groq: No API key found")
        return False
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {key}'
            },
            json={
                'model': 'llama-3.1-70b-versatile',
                'max_tokens': 100,
                'messages': [{'role': 'user', 'content': 'Say "test"'}]
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Groq: API key works")
            return True
        else:
            print(f"❌ Groq: Failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Groq: Error - {e}")
        return False

if __name__ == '__main__':
    print("Testing API Keys...\n")
    test_claude()
    test_openai()
    test_gemini()
    test_groq()