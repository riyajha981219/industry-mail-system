"""
News Service for fetching articles from NewsAPI
"""
import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.config import settings
from app.services.ai_service import AIService

class NewsService:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = settings.NEWS_API_URL
    
    async def fetch_news(self, keywords: str, days: int = 1, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch news articles from NewsAPI
        
        Args:
            keywords: Search keywords (comma-separated)
            days: Number of days to look back (1, 7, or 30)
            limit: Maximum number of articles to return
        
        Returns:
            List of news articles
        """
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        # Normalize keywords: if provided comma-separated, convert to OR query for NewsAPI
        q = keywords
        if isinstance(keywords, str) and "," in keywords:
            # remove extra spaces and replace commas with ' OR '
            parts = [p.strip() for p in keywords.split(',') if p.strip()]
            q = ' OR '.join(parts)

        if not self.api_key:
            raise RuntimeError("NEWS_API_KEY is not configured")

        params = {
            "q": q,
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "sortBy": "relevancy",
            "pageSize": limit,
            "language": "en"
        }

        headers = {
            "X-Api-Key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params, headers=headers)
                # Log status for debugging
                print(f"NewsAPI request url: {response.url}")
                print(f"NewsAPI response status: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                # For debugging, log a truncated version of the response body
                try:
                    body_preview = str(data)[:500]
                    print(f"NewsAPI body preview: {body_preview}")
                except Exception:
                    pass

                # If the API returned an error status, raise with message
                if data.get("status") != "ok":
                    msg = data.get("message") or "Unknown NewsAPI error"
                    print(f"NewsAPI error: {msg}")
                    raise RuntimeError(f"NewsAPI error: {msg}")

                articles = []
                for article in data.get("articles", [])[:limit]:
                    articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "url": article.get("url", ""),
                        "source": article.get("source", {}).get("name", "Unknown"),
                        "published_at": article.get("publishedAt", ""),
                        "image_url": article.get("urlToImage")
                    })

                # Log when no articles are found for visibility
                if not articles:
                    print(f"NewsAPI returned zero articles for keywords={keywords} (q={q})")

                    # Fallback: if original keywords were comma-separated, try each part separately
                    if isinstance(keywords, str) and "," in keywords:
                        for part in parts:
                            if not part:
                                continue
                            params_single = {**params, "q": part}
                            resp2 = await client.get(self.base_url, params=params_single, headers={'X-Api-Key': self.api_key})
                            try:
                                resp2.raise_for_status()
                                data2 = resp2.json()
                                arts2 = data2.get("articles", [])[:limit]
                                if arts2:
                                    found = []
                                    for article in arts2:
                                        found.append({
                                            "title": article.get("title", ""),
                                            "description": article.get("description", ""),
                                            "url": article.get("url", ""),
                                            "source": article.get("source", {}).get("name", "Unknown"),
                                            "published_at": article.get("publishedAt", ""),
                                            "image_url": article.get("urlToImage")
                                        })
                                    print(f"NewsAPI fallback succeeded for keyword='{part}' with {len(found)} articles")
                                    # Summarize found articles before returning
                                    ai = AIService()
                                    return await ai.summarize_articles(found, max_length=200)
                            except Exception:
                                continue

                # Summarize articles with AI service (fallback-friendly)
                ai = AIService()
                articles = await ai.summarize_articles(articles, max_length=200)

                return articles

        except httpx.HTTPError as e:
            print(f"HTTP error fetching news: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error fetching news: {str(e)}")
            raise
