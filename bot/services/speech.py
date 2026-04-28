import asyncio
import logging
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

# Initialize the model globally to load it into memory only once.
# "base" provides a great balance between speed and accuracy. 
# compute_type="int8" reduces CPU memory usage.
try:
    logger.info("Loading Faster-Whisper 'base' model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load Whisper model: {e}")
    model = None

def _transcribe_sync(file_path: str) -> str:
    """Synchronous function performing the heavy STT calculation."""
    if model is None:
        return ""
    
    # beam_size=5 slightly improves accuracy; language="ru" forces Russian
    segments, _ = model.transcribe(file_path, beam_size=5, language="ru")
    
    # Combine all transcribed segments into a single string
    text = " ".join([segment.text for segment in segments])
    return text.strip()

async def transcribe_voice(file_path: str) -> str:
    """Asynchronous wrapper to offload STT to a background thread."""
    try:
        # Run the blocking function in a separate thread so aiogram doesn't freeze
        text = await asyncio.to_thread(_transcribe_sync, file_path)
        return text
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return ""