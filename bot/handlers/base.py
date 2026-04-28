from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.utils.constants import START_WELCOME, BTN_START
from bot.keyboards.reply import get_main_menu_keyboard
from bot.database import queries  # <-- Import queries



base_router = Router(name="base_router")

@base_router.message(CommandStart())
@base_router.message(F.text == BTN_START)
async def cmd_start(message: Message):
    """Handler for the /start command and Start button."""
    user = message.from_user
    
    # Защита от None (убирает ошибку линтера)
    if not user:
        return
    
    # Register the user in the database safely
    await queries.add_user(
        user_id=user.id,
        username=user.username or "unknown",  # Защита, если username скрыт
        first_name=user.first_name
    )
    
    welcome_text = START_WELCOME.format(name=user.first_name)
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())   