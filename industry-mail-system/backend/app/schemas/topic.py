"""
Topic Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None
    keywords: str

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    is_active: Optional[bool] = None

class TopicResponse(TopicBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
