
import logging
import datetime
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")

# Установим даты начала менструации
MENSTRUATION_START = datetime.date(2025, 5, 26)
MENSTRUATION_END = datetime.date(2025, 5, 31)

# Проверка, находится ли сегодня в фазе менструации
def is_menstruation():
    today = datetime.date.today()
    return MENSTRUATION_START <= today <= MENSTRUATION_END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет, я твой мягкий трекер привычек 🌸\n\n"
        "Я буду каждый день напоминать тебе о заботе о себе.\n"
        "Если ты в ПМС или менструации — будь особенно бережна к себе 💗"
    )

async def morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "☀️ Доброе утро! Вот мягкие привычки на сегодня:\n"
    msg += "- 💧 Стакан воды\n- 🌿 Что-то приятное\n- 🧘‍♀️ Лёгкая растяжка\n"
    if is_menstruation():
        msg += "\nСегодня нежная фаза — просто будь. Тебе можно всё 💗"
    await update.message.reply_text(msg)

async def evening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🌙 Добрый вечер!\n\n"
    msg += "Ты молодец, что прожила этот день.\n"
    if is_menstruation():
        msg += "Менструация всё ещё идёт, береги себя 🌸\n"
    msg += "Завтра снова напомню о заботе 💛"
    await update.message.reply_text(msg)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("morning", morning))
    app.add_handler(CommandHandler("evening", evening))

    print("Bot is running...")
    app.run_polling()
