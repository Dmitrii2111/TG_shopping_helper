import logging
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from bot.database import queries
from bot.utils import constants

logger = logging.getLogger(__name__)

async def broadcast_addition(bot: Bot, sender_id: int, sender_name: str, items_list: list[str]):
    """Send a notification to all family members except the sender."""
    if not items_list:
        return
        
    users = await queries.get_all_users()
    
    # Format items as a bulleted list
    items_str = "\n".join([f"• {item}" for item in items_list])
    
    message_text = constants.MSG_ADDITION_NOTIFICATION.format(
        user_name=sender_name,
        items=items_str
    )

    for user_id in users:
        if user_id != sender_id:
            try:
                await bot.send_message(chat_id=user_id, text=message_text)
            except TelegramAPIError as e:
                logger.error(f"Failed to send notification to {user_id}: {e}")