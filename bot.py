import telebot
import time
import random
import re
import threading
import os
import string
import logging
import sqlite3
from flask import Flask
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException

# --- [ CONFIGURACIÓN MAESTRA DE ALTA DISPONIBILIDAD ] ---
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617 
LOG_CHANNEL = -1002319403816

# Configuración de Logging de Grado Industrial
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("CJKiller_Apex")

app = Flask(__name__)
MAINTENANCE = False
SHADOW_REALM = set() 
ANTIFLOOD_CACHE = {}

# --- [ MÓDULO DE BASE DE DATOS: ARQUITECTURA PERSISTENTE ] ---
class GlobalDatabase:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000)
            self.db = self.client.get_database()
            self.users = self.db['users']
            self.keys = self.db['keys']
            self.blacklist = self.db['blacklist']
            self.logs = self.db['action_logs']
            # Índices de optimización para millones de registros
            self.users.create_index("user_id", unique=True)
            self.keys.create_index("key", unique=True)
            logger.info("📡 MongoDB Core: Online y sincronizado.")
        except Exception as e:
            logger.critical(f"❌ Fallo crítico en conexión DB: {e}")

    def get_user(self, uid):
        return self.users.find_one({"user_id": uid})

    def update_user(self, uid, data):
        self.users.update_one({"user_id": uid}, {"$set": data}, upsert=True)

    def log_admin_action(self, admin_id, action):
        self.logs.insert_one({
            "admin_id": admin_id,
            "action": action,
            "timestamp": datetime.now()
        })

db_core = GlobalDatabase()
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=1000)

# --- [ MÓDULO DE SEGURIDAD Y ALGORITMOS ] ---

def validate_luhn(card_number):
    """Verificación estructural de tarjetas al 100%"""
    digits = [int(d) for d in str(card_number)]
    checksum = digits[-1]
    payload = digits[:-1][::-1]
    total = 0
    for i, d in enumerate(payload):
        if i % 2 == 0:
            d *= 2
            if d > 9: d -= 9
        total += d
    return (total + checksum) % 10 == 0

def check_vip_status(uid):
    if uid == ADMIN_ID: return True
    user = db_core.get_user(uid)
    if user and user.get('expiry'):
        return user['expiry'] > datetime.now()
    return False

# --- [ PANEL DE CONTROL OVERLORD: PODER ABSOLUTO ] ---

@bot.message_handler(commands=['panel'])
def admin_panel_massive(message):
    if message.from_user.id != ADMIN_ID: return
    
    # Recolección de estadísticas en tiempo real
    total_users = db_core.users.count_documents({})
    active_keys = db_core.keys.count_documents({"status": "active"})
    banned_count = db_core.blacklist.count_documents({})
    
    panel_msg = (
        f"👑 <b>CJKILLER OVERLORD CORE v21.0</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 <b>ESTADÍSTICAS GLOBALES:</b>\n"
        f"├ Usuarios Totales: <code>{total_users}</code>\n"
        f"├ Licencias Activas: <code>{active_keys}</code>\n"
        f"└ Infractores Baneados: <code>{banned_count}</code>\n\n"
        f"⚙️ <b>CONFIGURACIÓN DE NÚCLEO:</b>\n"
        f"├ Mantenimiento: <code>{'ACTIVO' if MAINTENANCE else 'OFF'}</code>\n"
        f"└ Threads Activos: <code>1000</code>\n\n"
        f"⚡ <b>COMANDOS DE ALTA SEGURIDAD:</b>\n"
        f"👉 <code>/db_exec [query]</code> - Control Total Python\n"
        f"👉 <code>/genkey [dias] [cant]</code> - Generador Masivo\n"
        f"👉 <code>/add_vip [id] [dias]</code> - Inyección VIP\n"
        f"👉 <code>/shadow [id]</code> - Shadow Ban (Engaño)\n"
        f"👉 <code>/bc [msg]</code> - Broadcast Multimedia\n\n"
        f"🎭 <b>MIMETISMO DE IDENTIDAD:</b>\n"
        f"👉 <code>/set_identity [Nom] | [Bio]</code>\n"
        f"👉 <code>/set_photo</code> (Responde a foto)"
    )
    bot.reply_to(message, panel_msg, parse_mode="HTML")

@bot.message_handler(commands=['db_exec'])
def nucleus_execution(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        command = message.text.replace('/db_exec ', '')
        # Ejecución con acceso a todo el ecosistema del bot
        exec_env = {
            'db': db_core.db,
            'users': db_core.users,
            'bot': bot,
            'time': time,
            'datetime': datetime
        }
        exec(command, exec_env)
        db_core.log_admin_action(ADMIN_ID, f"Exec: {command[:100]}")
        bot.reply_to(message, "✅ <b>COMANDO EJECUTADO EN EL NÚCLEO.</b>")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>FALLO DE EJECUCIÓN:</b>\n<code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['genkey'])
def key_generator_engine(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        days = int(parts[1])
        cant = int(parts[2]) if len(parts) > 2 else 1
        
        keys_generated = []
        for _ in range(cant):
            new_key = f"CJ-{random.randint(1000,9999)}-{random.choice(string.ascii_uppercase)}{random.randint(10,99)}"
            db_core.keys.insert_one({"key": new_key, "days": days, "status": "active", "created_at": datetime.now()})
            keys_generated.append(f"<code>{new_key}</code>")
        
        bot.reply_to(message, f"🔑 <b>KEYS ({days} DÍAS):</b>\n" + "\n".join(keys_generated), parse_mode="HTML")
    except:
        bot.reply_to(message, "⚠️ Uso: /genkey [dias] [cantidad]")

# --- [ MOTOR DE GENERACIÓN: THE PRECISION STRIKE ] ---

@bot.message_handler(commands=['precision', 'gen'])
def strike_module(message):
    uid = message.from_user.id
    # Verificaciones de Seguridad Capa 1
    if db_core.blacklist.find_one({"user_id": uid}): return
    if MAINTENANCE and uid != ADMIN_ID:
        return bot.reply_to(message, "🚧 **SISTEMA EN MANTENIMIENTO.**")
    
    # Verificación VIP
    if not check_vip_status(uid):
        return bot.reply_to(message, "⚠️ **ACCESO DENEGADO.** Requiere suscripción activa.")

    # Anti-Flood Avanzado
    now = time.time()
    if uid in ANTIFLOOD_CACHE and now - ANTIFLOOD_CACHE[uid] < 3:
        return bot.reply_to(message, "⏳ **PROTECCIÓN ANTI-SPAM.** Espera 3s.")
    ANTIFLOOD_CACHE[uid] = now

    try:
        bin_extract = re.findall(r'\d+', message.text)[0][:6]
        progress = bot.reply_to(message, "🌀 **CALIBRANDO ALGORITMOS...**", parse_mode="Markdown")
        
        is_shadow = uid in SHADOW_REALM
        valid_hits = []
        
        # Generación intensiva con validación Luhn
        attempt = 0
        while len(valid_hits) < 10 and attempt < 500:
            suffix = "".join([str(random.randint(0,9)) for _ in range(10)])
            full_card = f"{bin_extract}{suffix}"
            if validate_luhn(full_card) or is_shadow:
                exp_m = f"{random.randint(1,12):02d}"
                exp_a = f"{random.randint(2025, 2031)}"
                cvv = f"{random.randint(100, 999)}"
                valid_hits.append(f"`{full_card}|{exp_m}|{exp_a}|{cvv}`")
            attempt += 1

        response = (
            f"🎯 **STRIKE SUCCESS: {bin_extract}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            + "\n".join(valid_hits) +
            f"\n━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **User:** `{uid}` | 💠 **Rank:** {db_core.get_user(uid).get('rank', 'N/A')}"
        )
        bot.edit_message_text(response, message.chat.id, progress.message_id, parse_mode="Markdown")
        db_core.users.update_one({"user_id": uid}, {"$inc": {"hits": 1}})
        bot.send_message(LOG_CHANNEL, f"💎 **HIT GENERADO:** {bin_extract} por ID {uid}")
        
    except Exception as e:
        bot.reply_to(message, "❌ **ERROR EN MOTOR:** Ingrese un BIN válido de 6 dígitos.")

# --- [ INTERFAZ, REFERIDOS Y ECONOMÍA ] ---

@bot.message_handler(commands=['start'])
def portal_start(message):
    uid = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    # Manejo de Referidos con detección de fraude
    if not db_core.get_user(uid):
        ref_id = None
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            ref_candidate = int(args[1])
            if ref_candidate != uid: ref_id = ref_candidate
            
        db_core.update_user(uid, {
            "user_id": uid, "username": username, "referrals": 0,
            "hits": 0, "rank": "🔰 RECLUTA", "joined": datetime.now(),
            "rewarded": False, "referred_by": ref_id
        })
        
        if ref_id:
            db_core.users.update_one({"user_id": ref_id}, {"$inc": {"referrals": 1}})
            # Lógica de Recompensa Automática (100 Referidos = 30 días VIP)
            u_ref = db_core.get_user(ref_id)
            if u_ref and u_ref.get('referrals', 0) >= 100 and not u_ref.get('rewarded'):
                new_expiry = datetime.now() + timedelta(days=30)
                db_core.users.update_one({"user_id": ref_id}, {"$set": {"expiry": new_expiry, "rewarded": True, "rank": "💎 LEYENDA"}})
                try: bot.send_message(ref_id, "🎊 **¡RECOMPENSA DE CLAN!** Has ganado 30 días VIP por tus 100 referidos.")
                except: pass

    # Menú Principal
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎯 GENERAR", callback_data="gen"),
        InlineKeyboardButton("🔑 CANJEAR", callback_data="claim"),
        InlineKeyboardButton("👤 PERFIL", callback_data="me"),
        InlineKeyboardButton("👥 CLAN", callback_data="ref"),
        InlineKeyboardButton("🆘 SOPORTE", callback_data="ticket")
    )
    bot.send_message(message.chat.id, f"👑 <b>CJKILLER APEX</b>\n<i>Dominando el éter digital.</i>", reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['claim'])
def claim_license(message):
    uid = message.from_user.id
    try:
        key_input = message.text.split()[1]
        key_data = db_core.keys.find_one({"key": key_input, "status": "active"})
        
        if key_data:
            days = key_data['days']
            current_expiry = db_core.get_user(uid).get('expiry') or datetime.now()
            if current_expiry < datetime.now(): current_expiry = datetime.now()
            
            new_expiry = current_expiry + timedelta(days=days)
            db_core.users.update_one({"user_id": uid}, {"$set": {"expiry": new_expiry, "rank": "💎 PREMIUM"}})
            db_core.keys.update_one({"key": key_input}, {"$set": {"status": "used", "claimed_by": uid, "claimed_at": datetime.now()}})
            
            bot.reply_to(message, f"✅ <b>LICENCIA ACTIVADA.</b>\nSe han añadido {days} días a tu cuenta.")
        else:
            bot.reply_to(message, "❌ <b>KEY INVÁLIDA O YA USADA.</b>")
    except:
        bot.reply_to(message, "⚠️ Uso: /claim [KEY-XXXX-XXXX]")

# --- [ SOPORTE Y MIMETISMO ] ---

@bot.message_handler(commands=['ticket'])
def ticket_module(message):
    uid = message.from_user.id
    content = message.text.replace('/ticket ', '')
    if len(content) < 10: return bot.reply_to(message, "⚠️ Por favor, detalla tu reporte (mínimo 10 caracteres).")
    
    bot.send_message(ADMIN_ID, f"📩 <b>NUEVO TICKET SOPORTE:</b>\nID: <code>{uid}</code>\nMsg: {content}", parse_mode="HTML")
    bot.reply_to(message, "✅ **Reporte enviado al administrador.**")

@bot.message_handler(commands=['set_identity'])
def admin_mimetismo(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        data = message.text.replace('/set_identity ', '').split('|')
        name = data[0].strip()
        bio = data[1].strip()
        bot.set_my_name(name)
        bot.set_my_description(bio)
        bot.reply_to(message, "✅ **IDENTIDAD DEL BOT MUTADA EXITOSAMENTE.**")
    except:
        bot.reply_to(message, "❌ Uso: /set_identity Nombre | Bio")

# --- [ CICLO DE VIDA Y ESTABILIDAD ANTI-409 ] ---

def start_server():
    app.run(host='0.0.0.0', port=10000)

def main_execution():
    while True:
        try:
            bot.remove_webhook()
            logger.info("🚀 NÚCLEO CJKILLER ONLINE - INTEGRACIÓN AL 1000%")
            bot.infinity_polling(timeout=60, long_polling_timeout=40, skip_pending=True)
        except ApiTelegramException as e:
            if e.error_code == 409:
                logger.warning("⚠️ Conflicto de sesión (409). Reiniciando núcleo...")
                time.sleep(5)
            else: raise e
        except Exception as e:
            logger.error(f"⚠️ Error inesperado: {e}")
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    main_execution()
