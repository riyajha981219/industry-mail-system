"""
Subscription API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.subscription import Subscription
from app.models.user import User
from app.models.topic import Topic
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate

router = APIRouter()

@router.post("/", response_model=SubscriptionResponse, status_code=201)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create a new subscription"""
    # Verify user exists
    user = db.query(User).filter(User.id == subscription.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == subscription.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Check if subscription already exists
    existing = db.query(Subscription).filter(
        Subscription.user_id == subscription.user_id,
        Subscription.topic_id == subscription.topic_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Subscription already exists")
    
    new_subscription = Subscription(**subscription.model_dump())
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

@router.get("/", response_model=List[SubscriptionResponse])
def get_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all subscriptions"""
    subscriptions = db.query(Subscription).offset(skip).limit(limit).all()
    return subscriptions

@router.get("/user/{user_id}", response_model=List[SubscriptionResponse])
def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    """Get all subscriptions for a specific user"""
    subscriptions = db.query(Subscription).filter(Subscription.user_id == user_id).all()
    return subscriptions

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Get a specific subscription"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(subscription_id: int, subscription_update: SubscriptionUpdate, db: Session = Depends(get_db)):
    """Update a subscription"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    for key, value in subscription_update.model_dump(exclude_unset=True).items():
        setattr(subscription, key, value)
    
    db.commit()
    db.refresh(subscription)
    return subscription

@router.delete("/{subscription_id}", status_code=204)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Delete a subscription"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    return None
