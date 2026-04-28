from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.utils.constants import START_WELCOME

# Create a router for basic commands
base_router = Router(name="base_router")

@base_router.message(CommandStart())
async def cmd_start(message: Message):
    """Handler for the /start command."""
    welcome_text = START_WELCOME.format(name=message.from_user.first_name)
    await message.answer(welcome_text)

"""@base_router.message(F.text)
async def echo_handler(message: Message):
    # In the future, this is where we will pass the text to Natasha for extraction
    await message.answer(f"Echo: You want to add '{message.text}' to the list. (NLP processing coming soon!)")"""