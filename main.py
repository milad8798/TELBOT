import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("مولتی 1", callback_data="btn1")],
        [InlineKeyboardButton("بتل 2", callback_data="btn2")],
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مود دلخواه رو انتخاب کن:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"شما {query.data} رو زدی ✅")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()