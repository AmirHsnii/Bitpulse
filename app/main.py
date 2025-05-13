from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, col
from typing import List, Optional
import json
import logging
from datetime import datetime, timedelta
from celery import Celery
from celery.schedules import crontab

from .db import get_session, init_db, engine
from .models import Feed, Article
from .schemas import (
    FeedCreate, FeedUpdate, FeedInDB,
    ArticleCreate, ArticleUpdate, ArticleInDB,
    ArticleQueryParams, PaginatedResponse
)
from .crud import (
    create_feed, get_feed, get_feeds, update_feed, delete_feed,
    create_article, get_article, get_articles, update_article
)
from .core.config import settings
from .scheduler import scheduler
from .rss import RSSParser

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    BitPulse - Persian Crypto RSS Aggregator
    
    بیت‌پالس - تجمیع‌کننده خوراک‌های رمزارزی
    """,
    openapi_tags=[
        {
            "name": "feeds",
            "description": "Operations with RSS feeds",
        },
        {
            "name": "articles",
            "description": "Operations with articles",
        },
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

manager = ConnectionManager()

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    init_db()
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()

# WebSocket endpoint
@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Feed endpoints
@app.post("/feeds", response_model=FeedInDB, tags=["feeds"])
def create_feed_endpoint(
    feed: FeedCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """Create a new RSS feed and fetch articles immediately."""
    db_feed = Feed(**feed.dict())
    created_feed = create_feed(session, db_feed)

    # Add background task to fetch articles for this feed
    def fetch_articles_for_feed(feed_id):
        with Session(engine) as s:
            parser = RSSParser(s)
            feed_obj = get_feed(s, feed_id)
            if feed_obj:
                import asyncio
                asyncio.run(parser.process_feed(feed_obj))
            s.commit()

    background_tasks.add_task(fetch_articles_for_feed, created_feed.id)
    return created_feed

@app.get("/feeds", response_model=List[FeedInDB], tags=["feeds"])
def read_feeds(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all feeds."""
    return get_feeds(session, skip=skip, limit=limit)

@app.get("/feeds/{feed_id}", response_model=FeedInDB, tags=["feeds"])
def read_feed(feed_id: int, session: Session = Depends(get_session)):
    """Get a specific feed."""
    db_feed = get_feed(session, feed_id)
    if not db_feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return db_feed

@app.put("/feeds/{feed_id}", response_model=FeedInDB, tags=["feeds"])
def update_feed_endpoint(
    feed_id: int,
    feed: FeedUpdate,
    session: Session = Depends(get_session)
):
    """Update a feed."""
    db_feed = update_feed(session, feed_id, feed.dict(exclude_unset=True))
    if not db_feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return db_feed

@app.delete("/feeds/{feed_id}", tags=["feeds"])
def delete_feed_endpoint(feed_id: int, session: Session = Depends(get_session)):
    """Delete a feed."""
    success = delete_feed(session, feed_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feed not found")
    return {"message": "Feed deleted successfully"}

# Article endpoints
@app.get("/articles", response_model=PaginatedResponse, tags=["articles"])
def read_articles(
    params: ArticleQueryParams = Depends(),
    session: Session = Depends(get_session)
):
    # Build the base query with filters
    base_statement = select(Article, Feed).join(Feed, Article.feed_id == Feed.id)
    # (Apply filters from params here as needed)

    # Get total count (without pagination)
    count_statement = select(Article).join(Feed, Article.feed_id == Feed.id)
    total = len(session.exec(count_statement).all())

    # Pagination
    statement = base_statement.offset((params.page - 1) * params.size).limit(params.size)
    # Order by published_at descending
    statement = statement.order_by(Article.published_at.desc())

    results = session.exec(statement).all()
    articles = []
    for article, feed in results:
        article_data = ArticleInDB.model_validate(article)
        article_data.feed = FeedInDB.model_validate(feed)
        articles.append(article_data)

    return PaginatedResponse(
        total=total,
        page=params.page,
        size=params.size,
        pages=(total + params.size - 1) // params.size,
        items=articles
    )

@app.get("/articles/{article_id}", response_model=ArticleInDB, tags=["articles"])
def read_article(article_id: int, session: Session = Depends(get_session)):
    """Get a specific article."""
    db_article = get_article(session, article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.put("/articles/{article_id}", response_model=ArticleInDB, tags=["articles"])
def update_article_endpoint(
    article_id: int,
    article: ArticleUpdate,
    session: Session = Depends(get_session)
):
    """Update an article."""
    db_article = update_article(session, article_id, article.dict(exclude_unset=True))
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

def cleanup_old_articles():
    from sqlmodel import Session
    from .models import Article
    from .db import engine
    from datetime import datetime, timedelta
    with Session(engine) as session:
        cutoff = datetime.utcnow() - timedelta(days=20)
        session.exec(
            select(Article).where(Article.published_at < cutoff)
        ).delete()
        session.commit() 