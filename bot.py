import telebot
from flask import Flask
import threading
import os
import requests
import time
import random

# --- CONFIGURACIÓN FINAL CJkiller ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
ADMIN_ID = 7012561892 
AUTHORIZED_USERS = [ADMIN_ID] 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- MEMORIA Y ESTADÍSTICAS ---
stats = {"chks": 0, "gens": 0, "start_time": time.time()}
last_use = {}

def log_to_admin(action, detail):
    """Envía un respaldo de cada acción al Admin"""
    try:
        log_msg = f"📂 **LOG DE ACTIVIDAD**\n🔹 **Acción:** {action}\n🔹 **Detalle:** `{detail}`\n🔹 **Hora:** {time.strftime('%H:%M:%S')}"
        bot.send_message(ADMIN_ID, log_msg, parse_mode="Markdown")
    except: pass

def luhn_check(n):
    r = [int(ch) for ch in n][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

def generate_cards(bin_str, amount=10):
    cards = []
    while len(cards) < amount:
        cc = bin_str + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_str))])
        if luhn_check(cc): cards.append(cc)
    return cards

# --- RUTAS FLASK ---
@app.route('/')
def index(): 
    return "CJkiller ULTIMATE v7.0 - SYSTEM ONLINE"

# --- COMANDOS DEL BOT ---
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id not in AUTHORIZED_USERS: return
    menu = (
        "💎 **CJkiller ULTIMATE v7.0** 💎\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🛠️ `/chk` - Scanner de Precisión\n"
        "🎲 `/gen` - Generador & Auto-Log\n"
        "📊 `/stats` - Rendimiento\n"
        "🧹 `/limpiar` - Wipe History\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "✅ **Status:** `Privado & Activo`"
    )
    bot.reply_to(message, menu, parse_mode="Markdown")

@bot.message_handler(commands=['chk'])
def chk_cmd(message):
    if message.from_user.id not in AUTHORIZED_USERS: return
    try:
        cc_full = message.text.split(maxsplit=1)[1]
        sent = bot.reply_to(message, "📡 `Extrayendo datos de la Matrix...`", parse_mode="Markdown")
        
        bin_n = cc_full.split('|')[0][:6]
        res = requests.get(f"https://lookup.binlist.net/{bin_n}")
        d = res.json() if res.status_code == 200 else {}
        
        stats["chks"] += 1
        log_to_admin("SCANNER", cc_full)

        report = (
            f"🛡️ **ULTIMATE SCAN**\n━━━━━━━━━━━━━━\n"
            f"💳 `{cc_full}`\n"
            f"🏛️ **Banco:** {d.get('bank',{}).get('name','N/A')}\n"
            f"🌎 **País:** {d.get('country',{}).get('name','')} {d.get('country',{}).get('emoji','')}\n"
            f"📑 **Tipo:** {d.get('scheme','?').upper()} - {d.get('type','?').upper()}\n"
            f"━━━━━━━━━━━━━━\n✅ **SUCCESS**"
        )
        bot.edit_message_text(report, chat_id=sent.chat.id, message_id=sent.message_id, parse_mode="Markdown")
    except: bot.reply_to(message, "❌ Formato: `/chk tarjeta|mes|año|cvv`")

@bot.message_handler(commands=['gen'])
def gen_cmd(message):
    if message.from_user.id not in AUTHORIZED_USERS: return
    try:
        bin_in = message.text.split(maxsplit=1)[1].split('|')[0][:12]
        cards = generate_cards(bin_in)
        stats["gens"] += 1
        
        res = f"🎲 **ULTIMATE GEN**\n`BIN: {bin_in}`\n━━━━━━━━━━━━━━\n"
        for card in cards:
            line = f"{card}|01|2027|{random.randint(100,999)}"
            res += f"💳 `{line}`\n"
        
        bot.reply_to(message, res + "━━━━━━━━━━━━━━", parse_mode="Markdown")
        log_to_admin("GENERACIÓN", f"BIN: {bin_in}")
    except: bot.reply_to(message, "❌ Use: `/gen bin` (ej: 454021)")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id not in AUTHORIZED_USERS: return
    uptime = round((time.time() - stats["start_time"]) / 3600, 2)
    bot.reply_to(message, f"📊 **HISTORIAL DE USO**\n\n✅ Total Chk: `{stats['chks']}`\n🎲 Total Gen: `{stats['gens']}`\n⏱️ Uptime: `{uptime}h`", parse_mode="Markdown")

@bot.message_handler(commands=['limpiar'])
def clear(message):
    if message.from_user.id not in AUTHORIZED_USERS: return
    bot.send_message(message.chat.id, "🧹 **Limpiando rastro del chat...**")
    for i in range(message.message_id, message.message_id - 50, -1):
        try: bot.delete_message(message.chat.id, i)
        except: pass

# --- SISTEMA KEEP-ALIVE (EVITA SUSPENSIÓN) ---
def keep_alive():
    while True:
        try:
            # URL de tu proyecto en Render para que no se apague
            requests.get("https://cjkiller-bot.onrender.com")
        except: pass
        time.sleep(600) # Revisa cada 10 minutos

# --- INICIO DE HILOS ---
threading.Thread(target=keep_alive, daemon=True).start()
threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
