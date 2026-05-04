# 🤖 AI Page Summarizer - Django Backend

Production-ready Django backend that acts as a secure proxy for multiple AI providers (Claude, OpenAI, Gemini, Groq) with automatic fallback. Deployable to Vercel.

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone [GITHUB REPO](https://github.com/FavieCodes/ai-summarizer-backend.git)
cd ai-summarizer-backend
```
2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Start development server**

```bash
python manage.py runserver
```
7. **Test the API**

```bash
curl -X POST http://localhost:8000/api/summarize/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Article","content":"This is a test article about AI..."}'
  ```

## 🌐 Deploy to Vercel

```bash
Step 1: Install Vercel CLI

npm i -g vercel
```

```bash
Step 2: Set up environment variables on Vercel
Go to your Vercel project dashboard → Settings → Environment Variables, add:

Name	Value
SECRET_KEY	Your Django secret key
CLAUDE_API_KEY	Your Claude API key (optional)
OPENAI_API_KEY	Your OpenAI API key (optional)
GEMINI_API_KEY	Your Gemini API key (optional)
GROQ_API_KEY	Your Groq API key (optional)
DEBUG	False
Step 3: Deploy
bash
vercel --prod
Step 4: Update Chrome Extension
In your Chrome extension's background.js, update:

javascript
const BACKEND_URL = 'https://your-app-name.vercel.app/api/summarize/';
```
## 📡 API Documentation
POST /api/summarize/
Summarizes webpage content using AI providers.

Request Body:

```json
{
  "title": "Page Title",
  "content": "Extracted page content (max 8000 chars)"
}
```

Success Response (200 OK):

```json
{
  "success": true,
  "summary": {
    "summary": ["bullet point 1", "bullet point 2", ...],
    "keyInsights": ["insight 1", "insight 2", ...],
    "readingTime": "5 min read",
    "wordCount": "approximately 1200 words",
    "topicTags": ["AI", "Technology", "Innovation"]
  },
  "provider": "groq",
  "fromCache": false
}
```
Error Response (503 Service Unavailable):

```json
{
  "success": false,
  "error": "All AI providers failed",
  "details": ["claude: API key not configured", "openai: Rate limit exceeded"]
}
```
GET /api/health/
Health check endpoint for monitoring.

Response:

```json
{
  "status": "healthy",
  "providers_available": ["groq", "gemini"]
}
```
## 🔧 Configuration
Environment Variables
```
Variable	Required	Description
SECRET_KEY	✅	Django secret key (generate with python -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG	❌	Set to False in production
ALLOWED_HOSTS	❌	Comma-separated list of allowed hosts
CLAUDE_API_KEY	❌	Anthropic Claude API key
OPENAI_API_KEY	❌	OpenAI API key
GEMINI_API_KEY	❌	Google Gemini API key
GROQ_API_KEY	❌	Groq API key (recommended for free tier)
RATE_LIMIT	❌	Requests per minute (default: 30)
Provider Fallback Order
Claude (requires API key)
OpenAI (requires API key)
Gemini (free tier available)
Groq (free tier, fastest)

The system automatically tries the next provider if one fails.
```
## 🛡️ Security Features
No API keys in client-side code - All keys stored server-side
Environment variables - Keys never committed to version control
Rate limiting - Prevents abuse (30 requests/minute per IP)
CORS protection - Configurable allowed origins
HTTPS enforcement - Redirects HTTP to HTTPS in production
Input validation - Validates all request data
Error handling - No sensitive info in error responses

## 📊 Performance Optimizations
Content truncation - Limits to 8000 characters
Timeout handling - 30-second timeout for API calls
Async ready - Can be upgraded to async views
Response caching - Can be added at CDN level

## 🧪 Testing
```bash
# Run tests
python manage.py test

# Test with curl
curl -X POST http://localhost:8000/api/summarize/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Machine learning is a subset of AI..."}'
```
## 📝 License
MIT License - Free for personal and commercial use

## 🤝 Contributing
Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Open a Pull Request

