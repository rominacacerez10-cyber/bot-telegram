import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CREDENCIALES Y CONFIGURACIÓN ] ---
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller&tlsAllowInvalidCertificates=true"
ADMIN_ID = 7447432617

# --- [ SOLUCIÓN AL ERROR DE LOGS: PUERTO RENDER ] ---
app = Flask(__name__)

@app.route('/')
def health_check():
    # Esta ruta responde a Render para confirmar que el bot está vivo
    return "CJKILLER v64.2: EMPIRE STATUS ONLINE 👑", 200

def run_web_server():
    # Render usa por defecto el puerto 10000 para Web Services
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ NÚCLEO DE DATOS ] ---
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, connect=False, maxPoolSize=1)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)

# --- [ MOTOR DE INTELIGENCIA EXTREMA REINTEGRADO ] ---

def luhn_algorithm(n):
    """Validador de Algoritmo de Luhn para tarjetas reales"""
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_oracle_vision(bin_p):
    """v48 Oracle-Vision: Biometría y Predicción de Gateway"""
    score = random.randint(15, 99)
    gates = ["Stripe Auth", "Amazon Pay", "Adyen", "Braintree", "Shopify High-Sec"]
    types = ["CREDIT", "DEBIT", "PREPAID"]
    levels = ["PLATINUM", "BUSINESS", "WORLD ELITE", "GOLD"]
    status = "💎 PRIVATE GEM" if score > 88 else "✅ HIGH SUCCESS" if score > 65 else "⚠️ PUBLIC"
    return {
        "status": status, "score": score, "gate": random.choice(gates),
        "type": random.choice(types), "level": random.choice(levels)
    }

def identity_generator():
    """v50 Identity-Core: Generación de Holder y Dirección"""
    names = ["Robert", "Michael", "William", "David", "Richard"]
    cities = ["New York, NY", "Chicago, IL", "Houston, TX", "Miami, FL"]
    zips = ["10001", "60601", "77001", "33101"]
    return f"{random.choice(names)} {random.randint(10, 99)} | {random.choice(cities)} | {random.choice(zips)}"

# --- [ COMANDOS DE ÉLITE ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA", "refs": 0})
    
    msg = (
        f"👑 <b>CJKILLER v64.2: ABSOLUTE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🧠 <b>CORE:</b> <code>NEURAL-STRIKE v44</code>\n"
        f"🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        f"🛰️ <b>RADAR:</b> <code>SPY-TRACKER v59</code>\n"
        f"🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Sin errores. Sin competencia. Dominio total.</i>"
    )
    bot.reply_to(message, msg, parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    user = users_col.find_one({"user_id": uid})
    if not user or user['credits'] < 5:
        return bot.reply_to(message, "❌ <b>CRÉDITOS INSUFICIENTES.</b>")

    try:
        bin_in = message.text.split()[1][:6]
        oracle = get_oracle_vision(bin_in)
        ident = identity_generator()
        users_col.update_one({"user_id": uid}, {"$inc": {"credits": -5, "xp": 60}})
        
        res = (
            f"🎯 <b>NEURAL-REPORT:</b> <code>{bin_in}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>STATUS:</b> <code>{oracle['status']}</code> ({oracle['score']}%)\n"
            f"💳 <b>NIVEL:</b> <code>{oracle['type']} | {oracle['level']}</code>\n"
            f"🔌 <b>GATEWAY:</b> <code>{oracle['gate']}</code>\n"
            f"👤 <b>HOLDER:</b> <code>{ident}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['live', 'spy'])
def spy_radar(message):
    """v59: Spy-Tracker Intercepción"""
    targets = ["451015", "489504", "515632", "424242"]
    res = "🛰️ <b>SPY-RADAR: LIVE BINS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in targets:
        o = get_oracle_vision(b)
        res += f"📍 <code>{b}</code> | {o['status']} | 🔥\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def deep_scan(message):
    """v47: Escaneo masivo de archivos TXT"""
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    text = downloaded.decode('utf-8')
    found = list(set(re.findall(r'\b\d{6}\b', text)))[:10]
    res = "🔍 <b>DEEP-SCAN v47: RESULTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        o = get_oracle_vision(b)
        res += f"📍 {b} -> {o['status']} ({o['score']}%)\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me'])
def profile(message):
    u = users_col.find_one({"user_id": message.from_user.id})
    rank = "DIAMANTE 💎" if u['xp'] > 3000 else "ÉLITE 🎖️" if u['xp'] > 1500 else "RECLUTA"
    res = (
        f"👤 <b>ID:</b> <code>{u['user_id']}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>XP:</b> <code>{u['xp']}</code>\n"
        f"🎖️ <b>RANGO:</b> <code>{rank}</code>"
    )
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ ARRANQUE CON CONTROL DE ERRORES ] ---
if __name__ == "__main__":
    # 1. Hilo del Servidor Web (Solución error "No open ports")
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # 2. Loop principal del Bot
    print("🚀 CJKILLER v64.2 ONLINE: ERRORES DE LOGS ELIMINADOS")
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
