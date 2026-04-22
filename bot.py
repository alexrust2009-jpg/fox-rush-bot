import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- НАСТРОЙКИ ---
API_TOKEN = '8675521925:AAGIYRx3848sbH9nz3P_OnJoEjV9quZcrWI'
# Твоя ссылка от Firebase (например, https://foxrush-2777e.web.app)
WEB_APP_URL = ' https://foxrush-2777e.web.app' 

# Логирование (помогает видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Получаем ID пригласившего из команды /start (если он есть)
    # Пример: /start 12345678 -> start_param будет "12345678"
    start_param = message.get_args()
    
    # Формируем URL для Web App с параметром реферала
    # Telegram передаст этот параметр в твой JS код (tg.initDataUnsafe.start_param)
    final_url = WEB_APP_URL
    if start_param:
        final_url += f"?startapp={start_param}"

    # Создаем кнопку, которая открывает Mini App
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(
        text="🦊 Запустить Fox Rush", 
        web_app=WebAppInfo(url=final_url)
    )
    markup.add(btn)

    # Приветственный текст
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 🦊\n\n"
        "Добро пожаловать в Fox Rush!\n"
        "Это игра, где твой лис добывает монеты, пока ты отдыхаешь.\n\n"
        "Нажимай на кнопку ниже, чтобы начать!"
    )

    await message.answer(welcome_text, reply_markup=markup)

if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)