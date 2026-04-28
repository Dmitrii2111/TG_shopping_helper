import aiosqlite
from bot.config import config

async def add_item(user_id: int, item_name: str, category: str = "Pending") -> int:
    """Insert a new item into shopping_items."""
    async with aiosqlite.connect(config.db_path) as db:
        cursor = await db.execute(
            "INSERT INTO shopping_items (user_id, item_name, category) VALUES (?, ?, ?)",
            (user_id, item_name, category)
        )
        await db.commit()
        return cursor.lastrowid

async def get_shopping_list() -> list[dict]:
    """Select all items where is_purchased = 0."""
    async with aiosqlite.connect(config.db_path) as db:
        # This allows us to access columns by name (e.g., row['item_name'])
        db.row_factory = aiosqlite.Row 
        async with db.execute(
            "SELECT id, item_name, category FROM shopping_items WHERE is_purchased = 0 ORDER BY created_at ASC"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def mark_as_purchased(item_id: int) -> None:
    """Update is_purchased to 1 for a specific ID."""
    async with aiosqlite.connect(config.db_path) as db:
        await db.execute(
            "UPDATE shopping_items SET is_purchased = 1 WHERE id = ?",
            (item_id,)
        )
        await db.commit()