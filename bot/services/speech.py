import asyncio
import logging
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

# Initialize the model globally so it's loaded only once.
# "tiny" is very fast but slightly less accurate. "base" is a great middle-ground.
# compute_type="int8" reduces memory usage on CPU.
try:
    logger.info("Loading Faster-Whisper model...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load Whisper model: {e}")
    model = None

def _transcribe_sync(file_path: str) -> str:
    """Synchronous function to perform the actual STT task."""
    if model is None:
        return ""
    
    # beam_size=5 improves accuracy slightly
    segments, info = model.transcribe(file_path, beam_size=5, language="ru")
    
    # Combine all speech segments into one string
    text = " ".join([segment.text for segment in segments])
    return text.strip()

async def transcribe_voice(file_path: str) -> str:
    """Asynchronous wrapper to run STT in a separate thread without blocking the bot."""
    try:
        # Offload the CPU-heavy blocking STT function to a thread
        text = await asyncio.to_thread(_transcribe_sync, file_path)
        return text
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return ""