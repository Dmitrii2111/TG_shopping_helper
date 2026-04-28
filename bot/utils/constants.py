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

# Voice processing messages
VOICE_PROCESSING = "⏳ Распознаю голосовое сообщение..."
VOICE_RECOGNIZED = "Распознано: <b>{text}</b>\nДобавлено в список!"
VOICE_ERROR = "❌ Не удалось распознать текст. Попробуйте сказать громче и четче."