import telebot
import os
import time
import uuid
import random
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
keys_col = db['keys']

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- BASES DE DATOS PARA /FAKE ---
PAISES_ELITE = {
    "US": {"n": "Estados Unidos", "cities": ["Miami", "New York", "Los Angeles"], "zip": "33101", "st": "FL"},
    "MX": {"n": "México", "cities": ["CDMX", "Guadalajara", "Monterrey"], "zip": "01000", "st": "DF"},
    "ES": {"n": "España", "cities": ["Madrid", "Barcelona", "Valencia"], "zip": "28001", "st": "MD"},
    "CO": {"n": "Colombia", "cities": ["Bogotá", "Medellín", "Cali"], "zip": "110111", "st": "DC"},
    "AR": {"n": "Argentina", "cities": ["Buenos Aires", "Córdoba"], "zip": "1000", "st": "BA"}
}

# --- FUNCIONES INTERNAS ---
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
        InlineKeyboardButton("🆔 Fake Data", callback_data="btn_fake"),
        InlineKeyboardButton("🎟️ Canjear Key", callback_data="btn_key")
    )
    return markup

# --- COMANDOS DE MENÚ ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    setup_user(message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id, 
        f"🔥 **BIENVENIDO A CJKILLER ELITE v21.0**\n\nEl sistema más avanzado para consultas y generación de datos.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['me'])
def my_info(message):
    user = users_col.find_one({"id": message.from_user.id})
    if not user: return
    text = f"📊 **TU ESTADO**\n\n🆔 ID: `{user['id']}`\n🏅 Rango: `{user['role']}`\n💎 Créditos: `{user['credits']}`"
    bot.reply_to(message, text, parse_mode="Markdown")

# --- COMANDO FAKE (NIVEL ELITE) ---

@bot.message_handler(commands=['fake'])
def fake_gen(message):
    try:
        args = message.text.split()
        code = args[1].upper() if len(args) > 1 else "US"
        if code not in PAISES_ELITE: code = "US"
        
        p = PAISES_ELITE[code]
        num = random.randint(100, 9999)
        email = f"{random.choice(['cjkiller', 'user', 'pro'])}{num}@{random.choice(['gmail.com', 'outlook.com', 'icloud.com'])}"
        
        fake_msg = (
            f"🌐 **IDENTIDAD GENERADA ({code})**\n"
            f"--- --- --- --- --- --- ---\n"
            f"👤 **Nombre:** `{random.choice(['Carlos', 'John', 'Maria'])} {random.choice(['Perez', 'Doe', 'Garcia'])}` {num}\n"
            f"📧 **Email:** `{email}`\n"
            f"🏠 **Dirección:** `Calle {random.choice(['Principal', 'Libertad'])} #{num}`\n"
            f"🏙️ **Ciudad:** `{random.choice(p['cities'])}, {p['st']}`\n"
            f"📮 **ZIP:** `{p['zip']}`\n"
            f"📞 **Tel:** `+{random.randint(1, 99)} {random.randint(200, 999)}-{num}`"
        )
        bot.reply_to(message, fake_msg, parse_mode="Markdown")
    except: bot.reply_to(message, "❌ Uso: `/fake US`")

# --- SISTEMA DE KEYS Y ADMINISTRACIÓN ---

@bot.message_handler(commands=['gen'])
def generate_key(message):
    if message.from_user.id != OWNER_ID: return
    try:
        creds = int(message.text.split()[1])
        new_key = f"CJ-{str(uuid.uuid4())[:8].upper()}"
        keys_col.insert_one({"key": new_key, "credits": creds, "status": "active"})
        bot.reply_to(message, f"🎫 **KEY GENERADA:**\n\n`{new_key}`\n💎 Valor: `{creds}` créditos.")
    except: bot.reply_to(message, "❌ Uso: `/gen [cantidad]`")

@bot.message_handler(commands=['claim'])
def claim_key(message):
    try:
        key_str = message.text.split()[1].upper()
        key_data = keys_col.find_one({"key": key_str, "status": "active"})
        if not key_data: return bot.reply_to(message, "❌ Key inválida o ya usada.")
        
        users_col.update_one({"id": message.from_user.id}, {"$inc": {"credits": key_data['credits']}})
        keys_col.update_one({"key": key_str}, {"$set": {"status": "used"}})
        
        bot.reply_to(message, f"✅ **Canje Exitoso:** +`{key_data['credits']}` créditos.")
        # ALERTA PARA EL OWNER
        bot.send_message(OWNER_ID, f"💰 **AVISO DE VENTA**\nID: `{message.from_user.id}`\nKey: `{key_str}`\nCréditos: `{key_data['credits']}`")
    except: bot.reply_to(message, "❌ Uso: `/claim [TU-KEY]`")

# --- CALLBACKS BOTONES ---

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)
    if call.data == "btn_shk": bot.send_message(call.message.chat.id, "🔍 Usa `/shk [numero]`")
    elif call.data == "btn_me": my_info(call.message)
    elif call.data == "btn_fake": bot.send_message(call.message.chat.id, "🌐 Usa `/fake [PAIS]` (Ej: `/fake US`, `/fake MX`)")
    elif call.data == "btn_key": bot.send_message(call.message.chat.id, "🎟️ Escribe `/claim [TU-KEY]`")

# --- LÓGICA WEBHOOK ---

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

@app.route("/")
def webhook_setup():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=URL_PROYECTO + '/' + TOKEN)
    return "CJkiller v21.0: Elite System Active", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
