from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class Post(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10, max_length=5000)
    author: Optional[str] = Field(None, min_length=2, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("title", "content", "author")
    @classmethod
    def strip_whitespace(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty or blank")
        return v


class Comment(BaseModel):
    id: int = Field(..., ge=1)
    post_id: int = Field(..., ge=1)
    content: str = Field(..., min_length=2, max_length=300)
    author: Optional[str] = Field(None, min_length=2, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("content", "author")
    @classmethod
    def strip_whitespace(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty or blank")
        return v
