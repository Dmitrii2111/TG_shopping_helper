from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot.utils.constants import ITEM_BUTTON_FORMAT

class ItemCallback(CallbackData, prefix="buy"):
    item_id: int

def build_shopping_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    """Generate an inline keyboard for unpurchased items."""
    builder = InlineKeyboardBuilder()
    
    for item in items:
        # Format the button text dynamically using constants
        button_text = ITEM_BUTTON_FORMAT.format(
            item_name=item['item_name'], 
            category=item['category']
        )
        
        builder.button(
            text=button_text,
            callback_data=ItemCallback(item_id=item['id'])
        )
        
    builder.adjust(1)
    return builder.as_markup()