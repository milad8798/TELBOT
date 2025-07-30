from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

# /start command
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("دکمه 1", callback_data='btn1')],
        [InlineKeyboardButton("دکمه 2", callback_data='btn2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("سلام! یکی از دکمه‌ها رو بزن:", reply_markup=reply_markup)

# Callback for buttons
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'btn1':
        query.edit_message_text("شما دکمه 1 رو زدید ✅")
    elif query.data == 'btn2':
        query.edit_message_text("شما دکمه 2 رو زدید ✅")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()