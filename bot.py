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
# Tu ID de Administrador configurado
ADMIN_ID = 7012561892 
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN, threaded=False)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 3. LÓGICA DE ENCRIPTACIÓN ADYEN ---
def encrypt_adyen(card, month, year, cvv):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {"number": card, "cvc": cvv, "expiryMonth": month, "expiryYear": year, "generationtime": gen_time}
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except: return {"success": False}

# --- 4. COMANDOS DE USUARIO Y REFERIDOS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    args = message.text.split()
    
    user = users_col.find_one({"user_id": user_id})
    
    if not user:
        new_user = {
            "user_id": user_id,
            "username": username,
            "credits": 10,
            "role": "user",
            "referred_by": None,
            "referrals_count": 0
        }
        
        # Lógica de Referidos: /start [id_referidor]
        if len(args) > 1 and args[1].isdigit():
            referrer_id = int(args[1])
            if referrer_id != user_id:
                new_user["referred_by"] = referrer_id
                users_col.update_one({"user_id": referrer_id}, {"$inc": {"credits": 5, "referrals_count": 1}})
                try:
                    bot.send_message(referrer_id, f"🎊 **¡Nuevo Referido!** @{username} se unió con tu link. +5 Créditos.")
                except: pass

        users_col.insert_one(new_user)
        user = new_user

    texto = (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        "🔥 **CJKILLER ULTIMATE**\n"
        "━━━━━━━━━━━━━━\n"
        f"👤 **Usuario:** @{username}\n"
        f"💰 **Créditos:** {user.get('credits', 0)}\n"
        f"👑 **Rango:** {'ADMIN' if user_id == ADMIN_ID else 'FREE'}\n"
        "━━━━━━━━━━━━━━\n"
        "🚀 **MENU:**\n"
        "• `/adyen` CC|MES|ANO|CVV\n"
        "• `/fake` - Generar Datos\n"
        "• `/ref` - Link de Referido\n"
        "• `/me` - Mi Perfil\n"
        "━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, texto, parse_mode="Markdown")

@bot.message_handler(commands=['ref'])
def cmd_ref(message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
    user = users_col.find_one({"user_id": user_id})
    
    response = (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        "🔗 **REFERIDOS**\n"
        "━━━━━━━━━━━━━━\n"
        "Gana **5 créditos** por invitado.\n\n"
        f"📥 **Link:** `{ref_link}`\n"
        f"👥 **Total:** {user.get('referrals_count', 0)}\n"
        "━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        data = message.text.split()[1]
        p = data.split('|')
        res = encrypt_adyen(p[0], p[1], p[2], p[3])
        # Estética recuperada de tus capturas
        response = (
            "| Hardcore:() |\n"
            "━━━━━━━━━━━━━━\n"
            f"🔹 **CC:** `{data}`\n"
            "━━━━━━━━━━━━━━\n"
            "💎 **HASH:**\n"
            f"`{res['encrypted']}`\n"
            "━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Formato: `/adyen CC|MES|ANO|CVV`")

# --- 5. COMANDOS EXCLUSIVOS DEL DUEÑO (ID: 7012561892) ---

@bot.message_handler(commands=['addcredits'])
def add_credits(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "⚠️ Solo el Owner puede usar esto.")
    
    try:
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        
        users_col.update_one({"user_id": target_id}, {"$inc": {"credits": amount}})
        bot.reply_to(message, f"✅ Has enviado {amount} créditos al usuario `{target_id}`.")
        bot.send_message(target_id, f"💎 **¡CRÉDITOS RECIBIDOS!**\nEl Owner te ha asignado {amount} créditos.")
    except:
        bot.reply_to(message, "❌ Uso: `/addcredits [ID] [CANTIDAD]`")

# --- 6. ARRANQUE SEGURO ---
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(10) # Espera técnica para Render
    bot.remove_webhook()
    print(f"🚀 CJKILLER ONLINE - ADMIN: {ADMIN_ID}")
    bot.polling(none_stop=True, interval=2, timeout=20)
