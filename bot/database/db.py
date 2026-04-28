import aiosqlite
import logging
from bot.config import config

logger = logging.getLogger(__name__)

async def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    try:
        async with aiosqlite.connect(config.db_path) as db:
            # Added 'added_by' column
            await db.execute("""
                CREATE TABLE IF NOT EXISTS shopping_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    added_by TEXT,
                    item_name TEXT NOT NULL,
                    category TEXT,
                    is_purchased BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Updated 'users' table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
            logger.info(f"Database initialized successfully at '{config.db_path}'")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e