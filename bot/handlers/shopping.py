from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database import queries
from bot.keyboards.inline import get_shopping_list_keyboard, BuyItemCallback

shopping_router = Router(name="shopping_router")

@shopping_router.message(Command("list"))
async def cmd_list(message: Message):
    """Display the current shopping list."""
    items = await queries.get_unpurchased_items()
    
    if not items:
        await message.answer("🛒 The shopping list is currently empty!")
        return
    
    keyboard = get_shopping_list_keyboard(items)
    await message.answer("🛒 <b>Shopping List:</b>\n<i>Click an item to mark it as purchased.</i>", reply_markup=keyboard)


@shopping_router.callback_query(BuyItemCallback.filter())
async def process_buy_item(callback_query: CallbackQuery, callback_data: BuyItemCallback):
    """Handle clicks on the inline keyboard items."""
    # 1. Mark the item as purchased in DB
    await queries.mark_item_purchased(callback_data.item_id)
    
    # 2. Answer the callback to dismiss the loading state on the user's client
    await callback_query.answer("Item marked as purchased! ✅")
    
    # 3. Fetch the updated list
    items = await queries.get_unpurchased_items()
    
    # 4. Update the message inline
    if not items:
        await callback_query.message.edit_text("🛒 All items have been purchased! 🎉")
    else:
        keyboard = get_shopping_list_keyboard(items)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)


@shopping_router.message(F.text & ~F.text.startswith('/'))
async def add_item_handler(message: Message):
    """Catch plain text messages and add them to the list."""
    item_name = message.text.strip()
    user_id = message.from_user.id
    
    await queries.add_item(user_id=user_id, item_name=item_name, category="Pending")
    
    await message.answer(
        f"✅ Added <b>{item_name}</b> to the list.\n"
        f"<i>Category: Pending</i>"
    )