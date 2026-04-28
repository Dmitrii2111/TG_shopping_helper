from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

# Create a router for basic commands
base_router = Router(name="base_router")

@base_router.message(CommandStart())
async def cmd_start(message: Message):
    """Handler for the /start command."""
    welcome_text = (
        f"Hello, {message.from_user.first_name}! 👋\n\n"
        "I am your Family Shopping Bot. I can help you manage your shopping list.\n"
        "Send me a text message with items to buy, or a voice message, and I will categorize them!"
    )
    await message.answer(welcome_text)

@base_router.message(F.text)
async def echo_handler(message: Message):
    """Temporary echo handler to catch text messages before NLP is implemented."""
    # In the future, this is where we will pass the text to Natasha for extraction
    await message.answer(f"Echo: You want to add '{message.text}' to the list. (NLP processing coming soon!)")