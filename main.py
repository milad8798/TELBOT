import telebot

TOKEN = "8252909254:AAF6Guzpm18fb3K8puNq4zp-eDBeYqOXCE4"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ربات روشن شد ✅")

print("Bot is running...")
bot.polling(none_stop=True)