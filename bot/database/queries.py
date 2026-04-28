import aiosqlite
from bot.config import config

async def add_item(user_id: int, item_name: str, category: str = "Pending") -> int:
    """Add a new item to the database."""
    async with aiosqlite.connect(config.db_path) as db:
        cursor = await db.execute(
            "INSERT INTO shopping_items (user_id, item_name, category) VALUES (?, ?, ?)",
            (user_id, item_name, category)
        )
        await db.commit()
        return cursor.lastrowid

async def get_unpurchased_items() -> list[dict]:
    """Retrieve all unpurchased items."""
    async with aiosqlite.connect(config.db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, item_name, category FROM shopping_items WHERE is_purchased = 0 ORDER BY created_at ASC"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def mark_item_purchased(item_id: int) -> None:
    """Mark a specific item as purchased."""
    async with aiosqlite.connect(config.db_path) as db:
        await db.execute(
            "UPDATE shopping_items SET is_purchased = 1 WHERE id = ?",
            (item_id,)
        )
        await db.commit()   