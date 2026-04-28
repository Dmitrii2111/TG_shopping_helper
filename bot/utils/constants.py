# Welcome message for the /start command. We will use .format(name=...) to inject the user's name.
START_WELCOME = (
    "Привет, {name}! 👋\n\n"
    "Я твой семейный помощник для покупок. "
    "Присылай мне названия товаров текстом или голосом, и я добавлю их в список."
)

# Shopping list messages
EMPTY_LIST = "🛒 Список пока пуст!"
LIST_HEADER = "🛒 <b>Список покупок:</b>\n<i>Нажми на товар, чтобы отметить его как купленный.</i>"
ALL_PURCHASED = "🛒 Все товары куплены! 🎉"

# Confirmation messages
ITEM_ADDED = "✅ Добавлено: <b>{item_name}</b>"
PURCHASED_CONFIRM = "Куплено! ✅"

# Defaults & Button formats
DEFAULT_CATEGORY = "Без категории"
ITEM_BUTTON_FORMAT = "🛒 {item_name} ({category})"

# ... existing constants ...
VOICE_PROCESSING = "⏳ Обрабатываю голосовое сообщение..."
# Updated to show what was extracted:
VOICE_RECOGNIZED = "🎙 Распознано: <i>{text}</i>\n✅ Добавлено: <b>{added_items}</b>"
VOICE_ERROR = "❌ Не удалось распознать текст. Попробуйте сказать четче."

# Reply Keyboard Buttons
BTN_START = "🚀 Старт"
BTN_LIST = "🛒 Список покупок"