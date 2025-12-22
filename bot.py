import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CONFIGURACIÓN MAESTRA ] ---
# Token actualizado para limpiar errores de sesión previos
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"

# --- [ NÚCLEO WEB ANTI-SHUTDOWN ] ---
app = Flask(__name__)
@app.route('/')
def home(): return "CJKILLER v66.7: OMNISCIENTE ONLINE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ INFRAESTRUCTURA DE DATOS ] ---
users_col = None
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, connect=False)
    db = client.get_database()
    users_col = db['users']
    print("📡 Base de Datos: Enlace activo.")
except:
    print("⚠️ Base de Datos: Modo offline temporal.")

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- [ MOTORES DE ÉLITE REINTEGRADOS ] ---

def luhn_check(n):
    """v44: Validación Matemática Rigurosa"""
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_complete_intel(bin_p):
    """v48: Oracle-Vision & Biometría"""
    score = random.randint(45, 99)
    vendas = ["VISA", "MASTERCARD", "AMEX"]
    levels = ["PLATINUM", "WORLD ELITE", "INFINITE", "BUSINESS"]
    gates = ["Stripe Auth", "Adyen", "Amazon Pay", "Shopify Elite"]
    status = "💎 PRIVATE" if score > 88 else "✅ HIGH SUCCESS"
    return {
        "status": status, "score": score, "gate": random.choice(gates),
        "vendor": random.choice(vendas), "level": random.choice(levels)
    }

def identity_core():
    """v50: Identity-Core (Datos de Holder Sincronizados)"""
    data = [
        {"n": "Alexander Rhodes", "a": "725 5th Ave", "c": "New York, NY", "z": "10022"},
        {"n": "Dominic Sterling", "a": "1060 West Addison St", "c": "Chicago, IL", "z": "60613"},
        {"n": "Julian Blackwood", "a": "1600 Amphitheatre Pkwy", "c": "Mountain View, CA", "z": "94043"},
        {"n": "Tristan Vance", "a": "1 Infinite Loop", "c": "Cupertino, CA", "z": "95014"}
    ]
    sel = random.choice(data)
    return f"{sel['n']} | {sel['a']} | {sel['c']} | {sel['z']}"

# --- [ PROTECCIÓN SENTINEL ANTI-BAN ] ---
user_last_msg = {}
def sentinel_alpha(uid):
    now = time.time()
    if uid in user_last_msg and now - user_last_msg[uid] < 3: return False
    user_last_msg[uid] = now
    return True

# --- [ COMANDOS DE DOMINIO ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    if users_col is not None:
        try:
            if not users_col.find_one({"user_id": uid}):
                users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA"})
        except: pass

    bot.reply_to(message, (
        "👑 <b>CJKILLER v66.7: OMNISCIENTE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>NEURAL-STRIKE v66</code>\n"
        "🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        "👤 <b>HOLDER:</b> <code>IDENTITY-CORE v50</code>\n"
        "🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Protocolo Génesis activo. El bot está en su nivel máximo.</i>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    if not sentinel_alpha(uid): return
    
    try:
        bin_in = re.findall(r'\d+', message.text)[0][:6]
        intel = get_complete_intel(bin_in)
        ident = identity_core()
        
        res = (
            f"🎯 <b>NEURAL-REPORT:</b> <code>{bin_in}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>STATUS:</b> <code>{intel['status']}</code> ({intel['score']}%)\n"
            f"💳 <b>INFO:</b> <code>{intel['vendor']} | {intel['level']}</code>\n"
            f"🔌 <b>GATEWAY:</b> <code>{intel['gate']}</code>\n"
            f"👤 <b>HOLDER:</b> <code>{ident}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        count = 0
        while count < 10:
            cc = f"{bin_in}{''.join([str(random.randint(0,9)) for _ in range(10)])}"
            if luhn_check(cc):
                res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
                count += 1
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <code>/precision [BIN]</code>")

@bot.message_handler(content_types=['document'])
def deep_scan(message):
    """v47: Escaneo Masivo"""
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    found = list(set(re.findall(r'\b\d{6}\b', downloaded.decode('utf-8'))))[:10]
    res = "🔍 <b>DEEP-SCAN v47 RESULTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        intel = get_complete_intel(b)
        res += f"📍 {b} -> {intel['status']} ({intel['score']}%)\n"
    res += "━━━━━━━━━━━━━━━━━━━━"
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ ARRANQUE DEFINITIVO ] ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Limpieza de Webhook sin cerrar sesión
    try:
        bot.remove_webhook()
        time.sleep(1)
    except: pass
    
    print("🚀 CJKILLER v66.7: TOTAL DOMINATION ONLINE")
    bot.infinity_polling(timeout=60, skip_pending=True)
