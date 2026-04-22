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

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER (ЧТОБЫ НЕ ВЫКЛЮЧАЛСЯ) ---
app = Flask('')

@app.route('/')
def home():
    return "FoxRush is running 24/7!"

def run_flask():
    # Берем порт из настроек сервера или используем 10000 по умолчанию
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- НАСТРОЙКИ БОТА ---
# Замени на свои данные, если они еще не вписаны
API_TOKEN = 'ТВОЙ_ТОКЕН_ИЗ_BOTFATHER'
WEB_APP_URL = 'https://foxrush-2777e.web.app' 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- ОБРАБОТКА КОМАНДЫ /START ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем кнопку для запуска игры
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🦊 Запустить FoxRush!", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ])
    
    # Твой оригинальный текст приветствия
    await message.answer(
        f"🦊 Добро пожаловать в FoxRush, {message.from_user.first_name}!\n\n"
        "💨 Твоя скорость — твой капитал.\n"
        "Нажимай на кнопку ниже и начинай забег! 🚀",
        reply_markup=markup
    )

# --- ЗАПУСК ---
async def main():
    # Запускаем фоновый поток для проверки порта Render
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("--- СЕРВЕР ПРОВЕРКИ ПОРТА ЗАПУЩЕН ---")
    print("--- БОТ FOX RUSH В ЭФИРЕ ---")
    
    # Запуск бота в режиме бесконечного опроса
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
