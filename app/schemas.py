from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field

# Feed Schemas
class FeedBase(BaseModel):
    url: str
    title: str
    description: Optional[str] = None

class FeedCreate(FeedBase):
    pass

class FeedUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class FeedInDB(FeedBase):
    id: int
    last_updated: Optional[datetime] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    link: str
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_at: datetime

class ArticleCreate(ArticleBase):
    feed_id: int

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    is_new: Optional[bool] = None

class ArticleInDB(ArticleBase):
    id: int
    feed_id: int
    feed: Optional[FeedInDB] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_new: bool

    class Config:
        from_attributes = True

# Response Schemas
class PaginatedResponse(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    items: List[ArticleInDB]

# Query Parameters
class ArticleQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    feed_id: Optional[int] = None
    search: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_new: Optional[bool] = None 