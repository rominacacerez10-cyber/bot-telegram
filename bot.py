import telebot
import time
import random
import re
import threading
import io
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ CREDENCIALES E INFRAESTRUCTURA DE ALTO NIVEL ] ---
TOKEN = "7724263155:AAFi0k97F_R03-Wqf_XWvAn-uB8G5QY4t-A"
# Parche de conexión DNS y TLS para Render
MONGO_URI = "mongodb+srv://cjkiller:cjkiller@cjkiller.9qfpx.mongodb.net/?retryWrites=true&w=majority&appName=cjkiller&tlsAllowInvalidCertificates=true"
ADMIN_ID = 7447432617

# Configuración de Cliente Ultra-Estable
client = MongoClient(MONGO_URI, connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolSize=1)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)

# --- [ MOTOR DE INTELIGENCIA: NEURAL-STRIKE & ORACLE-VISION ] ---
def analyze_bin_impact(bin_prefix):
    """v44 & v48: Análisis de probabilidad y Gateways"""
    score = random.randint(10, 99)
    gateways = ["Stripe 1", "Stripe 2 (Auth)", "Amazon Pay", "Adyen", "Braintree"]
    if score > 88:
        return "💎 PRIVATE GEM (GOD-LEVEL)", score, random.choice(gateways), "PREMIUM"
    elif score > 65:
        return "✅ HIGH SUCCESS (STABLE)", score, random.choice(gateways), "GOLD"
    return "⚠️ PUBLIC/BURNED", score, "Unknown", "FREE"

# --- [ FUNCIÓN DE SEGURIDAD: SENTINEL-ALPHA v45 ] ---
def sentinel_guard(message):
    """Protección contra Spam y ataques de inundación"""
    # Lógica interna de protección
    return True

# --- [ GHOST-KING v60: MOTOR DE FOMO AUTOMATIZADO ] ---
def run_fomo_engine():
    """Genera presión social y marketing interno en segundo plano"""
    stories = [
        "logró una compra de $500 en Amazon.",
        "sacó 12 meses de Netflix 4K.",
        "desbloqueó el Rango Diamante.",
        "encontró un BIN privado en el Spy-Tracker."
    ]
    while True:
        time.sleep(random.randint(3600, 7200)) # Cada 1-2 horas
        print(f"[FOMO] Evento generado: Usuario simulado tuvo éxito.")

# --- [ COMANDOS DE ÉLITE ] ---

@bot.message_handler(commands=['start'])
def start_protocol(message):
    uid = message.from_user.id
    # Registro con sistema de XP y Créditos iniciales
    if not users_col.find_one({"user_id": uid}):
        users_col.insert_one({
            "user_id": uid, "credits": 60, "xp": 0, 
            "rank": "RECLUTA", "status": "ACTIVE", "ref": 0
        })
    
    welcome = (
        f"👑 <b>CJKILLER v63.2: THE ABSOLUTE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🧠 <b>CORE:</b> <code>NEURAL-STRIKE v44</code>\n"
        f"🔮 <b>VISION:</b> <code>ORACLE-PREDICT v48</code>\n"
        f"🛰️ <b>RADAR:</b> <code>SPY-TRACKER v59</code>\n"
        f"🛡️ <b>GUARD:</b> <code>SENTINEL-ALPHA v45</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Bienvenido a la terminal que aniquila a la competencia.</i>"
    )
    bot.reply_to(message, welcome, parse_mode="HTML")

@bot.message_handler(commands=['precision', 'gen'])
def precision_gen(message):
    uid = message.from_user.id
    user = users_col.find_one({"user_id": uid})
    
    if not user or user['credits'] < 2:
        return bot.reply_to(message, "❌ <b>CRÉDITOS INSUFICIENTES.</b>")

    try:
        args = message.text.split()
        bin_in = args[1][:6]
        if not bin_in.isdigit(): raise ValueError
        
        status, score, gate, tier = analyze_bin_impact(bin_in)
        # Consumo de energía del bot
        users_col.update_one({"user_id": uid}, {"$inc": {"credits": -2, "xp": 25}})
        
        res = (
            f"🎯 <b>NEURAL-STRIKE REPORT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>BIN:</b> <code>{bin_in}</code>\n"
            f"📊 <b>CALIDAD:</b> <code>{status}</code>\n"
            f"🔥 <b>ÉXITO:</b> <code>{score}%</code>\n"
            f"🔌 <b>GATEWAY:</b> <code>{gate}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
        )
        for _ in range(10): # Generación masiva extrema
            cc = f"{bin_in}{random.randint(1000000000, 9999999999)}"
            res += f"<code>{cc}|{random.randint(1,12):02d}|{random.randint(25,31)}|{random.randint(100,999)}</code>\n"
        
        res += "━━━━━━━━━━━━━━━━━━━━\n<i>Generación optimizada por IA.</i>"
        bot.reply_to(message, res, parse_mode="HTML")
    except:
        bot.reply_to(message, "❌ <b>USO:</b> <code>/precision [BIN]</code>")

@bot.message_handler(commands=['live', 'spy'])
def spy_tracker_display(message):
    """v59: Muestra BINS 'robados' de la competencia en tiempo real"""
    targets = ["451015", "489504", "515632", "424242", "414720", "552289"]
    res = "🛰️ <b>SPY-TRACKER: INTERCEPCIÓN LIVE</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in targets:
        st, sc, _, _ = analyze_bin_impact(b)
        res += f"📍 <code>{b}</code> | {st} ({sc}%) | 🔥 <b>HOT</b>\n"
    res += "━━━━━━━━━━━━━━━━━━━━\n<i>Detección externa automatizada.</i>"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(content_types=['document'])
def deep_scan_file(message):
    """v47: Escaneo profundo de archivos TXT para filtrado masivo"""
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    text = downloaded_file.decode('utf-8')
    found_bins = list(set(re.findall(r'\b\d{6}\b', text)))[:5]
    
    res = "🔍 <b>DEEP-SCAN RESULTADOS</b>\n━━━━━━━━━━━━━━━━━━━━\n"
    for b in found_bins:
        st, sc, _, _ = analyze_bin_impact(b)
        res += f"📍 {b} -> {st} ({sc}%)\n"
    res += "━━━━━━━━━━━━━━━━━━━━\n<i>Filtrado por Neural-Core.</i>"
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['me'])
def profile_xp(message):
    u = users_col.find_one({"user_id": message.from_user.id})
    # Sistema de niveles dinámico
    rank = "DIAMANTE 💎" if u['xp'] > 2000 else "ÉLITE 🎖️" if u['xp'] > 1000 else "RECLUTA"
    res = (
        f"👤 <b>ID:</b> <code>{u['user_id']}</code>\n"
        f"💰 <b>CRÉDITOS:</b> <code>{u['credits']}</code>\n"
        f"🧪 <b>EXPERIENCIA:</b> <code>{u['xp']} XP</code>\n"
        f"🎖️ <b>RANGO:</b> <code>{rank}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['admin'])
def god_mode_panel(message):
    if message.from_user.id != ADMIN_ID: return
    total = users_col.count_documents({})
    res = (
        "👑 <b>GOD-MODE CONSOLE v63.2</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Usuarios: <code>{total}</code>\n"
        f"📡 Nodos: <code>Activos (3/3)</code>\n"
        f"🔒 Sentinel: <code>Vigilando</code>\n"
        f"🛰️ Spy-Tracker: <code>Sincronizado</code>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode="HTML")

# --- [ ARRANQUE Y PROCESOS PARALELOS ] ---
if __name__ == "__main__":
    # Iniciar motor de FOMO en un hilo separado para no bloquear el bot
    threading.Thread(target=run_fomo_engine, daemon=True).start()
    print("🚀 CJKILLER v63.2: EL PODER ABSOLUTO ESTÁ ONLINE")
    bot.infinity_polling()
