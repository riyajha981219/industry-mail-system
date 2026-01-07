"""
Subscription Database Model
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class FrequencyEnum(str, enum.Enum):
    DAILY = "1"
    WEEKLY = "7"
    MONTHLY = "30"

class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (UniqueConstraint('user_id', 'topic_id', name='uq_user_topic'),)
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    frequency = Column(Enum(FrequencyEnum), nullable=False, default=FrequencyEnum.DAILY)
    last_sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    topic = relationship("Topic", back_populates="subscriptions")
