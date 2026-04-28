import os
from aiogram import Router, F, Bot
from aiogram.types import Message

from bot.services.speech import transcribe_voice
from bot.database import queries
from bot.utils import constants

voice_router = Router(name="voice_router")

# Ensure the temporary downloads directory exists
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@voice_router.message(F.voice)
async def handle_voice_message(message: Message, bot: Bot):
    """Handle incoming voice messages."""
    # 1. Notify user that processing has started
    processing_msg = await message.answer(constants.VOICE_PROCESSING)
    
    # 2. Define path and download the voice file from Telegram
    file_id = message.voice.file_id
    file_path = os.path.join(DOWNLOADS_DIR, f"{file_id}.ogg")
    
    await bot.download(message.voice, destination=file_path)
    
    # 3. Transcribe the audio
    recognized_text = await transcribe_voice(file_path)
    
    # 4. Clean up the downloaded file to save disk space
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # 5. Handle empty or failed transcriptions
    if not recognized_text:
        await processing_msg.edit_text(constants.VOICE_ERROR)
        return

    # 6. Save the recognized text to the database as a single item
    # Note: Later, Natasha NLP will split "Milk and bread" into two separate items.
    # For now, it adds the whole phrase as one item.
    user_id = message.from_user.id
    await queries.add_item(
        user_id=user_id,
        item_name=recognized_text,
        category=constants.DEFAULT_CATEGORY
    )
    
    # 7. Edit the processing message with the success confirmation
    await processing_msg.edit_text(
        constants.VOICE_RECOGNIZED.format(text=recognized_text)
    )