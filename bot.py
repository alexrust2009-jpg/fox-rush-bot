import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
# Вставь сюда свой токен, который дал @BotFather
API_TOKEN = '8675521925:AAGIYRx3848sbH9nz3P_OnJoEjV9quZcrWI'

# Вставь сюда ссылку, которую ты получил после 'firebase deploy'
WEB_APP_URL = 'https://foxrush-2777e.web.app' 

# Включаем логирование, чтобы видеть ошибки в терминале
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем кнопку, которая открывает Web App (твою игру)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🦊 Запустить FoxRush!", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])
    
    # Отправляем приветственное сообщение с кнопкой
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🦊\n\n"
        "Добро пожаловать в FoxRush! Твоя скорость — твой капитал.\n"
        "Нажимай на кнопку ниже, чтобы начать собирать монеты!",
        reply_markup=markup
    )

# Основная функция запуска
async def main():
    print("--- БОТ ЗАПУЩЕН ---")
    print(f"Ссылка на игру: {WEB_APP_URL}")
    print("Нажми Ctrl+C в терминале, чтобы остановить бота.")
    
    # Запуск процесса опроса новых сообщений
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
