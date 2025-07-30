import telebot

TOKEN = "8384449381:AAG2t91OlgL6puuZ17JNYHsdKXgkBtnAXMk"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ربات روشن شد ✅")

print("Bot is running...")
bot.polling(none_stop=True)