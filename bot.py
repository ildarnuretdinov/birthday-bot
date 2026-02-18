import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

# 🔥 Список администраторов — сюда можно добавлять ID через запятую
ADMINS = [386263154, 2032273338]

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не найден. Проверь переменные окружения Render.")

guests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("✅ Приду!", callback_data='yes'),
        InlineKeyboardButton("❌ Не смогу", callback_data='no')
    ]]

    text = (
        "🎉 Друзья, приглашаю вас на мой День Рождения!\n\n"
        "📅 Дата: 27 февраля\n"
        "⏰ Время: 19:00\n\n"
        "📍 Место: Кафе «Городок»\n"
        "🏙 Адрес: ул. Карла Маркса, 56, Калтасы\n\n"
        "Буду рада видеть вас! Придёте?"
    )

    # 🔥 1. Отправляем картинку
    await update.message.reply_photo(
        photo="https://i.imgur.com/0V8p6dC.jpeg"  # ← твоя картинка из Imgur
    )

    # 🔥 2. Отправляем текст + кнопки
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    name = f"{user.first_name} (@{user.username})" if user.username else user.first_name
    status = "✅ Придет" if query.data == 'yes' else "❌ Не придет"

    guests[user.id] = f"{status}: {name}"

    await query.edit_message_text(text="Ответ записан! Спасибо!")

    # 🔥 Отправляем уведомление всем администраторам
    for admin in ADMINS:
        await context.bot.send_message(
            chat_id=admin,
            text=f"🔔 {name} ответил(а): {status}"
        )

async def guests_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔥 Доступ к списку гостей для всех админов
    if update.effective_user.id in ADMINS:
        text = "📋 Список гостей:\n" + "\n".join(guests.values()) if guests else "Пока никто не ответил"
        await update.message.reply_text(text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("guests", guests_list))
    app.add_handler(CallbackQueryHandler(button))

    port = int(os.environ.get("PORT", 8443))

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
