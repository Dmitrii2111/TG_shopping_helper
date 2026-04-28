import os
from aiogram import Router, F, Bot
from aiogram.types import Message

from bot.services.speech import transcribe_voice
from bot.services.nlp import extract_products  # <-- Import NLP
from bot.database import queries
from bot.utils import constants
from bot.services.notifier import broadcast_addition

voice_router = Router(name="voice_router")
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@voice_router.message(F.voice)
async def handle_voice_message(message: Message, bot: Bot):
    processing_msg = await message.answer(constants.VOICE_PROCESSING)
    
    file_id = message.voice.file_id
    file_path = os.path.join(DOWNLOADS_DIR, f"{file_id}.ogg")
    
    await bot.download(message.voice, destination=file_path)
    recognized_text = await transcribe_voice(file_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    if not recognized_text:
        await processing_msg.edit_text(constants.VOICE_ERROR)
        return

    # --- NLP MAGIC HAPPENS HERE ---
    products = extract_products(recognized_text)
    user = message.from_user
    
    # Защита от None
    if not user:
        return
    
    for product in products:
        await queries.add_item(
            user_id=user.id,
            item_name=product,
            category=constants.DEFAULT_CATEGORY,
            added_by=user.first_name
        )
    
    added_items_str = ", ".join(products)
    await processing_msg.edit_text(
        constants.VOICE_RECOGNIZED.format(
            text=recognized_text, 
            added_items=added_items_str
        )
    )
    
    # Broadcast to family
    await broadcast_addition(bot, user.id, user.first_name, products)