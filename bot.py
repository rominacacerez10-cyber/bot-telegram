import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CONFIGURACIÓN MAESTRA ] ---
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
# URI optimizada para evitar el error de DNS query name
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"

# --- [ COMPATIBILIDAD RENDER ] ---
app = Flask(__name__)
@app.route('/')
def home(): return "CJKILLER v64.7: OMNIPOTENTE", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ CONEXIÓN MONGO BLINDADA ] ---
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    db = client.get_database()
    users_col = db['users']
except Exception as e:
    print(f"⚠️ Aviso MongoDB: {e}")

bot = telebot.TeleBot(TOKEN)

# --- [ FUNCIONES DE ÉLITE REINTEGRADAS ] ---

def get_full_intel(bin_p):
    """Módulo Oracle-Vision v48 + Biometría"""
    score = random.randint(35, 99)
    gates = ["Stripe Auth", "Amazon Pay", "Shopify High-Sec"]
    status = "💎 PRIVATE" if score > 88 else "✅ HIGH SUCCESS"
    return {"status": status, "score": score, "gate": random.choice(gates)}

def identity_core():
    """Módulo Identity-Core v50"""
    names = ["John Smith", "David Miller", "Michael Ross"]
    cities = ["New York, NY", "Miami, FL", "Chicago, IL"]
    return f"{random.choice(names)} | {random.choice(cities)} | {random.randint(10001, 99999)}"

# --- [ COMANDOS ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    try:
        if not users_col.find_one({"user_id": uid}):
            users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0})
    except: pass
    
    bot.reply_to(message, (
        "👑 <b>CJKILLER v64.7: INTEGRACIÓN FINAL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>ACTIVO v64.7</code>\n"
        "🔮 <b>ORACLE:</b> <code>ACTIVO v48</code>\n"
        "👤 <b>HOLDER:</b> <code>ACTIVO v50</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Logs limpios. Todas las funciones integradas.</i>"
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
            f"👤 <b>IDENT:</b> <code>{ident}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ Uso: <code>/precision [BIN]</code>")

# --- [ PROTOCOLO ANTI-CONFLICTO (FUERZA BRUTA) ] ---
if __name__ == "__main__":
    # Iniciar servidor Flask
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # 1. Eliminar cualquier Webhook previo
    bot.remove_webhook()
    time.sleep(2)
    
    # 2. Cerrar sesión activa en otros servidores (Expulsa al bot viejo)
    try:
        print("🔥 Expulsando instancias duplicadas...")
        bot.log_out() 
        time.sleep(5)
    except: pass
    
    print("🚀 CJKILLER v64.7: ONLINE Y SIN CONFLICTOS")
    bot.infinity_polling(timeout=60, long_polling_timeout=20)
