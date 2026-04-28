from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.utils.constants import START_WELCOME, BTN_START
from bot.keyboards.reply import get_main_menu_keyboard

base_router = Router(name="base_router")

# React to both /start command AND the "🚀 Старт" button
@base_router.message(CommandStart())
@base_router.message(F.text == BTN_START)
async def cmd_start(message: Message):
    """Handler for the /start command and Start button."""
    welcome_text = START_WELCOME.format(name=message.from_user.first_name)
    
    # Send the welcome message AND the persistent reply keyboard
    await message.answer(
        welcome_text, 
        reply_markup=get_main_menu_keyboard()
    )