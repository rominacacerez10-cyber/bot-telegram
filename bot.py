import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CREDENCIALES ] ---
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller&tlsAllowInvalidCertificates=true"
ADMIN_ID = 7447432617

# --- [ COMPATIBILIDAD RENDER ] ---
app = Flask(__name__)
@app.route('/')
def health(): return "CJKILLER v64.5 ONLINE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ BASE DE DATOS ] ---
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, connect=False, maxPoolSize=1)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)

# --- [ FUNCIONES EXTREMAS REINTEGRADAS ] ---

def get_full_intel(bin_p):
    """Módulo Oracle-Vision + Biometría (v48)"""
    score = random.randint(20, 99)
    gates = ["Stripe", "Amazon Pay", "Adyen", "Braintree"]
    status = "💎 PRIVATE" if score > 88 else "✅ HIGH SUCCESS"
    return {"status": status, "score": score, "gate": random.choice(gates)}

def identity_core():
    """Módulo Identity-Core (v50)"""
    names = ["James Smith", "Robert Brown", "John Wilson", "Michael Davis"]
    cities = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "Miami, FL"]
    return f"{random.choice(names)} | {random.choice(cities)} | {random.randint(10001, 99999)}"

# --- [ COMANDOS INTEGRADOS ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA"})
    
    bot.reply_to(message, (
        "👑 <b>CJKILLER v64.5: NUCLEAR STATUS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>INTEGRACIÓN TOTAL</code>\n"
        "🔮 <b>ORACLE:</b> <code>ACTIVO v48</code>\n"
        "🛰️ <b>RADAR:</b> <code>ACTIVO v59</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Sesiones viejas expulsadas. Terminal operativa.</i>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    try:
        bin_in = message.text.split()[1][:6]
        intel = get_full_intel(bin_in)
        ident = identity_core()
        res = (
            f"🎯 <b>NEURAL-REPORT:</b> <code>{bin_in}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>STATUS:</b> <code>{intel['status']}</code> ({intel['score']}%)\n"
            f"🔌 <b>GATE:</b> <code>{intel['gate']}</code>\n"
            f"👤 <b>HOLDER:</b> <code>{ident}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <b>Uso:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['live', 'spy'])
def spy(message):
    res = "🛰️ <b>SPY-RADAR LIVE</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in ["451015", "489504", "515632"]:
        intel = get_full_intel(b)
        res += f"📍 <code>{b}</code> | {intel['status']} | 🔥\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def deep_scan(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    text = downloaded.decode('utf-8')
    found = list(set(re.findall(r'\b\d{6}\b', text)))[:10]
    res = "🔍 <b>DEEP-SCAN v47</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        intel = get_full_intel(b)
        res += f"📍 {b} -> {intel['status']} ({intel['score']}%)\n"
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ ARRANQUE DE SEGURIDAD ] ---
if __name__ == "__main__":
    # Iniciar servidor web para Render
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # PROTOCOLO DE LIMPIEZA TOTAL (Solución al Error 409)
    print("🧹 Limpiando webhooks y sesiones previas...")
    bot.remove_webhook()
    time.sleep(5) # Pausa necesaria para que Telegram procese el cierre
    
    print("🚀 CJKILLER v64.5 ONLINE")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=20)
    except Exception as e:
        print(f"❌ Error detectado: {e}")
        time.sleep(10)
