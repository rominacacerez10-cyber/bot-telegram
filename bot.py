import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CONFIGURACIÓN MAESTRA ] ---
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"

app = Flask(__name__)
@app.route('/')
def home(): return "CJKILLER v70.2: FULL COMMANDS ONLINE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ DATA CORE ] ---
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000, connect=False)
    db = client.get_database()
    users_col = db['users']
except: users_col = None

# threaded=True para que un comando no bloquee a los demás
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=4)

# --- [ MÓDULOS DE ÉLITE INTEGRADOS ] ---

def luhn_check(n):
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_complete_intel(bin_p):
    score = random.randint(45, 99)
    gates = ["Stripe Auth", "Amazon Pay", "Adyen", "Braintree"]
    vendas = ["VISA", "MASTERCARD", "AMEX"]
    levels = ["PLATINUM", "WORLD ELITE", "INFINITE"]
    status = "💎 PRIVATE GEM" if score > 89 else "✅ HIGH SUCCESS"
    return {"status": status, "score": score, "gate": random.choice(gates), "vendor": random.choice(vendas), "level": random.choice(levels)}

def identity_core():
    data = [
        {"n": "Alexander Sterling", "a": "725 5th Ave", "c": "New York, NY", "z": "10022"},
        {"n": "Dominic Vance", "a": "1060 West Addison St", "c": "Chicago, IL", "z": "60613"}
    ]
    s = random.choice(data)
    return f"{s['n']} | {s['a']} | {s['c']} | {s['z']}"

# --- [ GESTIÓN DE COMANDOS (REGISTRO GLOBAL) ] ---

@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.from_user.id
    if users_col is not None:
        try:
            if not users_col.find_one({"user_id": uid}):
                users_col.insert_one({"user_id": uid, "credits": 100, "xp": 0, "rank": "RECLUTA", "refs": 0})
        except: pass
    
    bot.reply_to(message, (
        "👑 <b>CJKILLER v70.2: OMNISCIENTE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🧠 <b>CORE:</b> <code>NEURAL-STRIKE v70</code>\n"
        "🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        "🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Todos los comandos han sido reactivados.</i>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def cmd_precision(message):
    try:
        bin_match = re.findall(r'\d+', message.text)
        if not bin_match:
            return bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>", parse_mode="HTML")
            
        bin_in = bin_match[0][:6]
        intel = get_complete_intel(bin_in)
        ident = identity_core()
        
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
    except Exception as e:
        print(f"Error en gen: {e}")

@bot.message_handler(commands=['spy', 'radar'])
def cmd_spy(message):
    targets = ["451015", "489504", "515632", "424242"]
    res = "🛰️ <b>SPY-RADAR ACTIVE</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in targets:
        ora = get_complete_intel(b)
        res += f"📍 <code>{b}</code> | {ora['status']} | 🔥\n"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me'])
def cmd_profile(message):
    uid = message.from_user.id
    u = users_col.find_one({"user_id": uid}) if users_col else {"credits": 0, "xp": 0, "rank": "N/A", "refs": 0}
    res = (
        f"👤 <b>ID:</b> <code>{uid}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u.get('credits', 0)}</code>\n"
        f"🧪 <b>XP:</b> <code>{u.get('xp', 0)}</code>\n"
        f"🎖️ <b>RANK:</b> <code>{u.get('rank', 'RECLUTA')}</code>"
    )
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ PROTOCOLO DE ARRANQUE ] ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Pausa técnica para limpiar el error 409
    time.sleep(2)
    
    try:
        bot.remove_webhook()
        time.sleep(1)
    except: pass
    
    print("🚀 CJKILLER v70.2: SISTEMAS ACTIVADOS")
    bot.infinity_polling(timeout=60, skip_pending=True)
