import telebot
import os
import time
import threading
import random
from pymongo import MongoClient
from flask import Flask

# --- CONFIGURACIÓN DE NÚCLEO ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
MONGO_URI = os.environ.get("MONGO_URI")

# Conexión a Base de Datos
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- FUNCIONES DE APOYO ---
def setup_owner():
    """Asegura que tú tengas créditos infinitos"""
    users_col.update_one(
        {"id": OWNER_ID},
        {"$set": {"role": "OWNER", "credits": 999999}},
        upsert=True
    )

# --- COMANDOS PRINCIPALES ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    setup_owner()
    nombre = message.from_user.first_name
    bot.reply_to(message, f"🚀 **CJkiller v20.5 ONLINE**\n\nHola {nombre}, el bot está listo. \nUsa `/shk [numero]` para probar el comando corregido.", parse_mode="Markdown")

@bot.message_handler(commands=['shk'])
def shk_cmd(message):
    # Verificación de seguridad
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "❌ **Uso:** `/shk 450012xxxx`", parse_mode="Markdown")
    
    target = args[1]
    sent_msg = bot.reply_to(message, "🔍 **Consultando base de datos SHK...**", parse_mode="Markdown")
    
    # Simulación de proceso (Aquí puedes meter tu lógica de scraping o API)
    time.sleep(1.5)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=sent_msg.message_id,
        text=f"✅ **RESULTADO SHK**\n\n**BIN/CC:** `{target}`\n**ESTADO:** `Limpio` \n**INFO:** `Procesado correctamente en Render`",
        parse_mode="Markdown"
    )

# --- INTEGRACIÓN CON RENDER ---

@app.route('/')
def home():
    return "CJkiller Bot is Live"

def run_bot_polling():
    """Mantiene al bot escuchando sin interrupciones"""
    while True:
        try:
            bot.remove_webhook()
            print(">>> Bot escuchando mensajes...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Error en polling: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # 1. Hilo para el Bot
    threading.Thread(target=run_bot_polling, daemon=True).start()
    
    # 2. Servidor Flask para Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
