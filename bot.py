from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# TOKEN
TOKEN = "8376572959:AAH7T9wa2wtWHtxHU9htdWvcLvB8IWWCs-o"

# ------- CONFIG --------
config = {
    "main_menu": {
        "choose_city": "Выбор города / Shaharni tanlash(9)",
        "balance": "Баланс / Balans(0 ₽)",
        "purchases": "Покупки / Xaridlar(0)",
        "reviews": "Отзывы"
    },
    "texts": {
        "start": "Главное меню 👇 / Asosiy menyu 👇",
        "balance": "💳 Ваш баланс: 0 ₽\n\nПополните баланс.",
        "purchases": "📦 Ваши покупки (0) / Sizning xaridlaringiz (0)",
        "reviews": "⭐️ Я купил товар, очень качественный! / Men mahsulot sotib oldim, juda sifatli!",
        "operator": "@Warrenbufett1",
        "LTC BABY": "@ltc_baby",
        "ltc_wallet": "ltc1qzu266xuw83gf8hyxvveqr5m95ge55hvhmenze6",
        "card": "6373 7473 9373 3636"
    }
}

# ------- SHAHARLAR --------
shaharlar = [
    "Ташкент", "Самарканд", "Сырдарья", "Наманган",
    "Фергана", "Андижан", "Маргилан", "Коканд", "Ургенч"
]

# ------- USER DATA --------
user_data = {}

# ------- START --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0, "purchases": 0}

    menu = ReplyKeyboardMarkup(
        [
            [KeyboardButton(config["main_menu"]["choose_city"]), KeyboardButton(config["main_menu"]["balance"])],
            [KeyboardButton(config["main_menu"]["purchases"]), KeyboardButton(config["main_menu"]["reviews"])]
        ],
        resize_keyboard=True
    )
    if update.message:
        await update.message.reply_text(config["texts"]["start"], reply_markup=menu)
    elif update.callback_query:
        await update.callback_query.message.reply_text(config["texts"]["start"], reply_markup=menu)

# ------- SHOW CITIES --------
async def show_cities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    buttons = []
    row = []
    for city in shaharlar:
        if city == "Ургенч":
            buttons.append([
                InlineKeyboardButton(city, callback_data=f"city_{city}"),
                InlineKeyboardButton("Operator", url=f"https://t.me/{config['texts']['operator'].replace('@','')}")
            ])
        else:
            row.append(InlineKeyboardButton(city, callback_data=f"city_{city}"))
            if len(row) == 2:
                buttons.append(row)
                row = []
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton("LTC BABY", url=f"https://t.me/{config['texts']['LTC BABY'].replace('@','')}")])
    buttons.append([InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")])

    if update.message:
        await update.message.reply_text("🏙 Выберите город / Shaharni tanlang:", reply_markup=InlineKeyboardMarkup(buttons))
    elif query:
        await query.message.reply_text("🏙 Выберите город / Shaharni tanlang:", reply_markup=InlineKeyboardMarkup(buttons))

# ------- CITY HANDLER --------
async def city_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    city = query.data.replace("city_", "")

    buttons = [
        [InlineKeyboardButton("СК SUGAR (😋) 1.0g 6580₽", callback_data=f"product_{city}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]

    await query.message.reply_text(
        f"Вы выбрали город / Siz shaharni tanladingiz: {city}\n\n"
        f"Выбор товара / Mahsulotni tanlash:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ------- PRODUCT HANDLER --------
async def product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    city = query.data.replace("product_", "")

    buttons = [
        [InlineKeyboardButton("Центр", callback_data=f"region_{city}_Центр")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]

    await query.message.reply_text(
        f"Вы выбрали товар / Siz mahsulotni tanladingiz:\n\n"
        f"Город / Shahar: {city}\n\n"
        f"Товар / Mahsulot: СК SUGAR (😋) 1.0g 6580₽\n\n"
        f"Выберете район / Tumanni tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ------- REGION HANDLER --------
async def region_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, city, region = query.data.split("_")

    buttons = [
        [InlineKeyboardButton("LTC *к оплате*/to'lov uchun: 1.4578645", callback_data=f"pay_{city}_{region}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]

    await query.message.reply_text(
        f"Вы выбрали район / Siz mahsulotni tanladingiz: {region}\n\n"
        f"Город / Shahar: {city}\n"
        f"Район / Tuman: {region}\n\n"
        f"Товар / Mahsulot: СК SUGAR (😋) 1.0g 6580₽  \n\n"
        f"Ваш Баланс / Sizning Balansingiz: 0 ₽ \n\n"
        f"Выбор способа оплаты / To'lov usulini tanlash:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ------- PAYMENT HANDLER --------
async def payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, city, region = query.data.split("_")

    buttons = [
        [InlineKeyboardButton("LTC BABY", url=f"https://t.me/{config['texts']['LTC BABY'].replace('@','')}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]

    text = (
        "Способ оплаты: LTC\n\n"
        "Оплатите желаемую сумму на кошелек\n\n"
        f"{config['texts']['ltc_wallet']}\n\n"
        "Оплата зачислится автоматически в течении 5 минут\n\n"
        "НЕ ПОПОЛНЯЙТЕ ЭТОТ АДРЕС ДВАЖДЫ\n"
        "//////////////////////////////////////////////////////////////////////\n"
        "To'lov avtomatik ravishda 5 daqiqa ichida amalga oshiriladi\n\n"
        "BALANSNI YANA TO'LDIRISH UCHUN BOT BERADIGAN YANGI HAMYONDAN FOYDALANING\n\n"
        "➖➖➖➖➖➖➖➖ \n"
        "💎 TO PAY: 1.4578645 LTC\n\n"
        "🎁 Product: СК SUGAR (😋) 1.0g 6580₽\n\n"
        f"🔦 Address: {city}-{city}-{region} \n"
        "➖➖➖➖➖➖➖➖"
    )

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# ------- BALANCE --------
async def balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = user_data.get(user_id, {}).get("balance", 0)
    text = f"💳 Ваш баланс: {balance} ₽\n\nПополните баланс."
    buttons = [[InlineKeyboardButton("LITECOIN", callback_data="recharge_ltc")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def recharge_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = [
        [InlineKeyboardButton("LTC BABY", url=f"https://t.me/{config['texts']['LTC BABY'].replace('@','')}")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]

    text = (
        "Способ оплаты: LTC\n\n"
        "Оплатите желаемую сумму на кошелек\n\n"
        "ltc1qzu266xuw83gf8hyxvveqr5m95ge55hvhmenze6\n\n"
        "Оплата зачислится автоматически в течении 5 минут\n\n"
        "ЧТО-БЫ ПОПОЛНИТЬ БАЛАНС ЕЩЕ РАЗ, ИСПОЛЬЗУЙТЕ НОВЫЙ LTC КОШЕЛЕК КОТОРЫЙ ВЫДАЕТ БОТ\n\n"
        "НЕ ПОПОЛНЯЙТЕ ЭТОТ АДРЕС ДВАЖДЫ\n"
        "//////////////////////////////////////////////////////////////////////\n"
        "To'lov avtomatik ravishda 5 daqiqa ichida amalga oshiriladi\n\n"
        "BALANSNI YANA TO'LDIRISH UCHUN BOT BERADIGAN YANGI HAMYONDAN FOYDALANING\n\n"
    )

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

# ------- PURCHASES --------
async def purchases_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = user_data.get(user_id, {}).get("purchases", 0)
    text = f"📦 Ваши покупки ({count}) / Sizning xaridlaringiz ({count})"
    await update.message.reply_text(text)

# ------- CALLBACKS --------
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.message.delete()
        await start(update, context)
    elif data.startswith("city_"):
        await city_handler(update, context)
    elif data.startswith("product_"):
        await product_handler(update, context)
    elif data.startswith("region_"):
        await region_handler(update, context)
    elif data.startswith("pay_"):
        await payment_handler(update, context)
    elif data == "recharge_ltc":
        await recharge_handler(update, context)

# ------- MESSAGE HANDLER --------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == config["main_menu"]["choose_city"]:
        await show_cities(update, context)
    elif text == config["main_menu"]["balance"]:
        await balance_handler(update, context)
    elif text == config["main_menu"]["purchases"]:
        await purchases_handler(update, context)
    elif text == config["main_menu"]["reviews"]:
        otviz_text = (
            "🎁 Product:СК Альфа-пвп кристалл  (💫) 0.35 гр 2650₽\n"
            "📆 Time: 5-05-2025 (07:42)\n\n"
            "👑 наманган 0.35cк (бонус 9+1 ) дождалась 😅🤝👍✅ Нашла легко не смотря на то что ландшафт изменился и дождь шёл 😅👀💯✅ Кладмен красава 👍👍👍 Всё супер гуд 🥳🤩😍 спасибочки💋💋💋💋💋\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            "🎁 Product: СК Альфа-пвп кристалл (⭐️) 0.35g 3950₽\n"
            "📆 Time: 9-05-2025 (09:53)\n\n"
            "👑 Найс\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            "🎁 Product: СК Альфа-пвп кристалл (⭐️) 0.35g 3950₽\n"
            "📆 Time: 10-08-2025 (09:41)\n\n"
            "👑 птички 🐦 в клетке оба двоих Мишка мужик\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            "🎁 Product: СК Альфа-пвп кристалл (⭐️) 0.35g 3750₽\n"
            "📆 Time: 12-08-2025 (12:10)\n\n"
            "👑 касание\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            "🎁 Product: СК Альфа-пвп кристалл 0.35г 2990₽\n"
            "📆 Time: 11-08-2025 (07:44)\n\n"
            "👑 0.35  дома спасибо за ровность"
        )
        await update.message.reply_text(otviz_text)
    else:
        await start(update, context)

# ------- MAIN --------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.run_polling()

if __name__ == "__main__":
    main()
