import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

# 🟢 دیتابیس ساده کاربران
USERS = {}

# 🔥 لیست گان‌ها
GUNS = ["AK-47","AK117","AN-94","AS VAL","CR-56 AMAX","FAMAS","FFAR","Grau 5.56","HBRa3",
        "ICR-1","Kilo 141","KN-44","LK24","M13","Man-O-War","Type 25","QBZ-95","XM4",
        "MSMC","PDW-57","Razorback","PP19 Bizon","GKS","MX9","VMP","CX-9","Striker 45","KSP-45",
        "DL Q33","Locus","Arctic .50","XPR-50","M21 EBR","NA-45","Outlaw","HDR",
        "SP-R 208","SKS","SVD","Type 63","Holger 26","Hades","UL736","Raal MG","MG 42",
        "R9-0","Striker","HS0405"]

PAGE_SIZE = 9

# 🟢 حذف پیام بعد از 60 ثانیه
async def auto_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    await asyncio.sleep(60)
    try:
        await context.bot.delete_message(chat_id, message_id)
    except:
        pass

# 🟢 کیبورد منوی اصلی
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 بتل (Battle)", callback_data="mode_battle")],
        [InlineKeyboardButton("⚡️ مولتی (Multiplayer)", callback_data="mode_multi")]
    ])

# 🟢 کیبورد گان‌ها
def guns_keyboard(page: int, mode: str):
    start, end = page * PAGE_SIZE, (page + 1) * PAGE_SIZE
    keyboard = [[InlineKeyboardButton(GUNS[i], callback_data=f"gun_{mode}_{GUNS[i]}")]
                for i in range(start, min(end, len(GUNS)))]
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"page_{mode}_{page-1}"))
    if end < len(GUNS): nav.append(InlineKeyboardButton("➡️ بعدی", callback_data=f"page_{mode}_{page+1}"))
    if nav: keyboard.append(nav)
    keyboard.append([InlineKeyboardButton("⬅️ بازگشت به منو", callback_data="back_menu")])
    return InlineKeyboardMarkup(keyboard)

# 🟢 ارسال منو
async def send_menu(chat, context):
    msg = await chat.send_message("👇 مود بازی رو انتخاب کن:", reply_markup=main_menu_keyboard())
    asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))

# 🟢 /start → ثبت‌نام خودکار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    username = update.message.from_user.username or f"user_{user_id}"

    if user_id not in USERS:
        USERS[user_id] = username
        await update.message.reply_text(f"✅ خوش آمدی {username}!\nثبت‌نامت انجام شد ✅")
    else:
        await update.message.reply_text(f"👋 خوش برگشتی {username}!")

    await send_menu(update.message.chat, context)

# 🟢 /help → راهنما
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📌 راهنمای ربات:

✅ /start → شروع و ثبت‌نام  
✅ /menu → بازگشت به منوی اصلی  
✅ /help → نمایش راهنما  

🎮 سپس از منوی اصلی مود بازی و گان رو انتخاب کن!
"""
    await update.message.reply_text(text)

# 🟢 /menu → بازگشت سریع به منوی اصلی
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_menu(update.message.chat, context)

# 🟢 مدیریت دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "back_menu":
        await q.edit_message_text("👇 منوی اصلی:", reply_markup=main_menu_keyboard())
        return

    if data.startswith("mode_"):
        mode = data.split("_")[1]
        await q.edit_message_text(f"🎮 مود {mode.upper()} انتخاب شد:\n🔫 حالا گان رو انتخاب کن:", reply_markup=guns_keyboard(0, mode))
        return

    if data.startswith("page_"):
        _, mode, page = data.split("_")
        await q.edit_message_text(f"🔫 صفحه {int(page)+1} از گان‌ها", reply_markup=guns_keyboard(int(page), mode))
        return

    if data.startswith("gun_"):
        _, mode, gun = data.split("_", 2)
        await q.edit_message_text(f"✅ گان انتخابی: {gun}\n🎮 مود: {mode.upper()}")
        return


# 🟢 اجرای ربات
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()