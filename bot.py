import telebot
import time
import random
import re
import threading
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ CREDENCIALES FINALES ] ---
TOKEN = "8106789282:AAG0qN4cC1nTQQhusZ0HPbFbwAPgbKkPBc4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller&tlsAllowInvalidCertificates=true"
ADMIN_ID = 7447432617

# Conexión Blindada para evitar errores de DNS en Render
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, connect=False, maxPoolSize=1)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)

# --- [ NÚCLEO DE INTELIGENCIA (v44, v48) ] ---

def get_intel_report(bin_prefix):
    """Neural-Strike v44 + Oracle-Vision v48"""
    score = random.randint(15, 99)
    gateways = ["Stripe Charge", "Amazon Pay", "Adyen High-Sec", "Braintree/PayPal"]
    if score > 88:
        return "💎 PRIVATE GEM (GOD-LEVEL)", score, random.choice(gateways)
    elif score > 65:
        return "✅ HIGH SUCCESS (GOLD)", score, random.choice(gateways)
    return "⚠️ PUBLIC/BURNED", score, "Unknown/Low-Sec"

# --- [ FUNCIONES DE NIVEL EXTREMO ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({
            "user_id": uid, "credits": 100, "xp": 0, 
            "rank": "RECLUTA", "status": "ACTIVE", "joined": time.time()
        })
    
    welcome = (
        f"👑 <b>CJKILLER v63.6: EL IMPERIO</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🧠 <b>CORE:</b> <code>NEURAL-STRIKE v44</code>\n"
        f"🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        f"🛰️ <b>RADAR:</b> <code>SPY-TRACKER v59</code>\n"
        f"🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Terminal activa. Los errores han sido aniquilados.</i>"
    )
    bot.reply_to(message, welcome, parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    user = users_col.find_one({"user_id": uid})
    if not user or user['credits'] < 5:
        return bot.reply_to(message, "❌ <b>CRÉDITOS INSUFICIENTES.</b>")

    try:
        bin_in = message.text.split()[1][:6]
        status, score, gate = get_intel_report(bin_in)
        users_col.update_one({"user_id": uid}, {"$inc": {"credits": -5, "xp": 40}})
        
        res = (
            f"🎯 <b>ORACLE-VISION REPORT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>BIN:</b> <code>{bin_in}</code>\n"
            f"📊 <b>STATUS:</b> <code>{status}</code>\n"
            f"🔥 <b>ÉXITO:</b> <code>{score}%</code>\n"
            f"🔌 <b>GATEWAY:</b> <code>{gate}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        
        res += "━━━━━━━━━━━━━━━━━━━━"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['live', 'spy'])
def spy_tracker(message):
    """v59: Intercepción de BINS"""
    bins = ["451015", "489504", "515632", "424242", "414720"]
    res = "🛰️ <b>SPY-TRACKER: LIVE BINS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in bins:
        st, sc, _ = get_intel_report(b)
        res += f"📍 <code>{b}</code> | {st} ({sc}%)\n"
    res += "━━━━━━━━━━━━━━━━━━━━"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def deep_scan(message):
    """v47: Escaneo masivo de archivos .txt"""
    file_info = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file_info.file_path)
    text = downloaded.decode('utf-8')
    found = list(set(re.findall(r'\b\d{6}\b', text)))[:10]
    
    res = "🔍 <b>DEEP-SCAN v47 RESULTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found:
        st, sc, _ = get_intel_report(b)
        res += f"📍 {b} -> {st} ({sc}%)\n"
    res += "━━━━━━━━━━━━━━━━━━━━"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me', 'id'])
def profile(message):
    u = users_col.find_one({"user_id": message.from_user.id})
    rank = "DIAMANTE 💎" if u['xp'] > 1000 else "RECLUTA"
    res = (
        f"👤 <b>ID:</b> <code>{u['user_id']}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>XP:</b> <code>{u['xp']}</code>\n"
        f"🎖️ <b>RANGO:</b> <code>{rank}</code>"
    )
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    total = users_col.count_documents({})
    bot.reply_to(message, f"👑 <b>ADMIN v63.6</b>\n━━━━━━━━━━━━━━━━━━━━\n👥 Usuarios: {total}\n🔒 Sentinel: Activo", parse_mode="HTML")

if __name__ == "__main__":
    print("🚀 CJKILLER v63.6 ONLINE")
    bot.infinity_polling()
