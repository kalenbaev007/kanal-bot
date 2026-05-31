import telebot
import json
import os

TOKEN = "8879006260:AAGzNDn8woox4ojyD-WzTyaAPvb1GWX6c_U"
SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["sethavola"])
def set_havola(message):
    if message.chat.type != "private":
        return
    try:
        havola = message.text.split(" ", 1)[1]
        settings = load_settings()
        settings["havola"] = havola
        save_settings(settings)
        bot.reply_to(message, f"✅ Havola saqlandi:\n{havola}")
    except:
        bot.reply_to(message, "❌ Xato! To'g'ri yozing:\n/sethavola @kanalim")

@bot.message_handler(commands=["havola"])
def get_havola(message):
    if message.chat.type != "private":
        return
    settings = load_settings()
    havola = settings.get("havola", "Havola o'rnatilmagan")
    bot.reply_to(message, f"📌 Hozirgi havola:\n{havola}")

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type != "private":
        return
    bot.reply_to(message,
        "👋 Salom! Men kanal post botiman.\n\n"
        "📌 Buyruqlar:\n"
        "/sethavola @kanalim — havola o'rnatish\n"
        "/havola — hozirgi havolani ko'rish\n\n"
        "Botni kanalga admin qilib qo'shing!")

@bot.channel_post_handler(content_types=["text"])
def handle_post(message):
    settings = load_settings()
    havola = settings.get("havola", "")
    if not havola:
        return
    new_text = message.text + f"\n\n{havola}"
    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=new_text
        )
    except:
        pass

print("Bot ishlamoqda...")
bot.polling(none_stop=True)
