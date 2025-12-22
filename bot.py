import telebot
import time
import random
import re
import threading
import os
import string
import logging
import json
from flask import Flask
from pymongo import MongoClient
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException

# =================================================================
# 1. CONFIGURACIÓN MAESTRA DE GRADO MILITAR
# =================================================================
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/cjkiller_db?retryWrites=true&w=majority"
ADMIN_ID = 7447432617 
LOG_CHANNEL = -1002319403816

# Configuración de logs para detectar fallos en tiempo real
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("CJKiller_System")

app = Flask(__name__)
MAINTENANCE = False
SHADOW_REALM = set() 
ANTIFLOOD = {}
START_UP_TIME = datetime.now()

# =================================================================
# 2. SISTEMA DE DATOS DINÁMICO (PREVIENE EL ERROR 409 Y ATTR ERR)
# =================================================================
class SystemCore:
    def __init__(self):
        self.db_active = False
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
            self.db = self.client.get_database()
            self.users = self.db['users']
            self.keys = self.db['keys']
            self.blacklist = self.db['blacklist']
            self.logs = self.db['audit_logs']
            
            # Índices para velocidad extrema
            self.users.create_index("user_id", unique=True)
            self.keys.create_index("key", unique=True)
            
            self.client.admin.command('ping')
            self.db_active = True
            logger.info("🟢 SISTEMA DE DATOS: ACTIVADO AL 1000%")
        except Exception as e:
            logger.error(f"🔴 ERROR EN NÚCLEO DB: {e}")

    def get_user_data(self, uid):
        if not self.db_active: return None
        return self.users.find_one({"user_id": uid})

    def save_user(self, uid, data):
        if not self.db_active: return
        self.users.update_one({"user_id": uid}, {"$set": data}, upsert=True)

# Inicialización del núcleo
core = SystemCore()
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=1000)

# =================================================================
# 3. SEGURIDAD Y HERRAMIENTAS DE ALGORITMO
# =================================================================

def validate_card_luhn(n):
    """Algoritmo de Luhn para validación de estructuras binarias"""
    digits = [int(d) for d in str(n)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10 == 0

def is_user_premium(uid):
    if uid == ADMIN_ID: return True
    u = core.get_user_data(uid)
    if u and u.get('expiry'):
        return u['expiry'] > datetime.now()
    return False

# =================================================================
# 4. MÓDULO DE ADMINISTRACIÓN (CONTROLES COMPLETOS)
# =================================================================

@bot.message_handler(commands=['panel'])
def master_control_room(message):
    """Estación de mando con todas las métricas integradas"""
    if message.from_user.id != ADMIN_ID: return
    
    try:
        total = core.users.count_documents({}) if core.db_active else "N/A"
        active_keys = core.keys.count_documents({"status": "active"}) if core.db_active else "N/A"
        uptime = datetime.now() - START_UP_TIME
        
        panel_text = (
            f"👑 <b>CJKILLER GIGANT ARCHITECT v26.0</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>ESTADÍSTICAS EN VIVO:</b>\n"
            f"├ Usuarios Totales: <code>{total}</code>\n"
            f"├ Llaves Disponibles: <code>{active_keys}</code>\n"
            f"├ Tiempo Online: <code>{str(uptime).split('.')[0]}</code>\n"
            f"└ Base de Datos: <code>{'ACTIVA' if core.db_active else 'FALLO'}</code>\n\n"
            f"🛠️ <b>COMANDOS DE CONTROL TOTAL:</b>\n"
            f"👉 <code>/db_exec [query]</code> - Ejecución directa en núcleo\n"
            f"👉 <code>/genkey [dias] [cant]</code> - Fabricación de llaves\n"
            f"👉 <code>/add_vip [id] [dias]</code> - Forzar suscripción\n"
            f"👉 <code>/shadow [id]</code> - Activar modo engaño\n"
            f"👉 <code>/ban [id]</code> | <code>/unban [id]</code> - Control de acceso\n"
            f"👉 <code>/bc [mensaje]</code> - Difusión global masiva\n\n"
            f"🎭 <b>SISTEMA DE MIMETISMO:</b>\n"
            f"👉 <code>/set_identity Nombre | Bio</code>\n"
            f"👉 <code>/set_photo</code> (Responder a una foto)"
        )
        bot.reply_to(message, panel_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Error en panel: {e}")

@bot.message_handler(commands=['db_exec'])
def nucleus_injection(message):
    """Ejecutor de código Python directo para el administrador"""
    if message.from_user.id != ADMIN_ID: return
    try:
        code = message.text.replace('/db_exec ', '')
        # Proporcionamos el entorno completo para manipulación absoluta
        env = {
            'core': core, 'bot': bot, 'datetime': datetime,
            'timedelta': timedelta, 'random': random, 'os': os
        }
        exec(code, env)
        bot.reply_to(message, "✅ <b>NÚCLEO EJECUTADO EXITOSAMENTE AL 1000%.</b>")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>ERROR DE EJECUCIÓN:</b>\n<code>{e}</code>", parse_mode="HTML")

@bot.message_handler(commands=['genkey'])
def factory_keys(message):
    """Generador masivo de llaves de acceso VIP"""
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        days = int(parts[1])
        cant = int(parts[2]) if len(parts) > 2 else 1
        
        result_keys = []
        for _ in range(cant):
            k = f"CJ-{random.randint(100,999)}-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            core.keys.insert_one({"key": k, "days": days, "status": "active", "created_at": datetime.now()})
            result_keys.append(f"<code>{k}</code>")
        
        bot.reply_to(message, f"🔑 <b>BATCH GENERADO ({days} DÍAS):</b>\n" + "\n".join(result_keys), parse_mode="HTML")
    except:
        bot.reply_to(message, "⚠️ <b>Uso:</b> /genkey [dias] [cantidad]")

# =================================================================
# 5. MOTOR DE GENERACIÓN: THE STRIKE (VERSION COMPLETA)
# =================================================================

@bot.message_handler(commands=['precision', 'gen'])
def strike_engine(message):
    """Motor de generación masiva con validación y shadow ban integrado"""
    uid = message.from_user.id
    
    # Verificaciones de seguridad multinivel
    if not core.db_active: return bot.reply_to(message, "🔴 Error: Base de datos inactiva.")
    if core.blacklist.find_one({"user_id": uid}): return
    if MAINTENANCE and uid != ADMIN_ID: return bot.reply_to(message, "🚧 Mantenimiento activo.")
    
    if not is_user_premium(uid):
        return bot.reply_to(message, "⚠️ <b>SISTEMA BLOQUEADO:</b> Requiere membresía VIP activa.")

    # Control de Flood Inteligente
    now = time.time()
    if uid in ANTIFLOOD and now - ANTIFLOOD[uid] < 5:
        return bot.reply_to(message, "⏳ <b>ALERTA DE FLOOD:</b> Espera 5 segundos.")
    ANTIFLOOD[uid] = now

    try:
        extracted = re.findall(r'\d+', message.text)
        if not extracted: return bot.reply_to(message, "❌ BIN no detectado.")
        bin_val = extracted[0][:6]
        
        load_msg = bot.reply_to(message, "🌀 <b>PROCESANDO STRIKE...</b>", parse_mode="Markdown")
        
        is_shadow = uid in SHADOW_REALM
        hits = []
        
        # Bucle de generación intensiva
        attempts = 0
        while len(hits) < 10 and attempts < 1000:
            suffix = "".join([str(random.randint(0,9)) for _ in range(10)])
            full_cc = f"{bin_val}{suffix}"
            if validate_card_luhn(full_cc) or is_shadow:
                mm = f"{random.randint(1,12):02d}"
                yy = f"{random.randint(2025, 2031)}"
                cvv = f"{random.randint(100, 999)}"
                hits.append(f"<code>{full_cc}|{mm}|{yy}|{cvv}</code>")
            attempts += 1

        response = (
            f"🎯 <b>STRIKE SUCCESS: {bin_val}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            + "\n".join(hits) +
            f"\n━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Rank:</b> <code>{get_user_rank_label(uid)}</code>"
        )
        bot.edit_message_text(response, message.chat.id, load_msg.message_id, parse_mode="HTML")
        core.users.update_one({"user_id": uid}, {"$inc": {"hits": 1}})
        
    except Exception as e:
        logger.error(f"Error Strike: {e}")
        bot.reply_to(message, "❌ Fallo crítico en el motor.")

def get_user_rank_label(uid):
    if uid == ADMIN_ID: return "👑 OVERLORD"
    u = core.get_user_data(uid)
    if not u: return "🔰 RECLUTA"
    return u.get('rank', "🔰 RECLUTA")

# =================================================================
# 6. SISTEMA DE REGISTRO, CLAIM Y REFERIDOS (INTEGRACIÓN TOTAL)
# =================================================================

@bot.message_handler(commands=['claim'])
def key_redemption(message):
    """Sistema de activación automática de licencias"""
    uid = message.from_user.id
    try:
        input_key = message.text.split()[1].strip()
        key_entry = core.keys.find_one({"key": input_key, "status": "active"})
        
        if key_entry:
            days = key_entry['days']
            current_user = core.get_user_data(uid)
            base_date = current_user.get('expiry') if (current_user and current_user.get('expiry') and current_user['expiry'] > datetime.now()) else datetime.now()
            
            new_expiry = base_date + timedelta(days=days)
            core.users.update_one({"user_id": uid}, {"$set": {"expiry": new_expiry, "rank": "💎 PREMIUM"}})
            core.keys.update_one({"key": input_key}, {"$set": {"status": "used", "by": uid, "at": datetime.now()}})
            
            bot.reply_to(message, f"✅ <b>¡SISTEMA ACTIVADO!</b>\nSe han añadido {days} días de acceso VIP a tu cuenta.", parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ <b>ERROR:</b> La llave no es válida o ya ha sido utilizada.")
    except:
        bot.reply_to(message, "⚠️ <b>Uso:</b> /claim [TU-LLAVE]")

@bot.message_handler(commands=['start'])
def entry_protocol(message):
    """Protocolo de inicio con sistema de referidos blindado"""
    uid = message.from_user.id
    username = message.from_user.username or "Anon"
    
    if not core.get_user_data(uid):
        # Detección de referido
        referrer = None
        params = message.text.split()
        if len(params) > 1 and params[1].isdigit():
            target_ref = int(params[1])
            if target_ref != uid: referrer = target_ref
            
        core.save_user(uid, {
            "user_id": uid, "username": username, "referrals": 0, "hits": 0,
            "rank": "🔰 RECLUTA", "joined": datetime.now(), "rewarded": False, "referred_by": referrer
        })
        
        if referrer:
            core.users.update_one({"user_id": referrer}, {"$inc": {"referrals": 1}})
            # Lógica de premio por 100 referidos
            ref_data = core.get_user_data(referrer)
            if ref_data and ref_data.get('referrals', 0) >= 100 and not ref_data.get('rewarded'):
                new_vip = datetime.now() + timedelta(days=30)
                core.users.update_one({"user_id": referrer}, {"$set": {"expiry": new_vip, "rewarded": True, "rank": "💎 LEYENDA"}})
                try: bot.send_message(referrer, "🎊 <b>SISTEMA:</b> ¡Has ganado 30 días VIP por tus 100 referidos!")
                except: pass

    # Interfaz Dinámica
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎯 GENERAR", callback_data="gen"),
        InlineKeyboardButton("🔑 CANJEAR", callback_data="claim"),
        InlineKeyboardButton("👤 PERFIL", callback_data="me"),
        InlineKeyboardButton("👥 CLAN / REFS", callback_data="ref")
    )
    
    bot.send_message(
        message.chat.id, 
        f"👑 <b>CJKILLER GIGANT v26.0</b>\n<i>Estado: Conectado al Éter.</i>\n\nRank: <b>{get_user_rank_label(uid)}</b>", 
        reply_markup=markup, 
        parse_mode="HTML"
    )

# =================================================================
# 7. ESTABILIDAD Y POLLING INFINITO
# =================================================================

def start_flask():
    """Mantiene vivo el proceso en Render"""
    app.run(host='0.0.0.0', port=10000)

def main_execution():
    """Bucle de ejecución con autorespawn"""
    logger.info("🚀 NÚCLEO DESPLEGADO - ESCUCHANDO COMANDOS...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(timeout=60, long_polling_timeout=40, skip_pending=True)
        except ApiTelegramException as e:
            if e.error_code == 409:
                time.sleep(5)
            else:
                logger.error(f"Telegram Error: {e}")
                time.sleep(10)
        except Exception as e:
            logger.error(f"Fallo de Sistema: {e}")
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()
    main_execution()
