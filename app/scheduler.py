from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlmodel import Session
import logging
from .rss import RSSParser
from .db import engine
from .core.config import settings

logger = logging.getLogger(__name__)

class FeedScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.parser = None

    async def update_feeds_job(self):
        """Job to update all feeds."""
        try:
            with Session(engine) as session:
                if not self.parser:
                    self.parser = RSSParser(session)
                
                new_articles = await self.parser.update_feeds()
                if new_articles > 0:
                    logger.info(f"Added {new_articles} new articles")
                
                # Mark old articles as not new
                old_count = self.parser.mark_old_articles(session)
                if old_count > 0:
                    logger.info(f"Marked {old_count} articles as not new")
        
        except Exception as e:
            logger.error(f"Error in update_feeds_job: {e}")

    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.add_job(
                self.update_feeds_job,
                trigger=IntervalTrigger(
                    minutes=settings.RSS_UPDATE_INTERVAL_MINUTES
                ),
                id='update_feeds',
                replace_existing=True
            )
            self.scheduler.start()
            logger.info("Feed scheduler started")

    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Feed scheduler shutdown")

# Create global scheduler instance
scheduler = FeedScheduler() 