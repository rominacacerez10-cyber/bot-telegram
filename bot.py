import os, telebot, base64, json, time, threading, io, random
from flask import Flask
from datetime import datetime
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ CONFIGURACIÓN DE ÉLITE ] ---
TOKEN = "8106789282:AAFI6CEgWuL-nq5jpSf3vSD8pzIlwLvoBLQ"
ADMIN_ID = 7012561892 
LOG_CHANNEL = -1002434567890 # ID de tu canal de registros
REQUIRED_CHANNEL = "@TuCanalOficial" # Marketing Automático
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN, threaded=False)
db = MongoClient(MONGO_URI)['cjkiller_db']
users_col = db['users']
last_msg_time = {}

# --- [ SERVIDOR DE ALTA DISPONIBILIDAD ] ---
app = Flask(__name__)
@app.route('/')
def index(): return "CJKILLER SUPREME ENGINE: ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# --- [ LÓGICA DE APOYO TÉCNICO ] ---
def encrypt_adyen(card, month, year, cvv):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {"number": card, "cvc": cvv, "expiryMonth": month, "expiryYear": year, "generationtime": gen_time}
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "hash": f"adyenjs_0_1_25${encoded}"}
    except: return {"success": False}

def get_fake_data():
    names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph"]
    lasts = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    states = ["NY", "CA", "TX", "FL", "IL", "GA"]
    return {
        "name": f"{random.choice(names)} {random.choice(lasts)}",
        "email": f"{random.choice(names).lower()}{random.randint(100,999)}@gmail.com",
        "address": f"{random.randint(100, 999)} Maple St",
        "city": f"New York, {random.choice(states)}",
        "zip": random.randint(10001, 99999)
    }

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(REQUIRED_CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True

# --- [ INTERFAZ VISUAL PREMIUM ] ---
def main_menu_buttons():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💎 Adyen Hash", callback_data="adyen_info"),
        InlineKeyboardButton("🌍 Fake Data", callback_data="run_fake"),
        InlineKeyboardButton("👤 Perfil", callback_data="show_me"),
        InlineKeyboardButton("🔗 Referidos", callback_data="show_ref"),
        InlineKeyboardButton("📢 Canal Oficial", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@','')}")
    )
    return markup

# --- [ MIDDLEWARE DE SEGURIDAD Y COMANDOS ] ---
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    uid = message.from_user.id
    current_time = time.time()

    # 1. Marketing Automático (Force Subscribe)
    if not is_subscribed(uid) and uid != ADMIN_ID:
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("📢 Únete aquí", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@','')}"))
        return bot.send_message(message.chat.id, "⚠️ **ACCESO RESTRINGIDO**\n\nDebes ser miembro de nuestro canal oficial para usar este bot.\n\n_Tu seguridad es nuestra prioridad._", reply_markup=markup, parse_mode="Markdown")

    # 2. Seguridad Anti-Spam (Borrado automático)
    if uid != ADMIN_ID:
        if uid in last_msg_time and current_time - last_msg_time[uid] < 5: # 5 segundos de cooldown
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return
        last_msg_time[uid] = current_time

    # 3. Procesador de Comandos
    text = message.text
    if text.startswith('/start'):
        user = users_col.find_one({"user_id": uid})
        if not user:
            args = text.split()
            ref_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
            user = {"user_id": uid, "credits": 15, "referrals": 0, "role": "Premium Member"}
            if ref_id and ref_id != uid:
                users_col.update_one({"user_id": ref_id}, {"$inc": {"credits": 5, "referrals": 1}})
                try: bot.send_message(ref_id, "🔥 **Bonus:** Alguien se unió con tu link. +5 Créditos.")
                except: pass
            users_col.insert_one(user)
        
        # --- MENSAJE DE BIENVENIDA DE ÉLITE CON IMAGEN ---
        # Puedes usar una URL de imagen o una imagen subida previamente a Telegram
        # Reemplaza 'URL_DE_TU_IMAGEN' o 'ID_DE_ARCHIVO_TELEGRAM_DE_TU_IMAGEN'
        welcome_image = "https://i.imgur.com/rXyY4v3.jpeg" # <--- Usa la URL de tu logo o imagen
        welcome_caption = (
            "╔═════════════════════╗\n"
            "      ⚔️ **CJKILLER SUPREME** ⚔️\n"
            "╚═════════════════════╝\n"
            f"👋 **Bienvenido, {message.from_user.first_name}!**\n"
            f"💰 **Tu Balance:** {user['credits']} créditos\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🔥 _El Motor de Encriptación y Testing más avanzado del mercado._\n"
            "🔒 _Nivel de Seguridad: Máximo._\n\n"
            "**¡Explora nuestras funciones!**"
        )
        bot.send_photo(message.chat.id, welcome_image, caption=welcome_caption, reply_markup=main_menu_buttons(), parse_mode="Markdown")

    elif text.startswith('/adyen'):
        try:
            cc_data =
