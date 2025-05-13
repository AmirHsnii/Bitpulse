from sqlmodel import SQLModel, create_engine, Session
from .core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create SQLite database engine
engine = create_engine(
    f"sqlite:///{settings.SQLITE_DB_PATH}",
    echo=False,
    connect_args={"check_same_thread": False}
)

def init_db():
    """Initialize the database by creating all tables."""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session 