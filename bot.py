import os
import telebot
import base64
import json
import time
import threading
import io
import random
from flask import Flask
from datetime import datetime
from pymongo import MongoClient

# --- 1. SERVIDOR WEB (Anticierre Render) ---
app = Flask(__name__)
@app.route('/')
def index(): return "CJKiller Ultimate System is Online"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# --- 2. CONFIGURACIÓN Y BASE DE DATOS ---
TOKEN = "8106789282:AAFI6CEgWuL-nq5jpSf3vSD8pzIlwLvoBLQ"
ADMIN_ID = 7012561892 
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN, threaded=False)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 3. LÓGICA DE APOYO ---
def encrypt_adyen(card, month, year, cvv):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {"number": card, "cvc": cvv, "expiryMonth": month, "expiryYear": year, "generationtime": gen_time}
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except: return {"success": False}

def get_fake_data():
    names = ["John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas"]
    last = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
    return {
        "name": f"{random.choice(names)} {random.choice(last)}",
        "email": f"{random.choice(names).lower()}{random.randint(100,999)}@gmail.com",
        "street": f"{random.randint(100, 999)} {random.choice(['Main St', 'Oak Ave', 'Park Blvd', 'Cedar Ln'])}",
        "city": random.choice(cities),
        "zip": random.randint(10001, 99999)
    }

# --- 4. COMANDOS DE USUARIO ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    args = message.text.split()
    
    user = users_col.find_one({"user_id": user_id})
    if not user:
        new_user = {"user_id": user_id, "username": username, "credits": 10, "role": "user", "referrals_count": 0}
        if len(args) > 1 and args[1].isdigit():
            ref_id = int(args[1])
            if ref_id != user_id:
                users_col.update_one({"user_id": ref_id}, {"$inc": {"credits": 5, "referrals_count": 1}})
                try: bot.send_message(ref_id, f"🎊 **¡Referido!** @{username} se unió. +5 créditos.")
                except: pass
        users_col.insert_one(new_user)
        user = new_user

    bot.reply_to(message, (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        f"🔥 **CJKILLER ULTIMATE**\n"
        f"👤 **User:** @{username}\n"
        f"💰 **Créditos:** {user.get('credits', 0)}\n"
        "━━━━━━━━━━━━━━\n"
        "🚀 **MENU:**\n"
        "• `/adyen` CC|MM|YY|CVV\n"
        "• `/fake` - Datos Falsos\n"
        "• `/me` - Ver Perfil\n"
        "• `/ref` - Ganar Créditos\n"
        "━━━━━━━━━━━━━━"
    ), parse_mode="Markdown")

@bot.message_handler(commands=['me'])
def cmd_me(message):
    user = users_col.find_one({"user_id": message.from_user.id})
    if not user: return
    bot.reply_to(message, (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        "👤 **TU PERFIL**\n"
        "━━━━━━━━━━━━━━\n"
        f"🆔 **ID:** `{user['user_id']}`\n"
        f"💰 **Créditos:** {user['credits']}\n"
        f"👥 **Referidos:** {user['referrals_count']}\n"
        f"👑 **Rango:** {'OWNER' if user['user_id'] == ADMIN_ID else 'USER'}\n"
        "━━━━━━━━━━━━━━"
    ), parse_mode="Markdown")

@bot.message_handler(commands=['fake'])
def cmd_fake(message):
    f = get_fake_data()
    bot.reply_to(message, (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        "🌐 **GENERATED DATA**\n"
        "━━━━━━━━━━━━━━\n"
        f"👤 **Nombre:** `{f['name']}`\n"
        f"📧 **Email:** `{f['email']}`\n"
        f"🏠 **Calle:** `{f['street']}`\n"
        f"📍 **Ciudad/ZIP:** `{f['city']} / {f['zip']}`\n"
        "━━━━━━━━━━━━━━"
    ), parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        data = message.text.split()[1]
        p = data.split('|')
        res = encrypt_adyen(p[0], p[1], p[2], p[3])
        bot.reply_to(message, (
            "| Hardcore:() |\n"
            "━━━━━━━━━━━━━━\n"
            f"🔹 **CC:** `{data}`\n"
            "━━━━━━━━━━━━━━\n"
            "💎 **HASH:**\n"
            f"`{res['encrypted']}`\n"
            "━━━━━━━━━━━━━━"
        ), parse_mode="Markdown")
    except: bot.reply_to(message, "❌ Use: `/adyen CC|MM|YY|CVV`")

@bot.message_handler(commands=['ref'])
def cmd_ref(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    bot.reply_to(message, (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        "🔗 **REFERIDOS**\n"
        "━━━━━━━━━━━━━━\n"
        f"📥 **Link:** `{ref_link}`\n"
        "🎁 Gana **5 créditos** por cada invitado.\n"
        "━━━━━━━━━━━━━━"
    ), parse_mode="Markdown")

# --- 5. ADMIN ---
@bot.message_handler(commands=['addcredits'])
def add_credits(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        _, tid, amt = message.text.split()
        users_col.update_one({"user_id": int(tid)}, {"$inc": {"credits": int(amt)}})
        bot.reply_to(message, f"✅ +{amt} créditos a `{tid}`")
    except: bot.reply_to(message, "❌ `/addcredits [ID] [CANTIDAD]`")

# --- 6. ARRANQUE ---
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(5)
    bot.remove_webhook()
    bot.polling(none_stop=True, interval=2)
