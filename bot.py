import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 386263154

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
    
    await query.edit_message_text(text=f"Ответ записан! Спасибо!")
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 {name} ответил(а): {status}")

async def guests_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        text = "📋 Список:\n" + "\n".join(guests.values()) if guests else "Пока пусто"
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
