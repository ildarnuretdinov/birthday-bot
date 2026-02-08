python
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

--- ВСТАВЬ СВОИ ДАННЫЕ ТУТ ---
TOKEN = '8582630303:AAHKku6RbbgSu7SzRid69gMlwTEKTMb7__k'
ADMIN_ID = 386263154  # Твой ID цифрами
------------------------------

logging.basicConfig(level=logging.INFO)
guests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("✅ Приду!", callback_data='yes'),
        InlineKeyboardButton("❌ Не смогу", callback_data='no')
    ]]
    await update.message.reply_text(
        "🎂 Приглашаю тебя на мой ДР!\n27 февраля, 19:00, Кафе 'Городок'.\n\nПридёшь?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    name = f"{user.first_name} (@{user.username})" if user.username else user.first_name
    
    status = "✅ Придет" if query.data == 'yes' else "❌ Не придет"
    guests[user.id] = f"{status}: {name}"
    
    await query.edit_message_text(text=f"Ответ записан: {status}. Спасибо!")
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
    app.run_polling()

if __name__ == '__main__':
    main()
