import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ТВОИ ДАННЫЕ — ПРАВИЛЬНЫЕ!
TOKEN = '8582630303:AAFNxoRd_rhnaPL39MbwtmWM6oq6M7utjbo'
ADMIN_ID = 386263154

# Список гостей
guests = {}

# DEBUG — покажем что происходит
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приглашение"""
    keyboard = [
        [InlineKeyboardButton("🎉 ПРИДУ!", callback_data='coming')],
        [InlineKeyboardButton("❌ НЕ ПРИДУ", callback_data='not_coming')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎂 *ПРИГЛАШАЮ ТЕБЯ НА ДЕНЬ РОЖДЕНИЯ!*\n\n"
        "📅 *27 февраля 2026*\n"
        "🕐 *19:00*\n"
        "📍 *Кафе Городок ул. Карла Маркса, 56, Калтасы*\n\n"
        "*Нажмите кнопку для подтверждения!* 🎁",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    logger.info(f"✅ /start отправлен пользователю {update.effective_user.id}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🎯 ИСПРАВЛЕНИЕ — обработка кнопок"""
    query = update.callback_query
    logger.info(f"🔥 КНОПКА НАЖАТА: {query.data} от {query.from_user.first_name} (ID: {query.from_user.id})")
    
    # ОБЯЗАТЕЛЬНО ответить на callback
    await query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name or "Гость"
    status = query.data
    
    # Сохраняем ответ
    guests[user_id] = {
        'name': username,
        'status': '✅ ПРИДУ' if status == 'coming' else '❌ НЕ ПРИДУ'
    }
    
    emoji = '🎉' if status == 'coming' else '😢'
    await query.edit_message_text(
        f"{emoji} *СПАСИБО, {username}!*\n\n"
        f"✅ Ваш ответ: `{guests[user_id]['status']}`\n\n"
        f"🎈Жду тебя !",
        parse_mode='Markdown'
    )
    logger.info(f"✅ Сохранено гостей: {len(guests)}")

async def guests_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Список только для именинника"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 *Только для именинника!*", parse_mode='Markdown')
        return
    
    if not guests:
        await update.message.reply_text("📝 *Пока никто не ответил*", parse_mode='Markdown')
        return
    
    coming = []
    not_coming = []
    
    for user_id, data in guests.items():
        if data['status'] == '✅ ПРИДУ':
            coming.append(f"✅ {data['name']}")
        else:
            not_coming.append(f"❌ {data['name']}")
    
    text = f"📋 *ФИНАЛЬНЫЙ СПИСОК ГОСТЕЙ* ({len(guests)} ответов)\n\n"
    text += f"🎉 *ПРИДУТ* ({len(coming)} чел.):\n"
    text += "\n".join(coming[:20]) + "\n\n"
    text += f"😢 *НЕ ПРИДУТ* ({len(not_coming)} чел.):\n"
    text += "\n".join(not_coming[:20])
    
    await update.message.reply_text(text, parse_mode='Markdown')

def main():
    print("🚀 Запускаю бота для ДР...")
    print(f"🔑 Токен: {TOKEN[:20]}...")
    print(f"👑 Админ: {ADMIN_ID}")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("guests", guests_list))
    app.add_handler(CallbackQueryHandler(button_handler))  # ✅ КЛЮЧЕВОЙ!
    
    print("🎉 Бот готов! Напиши /start")
    print("📱 Смотри Terminal — там DEBUG!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
