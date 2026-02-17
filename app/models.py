from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    """Base schema for Post."""
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10, max_length=5000)
    author: Optional[str] = Field(None, min_length=2, max_length=50)

    @field_validator("title", "content", "author")
    @classmethod
    def strip_whitespace(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty or blank")
        return v


class PostCreate(PostBase):
    """Schema for creating a new Post."""
    pass


class Post(PostBase):
    """Schema for Post response."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    """Base schema for Comment."""
    content: str = Field(..., min_length=2, max_length=300)
    author: Optional[str] = Field(None, min_length=2, max_length=50)

    @field_validator("content", "author")
    @classmethod
    def strip_whitespace(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty or blank")
        return v


class CommentCreate(CommentBase):
    """Schema for creating a new Comment."""
    post_id: int = Field(..., ge=1)


class Comment(CommentBase):
    """Schema for Comment response."""
    id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
