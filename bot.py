from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8670615757:AAGni477mgUpj8MduDtpoQh5gTh--d_3uAY"
GROUP_CHAT_ID = -1003794757443  # guruh ID

LANG, NAME, PHONE1, PHONE2, ADDRESS, LOCATION, WATER, NOTE_CHOICE, NOTE = range(9)

TEXT = {
    "uz": {
        "choose_lang": "🇷🇺 Русский язык | 🇺🇿 O'zbek tili",
        "enter_name": "1️⃣ Ism familiyangizni yozing:",
        "enter_phone1": "2️⃣ 1-telefon raqamni yozing:",
        "enter_phone2": "2️⃣ 2-telefon raqamni yozing:",
        "enter_address": "3️⃣ To'liq manzilingizni yozing:",
        "send_location": "4️⃣ Lokatsiyani tugma orqali yuboring:",
        "enter_water": "5️⃣ Nechta suv kerak? Masalan: 3 ta",
        "note_question": "6️⃣ Adminga izoh yozasizmi?",
        "note_yes": "📝 Izohingizni yozing:",
        "note_no": "✅ Buyurtma qabul qilindi",
        "sent": "✅ Buyurtmangiz qabul qilindi!",
        "start_again": "🇷🇺 Русский язык | 🇺🇿 O'zbek tili",
        "yes": "Ha",
        "no": "Yo'q",
        "back": "⬅️ Orqaga",
    },
    "ru": {
        "choose_lang": "🇷🇺 Русский язык | 🇺🇿 O'zbek tili",
        "enter_name": "1️⃣ Введите имя и фамилию:",
        "enter_phone1": "2️⃣ Введите 1-й номер телефона:",
        "enter_phone2": "2️⃣ Введите 2-й номер телефона:",
        "enter_address": "3️⃣ Введите полный адрес:",
        "send_location": "4️⃣ Отправьте локацию кнопкой:",
        "enter_water": "5️⃣ Сколько воды нужно? Например: 3 шт",
        "note_question": "6️⃣ Хотите оставить комментарий админу?",
        "note_yes": "📝 Напишите комментарий:",
        "note_no": "✅ Заказ принят",
        "sent": "✅ Ваш заказ принят!",
        "start_again": "🇷🇺 Русский язык | 🇺🇿 O'zbek tili",
        "yes": "Да",
        "no": "Нет",
        "back": "⬅️ Назад",
    },
}

def lang_kb():
    return ReplyKeyboardMarkup(
        [["🇷🇺 Русский язык", "🇺🇿 O'zbek tili"]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def yes_no_kb(lang):
    return ReplyKeyboardMarkup(
        [[TEXT[lang]["yes"], TEXT[lang]["no"]]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def location_kb(lang):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(TEXT[lang]["send_location"], request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🇷🇺 Русский язык | 🇺🇿 O'zbek tili",
        reply_markup=lang_kb()
    )
    return LANG

async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🇺🇿 O'zbek tili":
        context.user_data["lang"] = "uz"
    else:
        context.user_data["lang"] = "ru"

    lang = context.user_data["lang"]
    await update.message.reply_text(TEXT[lang]["enter_name"], reply_markup=ReplyKeyboardRemove())
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    lang = context.user_data["lang"]
    await update.message.reply_text(TEXT[lang]["enter_phone1"])
    return PHONE1

async def phone1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone1"] = update.message.text
    lang = context.user_data["lang"]
    await update.message.reply_text(TEXT[lang]["enter_phone2"])
    return PHONE2

async def phone2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone2"] = update.message.text
    lang = context.user_data["lang"]
    await update.message.reply_text(TEXT[lang]["enter_address"])
    return ADDRESS

async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    lang = context.user_data["lang"]
    await update.message.reply_text(
        TEXT[lang]["send_location"],
        reply_markup=location_kb(lang)
    )
    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.location:
        context.user_data["location"] = f"https://maps.google.com/?q={update.message.location.latitude},{update.message.location.longitude}"
    else:
        context.user_data["location"] = "Yuborilmadi"

    lang = context.user_data["lang"]
    await update.message.reply_text(TEXT[lang]["enter_water"])
    return WATER

async def water(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["water"] = update.message.text
    lang = context.user_data["lang"]
    await update.message.reply_text(TEXT[lang]["note_question"], reply_markup=yes_no_kb(lang))
    return NOTE_CHOICE

async def note_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    text = update.message.text

    if text == TEXT[lang]["yes"]:
        await update.message.reply_text(TEXT[lang]["note_yes"], reply_markup=ReplyKeyboardRemove())
        return NOTE
    else:
        context.user_data["note"] = "Yo'q"
        await send_to_group(context, update)
        await update.message.reply_text(
            TEXT[lang]["sent"],
            reply_markup=lang_kb()
        )
        return LANG

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["note"] = update.message.text
    await send_to_group(context, update)
    lang = context.user_data["lang"]
    await update.message.reply_text(
        TEXT[lang]["sent"],
        reply_markup=lang_kb()
    )
    return LANG

async def send_to_group(context: ContextTypes.DEFAULT_TYPE, update: Update):
    data = context.user_data
    user = update.effective_user
    lang = data.get("lang", "uz")

    tg_name = user.username if user.username else "yo'q"
    group_text = (
        f"🆕 YANGI BUYURTMA\n\n"
        f"👤 Ism:\n{data.get('name', '-')}\n\n"
        f"📞 Telefon:\n{data.get('phone1', '-')}, {data.get('phone2', '-')}\n\n"
        f"🏠 Manzil:\n{data.get('address', '-')}\n\n"
        f"📍 Lokatsiya:\n{data.get('location', '-')}\n\n"
        f"🚰 Suv:\n{data.get('water', '-')}\n\n"
        f"📝 Izoh:\n{data.get('note', '-')}\n\n"
        f"👤 Telegram:\n@{tg_name}\n\n"
        f"🌐 Til:\n{'🇺🇿 O\\'zbek tili' if lang == 'uz' else '🇷🇺 Русский язык'}"
    )

    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=group_text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_lang)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            PHONE1: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone1)],
            PHONE2: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone2)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)],
            LOCATION: [MessageHandler(filters.LOCATION, location)],
            WATER: [MessageHandler(filters.TEXT & ~filters.COMMAND, water)],
            NOTE_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, note_choice)],
            NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, note)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
