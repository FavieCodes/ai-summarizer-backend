from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from .services.claude_service import call_claude, claude_service
from .services.openai_service import call_openai, openai_service
from .services.gemini_service import call_gemini, gemini_service
from .services.groq_service import call_groq, groq_service
from .services.mock_service import call_mock
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import logging
import traceback
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import time

logger = logging.getLogger(__name__)

PROVIDERS = [
    ('groq', call_groq),
    ('gemini', call_gemini),
    ('openai', call_openai),
    ('claude', call_claude),
    ('mock', call_mock),
]

def homepage(request):
    """Serve the API documentation homepage"""
    return render(request, 'index.html')

def test_groq_connection(api_key):
    """Synchronously test Groq API connection"""
    if not api_key or len(api_key) < 20:
        return False
    try:
        url = 'https://api.groq.com/openai/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        payload = {
            'model': 'llama-3.3-70b-versatile',
            'max_tokens': 5,
            'messages': [{'role': 'user', 'content': 'test'}]
        }
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

def test_gemini_connection(api_key):
    """Synchronously test Gemini API connection"""
    if not api_key or len(api_key) < 10:
        return False
    try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models?key={api_key}'
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def test_openai_connection(api_key):
    """Synchronously test OpenAI API connection"""
    if not api_key or len(api_key) < 20:
        return False
    try:
        url = 'https://api.openai.com/v1/models'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

def test_claude_connection(api_key):
    """Synchronously test Claude API connection"""
    if not api_key or len(api_key) < 20:
        return False
    try:
        url = 'https://api.anthropic.com/v1/messages'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
        payload = {
            'model': 'claude-3-sonnet-20240229',
            'max_tokens': 5,
            'messages': [{'role': 'user', 'content': 'test'}]
        }
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

@api_view(['GET'])
def health_check(request):
    """
    Comprehensive health check endpoint with real-time provider availability
    """
    # Get current timestamp
    current_time = datetime.now()
    
    # cache for 60 seconds
    cache_key = 'provider_status'
    cached_status = cache.get(cache_key)
    
    if cached_status:
        providers_status = cached_status
    else:
        providers_status = {}
        
        # Test each provider synchronously with timeout
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tests
            groq_future = executor.submit(test_groq_connection, groq_service.api_key)
            gemini_future = executor.submit(test_gemini_connection, gemini_service.api_key)
            openai_future = executor.submit(test_openai_connection, openai_service.api_key)
            claude_future = executor.submit(test_claude_connection, claude_service.api_key)
            
            # Get results with timeout
            try:
                groq_available = groq_future.result(timeout=10)
            except FuturesTimeoutError:
                groq_available = False
            
            try:
                gemini_available = gemini_future.result(timeout=10)
            except FuturesTimeoutError:
                gemini_available = False
            
            try:
                openai_available = openai_future.result(timeout=10)
            except FuturesTimeoutError:
                openai_available = False
            
            try:
                claude_available = claude_future.result(timeout=10)
            except FuturesTimeoutError:
                claude_available = False
        
        # Build status responses
        providers_status['groq'] = {
            'available': groq_available,
            'configured': groq_service.is_available(),
            'message': 'API is responding' if groq_available else ('API key configured but not responding' if groq_service.is_available() else 'API key missing or invalid')
        }
        
        providers_status['gemini'] = {
            'available': gemini_available,
            'configured': gemini_service.is_available(),
            'message': 'API is responding' if gemini_available else ('API key configured but not responding' if gemini_service.is_available() else 'API key missing or invalid')
        }
        
        providers_status['openai'] = {
            'available': openai_available,
            'configured': openai_service.is_available(),
            'message': 'API is responding' if openai_available else ('API key configured but not responding' if openai_service.is_available() else 'API key missing or invalid')
        }
        
        providers_status['claude'] = {
            'available': claude_available,
            'configured': claude_service.is_available(),
            'message': 'API is responding' if claude_available else ('API key configured but not responding' if claude_service.is_available() else 'API key missing or invalid')
        }
        
        # Mock is always available
        providers_status['mock'] = {
            'available': True,
            'configured': True,
            'message': 'Always available for testing'
        }
        
        # Cache for 60 seconds
        cache.set(cache_key, providers_status, 60)
    
    # Calculate overall status
    any_available = any(p['available'] for p in providers_status.values())
    
    # Get base URL from request
    base_url = f"{request.scheme}://{request.get_host()}"
    
    return Response({
        'status': 'healthy' if any_available else 'degraded',
        'server': 'Django',
        'timestamp': current_time.isoformat(),
        'timestamp_formatted': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': str(current_time.astimezone().tzinfo),
        'uptime_seconds': time.time() - getattr(health_check, 'start_time', time.time()),
        'providers': providers_status,
        'available_providers': [name for name, status in providers_status.items() if status['available']],
        'endpoints': {
            'homepage': f"{base_url}/",
            'summarize': f"{base_url}/api/summarize/",
            'health': f"{base_url}/api/health/"
        },
        'rate_limit': '30 requests per minute',
        'version': '1.0.0'
    })

# Store start time for uptime tracking
health_check.start_time = time.time()

@api_view(['POST'])
@csrf_exempt
@throttle_classes([UserRateThrottle])
def summarize_page(request):
    """
    Summarize webpage content using AI providers with automatic fallback
    """
    start_time = time.time()
    
    try:
        # Validate request
        data = request.data
        title = data.get('title', 'No Title')
        content = data.get('content', '')
        url = data.get('url', '')
        
        # Log request (without sensitive data)
        logger.info(f"Summarize request - Title: {title[:50]}, Content length: {len(content)}, URL: {url[:50]}")
        
        if not content:
            logger.warning("No content provided in request")
            return Response({
                'success': False,
                'error': 'No content provided for summarization'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Truncate content if too long
        if len(content) > 8000:
            content = content[:8000]
            logger.info(f"Content truncated to 8000 characters")
        
        # Try each provider
        errors = []
        for provider_name, provider_func in PROVIDERS:
            try:
                logger.info(f"Attempting provider: {provider_name}")
                result = provider_func(title, content)
                
                if result and isinstance(result, dict):
                    processing_time = time.time() - start_time
                    logger.info(f"✓ {provider_name} succeeded in {processing_time:.2f}s")
                    
                    return Response({
                        'success': True,
                        'summary': result,
                        'provider': provider_name,
                        'fromCache': False,
                        'processing_time_seconds': round(processing_time, 2),
                        'timestamp': datetime.now().isoformat()
                    })
                    
            except Exception as e:
                error_msg = f"{provider_name}: {str(e)}"
                logger.warning(f"✗ {error_msg}")
                errors.append(error_msg)
                continue
        
        # All providers failed
        processing_time = time.time() - start_time
        logger.error(f"All providers failed after {processing_time:.2f}s. Errors: {errors}")
        
        return Response({
            'success': False,
            'error': 'All AI providers failed',
            'details': errors,
            'processing_time_seconds': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        
        return Response({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'processing_time_seconds': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)