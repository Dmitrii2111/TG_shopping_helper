from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

# Define a strongly-typed callback factory
class BuyItemCallback(CallbackData, prefix="buy"):
    item_id: int

def get_shopping_list_keyboard(items: list[dict]) -> InlineKeyboardMarkup:
    """Generate an inline keyboard containing all unpurchased items."""
    builder = InlineKeyboardBuilder()
    
    for item in items:
        # Create a button for each item
        builder.button(
            text=f"🛒 {item['item_name']} ({item['category']})",
            callback_data=BuyItemCallback(item_id=item['id'])
        )
        
    # Stack buttons vertically (1 button per row)
    builder.adjust(1)
    return builder.as_markup()