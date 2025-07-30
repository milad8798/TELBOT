import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = "8384449381:AAGDJNJaLAZ0f983ZN5SiPx8v4LAk52kAjs"

# 🔥 لیست کامل گان‌های کالاف
GUNS = [
    "AK-47","AK117","AN-94","AS VAL","CR-56 AMAX","FAMAS","FFAR","Grau 5.56","HBRa3",
    "ICR-1","Kilo 141","KN-44","LK24","M13","Man-O-War","Type 25","QBZ-95","XM4",
    "MSMC","PDW-57","Razorback","PP19 Bizon","GKS","MX9","VMP","CX-9","Striker 45","KSP-45",
    "DL Q33","Locus","Arctic .50","XPR-50","M21 EBR","NA-45","Outlaw","HDR",
    "SP-R 208","SKS","SVD","Type 63",
    "Holger 26","Hades","UL736","Raal MG","MG 42",
    "R9-0","Striker","HS0405"
]

PAGE_SIZE = 9

# 🟢 تابع حذف پیام بعد از 60 ثانیه
async def auto_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    await asyncio.sleep(60)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.warning(f"خطا در حذف پیام: {e}")

# 🟢 ساخت کیبورد ۳×۳ گان‌ها با صفحه‌بندی
def guns_keyboard(page: int, mode: str):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    items = GUNS[start:end]

    keyboard = []
    for i in range(0, len(items), 3):
        row = [InlineKeyboardButton(items[j], callback_data=f"gun_{mode}_{items[j]}") for j in range(i, min(i+3, len(items)))]
        keyboard.append(row)

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"page_{mode}_{page-1}"))
    if end < len(GUNS):
        nav.append(InlineKeyboardButton("➡️ بعدی", callback_data=f"page_{mode}_{page+1}"))
    if nav:
        keyboard.append(nav)

    keyboard.append([InlineKeyboardButton("⬅️ بازگشت به انتخاب مود", callback_data="back_mode")])
    return InlineKeyboardMarkup(keyboard)

# 🟢 دستور /start → انتخاب مود
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 بتل (Battle)", callback_data="mode_battle")],
        [InlineKeyboardButton("⚡️ مولتی (Multiplayer)", callback_data="mode_multi")]
    ]
    msg = await update.message.reply_text("👇 مود بازی رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))
    asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))

# 🟢 هندلر دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    # 🔹 بازگشت به انتخاب مود
    if data == "back_mode":
        kb = [
            [InlineKeyboardButton("🔥 بتل (Battle)", callback_data="mode_battle")],
            [InlineKeyboardButton("⚡️ مولتی (Multiplayer)", callback_data="mode_multi")]
        ]
        msg = await q.edit_message_text("👇 مود بازی رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(kb))
        asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))
        return

    # 🔹 انتخاب مود → نمایش گان‌ها (صفحه اول)
    if data.startswith("mode_"):
        mode = data.split("_")[1]
        msg = await q.edit_message_text(f"📂 مود انتخاب شده: {mode.upper()}\n🔫 گان مورد نظر رو انتخاب کن:", reply_markup=guns_keyboard(0, mode))
        asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))
        return

    # 🔹 صفحه‌بندی
    if data.startswith("page_"):
        _, mode, page = data.split("_")
        page = int(page)
        msg = await q.edit_message_text(f"🔫 لیست گان‌ها | صفحه {page+1}", reply_markup=guns_keyboard(page, mode))
        asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))
        return

    # 🔹 انتخاب گان
    if data.startswith("gun_"):
        _, mode, gun = data.split("_", 2)
        msg = await q.edit_message_text(f"✅ گان انتخابی: {gun}\n🎮 مود: {mode.upper()}")
        asyncio.create_task(auto_delete(context, msg.chat_id, msg.message_id))
        return
        # 🟢 اجرای ربات
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()