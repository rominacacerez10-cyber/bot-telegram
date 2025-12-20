import telebot
import os
import time
import uuid
import random
import requests
from flask import Flask, request
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURACIÓN ELITE ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
URL_PROYECTO = "https://cjkiller-bot.onrender.com"
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col, keys_col = db['users'], db['keys']

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- SISTEMA ANTISPAM ---
user_last_msg = {}
def is_spam(user_id):
    current_time = time.time()
    last_time = user_last_msg.get(user_id, 0)
    if current_time - last_time < 2: return True
    user_last_msg[user_id] = current_time
    return False

# --- LÓGICA DE GENERACIÓN (LUHN + BIN INFO) ---
def luhn_check(n):
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_bin_info(bin_num):
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5)
        if res.status_code == 200:
            d = res.json()
            return f"{d.get('country', {}).get('name')} {d.get('country', {}).get('emoji')}"
    except: pass
    return "Desconocido 🏳️"

def gen_cards(bin_format, quantity=10):
    cards = []
    while len(cards) < quantity:
        card = bin_format
        while len(card) < 15: card += str(random.randint(0, 9))
        for i in range(10):
            if luhn_check(card + str(i)):
                mm, yy, cvv = random.randint(1, 12), random.randint(2025, 2031), random.randint(100, 999)
                cards.append(f"`{card}{i}|{mm:02d}|{yy}|{cvv}`")
                break
    return cards

# --- COMANDOS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🔍 SHK", callback_data="btn_shk"),
               InlineKeyboardButton("💳 Gen Cards", callback_data="btn_gen"),
               InlineKeyboardButton("🆔 Fake Data", callback_data="btn_fake"),
               InlineKeyboardButton("🎟️ Canjear", callback_data="btn_key"))
    bot.send_message(message.chat.id, "🔥 **CJkiller Elite v22.0: NIVEL DIOS**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['gen'])
def multi_gen(message):
    if is_spam(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: return bot.reply_to(message, "❌ `/gen [BIN]` o `/gen [monto]`")

    # Si es el Owner creando una Key
    if args[1].isdigit() and len(args[1]) < 6:
        if message.from_user.id != OWNER_ID: return
        key = f"CJ-{str(uuid.uuid4())[:8].upper()}"
        keys_col.insert_one({"key": key, "credits": int(args[1]), "status": "active"})
        return bot.reply_to(message, f"🎫 **KEY:** `{key}`\n💎 Valor: `{args[1]}`")

    # Si es un usuario generando tarjetas
    bin_num = args[1][:6]
    pais = get_bin_info(bin_num)
    cards = gen_cards(bin_num)
    res = f"💳 **CARDS GENERADAS**\n🌍 **País:** `{pais}`\n🔢 **BIN:** `{bin_num}`\n\n" + "\n".join(cards)
    bot.reply_to(message, res, parse_mode="Markdown")
    bot.send_message(OWNER_ID, f"📑 **LOG:** `{message.from_user.id}` generó con BIN `{bin_num}`")

@bot.message_handler(commands=['fake'])
def fake_gen(message):
    if is_spam(message.from_user.id): return
    n = random.randint(1000, 9999)
    res = f"🌐 **FAKE DATA**\n👤 **Nombre:** `User {n}`\n📧 **Email:** `pro{n}@gmail.com`"
    bot.reply_to(message, res, parse_mode="Markdown")

@bot.message_handler(commands=['claim'])
def claim_key(message):
    try:
        key_str = message.text.split()[1].upper()
        key_data = keys_col.find_one({"key": key_str, "status": "active"})
        if not key_data: return bot.reply_to(message, "❌ Key inválida.")
        users_col.update_one({"id": message.from_user.id}, {"$inc": {"credits": key_data['credits']}}, upsert=True)
        keys_col.update_one({"key": key_str}, {"$set": {"status": "used"}})
        bot.reply_to(message, "✅ Créditos cargados.")
        bot.send_message(OWNER_ID, f"💰 **VENTA:** `{message.from_user.id}` usó `{key_str}`.")
    except: bot.reply_to(message, "❌ `/claim [key]`")

# --- CALLBACKS Y WEBHOOK ---
@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    bot.answer_callback_query(call.id)
    msg = {"btn_shk": "/shk", "btn_gen": "/gen [BIN]", "btn_fake": "/fake", "btn_key": "/claim"}.get(call.data)
    bot.send_message(call.message.chat.id, f"⚙️ Comando: `{msg}`")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
    return "!", 200

@app.route("/")
def webhook_setup():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=URL_PROYECTO + '/' + TOKEN)
    return "CJkiller v22.0: Elite System Active", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
