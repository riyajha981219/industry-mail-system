"""
Subscription Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.subscription import FrequencyEnum

class SubscriptionBase(BaseModel):
    user_id: int
    topic_id: int
    frequency: FrequencyEnum

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    frequency: Optional[FrequencyEnum] = None

class SubscriptionResponse(SubscriptionBase):
    id: int
    last_sent_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
