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
    return "I'm alive! FoxRush is running."

def run_flask():
    # Render передает номер порта через переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- НАСТРОЙКИ БОТА ---
API_TOKEN = '8675521925:AAGIYRx3848sbH9nz3P_OnJoEjV9quZcrWI'
WEB_APP_URL = 'https://foxrush-2777e.web.app'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработка команды /start
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
        f"Привет, {message.from_user.first_name}! 🦊\n\n"
        "Твой бот запущен на сервере 24/7. Нажимай кнопку и копи монеты!",
        reply_markup=markup
    )

# Основная функция запуска
async def main():
    # 1. Запускаем веб-сервер в отдельном потоке
    # Это нужно, чтобы Render видел открытый порт
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("--- ВЕБ-СЕРВЕР ЗАПУЩЕН ---")
    print("--- БОТ НАЧИНАЕТ ОПРОС ---")
    
    # 2. Запускаем самого бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
