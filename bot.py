import telebot
import os
import time
import threading
from pymongo import MongoClient
from flask import Flask

# --- CONFIGURACIÓN DE NÚCLEO ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- FUNCIONES DE APOYO ---
def setup_owner():
    users_col.update_one(
        {"id": OWNER_ID},
        {"$set": {"role": "OWNER", "credits": 999999}},
        upsert=True
    )

# --- COMANDOS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    setup_owner()
    bot.reply_to(message, "🚀 **CJkiller v20.5 ONLINE**\nConexión estabilizada.", parse_mode="Markdown")

@bot.message_handler(commands=['shk'])
def shk_cmd(message):
    if message.from_user.id != OWNER_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "❌ Uso: `/shk 450012`")
    bot.reply_to(message, f"✅ **SHK RESULT:** `{args[1]}` | Limpio")

# --- MANTENIMIENTO Y REDIRECCIÓN ---
@app.route('/')
def home():
    return "Bot status: Active"

def run_bot_polling():
    """Bucle infinito para evitar el error 409 y salidas prematuras"""
    while True:
        try:
            bot.remove_webhook()
            print(">>> Iniciando polling limpio...")
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception as e:
            print(f"Error detectado: {e}. Reintentando en 10s...")
            time.sleep(10)

if __name__ == "__main__":
    # Iniciar bot en segundo plano
    threading.Thread(target=run_bot_polling, daemon=True).start()
    # Iniciar servidor web requerido por Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
