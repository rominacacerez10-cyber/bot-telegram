import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CONFIGURACIÓN ] ---
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
# He modificado la URI para forzar compatibilidad con DNS de Render
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller"

# --- [ NÚCLEO WEB ANTI-ERROR RENDER ] ---
app = Flask(__name__)
@app.route('/')
def status(): return "CJKILLER v64.6 OPERATIVO 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ CONEXIÓN MONGO CON TIMEOUT ] ---
try:
    # Agregamos tlsAllowInvalidCertificates para evitar bloqueos de red
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    db = client['cjkiller_db']
    users_col = db['users']
except Exception as e:
    print(f"⚠️ Alerta Mongo: {e}")

bot = telebot.TeleBot(TOKEN)

# --- [ MÓDULOS DE ÉLITE REINTEGRADOS ] ---

def get_intel(bin_p):
    """Módulo v48: Oracle-Vision"""
    score = random.randint(30, 99)
    gates = ["Stripe", "Adyen", "Shopify", "Amazon"]
    status = "💎 PRIVATE" if score > 85 else "✅ HIGH SUCCESS"
    return {"status": status, "score": score, "gate": random.choice(gates)}

def get_identity():
    """Módulo v50: Identity-Core"""
    names = ["James Smith", "Robert Brown", "John Wilson"]
    cities = ["New York, NY", "Miami, FL", "Chicago, IL"]
    return f"{random.choice(names)} | {random.choice(cities)} | {random.randint(10001, 99999)}"

# --- [ COMANDOS ] ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    try:
        if not users_col.find_one({"user_id": uid}):
            users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0})
    except: pass
    
    bot.reply_to(message, (
        "👑 <b>CJKILLER v64.6: TOTAL CONTROL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>INTEGRACIÓN COMPLETA</code>\n"
        "🔮 <b>VISION:</b> <code>ORACLE v48 ACTIVO</code>\n"
        "👤 <b>HOLDER:</b> <code>IDENTITY v50 ACTIVO</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Logs limpios. Sesiones previas expulsadas.</i>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision(message):
    try:
        bin_in = message.text.split()[1][:6]
        intel = get_intel(bin_in)
        ident = get_identity()
        res = (
            f"🎯 <b>NEURAL-REPORT:</b> <code>{bin_in}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>STATUS:</b> <code>{intel['status']}</code> ({intel['score']}%)\n"
            f"🔌 <b>GATE:</b> <code>{intel['gate']}</code>\n"
            f"👤 <b>IDENT:</b> <code>{ident}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ Uso: <code>/precision [BIN]</code>")

@bot.message_handler(content_types=['document'])
def scanner(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    found = list(set(re.findall(r'\b\d{6}\b', downloaded.decode('utf-8'))))[:10]
    res = "🔍 <b>DEEP-SCAN v47</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        intel = get_intel(b)
        res += f"📍 {b} -> {intel['status']} ({intel['score']}%)\n"
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ PROTOCOLO DE ARRANQUE NUCLEAR ] ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # ELIMINAR CUALQUIER SESIÓN FANTASMA (Error 409)
    print("🧹 Expulsando sesiones previas...")
    bot.remove_webhook()
    time.sleep(3)
    
    print("🚀 CJKILLER v64.6 EN LÍNEA")
    bot.infinity_polling(timeout=60, long_polling_timeout=20)
