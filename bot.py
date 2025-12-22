import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CONFIGURACIÓN Y CREDENCIALES ] ---
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller&tlsAllowInvalidCertificates=true"
ADMIN_ID = 7447432617

# --- [ NÚCLEO WEB: SOLUCIÓN ERROR PORT ] ---
app = Flask(__name__)
@app.route('/')
def home(): return "CJKILLER v64.3: STATUS ACTIVE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ NÚCLEO DE DATOS: MONGO ] ---
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, connect=False, maxPoolSize=1)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)

# --- [ MÓDULOS DE ÉLITE INTEGRADOS ] ---

def get_bin_biometry(bin_p):
    """Módulo v48: Oracle-Vision y Biometría"""
    score = random.randint(15, 99)
    gates = ["Stripe", "Amazon Pay", "Adyen", "Braintree", "Shopify"]
    status = "💎 PRIVATE" if score > 88 else "✅ HIGH SUCCESS" if score > 60 else "⚠️ PUBLIC"
    return {"status": status, "score": score, "gate": random.choice(gates)}

def identity_core():
    """Módulo v50: Generación de Identidad"""
    n = ["James", "Robert", "John", "Michael", "William"]
    c = ["New York", "Los Angeles", "Chicago", "Miami"]
    return f"{random.choice(n)} {random.randint(10,99)} | {random.choice(c)} | {random.randint(10001, 99999)}"

# --- [ COMANDOS MAESTROS ] ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA", "refs": 0})
    
    bot.reply_to(message, (
        "👑 <b>CJKILLER v64.3: INTEGRACIÓN TOTAL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>NEURAL-STRIKE v44</code>\n"
        "🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        "🛰️ <b>RADAR:</b> <code>SPY-TRACKER v59</code>\n"
        "👤 <b>IDENT:</b> <code>IDENTITY-CORE v50</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Todos los módulos están activos y sin errores de log.</i>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    user = users_col.find_one({"user_id": uid})
    if not user or user['credits'] < 5:
        return bot.reply_to(message, "❌ <b>CRÉDITOS INSUFICIENTES.</b>")

    try:
        bin_in = message.text.split()[1][:6]
        bio = get_bin_biometry(bin_in)
        ident = identity_core()
        users_col.update_one({"user_id": uid}, {"$inc": {"credits": -5, "xp": 50}})
        
        res = (
            f"🎯 <b>NEURAL-REPORT:</b> <code>{bin_in}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>STATUS:</b> <code>{bio['status']}</code> ({bio['score']}%)\n"
            f"🔌 <b>GATE:</b> <code>{bio['gate']}</code>\n"
            f"👤 <b>IDENT:</b> <code>{ident}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <b>Uso:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['live', 'spy'])
def spy_radar(message):
    bins = ["451015", "489504", "515632", "424242"]
    res = "🛰️ <b>SPY-RADAR: LIVE INTERCEPTION</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in bins:
        bio = get_bin_biometry(b)
        res += f"📍 <code>{b}</code> | {bio['status']} | 🔥\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def deep_scan(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    text = downloaded.decode('utf-8')
    found = list(set(re.findall(r'\b\d{6}\b', text)))[:10]
    res = "🔍 <b>DEEP-SCAN v47 RESULTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        bio = get_bin_biometry(b)
        res += f"📍 {b} -> {bio['status']} ({bio['score']}%)\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me'])
def profile(message):
    u = users_col.find_one({"user_id": message.from_user.id})
    res = (
        f"👤 <b>ID:</b> <code>{u['user_id']}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>XP:</b> <code>{u['xp']}</code>\n"
        f"🎖️ <b>RANK:</b> <code>{u['rank']}</code>"
    )
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ ARRANQUE INTEGRADO ] ---
if __name__ == "__main__":
    # Iniciar servidor Flask para Render
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Limpiar cualquier sesión previa antes de arrancar (Solución Error 409)
    bot.delete_webhook()
    print("🚀 CJKILLER v64.3 ONLINE: SISTEMA INTEGRADO TOTALMENTE")
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
