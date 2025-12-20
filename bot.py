import telebot
import requests
import time
import random
import re
import os
import threading
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask

# --- CONFIGURACIÓN DE NÚCLEO ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
MONGO_URI = os.environ.get("MONGO_URI") # Configurado en Render

# Conexión a Base de Datos
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
user_cooldowns = {}

# --- FUNCIONES DE LÓGICA ---
def get_user(user_id):
    user = users_col.find_one({"id": user_id})
    if not user and user_id == OWNER_ID:
        user = {"id": OWNER_ID, "credits": 999999, "role": "OWNER"}
        users_col.insert_one(user)
    return user

def has_access(user_id):
    if user_id == OWNER_ID: return True
    user = get_user(user_id)
    return user is not None and user.get("credits", 0) > 0

# --- COMANDOS ADMIN ---
@bot.message_handler(commands=['add'])
def add_user_cmd(message):
    if message.from_user.id != OWNER_ID: return
    try:
        args = message.text.split()
        target_id, credits = int(args[1]), int(args[2])
        users_col.update_one({"id": target_id}, {"$inc": {"credits": credits}, "$set": {"role": "VIP"}}, upsert=True)
        bot.reply_to(message, f"💎 **ID {target_id} actualizado con {credits} créditos.**")
    except: bot.reply_to(message, "❌ `/add ID CREDITS`")

# --- COMANDO SCRAPER ---
@bot.message_handler(commands=['scr'])
def scraper_cmd(message):
    if not has_access(message.from_user.id): return
    
    text = message.reply_to_message.text if message.reply_to_message else message.text.replace('/scr', '')
    cards = re.findall(r'\d{15,16}[\s|/|-]\d{1,2}[\s|/|-]\d{2,4}[\s|/|-]\d{3,4}', text)
    
    if not cards:
        bot.reply_to(message, "❌ No detecté tarjetas.")
        return

    clean_cards = list(set([re.sub(r'[\s|/|-]+', '|', c) for c in cards]))
    bot.reply_to(message, f"🏴‍☠️ **CARDS EXTRACTED:**\n\n" + "\n".join(clean_cards[:15]), parse_mode="Markdown")

# --- COMANDO GEN ---
@bot.message_handler(commands=['gen'])
def gen_cmd(message):
    if not has_access(message.from_user.id): return
    try:
        bin_val = message.text.split()[1]
        res = [f"`{bin_val}{''.join([str(random.randint(0,9)) for _ in range(16-len(bin_val))])}|{random.randint(1,12):02d}|{random.randint(2025,2030)}|{random.randint(100,999)}`" for _ in range(10)]
        bot.reply_to(message, "💳 **GENERATED:**\n" + "\n".join(res), parse_mode="Markdown")
    except: bot.reply_to(message, "❌ `/gen BIN`")

# --- MENÚ START ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user = get_user(message.from_user.id)
    creds = user.get("credits", 0) if user else 0
    bot.reply_to(message, f"🔥 **CJkiller VIP**\n━━━━━━━━━━\n👤 **USER:** `{message.from_user.first_name}`\n💰 **CR:** `{creds if message.from_user.id != OWNER_ID else 'INF'}`\n━━━━━━━━━━\nUse `/gen`, `/scr`, `/chk1`", parse_mode="Markdown")

# --- FLASK & POLLING ---
@app.route('/')
def home(): return "System Online"

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(timeout=20)).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
