from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.utils import constants

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Build and return the main menu reply keyboard."""
    builder = ReplyKeyboardBuilder()
    
    # Add buttons using constants
    builder.button(text=constants.BTN_START)
    builder.button(text=constants.BTN_LIST)
    
    # Adjust to 2 buttons per row
    builder.adjust(2)
    
    # resize_keyboard=True ensures it doesn't take up half the screen
    return builder.as_markup(resize_keyboard=True)