import os
from aiogram import Router, F, Bot
from aiogram.types import Message

from bot.services.speech import transcribe_voice
from bot.services.nlp import extract_products  # <-- Import NLP
from bot.database import queries
from bot.utils import constants

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
    user_id = message.from_user.id
    
    # Save each extracted product as a separate item in the database
    for product in products:
        await queries.add_item(
            user_id=user_id,
            item_name=product,
            category=constants.DEFAULT_CATEGORY
        )
    
    # Format the extracted list for the user
    added_items_str = ", ".join(products)
    
    await processing_msg.edit_text(
        constants.VOICE_RECOGNIZED.format(
            text=recognized_text, 
            added_items=added_items_str
        )
    )