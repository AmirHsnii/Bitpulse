from typing import List, Optional, Tuple
from sqlmodel import Session, select, or_, and_
from datetime import datetime, timedelta
from .models import Feed, Article
from .schemas import ArticleQueryParams

def create_feed(session: Session, feed: Feed) -> Feed:
    """Create a new feed."""
    session.add(feed)
    session.commit()
    session.refresh(feed)
    return feed

def get_feed(session: Session, feed_id: int) -> Optional[Feed]:
    """Get a feed by ID."""
    return session.get(Feed, feed_id)

def get_feed_by_url(session: Session, url: str) -> Optional[Feed]:
    """Get a feed by URL."""
    statement = select(Feed).where(Feed.url == url)
    return session.exec(statement).first()

def get_feeds(session: Session, skip: int = 0, limit: int = 100) -> List[Feed]:
    """Get all feeds with pagination."""
    statement = select(Feed).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_feed(session: Session, feed_id: int, feed_data: dict) -> Optional[Feed]:
    """Update a feed."""
    feed = get_feed(session, feed_id)
    if feed:
        for key, value in feed_data.items():
            setattr(feed, key, value)
        session.add(feed)
        session.commit()
        session.refresh(feed)
    return feed

def delete_feed(session: Session, feed_id: int) -> bool:
    """Delete a feed."""
    feed = get_feed(session, feed_id)
    if feed:
        session.delete(feed)
        session.commit()
        return True
    return False

def create_article(session: Session, article: Article) -> Article:
    """Create a new article."""
    session.add(article)
    session.commit()
    session.refresh(article)
    return article

def get_article(session: Session, article_id: int) -> Optional[Article]:
    """Get an article by ID."""
    return session.get(Article, article_id)

def get_article_by_link(session: Session, link: str) -> Optional[Article]:
    """Get an article by link."""
    statement = select(Article).where(Article.link == link)
    return session.exec(statement).first()

def get_articles(
    session: Session,
    params: ArticleQueryParams
) -> Tuple[List[Article], int]:
    """Get articles with filtering and pagination."""
    # Build base query
    statement = select(Article)
    
    # Apply filters
    if params.feed_id:
        statement = statement.where(Article.feed_id == params.feed_id)
    
    if params.search:
        search_term = f"%{params.search}%"
        statement = statement.where(
            or_(
                Article.title.ilike(search_term),
                Article.description.ilike(search_term),
                Article.content.ilike(search_term)
            )
        )
    
    if params.start_date:
        statement = statement.where(Article.published_at >= params.start_date)
    
    if params.end_date:
        statement = statement.where(Article.published_at <= params.end_date)
    
    if params.is_new is not None:
        statement = statement.where(Article.is_new == params.is_new)
    
    # Get total count
    count_statement = select(Article).where(statement.whereclause)
    total = len(session.exec(count_statement).all())
    
    # Apply pagination
    statement = statement.offset((params.page - 1) * params.size).limit(params.size)
    
    # Order by published_at descending
    statement = statement.order_by(Article.published_at.desc())
    
    return session.exec(statement).all(), total

def update_article(session: Session, article_id: int, article_data: dict) -> Optional[Article]:
    """Update an article."""
    article = get_article(session, article_id)
    if article:
        for key, value in article_data.items():
            setattr(article, key, value)
        article.updated_at = datetime.utcnow()
        session.add(article)
        session.commit()
        session.refresh(article)
    return article

def mark_old_articles(session: Session, hours: int = 24) -> int:
    """Mark articles older than specified hours as not new."""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    statement = select(Article).where(
        and_(
            Article.is_new == True,
            Article.published_at < cutoff_time
        )
    )
    articles = session.exec(statement).all()
    for article in articles:
        article.is_new = False
        session.add(article)
    session.commit()
    return len(articles) 