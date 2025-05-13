import asyncio
import feedparser
import httpx
from datetime import datetime, timedelta
import pytz
from typing import List, Optional, Dict, Any
import logging
from .models import Feed, Article
from .core.config import settings
from sqlmodel import select
import re

logger = logging.getLogger(__name__)

class RSSParser:
    def __init__(self, session):
        self.session = session
        self.timezone = pytz.timezone(settings.DEFAULT_TIMEZONE)
        self.semaphore = asyncio.Semaphore(settings.RSS_MAX_CONCURRENT_REQUESTS)

    async def fetch_feed(self, feed: Feed) -> Optional[Dict[str, Any]]:
        """Fetch and parse a single feed."""
        try:
            async with self.semaphore:
                async with httpx.AsyncClient(timeout=settings.RSS_REQUEST_TIMEOUT) as client:
                    response = await client.get(feed.url)
                    response.raise_for_status()
                    return feedparser.parse(response.text)
        except Exception as e:
            logger.error(f"Error fetching feed {feed.url}: {e}")
            return None

    def parse_entry(self, entry: Dict[str, Any], feed_id: int) -> Optional[Article]:
        """Parse a single feed entry into an Article."""
        try:
            # Extract published date
            published = entry.get('published_parsed') or entry.get('updated_parsed')
            if published:
                published_dt = datetime(*published[:6])
                published_dt = pytz.UTC.localize(published_dt)
                published_dt = published_dt.astimezone(self.timezone)
            else:
                published_dt = datetime.now(self.timezone)

            # Extract content
            content = None
            if 'content' in entry:
                content = entry.content[0].value
            elif 'summary' in entry:
                content = entry.summary

            # Clean description
            description = entry.get('description')
            if description:
                description = clean_html(description)

            return Article(
                feed_id=feed_id,
                title=entry.title,
                link=entry.link,
                description=description,
                content=content,
                author=entry.get('author'),
                published_at=published_dt,
                is_new=True
            )
        except Exception as e:
            logger.error(f"Error parsing entry: {e}")
            return None

    async def process_feed(self, feed: Feed) -> List[Article]:
        """Process a single feed and return new articles."""
        parsed = await self.fetch_feed(feed)
        if not parsed:
            return []

        new_articles = []
        # Only process the 20 latest entries
        for entry in parsed.entries[:20]:
            article = self.parse_entry(entry, feed.id)
            if not article:
                logger.warning(f"Could not parse entry: {entry.get('title', 'No Title')}")
            else:
                # Check if article already exists by link OR (title and published_at)
                existing = self.session.exec(
                    select(Article).where(
                        (Article.link == article.link) |
                        ((Article.title == article.title) & (Article.published_at == article.published_at))
                    )
                ).first()
                if not existing:
                    new_articles.append(article)

        # Update feed metadata
        feed.title = parsed.feed.get('title', feed.title)
        feed.description = parsed.feed.get('description', feed.description)
        feed.last_updated = datetime.now(self.timezone)
        self.session.add(feed)
        
        # Save all new articles
        for article in new_articles:
            self.session.add(article)
        self.session.commit()

        return new_articles

    async def update_feeds(self) -> int:
        """Update all active feeds and return number of new articles."""
        feeds = self.session.exec(
            select(Feed).where(Feed.is_active == True)
        ).all()

        if not feeds:
            return 0

        tasks = [self.process_feed(feed) for feed in feeds]
        results = await asyncio.gather(*tasks)
        
        new_articles = []
        for articles in results:
            new_articles.extend(articles)

        # Save all new articles
        for article in new_articles:
            self.session.add(article)
        
        self.session.commit()
        return len(new_articles)

    def mark_old_articles(self, session):
        from .models import Article
        threshold = datetime.utcnow() - timedelta(hours=24)
        articles = session.exec(
            select(Article).where(Article.published_at < threshold, Article.is_new == True)
        ).all()
        for article in articles:
            article.is_new = False
            session.add(article)
        session.commit()
        return len(articles)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext 