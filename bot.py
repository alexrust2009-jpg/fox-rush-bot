import asyncio
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
API_TOKEN = 'AAGIYRx3848sbH9nz3P_OnJoEjV9quZcrWI'
WEB_APP_URL = 'https://foxrush-2777e.web.app'

# Создаем мини-сайт, чтобы Render не ругался
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- БОТ ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🦊 Играть!", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Привет! Нажимай кнопку и играй:", reply_markup=markup)

async def main():
    # Запускаем "обманку" в отдельном потоке
    threading.Thread(target=run_flask).start()
    print("Бот и веб-заглушка запущены!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
