import telebot
import time
import random
import re
import threading
import os
import string
import logging
from flask import Flask
from pymongo import MongoClient
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException

# --- [ CONFIGURACIÓN MAESTRA ] ---
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617 
LOG_CHANNEL = -1002319403816

app = Flask(__name__)
MAINTENANCE = False
SHADOW_REALM = set() 
ANTIFLOOD_CACHE = {}

# --- [ CLASE DE BASE DE DATOS - CORREGIDA AL 1000% ] ---
class GlobalDatabase:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000)
            self.db = self.client.get_database()
            self.users = self.db['users']  # Variable correcta
            self.keys = self.db['keys']
            self.blacklist = self.db['blacklist']
            self.logs = self.db['action_logs']
            self.users.create_index("user_id", unique=True)
            print("✅ Conexión a base de datos exitosa.")
        except Exception as e:
            print(f"❌ Error en DB: {e}")

    def get_user(self, uid):
        # Corregido: antes decía 'self.u', ahora 'self.users'
        return self.users.find_one({"user_id": uid})

    def update_user(self, uid, data):
        self.users.update_one({"user_id": uid}, {"$set": data}, upsert=True)

db_core = GlobalDatabase()
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=1000)

# --- [ FUNCIONES DE VALIDACIÓN ] ---

def validate_luhn(card_number):
    r = [int(ch) for ch in str(card_number)][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def check_vip_status(uid):
    if uid == ADMIN_ID: return True
    user = db_core.get_user(uid)
    return user and user.get('expiry') and user['expiry'] > datetime.now()

def get_rank(uid):
    if uid == ADMIN_ID: return "👑 OVERLORD-GOD"
    u = db_core.get_user(uid)
    if not u: return "🔰 RECLUTA"
    refs = u.get('referrals', 0)
    if refs >= 100: return "💎 LEYENDA"
    return u.get('rank', "🔰 RECLUTA")

# --- [ COMANDOS DE ADMINISTRACIÓN ] ---

@bot.message_handler(commands=['panel'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    count = db_core.users.count_documents({})
    bot.reply_to(message, (
        f"🌌 <b>CJKILLER APEX CORE v22.0</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Usuarios: <code>{count}</code>\n"
        f"⚙️ Estado: <code>{'MANTENIMIENTO' if MAINTENANCE else 'ONLINE'}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👉 <code>/db_exec [comando]</code>\n"
        f"👉 <code>/genkey [dias] [cantidad]</code>\n"
        f"👉 <code>/add_vip [id] [dias]</code>\n"
        f"👉 <code>/shadow [id]</code>\n"
        f"👉 <code>/bc [mensaje]</code>\n"
        f"👉 <code>/set_identity Nombre | Bio</code>"
    ), parse_mode="HTML")

@bot.message_handler(commands=['db_exec'])
def db_exec(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        query = message.text.replace('/db_exec ', '')
        exec_env = {'db': db_core.db, 'users': db_core.users, 'bot': bot, 'datetime': datetime}
        exec(query, exec_env)
        bot.reply_to(message, "✅ <b>NÚCLEO MODIFICADO.</b>")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

# --- [ MOTOR DE GENERACIÓN ] ---

@bot.message_handler(commands=['precision', 'gen'])
def strike(message):
    uid = message.from_user.id
    if (MAINTENANCE and uid != ADMIN_ID) or db_core.blacklist.find_one({"user_id": uid}): return
    if not check_vip_status(uid): return bot.reply_to(message, "⚠️ **PREMIUM REQUERIDO.**")

    # Anti-Flood
    now = time.time()
    if uid in ANTIFLOOD_CACHE and now - ANTIFLOOD_CACHE[uid] < 3:
        return bot.reply_to(message, "⏳ Espera 3s.")
    ANTIFLOOD_CACHE[uid] = now

    try:
        bin_in = re.findall(r'\d+', message.text)[0][:6]
        load = bot.reply_to(message, "🌀 **PROCESANDO...**", parse_mode="Markdown")
        
        is_shadow = uid in SHADOW_REALM
        hits = []
        while len(hits) < 10:
            cc = f"{bin_in}{''.join([str(random.randint(0,9)) for _ in range(10)])}"
            if validate_luhn(cc) or is_shadow:
                hits.append(f"`{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}`")
        
        bot.edit_message_text("\n".join(hits), message.chat.id, load.message_id, parse_mode="Markdown")
        db_core.users.update_one({"user_id": uid}, {"$inc": {"hits": 1}})
    except: bot.reply_to(message, "❌ BIN Inválido.")

# --- [ START Y REFERIDOS ] ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    username = message.from_user.username or "User"
    
    if not db_core.get_user(uid):
        ref_id = None
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            ref_id = int(args[1])
        
        db_core.update_user(uid, {
            "user_id": uid, "username": username, "referrals": 0,
            "hits": 0, "rank": "🔰 RECLUTA", "joined": datetime.now(),
            "rewarded": False, "referred_by": ref_id
        })
        
        if ref_id and ref_id != uid:
            db_core.users.update_one({"user_id": ref_id}, {"$inc": {"referrals": 1}})
            # Auto-reward
            u_ref = db_core.get_user(ref_id)
            if u_ref and u_ref.get('referrals', 0) >= 100 and not u_ref.get('rewarded'):
                expiry = datetime.now() + timedelta(days=30)
                db_core.users.update_one({"user_id": ref_id}, {"$set": {"expiry": expiry, "rewarded": True, "rank": "💎 LEYENDA"}})
                try: bot.send_message(ref_id, "🎊 ¡VIP activado por 100 referidos!")
                except: pass

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🎯 STRIKE", callback_data="gen"),
               InlineKeyboardButton("👤 PERFIL", callback_data="me"),
               InlineKeyboardButton("👥 REFS", callback_data="ref"),
               InlineKeyboardButton("🆘 TICKETS", callback_data="ticket"))
    bot.send_message(message.chat.id, f"👑 <b>CJKILLER APEX</b>\nRank: {get_rank(uid)}", reply_markup=markup, parse_mode="HTML")

# --- [ BYPASS Y CICLO DE VIDA ] ---

def run_bot():
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=60, skip_pending=True)
        except ApiTelegramException as e:
            if e.error_code == 409: time.sleep(5)
            else: raise e
        except Exception: time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    run_bot()
