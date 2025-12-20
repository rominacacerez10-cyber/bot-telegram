from datetime import datetime, timedelta
import telebot
import os
from pymongo import MongoClient

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
MONGO_URI = os.environ.get("MONGO_URI") 
OWNER_ID = 7012561892

client = MongoClient(MONGO_URI)
db = client['cjkiller_database']
users_col = db['vip_users']

bot = telebot.TeleBot(TOKEN, threaded=False)

# --- SISTEMA DE TIEMPO ---
def add_vip_with_time(user_id, days):
    expiry_date = datetime.now() + timedelta(days=days)
    # Guardamos el ID y la fecha de vencimiento
    users_col.update_one(
        {"user_id": user_id},
        {"$set": {"expiry": expiry_date.isoformat()}},
        upsert=True
    )
    return expiry_date.strftime('%Y-%m-%d')

def get_remaining_days(user_id):
    user = users_col.find_one({"user_id": user_id})
    if not user or "expiry" not in user: return 0
    
    expiry = datetime.fromisoformat(user["expiry"])
    remaining = (expiry - datetime.now()).days
    return max(0, remaining)

# --- COMANDOS DE ADMIN ---
@bot.message_handler(commands=['add'])
def add_vip(message):
    if message.from_user.id != OWNER_ID: return
    try:
        # Uso: /add ID DIAS (Ej: /add 12345 30)
        args = message.text.split()
        new_id = int(args[1])
        days = int(args[2]) if len(args) > 2 else 30
        
        date_str = add_vip_with_time(new_id, days)
        bot.reply_to(message, f"✅ **USUARIO ACTIVADO**\n🆔 ID: `{new_id}`\n📅 Vence: `{date_str}`\n⏳ Días: `{days}`")
    except:
        bot.reply_to(message, "❌ **Uso:** `/add ID DIAS`")

# --- MENÚ CON INFO DINÁMICA ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    days_left = get_remaining_days(user_id)
    
    if user_id != OWNER_ID and days_left <= 0:
        bot.reply_to(message, "🚫 **TU MEMBRESÍA HA EXPIRADO.**\nContacta al dueño para renovar.")
        return

    status = "INFINITY ♾️" if user_id == OWNER_ID else f"{days_left} Días"
    
    menu = (
        f"🛰️ **CJkiller v18.0 - VIP ACCESS**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **OPERADOR:** `{message.from_user.first_name}`\n"
        f"⏳ **EXPIRACIÓN:** `{status}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Utiliza `/gen`, `/chk1` o `/bin` para comenzar."
    )
    bot.send_message(message.chat.id, menu, parse_mode="Markdown")
