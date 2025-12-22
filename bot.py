import telebot
import time
import random
import re
import threading
import os
from flask import Flask
from pymongo import MongoClient

# --- [ CONFIGURACIÓN ] ---
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"

app = Flask(__name__)
@app.route('/')
def home(): return "CJKILLER v70.1 ONLINE 👑", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- [ DATA CORE ] ---
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000, connect=False)
    db = client.get_database()
    users_col = db['users']
except: users_col = None

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- [ MÓDULOS INTEGRALES MANTENIDOS ] ---
def luhn_check(n):
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_intel(bin_p):
    score = random.randint(45, 99)
    return {"status": "💎 PRIVATE" if score > 88 else "✅ HIGH", "score": score, "gate": random.choice(["Stripe", "Adyen", "Shopify"]), "lvl": random.choice(["INFINITE", "PLATINUM"])}

def identity_core():
    data = [("Alex Rhodes", "725 5th Ave", "NY", "10022"), ("Dom Vance", "1060 W Addison", "IL", "60613")]
    sel = random.choice(data)
    return f"{sel[0]} | {sel[1]} | {sel[2]} | {sel[3]}"

# --- [ COMANDOS ] ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👑 <b>CJKILLER v70.1</b>\n━━━━━━━━━━━━━\n🧠 CORE v70 | 🛡️ SENTINEL v45\n👤 IDENTITY v50 | 🔮 ORACLE v48\n━━━━━━━━━━━━━", parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def gen(message):
    try:
        bin_in = re.findall(r'\d+', message.text)[0][:6]
        intel = get_intel(bin_in)
        res = f"🎯 <b>REPORT:</b> <code>{bin_in}</code>\n📊 {intel['status']} ({intel['score']}%)\n🔌 GATE: {intel['gate']}\n👤 HOLDER: {identity_core()}\n━━━━━━━━━━━━━\n"
        c = 0
        while c < 10:
            cc = f"{bin_in}{''.join([str(random.randint(0,9)) for _ in range(10)])}"
            if luhn_check(cc):
                res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
                c += 1
        bot.reply_to(message, res, parse_mode="HTML")
    except: pass

# --- [ ARRANQUE ANTI-CONFLICTO ] ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    
    print("⏳ Pausa de seguridad para evitar Error 409...")
    time.sleep(5) # <--- CRÍTICO: Da tiempo a que la instancia vieja muera en Render
    
    try:
        bot.remove_webhook()
    except: pass
    
    print("🚀 CJKILLER v70.1 ACTIVADO")
    bot.infinity_polling(timeout=60, skip_pending=True)
