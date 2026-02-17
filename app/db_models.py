from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class DBPost(Base):
    """SQLAlchemy model for Post table."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String(5000), nullable=False)
    author = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    comments = relationship("DBComment", back_populates="post", cascade="all, delete-orphan")


class DBComment(Base):
    """SQLAlchemy model for Comment table."""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(String(300), nullable=False)
    author = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship("DBPost", back_populates="comments")
