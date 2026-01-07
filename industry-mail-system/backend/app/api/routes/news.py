"""
News API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.services.news_service import NewsService
from app.services.email_service import EmailService
from pydantic import BaseModel

router = APIRouter()

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    source: str
    published_at: str
    image_url: Optional[str] = None

class NewsResponse(BaseModel):
    articles: List[NewsArticle]
    total_results: int

class SendNewsletterRequest(BaseModel):
    topic_id: int
    days: int = 1

@router.get("/fetch", response_model=NewsResponse)
async def fetch_news(
    topic: str,
    days: int = 1,
    limit: int = 10
):
    """
    Fetch news articles for a specific topic
    days: 1, 7, or 30
    """
    if days not in [1, 7, 30]:
        raise HTTPException(status_code=400, detail="Days must be 1, 7, or 30")
    
    news_service = NewsService()
    articles = await news_service.fetch_news(topic, days, limit)
    
    return {
        "articles": articles,
        "total_results": len(articles)
    }

@router.post("/send-newsletter")
async def send_newsletter(
    request: SendNewsletterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send newsletter to all subscribers of a topic
    """
    from app.models.topic import Topic
    from app.models.subscription import Subscription
    
    # Get topic
    topic = db.query(Topic).filter(Topic.id == request.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Get subscribers
    subscriptions = db.query(Subscription).filter(
        Subscription.topic_id == request.topic_id
    ).all()
    
    if not subscriptions:
        return {"message": "No subscribers found for this topic"}
    
    # Fetch news
    news_service = NewsService()
    try:
        articles = await news_service.fetch_news(topic.keywords, request.days, 10)
    except Exception as e:
        # Surface the error from the news provider for easier debugging
        raise HTTPException(status_code=502, detail=str(e))

    if not articles:
        raise HTTPException(status_code=404, detail="No news articles found for the requested topic/days")
    
    # Send emails in background
    email_service = EmailService()
    for subscription in subscriptions:
        background_tasks.add_task(
            email_service.send_newsletter,
            subscription.user.email,
            topic.name,
            articles
        )
        
        # Update last_sent_at
        subscription.last_sent_at = datetime.now()
    
    db.commit()
    
    return {
        "message": f"Newsletter scheduled to be sent to {len(subscriptions)} subscribers",
        "articles_count": len(articles)
    }
