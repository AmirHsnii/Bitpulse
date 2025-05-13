from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import HttpUrl

class Feed(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(unique=True, index=True)
    title: str
    description: Optional[str] = None
    last_updated: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    feed_id: int = Field(foreign_key="feed.id")
    title: str
    link: str = Field(unique=True, index=True)
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    is_new: bool = Field(default=True)
    
    class Config:
        schema_extra = {
            "example": {
                "feed_id": 1,
                "title": "Bitcoin Reaches New All-Time High",
                "link": "https://example.com/bitcoin-news",
                "description": "Bitcoin has reached a new all-time high...",
                "content": "Full article content...",
                "author": "John Doe",
                "published_at": "2024-02-12T12:00:00Z",
                "is_new": True
            }
        } 