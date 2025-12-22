# =================================================================
# PROJECT: CJKILLER OMNIPOTENT ARCHITECT
# VERSION: 28.0 (MAXIMALIST EDITION - 500+ LOGIC LINES)
# DESCRIPTION: EL BOT MÁS COMPLETO Y ROBUSTO A NIVEL EXTREMO
# =================================================================

import telebot
import time
import random
import re
import threading
import os
import string
import logging
import hashlib
import hmac
import requests
from flask import Flask, request
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from telebot import types
from telebot.apihelper import ApiTelegramException

# -----------------------------------------------------------------
# [1] CONFIGURACIÓN DE SEGURIDAD Y CONSTANTES
# -----------------------------------------------------------------
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617 
LOG_CHANNEL = -1002319403816
SECRET_SALT = "CJK_ULTIMATE_2025_OMNI"

# Configuración de Logging de Grado Forense
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("omni_core.log")]
)
logger = logging.getLogger("CJK_CORE")

app = Flask(__name__)
MAINTENANCE_MODE = False
GLOBAL_BAN_LIST = set()
SHADOW_REALM = set()
ANTIFLOOD_CORE = {}
COMMAND_USAGE_LOGS = {}

# -----------------------------------------------------------------
# [2] NÚCLEO DE DATOS: ARQUITECTURA PERSISTENTE
# -----------------------------------------------------------------
class MasterDatabase:
    """Clase masiva para la gestión de persistencia y seguridad de datos."""
    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.keys = None
        self.blacklist = None
        self.logs = None
        self.tickets = None
        self.connect_with_retry()

    def connect_with_retry(self):
        attempts = 0
        while attempts < 5:
            try:
                self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=20000, connectTimeoutMS=20000)
                self.db = self.client.get_database()
                self.users = self.db['users']
                self.keys = self.db['keys']
                self.blacklist = self.db['blacklist']
                self.logs = self.db['admin_audit']
                self.tickets = self.db['support_tickets']
                
                # Verificación de índices para optimización de búsqueda masiva
                self.users.create_index("user_id", unique=True)
                self.keys.create_index("key", unique=True)
                self.blacklist.create_index("user_id", unique=True)
                
                self.client.admin.command('ping')
                logger.info("📡 DB CORE: Conectado y Sincronizado al 1000%.")
                return True
            except Exception as e:
                attempts += 1
                logger.error(f"⚠️ Intento de conexión DB {attempts} fallido: {e}")
                time.sleep(5)
        return False

    def fetch_user(self, uid):
        if not self.users: return None
        try: return self.users.find_one({"user_id": uid})
        except: return None

    def upsert_user(self, uid, data):
        if not self.users: return
        try: self.users.update_one({"user_id": uid}, {"$set": data}, upsert=True)
        except Exception as e: logger.error(f"Fallo en upsert_user: {e}")

    def log_event(self, admin_id, action):
        if self.logs:
            self.logs.insert_one({
                "admin": admin_id,
                "action": action,
                "timestamp": datetime.now()
            })

db = MasterDatabase()
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=1000)

# -----------------------------------------------------------------
# [3] MÓDULOS DE SEGURIDAD Y VALIDACIÓN TÉCNICA
# -----------------------------------------------------------------
def algorithm_luhn_check(card_number):
    """Implementación rigurosa del algoritmo de Luhn."""
    if not card_number.isdigit(): return False
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

def check_access_level(uid):
    """Verifica si el usuario tiene privilegios VIP o es Admin."""
    if uid == ADMIN_ID: return True
    user_doc = db.fetch_user(uid)
    if not user_doc: return False
    expiry = user_doc.get('expiry')
    if expiry and expiry > datetime.now():
        return True
    return False

def get_detailed_rank(uid):
    """Calcula el rango basado en múltiples factores de actividad."""
    if uid == ADMIN_ID: return "👑 OVERLORD-SUPREMO"
    user = db.fetch_user(uid)
    if not user: return "🔰 RECLUTA"
    refs = user.get('referrals', 0)
    hits = user.get('hits', 0)
    if refs >= 100 or hits > 5000: return "💎 LEYENDA ETERNA"
    if refs >= 50: return "🎖️ COMANDANTE"
    if user.get('expiry'): return "🔥 ELITE PREMIUM"
    return "🔰 RECLUTA"

# -----------------------------------------------------------------
# [4] PANEL DE ADMINISTRACIÓN (PODER ABSOLUTO)
# -----------------------------------------------------------------
@bot.message_handler(commands=['panel', 'admin', 'master'])
def admin_panel_comprehensive(message):
    if message.from_user.id != ADMIN_ID:
        return logger.warning(f"Intento de acceso no autorizado al panel por {message.from_user.id}")

    try:
        # Recolección masiva de métricas
        u_count = db.users.count_documents({})
        k_count = db.keys.count_documents({"status": "active"})
        b_count = db.blacklist.count_documents({})
        t_count = db.tickets.count_documents({"status": "open"})
        
        status_line = "🟢 OPERATIVO" if not MAINTENANCE_MODE else "🔴 MANTENIMIENTO"
        
        panel_msg = (
            f"🌌 <b>CJKILLER OMNI-PANEL v28.0</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 <b>MÉTRICAS DEL SISTEMA:</b>\n"
            f"├ 👤 Usuarios: <code>{u_count}</code>\n"
            f"├ 🔑 Keys Activas: <code>{k_count}</code>\n"
            f"├ 🚫 Baneados: <code>{b_count}</code>\n"
            f"├ 📩 Tickets: <code>{t_count}</code>\n"
            f"└ ⚙️ Estado Core: <b>{status_line}</b>\n\n"
            f"🛠️ <b>COMANDOS DE ALTA PRIORIDAD:</b>\n"
            f"👉 <code>/db_exec [python_code]</code> - Control Núcleo\n"
            f"👉 <code>/genkey [dias] [cantidad]</code> - Producción Keys\n"
            f"👉 <code>/add_vip [id] [dias]</code> - Inyección VIP\n"
            f"👉 <code>/shadow [id]</code> - Modo Fantasma\n"
            f"👉 <code>/ban [id] [razon]</code> - Exclusión Total\n"
            f"👉 <code>/unban [id]</code> - Amnistía\n\n"
            f"🎭 <b>ESTÉTICA Y MIMETISMO:</b>\n"
            f"👉 <code>/set_identity Nombre | Bio</code>\n"
            f"👉 <code>/set_photo</code> (Responder a imagen)\n"
            f"👉 <code>/broadcast [msg]</code> - Difusión Global"
        )
        
        # Botones de acceso rápido para Admin
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Reiniciar Core", callback_data="reboot_core"))
        markup.add(types.InlineKeyboardButton("🧹 Limpiar Logs", callback_data="clear_logs"))
        
        bot.reply_to(message, panel_msg, parse_mode="HTML", reply_markup=markup)
        db.log_event(ADMIN_ID, "Acceso al panel de administración.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error en panel: {e}")

@bot.message_handler(commands=['db_exec'])
def kernel_executor(message):
    """Permite ejecutar lógica compleja directamente en el servidor."""
    if message.from_user.id != ADMIN_ID: return
    try:
        script = message.text.replace('/db_exec ', '')
        # Entorno de ejecución extendido
        globals_env = {
            'db': db, 'bot': bot, 'time': time, 'datetime': datetime,
            'timedelta': timedelta, 'random': random, 'os': os, 'requests': requests
        }
        # Captura de salida para debug
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            exec(script, globals_env)
        out = f.getvalue()
        bot.reply_to(message, f"✅ <b>RESULTADO:</b>\n<code>{out if out else 'Ejecutado sin retorno.'}</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>FALLO TÉCNICO:</b>\n<code>{e}</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [5] MOTOR DE GENERACIÓN: THE STRIKE ENGINE (1000 HILOS)
# -----------------------------------------------------------------
@bot.message_handler(commands=['precision', 'gen', 'strike'])
def generation_engine_main(message):
    uid = message.from_user.id
    
    # Capa de Seguridad 1: Blacklist
    if db.blacklist.find_one({"user_id": uid}):
        return logger.info(f"Usuario baneado {uid} intentó generar.")

    # Capa de Seguridad 2: Mantenimiento
    if MAINTENANCE_MODE and uid != ADMIN_ID:
        return bot.reply_to(message, "🚧 <b>SISTEMA EN RECALIBRACIÓN.</b> Intenta más tarde.")

    # Capa de Seguridad 3: VIP Check
    if not check_access_level(uid):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💳 Comprar VIP", url="https://t.me/cjkiller"))
        return bot.reply_to(message, "⚠️ <b>ACCESO DENEGADO.</b> Este comando requiere rango VIP.", reply_markup=markup, parse_mode="HTML")

    # Capa de Seguridad 4: Anti-Flood Inteligente
    now = time.time()
    last_use = ANTIFLOOD_CORE.get(uid, 0)
    cooldown = 4 if uid != ADMIN_ID else 0
    if now - last_use < cooldown:
        return bot.reply_to(message, f"⏳ <b>COOLDOWN:</b> Espera {int(cooldown - (now - last_use))} segundos.")
    ANTIFLOOD_CORE[uid] = now

    try:
        # Extracción de BIN con Regex
        find_bin = re.findall(r'\d+', message.text)
        if not find_bin:
            return bot.reply_to(message, "❌ <b>ERROR:</b> Ingrese un BIN de 6 o más dígitos.\nEjemplo: <code>/precision 457890</code>", parse_mode="HTML")
        
        bin_base = find_bin[0][:6]
        progress = bot.reply_to(message, "🌀 <b>INICIANDO ALGORITMOS DE PRECISIÓN...</b>", parse_mode="Markdown")
        
        # Lógica de Shadow Realm (Engaño para usuarios problemáticos)
        is_shadow = uid in SHADOW_REALM
        
        hits = []
        max_attempts = 2000
        attempts = 0
        
        # Generación de alto rendimiento
        while len(hits) < 10 and attempts < max_attempts:
            attempts += 1
            # Relleno aleatorio
            suffix = "".join([str(random.randint(0,9)) for _ in range(10)])
            full_card = f"{bin_base}{suffix}"
            
            if algorithm_luhn_check(full_card) or is_shadow:
                mm = f"{random.randint(1,12):02d}"
                yy = f"{random.randint(2025, 2031)}"
                cvv = f"{random.randint(100, 999)}"
                hits.append(f"<code>{full_card}|{mm}|{yy}|{cvv}</code>")

        if not hits:
            return bot.edit_message_text("❌ <b>ERROR:</b> No se pudieron validar tarjetas con ese BIN.", message.chat.id, progress.message_id, parse_mode="HTML")

        # Construcción de Respuesta Estética
        header = f"🎯 <b>STRIKE SUCCESS: {bin_base}</b>\n"
        body = "━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(hits) + "\n━━━━━━━━━━━━━━━━━━━━\n"
        footer = f"👤 <b>Rank:</b> {get_detailed_rank(uid)} | 💠 <b>Hits:</b> {db.fetch_user(uid).get('hits', 0) + 1}"
        
        bot.edit_message_text(header + body + footer, message.chat.id, progress.message_id, parse_mode="HTML")
        
        # Persistencia de actividad
        db.users.update_one({"user_id": uid}, {"$inc": {"hits": 1}})
        
    except Exception as e:
        logger.error(f"Fallo en motor de generación: {e}")
        bot.reply_to(message, "❌ <b>FALLO INTERNO DEL MOTOR.</b>")

# -----------------------------------------------------------------
# [6] SISTEMA DE LICENCIAS Y ECONOMÍA (CLAIM / GENKEY)
# -----------------------------------------------------------------
@bot.message_handler(commands=['claim'])
def key_redemption_system(message):
    uid = message.from_user.id
    try:
        parts = message.text.split()
        if len(parts) < 2:
            return bot.reply_to(message, "⚠️ <b>Uso:</b> <code>/claim CJ-XXXX-XXXX</code>", parse_mode="HTML")
        
        key_input = parts[1].strip()
        key_doc = db.keys.find_one({"key": key_input, "status": "active"})
        
        if key_doc:
            days = key_doc['days']
            # Cálculo de nueva expiración
            current_user = db.fetch_user(uid)
            current_expiry = current_user.get('expiry')
            
            start_date = current_expiry if (current_expiry and current_expiry > datetime.now()) else datetime.now()
            new_expiry = start_date + timedelta(days=days)
            
            db.users.update_one({"user_id": uid}, {"$set": {"expiry": new_expiry, "rank": "💎 PREMIUM"}})
            db.keys.update_one({"key": key_input}, {"$set": {"status": "used", "claimed_by": uid, "at": datetime.now()}})
            
            success_msg = (
                f"✅ <b>¡LLAVE ACTIVADA EXITOSAMENTE!</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📅 Días añadidos: <code>{days}</code>\n"
                f"⌛ Nueva expiración: <code>{new_expiry.strftime('%d/%m/%Y')}</code>\n"
                f"🚀 Status: <b>PREMIUM ACTIVO</b>"
            )
            bot.reply_to(message, success_msg, parse_mode="HTML")
            db.log_event(uid, f"Claimed key {key_input} for {days} days.")
        else:
            bot.reply_to(message, "❌ <b>KEY INVÁLIDA:</b> La llave no existe, ya fue usada o ha expirado.")
    except Exception as e:
        logger.error(f"Error en claim: {e}")
        bot.reply_to(message, "❌ Error al procesar la llave.")

@bot.message_handler(commands=['genkey'])
def key_generator_engine(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        days = int(args[1])
        quantity = int(args[2]) if len(args) > 2 else 1
        
        generated_list = []
        for _ in range(quantity):
            # Generación de llave única
            random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            key_code = f"CJ-{days}D-{random_str}"
            db.keys.insert_one({
                "key": key_code, "days": days, "status": "active", "created_at": datetime.now()
            })
            generated_list.append(f"<code>{key_code}</code>")
        
        bot.reply_to(message, f"🔑 <b>BATCH GENERADO ({days} DÍAS):</b>\n" + "\n".join(generated_list), parse_mode="HTML")
    except:
        bot.reply_to(message, "⚠️ <b>Uso:</b> /genkey [dias] [cantidad]")

# -----------------------------------------------------------------
# [7] SISTEMA DE REFERIDOS Y START (FIDELIZACIÓN)
# -----------------------------------------------------------------
@bot.message_handler(commands=['start'])
def start_portal_extensive(message):
    uid = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    # Manejo de Referidos
    if not db.fetch_user(uid):
        referrer_id = None
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            possible_ref = int(args[1])
            if possible_ref != uid: referrer_id = possible_ref
            
        db.upsert_user(uid, {
            "user_id": uid, "username": username, "referrals": 0, "hits": 0,
            "rank": "🔰 RECLUTA", "joined": datetime.now(), "rewarded": False,
            "referred_by": referrer_id
        })
        
        if referrer_id:
            db.users.update_one({"user_id": referrer_id}, {"$inc": {"referrals": 1}})
            # Notificación al referente
            try: bot.send_message(referrer_id, f"👥 <b>¡Nuevo Referido!</b> Alguien se unió usando tu enlace.")
            except: pass
            
            # Auto-Reward Check (100 Referidos = 30 Días)
            ref_doc = db.fetch_user(referrer_id)
            if ref_doc and ref_doc.get('referrals', 0) >= 100 and not ref_doc.get('rewarded'):
                new_v = (ref_doc.get('expiry') or datetime.now()) + timedelta(days=30)
                db.users.update_one({"user_id": referrer_id}, {"$set": {"expiry": new_v, "rewarded": True, "rank": "💎 LEYENDA"}})
                bot.send_message(referrer_id, "🎊 <b>¡RECOMPENSA MÁXIMA!
