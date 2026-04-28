from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database import queries
from bot.keyboards.inline import build_shopping_keyboard, ItemCallback
from bot.utils import constants
from bot.services.nlp import extract_products
from aiogram import Bot
from bot.services.notifier import broadcast_addition

shopping_router = Router(name="shopping_router")

# React to both /list command AND the "🛒 Список покупок" button
@shopping_router.message(Command("list"))
@shopping_router.message(F.text == constants.BTN_LIST)
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
    await queries.mark_as_purchased(callback_data.item_id)
    await callback_query.answer(constants.PURCHASED_CONFIRM)
    items = await queries.get_shopping_list()
    
    if not items:
        await callback_query.message.edit_text(constants.ALL_PURCHASED)
    else:
        keyboard = build_shopping_keyboard(items)
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)


# IMPORTANT: This catch-all text handler MUST remain at the bottom 
# of this file so it doesn't intercept the button clicks!
@shopping_router.message(F.text & ~F.text.startswith('/'))
async def add_text_item(message: Message):
    """Save standard text to the database."""
    item_name = message.text.strip()
    user_id = message.from_user.id
    
    await queries.add_item(
        user_id=user_id, 
        item_name=item_name, 
        category=constants.DEFAULT_CATEGORY
    )

@shopping_router.message(F.text & ~F.text.startswith('/'))
async def add_text_item(message: Message):
    """Save standard text to the database using NLP extraction."""
    raw_text = message.text.strip()
    user_id = message.from_user.id
    
    # --- NLP MAGIC FOR TEXT ---
    products = extract_products(raw_text)
    
    # Save each extracted product separately
    for product in products:
        await queries.add_item(
            user_id=user_id, 
            item_name=product, 
            category=constants.DEFAULT_CATEGORY
        )
    added_items_str = ", ".join(products)
    await message.answer(constants.ITEM_ADDED.format(item_name=added_items_str))

@shopping_router.message(F.text & ~F.text.startswith('/'))
async def add_text_item(message: Message, bot: Bot):
    raw_text = message.text.strip()
    user = message.from_user
    
    # Защита от None
    if not user:
        return
        
    products = extract_products(raw_text)
    
    for product in products:
        await queries.add_item(
            user_id=user.id, 
            item_name=product, 
            category=constants.DEFAULT_CATEGORY,
            added_by=user.first_name
        )
    
    added_items_str = ", ".join(products)
    await message.answer(constants.ITEM_ADDED.format(item_name=added_items_str))
    
    # Broadcast to family
    await broadcast_addition(bot, user.id, user.first_name, products)