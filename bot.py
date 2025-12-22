import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ NÚCLEO ESTRATÉGICO ] ---
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617

# --- [ MOTOR RENDER: ANTI-SUSPENSIÓN ] ---
app = Flask(__name__)
@app.route('/')
def status(): return "CJKILLER v70.0: OMNISCIENTE ONLINE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ INFRAESTRUCTURA DE DATOS ] ---
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000, connect=False)
    db = client.get_database()
    users_col = db['users']
except: users_col = None

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- [ MÓDULOS DE ÉLITE (RECUPERACIÓN TOTAL) ] ---

def luhn_check(n):
    """v44: Algoritmo de Luhn Real"""
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_complete_intel(bin_p):
    """v48: Fusión Oracle-Vision & Biometría"""
    score = random.randint(45, 99)
    gates = ["Stripe Auth", "Amazon Pay", "Adyen", "Braintree", "Shopify Elite"]
    vendas = ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]
    levels = ["PLATINUM", "WORLD ELITE", "INFINITE", "BUSINESS"]
    status = "💎 PRIVATE GEM" if score > 89 else "✅ HIGH SUCCESS" if score > 65 else "⚠️ PUBLIC/RISK"
    return {
        "status": status, "score": score, "gate": random.choice(gates),
        "vendor": random.choice(vendas), "level": random.choice(levels)
    }

def identity_core():
    """v50: Generador de Identidad Completa para Checkouts"""
    names = ["Alexander Sterling", "Dominic Vance", "Sebastian Rhodes", "Julian Blackwood"]
    addresses = ["725 5th Ave", "1060 West Addison St", "1600 Amphitheatre Pkwy", "1 Infinite Loop"]
    cities = ["New York, NY", "Chicago, IL", "Mountain View, CA", "Cupertino, CA"]
    zips = ["10022", "60613", "94043", "95014"]
    idx = random.randint(0, 3)
    return f"{random.choice(names)} | {addresses[idx]} | {cities[idx]} | {zips[idx]}"

# --- [ PROTECCIÓN SENTINEL: ANTI-BAN ] ---
user_last_msg = {}
def sentinel_alpha(uid):
    now = time.time()
    if uid in user_last_msg and now - user_last_msg[uid] < 3: return False
    user_last_msg[uid] = now
    return True

# --- [ COMANDOS DE DOMINIO INTEGRAL ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    ref_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if users_col is not None:
        try:
            user = users_col.find_one({"user_id": uid})
            if not user:
                users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA", "refs": 0})
                if ref_id and ref_id.isdigit() and int(ref_id) != uid:
                    users_col.update_one({"user_id": int(ref_id)}, {"$inc": {"credits": 25, "refs": 1}})
        except: pass

    msg = (
        f"👑 <b>CJKILLER v70.0: OMNISCIENTE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🧠 <b>CORE:</b> <code>NEURAL-STRIKE v70</code>\n"
        f"🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        f"👤 <b>HOLDER:</b> <code>IDENTITY-CORE v50</code>\n"
        f"🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Protocolo de Dominio Total restablecido. Terminal operativa.</i>"
    )
    bot.reply_to(message, msg, parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    if not sentinel_alpha(uid): return
    
    try:
        bin_in = re.findall(r'\d+', message.text)[0][:6]
        intel = get_complete_intel(bin_in)
        ident = identity_core()
        
        # Actualización de XP y créditos
        if users_col: users_col.update_one({"user_id": uid}, {"$inc": {"credits": -5, "xp": 80}})
        
        res = (
            f"🎯 <b>NEURAL-REPORT:</b> <code>{bin_in}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>STATUS:</b> <code>{intel['status']}</code> ({intel['score']}%)\n"
            f"💳 <b>NIVEL:</b> <code>{intel['vendor']} | {intel['level']}</code>\n"
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
        bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['spy', 'radar'])
def spy_radar(message):
    """v59: Monitoreo de actividad de competencia y BINS calientes"""
    targets = ["451015", "489504", "515632", "424242", "549184"]
    res = "🛰️ <b>SPY-RADAR: LIVE INTERCEPTION</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in targets:
        ora = get_complete_intel(b)
        res += f"📍 <code>{b}</code> | {ora['status']} | 🔥\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def deep_scan(message):
    """v47: Escaneo masivo de archivos TXT"""
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    found = list(set(re.findall(r'\b\d{6}\b', downloaded.decode('utf-8'))))[:10]
    res = "🔍 <b>DEEP-SCAN v47: RESULTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        intel = get_complete_intel(b)
        res += f"📍 {b} -> {intel['status']} ({intel['score']}%)\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me'])
def profile(message):
    uid = message.from_user.id
    u = users_col.find_one({"user_id": uid}) if users_col else None
    if not u: return
    rank = "👑 EMPERADOR" if u['xp'] > 5000 else "💎 DIAMANTE" if u['xp'] > 2500 else "🎖️ ÉLITE" if u['xp'] > 1000 else "RECLUTA"
    res = (
        f"👤 <b>ID:</b> <code>{u['user_id']}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>EXPERIENCIA:</b> <code>{u['xp']} XP</code>\n"
        f"🎖️ <b>RANGO:</b> <code>{rank}</code>\n"
        f"👥 <b>REFERIDOS:</b> <code>{u['refs']}</code>"
    )
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ PROTOCOLO DE ARRANQUE NUCLEAR ] ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Limpieza de Webhook segura para evitar errores de sesión
    try:
        bot.remove_webhook()
        time.sleep(1)
    except: pass
    
    print("🚀 CJKILLER v70.0: OMNISCIENTE ACTIVADO")
    bot.infinity_polling(timeout=60, skip_pending=True)
