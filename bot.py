import telebot
import os
import time
import uuid
from flask import Flask, request
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
URL_PROYECTO = "https://cjkiller-bot.onrender.com"
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']
keys_col = db['keys'] # Nueva colección para automatización

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- FUNCIONES DE SOPORTE ---
def setup_user(user_id, username):
    is_owner = (user_id == OWNER_ID)
    users_col.update_one(
        {"id": user_id},
        {"$set": {"username": username, "role": "OWNER" if is_owner else "USER"},
         "$setOnInsert": {"credits": 999999 if is_owner else 0}},
        upsert=True
    )

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔍 Consultar SHK", callback_data="btn_shk"),
        InlineKeyboardButton("👤 Mi Perfil", callback_data="btn_me"),
        InlineKeyboardButton("🎟️ Canjear Key", callback_data="btn_key"),
        InlineKeyboardButton("📢 Soporte", url="https://t.me/TuUsuarioDeSoporte")
    )
    return markup

# --- MANEJADORES DE COMANDOS ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    setup_user(message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id, 
        f"🔥 **BIENVENIDO A CJKILLER PREMIUM**\n\nEl bot más rápido y estable del mercado.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['me'])
def my_info(message):
    user = users_col.find_one({"id": message.from_user.id})
    if not user: return
    text = f"📊 **TU ESTADO**\n\n🆔 ID: `{user['id']}`\n🏅 Rango: `{user['role']}`\n💎 Créditos: `{user['credits']}`"
    bot.reply_to(message, text, parse_mode="Markdown")

# --- SISTEMA DE KEYS (AUTOMATIZACIÓN) ---

@bot.message_handler(commands=['gen'])
def generate_key(message):
    """Solo el Owner genera llaves de créditos: /gen [créditos]"""
    if message.from_user.id != OWNER_ID: return
    try:
        credits = int(message.text.split()[1])
        new_key = f"CJ-{str(uuid.uuid4())[:8].upper()}"
        keys_col.insert_one({"key": new_key, "credits": credits, "status": "active"})
        bot.reply_to(message, f"🎫 **KEY GENERADA:**\n\n`{new_key}`\nValor: `{credits}` créditos.")
    except:
        bot.reply_to(message, "❌ Uso: `/gen [cantidad]`")

@bot.message_handler(commands=['claim'])
def claim_key(message):
    """Cualquier usuario canjea: /claim [key]"""
    try:
        key_str = message.text.split()[1].upper()
        key_data = keys_col.find_one({"key": key_str, "status": "active"})
        
        if not key_data:
            return bot.reply_to(message, "❌ Key inválida o ya usada.")
        
        # Sumar créditos y quemar la key
        users_col.update_one({"id": message.from_user.id}, {"$inc": {"credits": key_data['credits']}})
        keys_col.update_one({"key": key_str}, {"$set": {"status": "used"}})
        
        bot.reply_to(message, f"✅ **¡ÉXITO!**\nHas canjeado `{key_data['credits']}` créditos.")
    except:
        bot.reply_to(message, "❌ Uso: `/claim [TU-KEY]`")

# --- GESTIÓN DE CALLBACKS (BOTONES) ---

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "btn_shk":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔍 Usa `/shk [numero]` para consultar.")
    elif call.data == "btn_me":
        my_info(call.message)
    elif call.data == "btn_key":
        bot.send_message(call.message.chat.id, "🎟️ Para canjear, escribe: `/claim [TU-KEY]`")

# --- LÓGICA DE WEBHOOK (MANTENIENDO ESTABILIDAD) ---

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook_setup():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=URL_PROYECTO + '/' + TOKEN)
    return "CJkiller v21.0: Elite System Active", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
