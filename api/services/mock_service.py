import json
import random

def call_mock(title, content):
    """
    Mock service that always works - perfect for testing and fallback
    This doesn't require any API keys and always returns a valid summary
    """
    # Extract some keywords from content for realistic mock
    words = content.split()[:30]
    topic = "this topic" if len(words) < 5 else " ".join(words[:5])
    
    # Generate realistic reading time
    word_count = len(content.split())
    reading_time = max(1, word_count // 200)  # 200 words per minute
    
    # Create a list of topic tags based on content
    content_lower = content.lower()
    tags = []
    if 'ai' in content_lower or 'artificial' in content_lower:
        tags.append("Artificial Intelligence")
    if 'machine learning' in content_lower or 'ml' in content_lower:
        tags.append("Machine Learning")
    if 'data' in content_lower:
        tags.append("Data Science")
    if 'web' in content_lower or 'internet' in content_lower:
        tags.append("Web Technology")
    if not tags:
        tags = ["Information", "Article Summary", "Key Points"]
    tags = tags[:3]  # Max 3 tags
    
    return {
        "summary": [
            f"The article discusses {topic} and its key implications in detail",
            f"Several important points are made throughout the content about {topic}",
            f"The author presents evidence and examples supporting the main arguments",
            f"Practical applications and real-world use cases are highlighted",
            f"The conclusion summarizes the key takeaways and future implications"
        ],
        "keyInsights": [
            f"Understanding {topic} is crucial for staying current in this field",
            f"The data and examples suggest significant implications for practice",
            f"Future developments in this area are promising and worth monitoring"
        ],
        "readingTime": f"{reading_time} min read",
        "wordCount": f"approximately {word_count} words",
        "topicTags": tags
    }