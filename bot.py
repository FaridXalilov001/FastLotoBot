import logging
import re
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

TOKEN = "8989181923:AAHa3gch8iWi-Q-Br2w8kQq2j145nGd4Pcw"
ADMIN_ID = 1754605271 

DEPOZIT_MEBLEG = 1
KOD_MEBLEG = 2
CIXARIS_KART = 3

MAIN_KEYBOARD = [
    ["💰 Depozit Et", "🎟 Kod Yarat"],
    ["💼 Balans", "🔒 Kodu Bağla"],
    ["💸 Çıxarış Et", "🎁 Bonus"],
    ["🎡 Çarx"],
    ["🌐 Saytlar", "ℹ️ Məlumat"],
    ["🤝 Dostunu Dəvət Et Qazan"],
    ["📢 Kanal və Söhbət Qrupu"]
]

user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.00
        
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "👋 **Xoş gəldiniz!**\n\nAşağıdakı menyudan seçim edin:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return ConversationHandler.END

# ---- DEPOZİT PROSESİ ----
async def depozit_basla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 Zəhmət olmasa, depozit etmək istədiyiniz məbləği yazın (məsələn: 20 AZN):",
        reply_markup=ReplyKeyboardRemove()
    )
    return DEPOZIT_MEBLEG

async def depozit_qebul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    mebleg = update.message.text
    
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        f"✅ Depozit sorğunuz qəbul olundu: **{mebleg}**\n"
        "Admin kart nömrəsini göndərənə qədər gözləyin.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    admin_mesaj = (
        f"🚨 **Yeni Depozit Sorğusu!**\n\n"
        f"👤 Ad: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'Yoxdur'}\n"
        f"🆔 ID: `{user.id}`\n"
        f"💰 Məbləğ: **{mebleg}**"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_mesaj, parse_mode='Markdown')
    except Exception as e:
        print(f"Xəta: {e}")
        
    return ConversationHandler.END

# ---- KOD YARAT PROSESİ ----
async def kod_basla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.00
    balans = user_balances[user_id]
    
    await update.message.reply_text(
        f"🎟️ Neçə manat məbləğində kod istəyirsiz?\n\n💼 Cari balansınız: **{balans:.2f} AZN**",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    return KOD_MEBLEG

async def kod_qebul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    kod_meblegi = update.message.text
    balans = user_balances.get(user_id, 0.00)
    
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        f"✅ **{kod_meblegi}** məbləğində kod istəyiniz admine göndərildi.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    admin_mesaj = (
        f"🎟️ **Yeni Kod İstəyi!**\n\n"
        f"👤 Ad: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'Yoxdur'}\n"
        f"🆔 ID: `{user.id}`\n"
        f"💰 İstənilən kod: **{kod_meblegi}**\n"
        f"💼 Balans: **{balans:.2f} AZN**"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_mesaj, parse_mode='Markdown')
    except Exception as e:
        print(f"Xəta: {e}")
        
    return ConversationHandler.END

# ---- ÇIXARIŞ PROSESİ ----
async def cixaris_basla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0.00
    balans = user_balances[user_id]

    await update.message.reply_text(
        f"💸 Minimum çıxarış məbləği: **40 AZN**\n"
        f"💼 Cari balansınız: **{balans:.2f} AZN**\n\n"
        "💳 Zəhmət olmasa, çıxarış etmək istədiyiniz kart nömrəsini və məbləği yazın:\n"
        "*(Məsələn: 4169 7388 1234 5678 - 50 AZN)*",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    return CIXARIS_KART

async def cixaris_qebul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    kart_ve_mebleg = update.message.text
    balans = user_balances.get(user_id, 0.00)
    
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        f"✅ Çıxarış sorğunuz qəbul olundu!\n\n"
        f"📌 Məlumat: **{kart_ve_mebleg}**\n"
        "Admin sorğunuzu yoxladıqdan sonra ödəniş həyata keçiriləcək.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    admin_mesaj = (
        f"💸 **Yeni Çıxarış Sorğusu!**\n\n"
        f"👤 Ad: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'Yoxdur'}\n"
        f"🆔 ID: `{user.id}`\n"
        f"💳 Kart / Məbləğ: **{kart_ve_mebleg}**\n"
        f"💼 Cari Balansı: **{balans:.2f} AZN**"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_mesaj, parse_mode='Markdown')
    except Exception as e:
        print(f"Xəta: {e}")
        
    return ConversationHandler.END

async def legv_et(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text("Əməliyyat ləğv edildi.", reply_markup=reply_markup)
    return ConversationHandler.END

# ---- DİGƏR MENYU HİSSƏSİ ----
async def diger_mesajlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    user_id = user.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 0.00

    if text == "ℹ️ Məlumat":
        response = (
            "ℹ️ **FAST LOTO BOT Haqda Məlumat:**\n\n"
            "Botumuzu İstifadə Edərək 7/24 Saniyələr İçində Avtomatik CHC Və FastLoto Üçün Kod Ala Bilərsiz.\n\n"
            "🎟️ **Kod Yarat:** Depozit Etdikdən Sonra Kod Yarat Düyməsinə Toxunaraq Öz Kodunuzu Saniyələr İçində Yaradın.\n\n"
            "🔒 **Kodu Bağla:** Kodunuzda Uduş Olduğu Zaman Bu Düyməyə Toxunun.\n\n"
            "💰 **Minimum Depozit:** 1 AZN\n"
            "💸 **Minimum Çıxarış:** 40 AZN\n\n"
            "🎁 **BONUS:** Uduzduğunuz Hər Məbləğə Görə Bonus Balansınıza Avtomatik Bonus Yüklənir."
        )
    elif text == "🌐 Saytlar":
        response = (
            "🌐 **Rəsmi Saytlarımız:**\n\n"
            "1️⃣ [https://deer12.site/login/](https://deer12.site/login/)\n"
            "2️⃣ [https://nebula77.site/](https://nebula77.site/)"
        )
    elif text == "🤝 Dostunu Dəvət Et Qazan":
        bot_username = context.bot.username
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        response = (
            "🤝 **Dostunu Dəvət Et Qazan!**\n\n"
            "Sizə veriləcək xüsusi linki dostunuza göndərin. Dostunuzun etdiyi hər depozitdən həmişə siz də qazanın!\n\n"
            "🔗 **Sizin dəvət linkiniz:**\n"
            f"`{referral_link}`\n\n"
            "*(Nə qədər çox dost dəvət etsəz, bir o qədər çox qazanacaqsız. Qeyd: Dəvət etdiyiniz dostunuz depozit etməsə qazanc verilmir)*"
        )
    elif text == "💼 Balans":
        response = f"💼 Sizin cari balansınız: **{user_balances[user_id]:.2f} AZN**"
    elif text == "🎁 Bonus":
        response = "❌ **Sizin hazırda bonusunuz yoxdur.**\nBonus Yalnız Uduzulan Məbləğə Görə Verilir."
    else:
        response = f"Siz '{text}' seçdiniz."
        
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown', disable_web_page_preview=True)

# ---- ADMİNİN CAVAB MEXANİZMİ ----
async def admin_cavab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.reply_to_message:
        replied_text = update.message.reply_to_message.text
        match = re.search(r"🆔 ID:\s*`?(\d+)`?", replied_text)
        if match:
            target_user_id = int(match.group(1))
            melumat = update.message.text
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📌 **Admin cavabı / Məlumat:**\n\n{melumat}",
                    parse_mode='Markdown'
                )
                await update.message.reply_text("✅ İstifadəçiyə uğurla göndərildi!")
            except Exception as e:
                await update.message.reply_text(f"❌ Xəta baş verdi: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    depozit_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^💰 Depozit Et$"), depozit_basla)],
        states={
            DEPOZIT_MEBLEG: [MessageHandler(filters.TEXT & ~filters.COMMAND, depozit_qebul)]
        },
        fallbacks=[CommandHandler("cancel", legv_et)]
    )

    kod_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🎟 Kod Yarat$"), kod_basla)],
        states={
            KOD_MEBLEG: [MessageHandler(filters.TEXT & ~filters.COMMAND, kod_qebul)]
        },
        fallbacks=[CommandHandler("cancel", legv_et)]
    )

    cixaris_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^💸 Çıxarış Et$"), cixaris_basla)],
        states={
            CIXARIS_KART: [MessageHandler(filters.TEXT & ~filters.COMMAND, cixaris_qebul)]
        },
        fallbacks=[CommandHandler("cancel", legv_et)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(depozit_handler)
    app.add_handler(kod_handler)
    app.add_handler(cixaris_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(user_id=ADMIN_ID), admin_cavab))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, diger_mesajlar))

    print("Bot işə düşdü...")
    app.run_polling()

if __name__ == '__main__':
    main()

