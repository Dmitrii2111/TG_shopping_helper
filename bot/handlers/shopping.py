from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database import queries
from bot.keyboards.inline import build_shopping_keyboard, ItemCallback
from bot.utils import constants

shopping_router = Router(name="shopping_router")

@shopping_router.message(Command("list"))
async def cmd_list(message: Message):
    """Fetch items and display them using an Inline Keyboard."""
    items = await queries.get_shopping_list()
    
    if not items:
        await message.answer(constants.EMPTY_LIST)
        return
    
    keyboard = build_shopping_keyboard(items)
    await message.answer(constants.LIST_HEADER, reply_markup=keyboard)

@shopping_router.callback_query(ItemCallback.filter())
async def process_item_purchase(callback_query: CallbackQuery, callback_data: ItemCallback):
    """When a user clicks an item button, call mark_as_purchased and edit the message."""
    # 1. Update database
    await queries.mark_as_purchased(callback_data.item_id)
    
    # 2. Answer callback alert
    await callback_query.answer(constants.PURCHASED_CONFIRM)
    
    # 3. Fetch the updated list
    items = await queries.get_shopping_list()
    
    # 4. Edit the existing message
    if not items:
        await callback_query.message.edit_text(constants.ALL_PURCHASED)
    else:
        keyboard = build_shopping_keyboard(items)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)

@shopping_router.message(F.text & ~F.text.startswith('/'))
async def add_text_item(message: Message):
    """Save standard text to the database."""
    item_name = message.text.strip()
    user_id = message.from_user.id
    
    # Insert new item using the default category constant
    await queries.add_item(
        user_id=user_id, 
        item_name=item_name, 
        category=constants.DEFAULT_CATEGORY
    )
    
    # Format the confirmation message
    await message.answer(constants.ITEM_ADDED.format(item_name=item_name))