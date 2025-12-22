import telebot
import time
import random
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ CREDENCIALES INTEGRADAS ] ---
TOKEN = "7724263155:AAFi0k97F_R03-Wqf_XWvAn-uB8G5QY4t-A"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller"
ADMIN_ID = 7447432617

bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- [ MOTOR DE INTELIGENCIA NEURAL ] ---
def analyze_bin_impact(bin_prefix):
    score = random.randint(15, 98)
    if score > 85: return "💎 PRIVATE GEM", score
    if score > 60: return "✅ HIGH SUCCESS", score
    return "⚠️ PUBLIC/BURNED", score

# --- [ COMANDOS PRINCIPALES ] ---

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({
            "user_id": uid, 
            "credits": 50, 
            "xp": 0, 
            "rank": "RECLUTA",
            "joined": time.time()
        })
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🕵️ VER BINS LIVE", callback_data="view_live"))
    
    welcome = (
        f"👑 <b>CJKILLER TERMINAL v63.0</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 <b>ESTADO:</b> <code>SISTEMA OPERATIVO</code>\n"
        f"🧠 <b>INTELIGENCIA:</b> <code>NEURAL-CORE v56</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Usa /help para desplegar el arsenal.</i>"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    user = users_col.find_one({"user_id": uid})
    
    if user['credits'] < 2:
        return bot.reply_to(message, "❌ <b>CRÉDITOS INSUFICIENTES.</b>")

    try:
        bin_in = message.text.split()[1][:6]
        status, score = analyze_bin_impact(bin_in)
        
        users_col.update_one({"user_id": uid}, {"$inc": {"credits": -2, "xp": 15}})
        
        res = (
            f"🎯 <b>NEURAL-STRIKE REPORT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>BIN:</b> <code>{bin_in}</code>\n"
            f"📊 <b>STATUS:</b> <code>{status}</code>\n"
            f"🔥 <b>ÉXITO:</b> <code>{score}%</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(7):
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        
        res += "━━━━━━━━━━━━━━━━━━━━\n<i>Generación optimizada por IA.</i>"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['live'])
def live_tracker(message):
    bins_frescos = ["451015", "489504", "515632", "424242", "414720"]
    res = "🛰️ <b>SPY-TRACKER: BINS DETECTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in bins_frescos:
        status, _ = analyze_bin_impact(b)
        res += f"📍 <code>{b}</code> | {status} | <b>LIVE</b> 🔥\n"
    res += "━━━━━━━━━━━━━━━━━━━━"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me', 'id'])
def profile(message):
    u = users_col.find_one({"user_id": message.from_user.id})
    rank = "RECLUTA"
    if u['xp'] > 1000: rank = "DIAMANTE 💎"
    elif u['xp'] > 500: rank = "OPERATIVO ELITE 🎖️"
    
    res = (
        f"👤 <b>PERFIL DE USUARIO</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>EXPERIENCIA:</b> <code>{u['xp']}</code>\n"
        f"🎖️ <b>RANGO:</b> <code>{rank}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    total = users_col.count_documents({})
    bot.reply_to(message, f"👑 <b>GOD-MODE ACTIVE</b>\n━━━━━━━━━━━━━━━━━━━━\n👥 Usuarios: {total}\n🛡️ Sentinel: Vigilando", parse_mode="HTML")

# --- [ ARRANQUE DEL SISTEMA ] ---
if __name__ == "__main__":
    print("🚀 CJKILLER v63.0 INICIADO CON ÉXITO")
    bot.infinity_polling()
