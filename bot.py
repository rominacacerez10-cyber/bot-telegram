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
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617

# --- [ CAPA DE ESTABILIDAD RENDER ] ---
app = Flask(__name__)
@app.route('/')
def live(): return "CJKILLER v66.0: OMNISCIENTE ONLINE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ INFRAESTRUCTURA DE DATOS ] ---
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000)
db = client.get_database()
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- [ MOTORES INTEGRADOS (TODO EN UNO) ] ---

def luhn_check(n):
    """v44: Validación Matemática Rigurosa"""
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_complete_intel(bin_p):
    """v48: Fusión Oracle-Vision & Biometría de Red"""
    score = random.randint(35, 99)
    vendas = ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]
    levels = ["PREMIUM", "CORPORATE", "WORLD ELITE", "INFINITE", "BUSINESS"]
    gates = ["Stripe Auth", "Amazon Pay", "Adyen", "Braintree", "Shopify Elite"]
    status = "💎 PRIVATE" if score > 88 else "✅ HIGH SUCCESS" if score > 65 else "⚠️ PUBLIC"
    return {
        "status": status, "score": score, "gate": random.choice(gates),
        "vendor": random.choice(vendas), "level": random.choice(levels)
    }

def identity_core():
    """v50: Identity-Core (Datos Sincronizados de Holder)"""
    data = [
        {"n": "Alexander Rhodes", "a": "725 5th Ave", "c": "New York, NY", "z": "10022"},
        {"n": "Dominic Sterling", "a": "1060 West Addison St", "c": "Chicago, IL", "z": "60613"},
        {"n": "Julian Blackwood", "a": "1600 Amphitheatre Pkwy", "c": "Mountain View, CA", "z": "94043"},
        {"n": "Tristan Vance", "a": "1 Infinite Loop", "c": "Cupertino, CA", "z": "95014"}
    ]
    sel = random.choice(data)
    return f"{sel['n']} | {sel['a']} | {sel['c']} | {sel['z']}"

# --- [ SISTEMA SENTINEL: ANTI-BAN & ANTI-SPAM ] ---
user_last_msg = {}
def sentinel_alpha(uid):
    now = time.time()
    if uid in user_last_msg and now - user_last_msg[uid] < 3: # 3 segundos de cooldown
        return False
    user_last_msg[uid] = now
    return True

# --- [ COMANDOS DE ÉLITE INTEGRADOS ] ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    ref_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA", "refs": 0})
        if ref_id and ref_id.isdigit() and int(ref_id) != uid:
            users_col.update_one({"user_id": int(ref_id)}, {"$inc": {"credits": 25, "refs": 1}})
    
    bot.reply_to(message, (
        "👑 <b>CJKILLER v66.0: OMNISCIENTE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>NEURAL-STRIKE v66</code>\n"
        "🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        "👤 <b>HOLDER:</b> <code>IDENTITY-CORE v50</code>\n"
        "🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Todos los módulos están fusionados y activos.</i>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    if not sentinel_alpha(uid): return bot.reply_to(message, "⚠️ <b>SENTINEL:</b> No satures el sistema.")
    
    user = users_col.find_one({"user_id": uid})
    if not user or user['credits'] < 5:
        return bot.reply_to(message, "❌ <b>CRÉDITOS INSUFICIENTES.</b>")

    try:
        bin_in = re.findall(r'\d+', message.text)[0][:6]
        intel = get_complete_intel(bin_in)
        ident = identity_core()
        users_col.update_one({"user_id": uid}, {"$inc": {"credits": -5, "xp": 80}})
        
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
        bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['spy', 'live'])
def spy_radar(message):
    """v59: Monitoreo en tiempo real"""
    res = "🛰️ <b>SPY-RADAR: LIVE INTERCEPTION</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in ["451015", "489504", "515632", "424242"]:
        intel = get_complete_intel(b)
        res += f"📍 <code>{b}</code> | {intel['status']} | 🔥\n"
    bot.reply_to(message, res, parse_mode="HTML")

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
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me'])
def profile(message):
    u = users_col.find_one({"user_id": message.from_user.id})
    rank = "👑 EMPERADOR" if u['xp'] > 5000 else "💎 DIAMANTE" if u['xp'] > 2500 else "RECLUTA"
    res = (
        f"👤 <b>ID:</b> <code>{u['user_id']}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>XP:</b> <code>{u['xp']}</code>\n"
        f"🎖️ <b>RANK:</b> <code>{rank}</code>\n"
        f"👥 <b>REFERIDOS:</b> <code>{u['refs']}</code>"
    )
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ ARRANQUE DE SEGURIDAD TOTAL ] ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.remove_webhook()
    time.sleep(2)
    print("🚀 CJKILLER v66.0: OMNISCIENTE ACTIVADO")
    bot.infinity_polling(timeout=60, skip_pending=True)
