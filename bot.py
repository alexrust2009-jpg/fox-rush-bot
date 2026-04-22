import asyncio
import os
import threading
import logging
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ЛОГОВ ---
logging.basicConfig(level=logging.INFO)

# --- ПРИТВОРЯЕМСЯ САЙТОМ ДЛЯ RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "FoxRush is running 24/7!"

def run_flask():
    # Render передает номер порта через переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    # use_reloader=False критически важен для стабильности на Render
    app.run(host='0.0.0.0', port=port, use_reloader=False)

# --- НАСТРОЙКИ БОТА ---
# Вставь сюда свой токен и ссылку
API_TOKEN = '8675521925:AAGIYRx3848sbH9nz3P_OnJoEjV9quZcrWI'
WEB_APP_URL = 'https://foxrush-2777e.web.app' 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ОБРАБОТКА КОМАНДЫ /START ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🦊 Запустить FoxRush!", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])
    
    await message.answer(
        f"🦊 Добро пожаловать в FoxRush, {message.from_user.first_name}!\n\n"
        "💨 Твоя скорость — твой капитал.\n"
        "Нажимай на кнопку ниже и начинай забег! 🚀",
        reply_markup=markup
    )

# --- ГЛАВНАЯ ФУНКЦИЯ ---
async def main():
    # Запускаем Flask в фоновом потоке
    threading.Thread(target=run_flask, daemon=True).start()
    
    logging.info("--- ВЕБ-СЕРВЕР ЗАПУЩЕН ---")
    logging.info("--- БОТ НАЧИНАЕТ ОПРОС ---")
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
