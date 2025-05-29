
import os
import datetime
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Примерная дата начала цикла
CYCLE_START = datetime.date(2025, 5, 26)

def get_cycle_phase():
    today = datetime.date.today()
    days_since = (today - CYCLE_START).days % 28
    if days_since < 5:
        return "Менструация 🌧️"
    elif days_since < 14:
        return "Фолликулярная фаза 🌱"
    elif days_since < 17:
        return "Овуляция 🌸"
    else:
        return "Лютеиновая фаза 🌙"

# Кнопки главного меню
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("📋 Утренние привычки"))
main_kb.add(KeyboardButton("🌙 Вечерние итоги"))
main_kb.add(KeyboardButton("🧠 Настроение"))
main_kb.add(KeyboardButton("📆 Фаза цикла"))

# Кнопки для настроения
mood_kb = ReplyKeyboardMarkup(resize_keyboard=True)
mood_kb.add("😊 Хорошо", "😐 Нормально", "😣 Плохо")
mood_kb.add("🔁 Назад в меню")

user_mood_log = {}

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Привет, я твой мягкий трекер привычек 🌸\n"
                         "Я помогу тебе заботиться о себе каждый день.
"
                         "Выбирай, с чего начнём:", reply_markup=main_kb)

@dp.message_handler(Text(equals="📋 Утренние привычки"))
async def morning(message: types.Message):
    await message.answer("Доброе утро ☀️\n\nСегодня ты можешь:
"
                         "– Сделать глоток воды
"
                         "– Потянуться в постели
"
                         "– Позавтракать вкусно и без спешки

"
                         "Ты уже молодец просто потому, что проснулась 💗")

@dp.message_handler(Text(equals="🌙 Вечерние итоги"))
async def evening(message: types.Message):
    await message.answer("Добрый вечер 🌙\n\nВспомни, что хорошего было сегодня.
"
                         "Если день был тяжёлый — ты всё равно с ним справилась 💫\n"
                         "Пусть сон будет спокойным. Ты заслуживаешь отдыха 🛏️")

@dp.message_handler(Text(equals="📆 Фаза цикла"))
async def cycle_phase(message: types.Message):
    phase = get_cycle_phase()
    await message.answer(f"Сейчас у тебя: {phase}
"
                         "Будь особенно бережна к себе 🌷")

@dp.message_handler(Text(equals="🧠 Настроение"))
async def mood_request(message: types.Message):
    await message.answer("Как ты себя чувствуешь сейчас?", reply_markup=mood_kb)

@dp.message_handler(Text(startswith="😊"))
@dp.message_handler(Text(startswith="😐"))
@dp.message_handler(Text(startswith="😣"))
async def log_mood(message: types.Message):
    user_id = message.from_user.id
    mood = message.text
    date = datetime.date.today().isoformat()
    user_mood_log.setdefault(user_id, {})[date] = mood
    await message.answer("Я записала твоё настроение 💖", reply_markup=main_kb)

@dp.message_handler(Text(equals="🔁 Назад в меню"))
async def back_to_menu(message: types.Message):
    await message.answer("Возвращаемся в меню 🌀", reply_markup=main_kb)

if __name__ == '__main__':
    executor.start_polling(dp)
