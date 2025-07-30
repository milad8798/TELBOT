from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

# توکن رباتت رو اینجا بزار
TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("👋 سلام", callback_data='hello')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("ربات روشنه ✅", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"شما زدید: {query.data}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()