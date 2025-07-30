import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

# 🟢 تابع حذف پیام بعد از 60 ثانیه
async def auto_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    await asyncio.sleep(60)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.warning(f"خطا در حذف پیام: {e}")

# 🟢 دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("بتل ", callback_data="btn1")],
        [InlineKeyboardButton("مولتی ", callback_data="btn2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = await update.message.reply_text("سلام! یکی از دکمه‌ها رو انتخاب کن:", reply_markup=reply_markup)

    # حذف پیام بعد از 60 ثانیه
    asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))

# 🟢 هندلر دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # ویرایش متن پیام (پیام اصلی دکمه‌ها)
    await query.edit_message_text(f"شما {query.data} رو زدی ✅")

    # حذف پیام ویرایش‌شده بعد از 60 ثانیه
    asyncio.create_task(auto_delete(context, query.message.chat_id, query.message.message_id))

# 🟢 اجرای ربات
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()