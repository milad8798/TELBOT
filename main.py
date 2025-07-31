import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

# 🟢 دیتابیس ساده کاربران (نام کاربری و پسورد)
USERS = {}
LOGGED_IN = set()

# 🔥 لیست گان‌ها
GUNS = ["AK-47","AK117","AN-94","AS VAL","CR-56 AMAX","FAMAS","FFAR","Grau 5.56","HBRa3",
        "ICR-1","Kilo 141","KN-44","LK24","M13","Man-O-War","Type 25","QBZ-95","XM4",
        "MSMC","PDW-57","Razorback","PP19 Bizon","GKS","MX9","VMP","CX-9","Striker 45","KSP-45",
        "DL Q33","Locus","Arctic .50","XPR-50","M21 EBR","NA-45","Outlaw","HDR",
        "SP-R 208","SKS","SVD","Type 63","Holger 26","Hades","UL736","Raal MG","MG 42",
        "R9-0","Striker","HS0405"]

PAGE_SIZE = 9
USERNAME, PASSWORD = range(2)

HELP_TEXT = """📖 راهنمای استفاده از ربات:

1️⃣ /register → ثبت‌نام کاربر  
2️⃣ /login → ورود به حساب  
3️⃣ /menu → نمایش منوی اصلی  
4️⃣ انتخاب مود → انتخاب گان → مشاهده نتیجه  

⚠️ پیام‌ها بعد از ۶۰ ثانیه حذف می‌شوند!
"""

# 🟢 حذف پیام بعد از 60 ثانیه
async def auto_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    await asyncio.sleep(60)
    try:
        await context.bot.delete_message(chat_id, message_id)
    except:
        pass

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

# 🟢 ارسال منوی اصلی
async def send_menu(update, context):
    kb = [
        [InlineKeyboardButton("🔥 بتل (Battle)", callback_data="mode_battle")],
        [InlineKeyboardButton("⚡️ مولتی (Multiplayer)", callback_data="mode_multi")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")]
    ]
    msg = await update.message.reply_text("👇 مود بازی رو انتخاب کن یا از راهنما استفاده کن:", reply_markup=InlineKeyboardMarkup(kb))
    asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))

# 🟢 دستور /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")
    asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))

# 🟢 ثبت‌نام
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 لطفاً نام کاربری خود را وارد کنید:")
    return USERNAME

async def set_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔑 حالا پسورد رو وارد کنید:")
    return PASSWORD

async def set_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data["username"]
    password = update.message.text
    USERS[username] = password
    await update.message.reply_text("✅ ثبت‌نام موفق! حالا با /login وارد شو.")
    return ConversationHandler.END

# 🟢 ورود
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 نام کاربری برای ورود:")
    return USERNAME

async def login_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔑 پسورد:")
    return PASSWORD


async def login_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data["username"]
    password = update.message.text
    if USERS.get(username) == password:
        LOGGED_IN.add(update.message.chat_id)
        await update.message.reply_text("✅ ورود موفق! حالا منو رو ببین 👇")
        await send_menu(update, context)
    else:
        await update.message.reply_text("❌ نام کاربری یا پسورد اشتباهه!")
    return ConversationHandler.END

# 🟢 /menu → بازگشت به منوی اصلی
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id in LOGGED_IN:
        await send_menu(update, context)
    else:
        await update.message.reply_text("❌ اول باید با /login وارد بشی!")

# 🟢 دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "back_menu":
        kb = [
            [InlineKeyboardButton("🔥 بتل (Battle)", callback_data="mode_battle")],
            [InlineKeyboardButton("⚡️ مولتی (Multiplayer)", callback_data="mode_multi")],
            [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")]
        ]
        await q.edit_message_text("👇 منوی اصلی:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data == "help":
        await q.edit_message_text(HELP_TEXT, parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ بازگشت به منو", callback_data="back_menu")]]))
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

    reg_conv = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_password)]},
        fallbacks=[]
    )

    login_conv = ConversationHandler(
        entry_points=[CommandHandler("login", login)],
        states={USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_username)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_password)]},
        fallbacks=[]
    )

    app.add_handler(reg_conv)
    app.add_handler(login_conv)
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()