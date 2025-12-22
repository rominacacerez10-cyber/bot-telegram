import telebot
import time
import random
import re
import threading
import os
import string
import logging
import sys
from flask import Flask
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException

# ==========================================
# 1. CONFIGURACIÓN MAESTRA Y VARIABLES GLOBALES
# ==========================================
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617 
LOG_CHANNEL = -1002319403816

# Configuración de Logs para Auditoría de Grado Militar
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s: %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("bot_core.log")]
)
logger = logging.getLogger("CJKiller_Omnipotent")

app = Flask(__name__)
MAINTENANCE = False
SHADOW_REALM = set() 
ANTIFLOOD_MEM = {}
START_TIME = datetime.now()

# ==========================================
# 2. INFRAESTRUCTURA DE DATOS (NÚCLEO BLINDADO)
# ==========================================
class UltimateDatabase:
    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.keys = None
        self.blacklist = None
        self.logs = None
        self.connect()

    def connect(self):
        try:
            # Conexión con alta tolerancia y timeouts
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=15000, connectTimeoutMS=15000)
            self.db = self.client.get_database()
            self.users = self.db['users']
            self.keys = self.db['keys']
            self.blacklist = self.db['blacklist']
            self.logs = self.db['admin_logs']
            
            # Verificación de integridad
            self.client.admin.command('ping')
            self.users.create_index("user_id", unique=True)
            self.keys.create_index("key", unique=True)
            logger.info("✅ INFRAESTRUCTURA DE DATOS: ONLINE AL 1000%")
        except Exception as e:
            logger.critical(f"❌ FALLO CRÍTICO EN DB: {e}")
            # El bot no muere, pero las variables quedan en None para manejo de errores
            self.users = None

    def get_user(self, uid):
        if not self.users: return None
        try: return self.users.find_one({"user_id": uid})
        except: return None

    def update_user(self, uid, data):
        if not self.users: return
        try: self.users.update_one({"user_id": uid}, {"$set": data}, upsert=True)
        except Exception as e: logger.error(f"Error update_user: {e}")

    def is_banned(self, uid):
        if not self.blacklist: return False
        return self.blacklist.find_one({"user_id": uid}) is not None

# Inicialización global de la base de datos corregida
db_core = UltimateDatabase()
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=1000)

# ==========================================
# 3. MÓDULOS DE LÓGICA Y ALGORITMOS ELITE
# ==========================================

def luhn_algorithm(n):
    """Validación estructural de tarjetas"""
    r = [int(ch) for ch in str(n)][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

def get_vip_expiry(uid):
    if uid == ADMIN_ID: return datetime.now() + timedelta(days=36500)
    user = db_core.get_user(uid)
    if user and user.get('expiry'):
        return user['expiry']
    return None

def is_premium(uid):
    expiry = get_vip_expiry(uid)
    return expiry and expiry > datetime.now()

def get_rank_display(uid):
    if uid == ADMIN_ID: return "👑 OVERLORD-GOD"
    user = db_core.get_user(uid)
    if not user: return "🔰 RECLUTA"
    if user.get('referrals', 0) >= 100: return "💎 LEYENDA (100+ REFS)"
    return user.get('rank', "🔰 RECLUTA")

# ==========================================
# 4. ADMINISTRACIÓN TOTAL (OMNIPOTENCIA)
# ==========================================

@bot.message_handler(commands=['panel'])
def super_admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        u_count = db_core.users.count_documents({}) if db_core.users else "N/A"
        k_count = db_core.keys.count_documents({"status": "active"}) if db_core.keys else "N/A"
        uptime = datetime.now() - START_TIME
        
        msg = (
            f"🚀 <b>ESTACIÓN DE MANDO SUPREMA v25.0</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>MÉTRICAS DEL SISTEMA:</b>\n"
            f"├ Usuarios: <code>{u_count}</code>\n"
            f"├ Keys Activas: <code>{k_count}</code>\n"
            f"├ Uptime: <code>{str(uptime).split('.')[0]}</code>\n"
            f"└ Mantenimiento: <code>{'ACTIVO' if MAINTENANCE else 'INACTIVO'}</code>\n\n"
            f"🛡️ <b>ADMINISTRACIÓN DE NÚCLEO:</b>\n"
            f"👉 <code>/db_exec [query]</code> - Ejecución directa\n"
            f"👉 <code>/genkey [dias] [cant]</code> - Crear Licencias\n"
            f"👉 <code>/add_vip [id] [dias]</code> - Inyectar Premium\n"
            f"👉 <code>/shadow [id]</code> - Modo Engaño Silencioso\n"
            f"👉 <code>/ban [id]</code> | <code>/unban [id]</code>\n"
            f"👉 <code>/bc [mensaje]</code> - Broadcast Multimedia\n\n"
            f"🎭 <b>MUTACIÓN DE IDENTIDAD:</b>\n"
            f"👉 <code>/set_identity [Nom] | [Bio]</code>\n"
            f"👉 <code>/set_photo</code> (Responde a una imagen)"
        )
        bot.reply_to(message, msg, parse_mode="HTML")
    except Exception as e: logger.error(f"Error Panel: {e}")

@bot.message_handler(commands=['db_exec'])
def force_execute(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        query = message.text.replace('/db_exec ', '')
        # Contexto completo de objetos para control total
        context = {
            'db': db_core.db, 'users': db_core.users, 'keys': db_core.keys,
            'bot': bot, 'datetime': datetime, 'timedelta': timedelta, 'time': time
        }
        exec(query, context)
        bot.reply_to(message, "✅ <b>NÚCLEO MODIFICADO EXITOSAMENTE AL 1000%.</b>")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>ERROR DE SINTAXIS:</b>\n<code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['genkey'])
def key_factory(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        days = int(parts[1])
        cant = int(parts[2]) if len(parts) > 2 else 1
        generated = []
        for _ in range(cant):
            key = f"CJK-{random.randint(100,999)}-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            db_core.keys.insert_one({"key": key, "days": days, "status": "active", "created_at": datetime.now()})
            generated.append(f"<code>{key}</code>")
        bot.reply_to(message, f"🔑 <b>BATCH DE LLAVES ({days} DÍAS):</b>\n" + "\n".join(generated), parse_mode="HTML")
    except: bot.reply_to(message, "⚠️ <b>Uso:</b> /genkey [dias] [cantidad]")

@bot.message_handler(commands=['set_identity'])
def identity_shift(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        data = message.text.replace('/set_identity ', '').split('|')
        name = data[0].strip()
        bio = data[1].strip()
        bot.set_my_name(name)
        bot.set_my_description(bio)
        bot.reply_to(message, f"✅ <b>IDENTIDAD MUTADA:</b>\n<b>Nombre:</b> {name}\n<b>Bio:</b> {bio}", parse_mode="HTML")
    except: bot.reply_to(message, "⚠️ <b>Uso:</b> /set_identity Nombre | Bio")

# ==========================================
# 5. MOTOR DE GENERACIÓN "THE PRECISION STRIKE"
# ==========================================

@bot.message_handler(commands=['precision', 'gen'])
def strike_engine(message):
    uid = message.from_user.id
    if db_core.is_banned(uid): return
    if MAINTENANCE and uid != ADMIN_ID:
        return bot.reply_to(message, "🚧 <b>SISTEMA EN MANTENIMIENTO TÉCNICO.</b>")
    
    if not is_premium(uid):
        return bot.reply_to(message, "⚠️ <b>ACCESO DENEGADO.</b> Adquiere una suscripción VIP para usar el motor de generación.")

    # Protección Anti-Flood con memoria dinámica
    now = time.time()
    if uid in ANTIFLOOD_MEM and now - ANTIFLOOD_MEM[uid] < 4:
        return bot.reply_to(message, "⏳ <b>FLOOD CONTROL:</b> Espera 4 segundos para la siguiente consulta.")
    ANTIFLOOD_MEM[uid] = now

    try:
        raw_bin = re.findall(r'\d+', message.text)
        if not raw_bin: return bot.reply_to(message, "❌ <b>ERROR:</b> Ingrese un BIN válido de 6 dígitos.")
        bin_in = raw_bin[0][:6]
        
        load = bot.reply_to(message, "🌀 <b>CALIBRANDO MOTOR DE PRECISIÓN...</b>", parse_mode="Markdown")
        
        is_shadow = uid in SHADOW_REALM
        valid_hits = []
        
        # Generación con 500 intentos de validación interna
        for _ in range(500):
            if len(valid_hits) >= 10: break
            cc = f"{bin_in}{''.join([str(random.randint(0,9)) for _ in range(10)])}"
            if luhn_algorithm(cc) or is_shadow:
                m = f"{random.randint(1,12):02d}"
                y = f"{random.randint(2025, 2031)}"
                cvv = f"{random.randint(100, 999)}"
                valid_hits.append(f"<code>{cc}|{m}|{y}|{cvv}</code>")

        res = (
            f"🎯 <b>STRIKE SUCCESS: {bin_in}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            + "\n".join(valid_hits) +
            f"\n━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>ID:</b> <code>{uid}</code>\n"
            f"💎 <b>RANK:</b> {get_rank_display(uid)}"
        )
        bot.edit_message_text(res, message.chat.id, load.message_id, parse_mode="HTML")
        if db_core.users: db_core.users.update_one({"user_id": uid}, {"$inc": {"hits": 1}})
        
    except Exception as e:
        logger.error(f"Error Strike: {e}")
        bot.reply_to(message, "❌ <b>ERROR INTERNO EN EL MOTOR.</b>")

# ==========================================
# 6. SISTEMA DE USUARIOS, CLAIM Y REFERIDOS
# ==========================================

@bot.message_handler(commands=['claim'])
def claim_protocol(message):
    uid = message.from_user.id
    try:
        key_input = message.text.split()[1].strip()
        key_data = db_core.keys.find_one({"key": key_input, "status": "active"})
        
        if key_data:
            days = key_data['days']
            current = db_core.get_user(uid).get('expiry') or datetime.now()
            if current < datetime.now(): current = datetime.now()
            
            new_expiry = current + timedelta(days=days)
            db_core.users.update_one({"user_id": uid}, {"$set": {"expiry": new_expiry, "rank": "💎 PREMIUM"}})
            db_core.keys.update_one({"key": key_input}, {"$set": {"status": "used", "claimed_by": uid, "at": datetime.now()}})
            
            bot.reply_to(message, f"✅ <b>LICENCIA CANJEADA:</b> Se han añadido {days} días VIP a tu cuenta.")
        else:
            bot.reply_to(message, "❌ <b>ERROR:</b> La llave es inválida, expiró o ya fue utilizada.")
    except: bot.reply_to(message, "⚠️ <b>Uso:</b> /claim [TU-LLAVE]")

@bot.message_handler(commands=['start'])
def portal_start(message):
    uid = message.from_user.id
    username = message.from_user.username or "Anonymous"
    
    # Lógica de Referidos con Detección de Fraude Automática
    if not db_core.get_user(uid):
        ref_id = None
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            target_ref = int(args[1])
            if target_ref != uid: ref_id = target_ref
            
        db_core.update_user(uid, {
            "user_id": uid, "username": username, "referrals": 0, "hits": 0,
            "rank": "🔰 RECLUTA", "joined": datetime.now(), "rewarded": False, "referred_by": ref_id
        })
        
        if ref_id:
            db_core.users.update_one({"user_id": ref_id}, {"$inc": {"referrals": 1}})
            u_ref = db_core.get_user(ref_id)
            # Recompensa Automática por 100 referidos
            if u_ref and u_ref.get('referrals', 0) >= 100 and not u_ref.get('rewarded'):
                new_vip = (u_ref.get('expiry') or datetime.now()) + timedelta(days=30)
                db_core.users.update_one({"user_id": ref_id}, {"$set": {"expiry": new_vip, "rewarded": True, "rank": "💎 LEYENDA"}})
                try: bot.send_message(ref_id, "🎊 <b>¡SISTEMA:</b> Has alcanzado 100 referidos! Se han inyectado 30 días VIP automáticamente.")
                except: pass

    # Interfaz Gráfica (Inline)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎯 STRIKE ENGINE", callback_data="gen"),
        InlineKeyboardButton("🔑 CANJEAR LLAVE", callback_data="claim"),
        InlineKeyboardButton("👤 MI PERFIL", callback_data="me"),
        InlineKeyboardButton("👥 SISTEMA REFS", callback_data="ref"),
        InlineKeyboardButton("🆘 SOPORTE", callback_data="ticket")
    )
    
    welcome = (
        f"👑 <b>CJKILLER OMNIPOTENT v25.0</b>\n"
        f"<i>El bot más potente del mercado.</i>\n\n"
        f"👤 <b>Rank:</b> <code>{get_rank_display(uid)}</code>\n"
        f"📅 <b>Vencimiento:</b> <code>{get_vip_expiry(uid).strftime('%d/%m/%Y') if is_premium(uid) else 'SIN SUSCRIPCIÓN'}</code>"
    )
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="HTML")

# ==========================================
# 7. ESTABILIDAD Y BYPASS ANTI-ERROR 409
# ==========================================

def run_bot_infinite():
    """Bucle de ejecución con reconexión automática agresiva"""
    logger.info("🚀 NÚCLEO CJKILLER DESPLEGADO - INTEGRACIÓN AL 1000%")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=60, long_polling_timeout=40, skip_pending=True)
        except ApiTelegramException as e:
            if e.error_code == 409:
                logger.warning("⚠️ Conflicto 409 detectado. Limpiando webhooks y reintentando...")
                time.sleep(5)
            else:
                logger.error(f"Telegram API Error: {e}")
                time.sleep(10)
        except Exception as e:
            logger.error(f"Fallo de Sistema: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Servidor Flask en hilo separado para mantener vivo en Render
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    run_bot_infinite()
