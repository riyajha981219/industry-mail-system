"""
Topic API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicResponse, TopicUpdate

router = APIRouter()

@router.post("/", response_model=TopicResponse, status_code=201)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    """Create a new topic"""
    db_topic = db.query(Topic).filter(Topic.name == topic.name).first()
    if db_topic:
        raise HTTPException(status_code=400, detail="Topic already exists")
    
    new_topic = Topic(**topic.model_dump())
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@router.get("/", response_model=List[TopicResponse])
def get_topics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all topics"""
    topics = db.query(Topic).filter(Topic.is_active == True).offset(skip).limit(limit).all()
    return topics

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get a specific topic"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: int, topic_update: TopicUpdate, db: Session = Depends(get_db)):
    """Update a topic"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    for key, value in topic_update.model_dump(exclude_unset=True).items():
        setattr(topic, key, value)
    
    db.commit()
    db.refresh(topic)
    return topic

@router.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """Delete a topic"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db.delete(topic)
    db.commit()
    return None
