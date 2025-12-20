import telebot
import os
import time
import threading
from pymongo import MongoClient
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.from_user.id == OWNER_ID:
        users_col.update_one({"id": OWNER_ID}, {"$set": {"role": "OWNER", "credits": 999999}}, upsert=True)
    bot.reply_to(message, "✅ **CJkiller v20.5 Estable**\nLa conexión se ha limpiado correctamente.")

@bot.message_handler(commands=['shk'])
def shk_cmd(message):
    if message.from_user.id != OWNER_ID: return
    bot.reply_to(message, "🔍 Comando SHK activo y funcionando.")

@app.route('/')
def home(): return "Bot Live"

def run_bot():
    # TRUCO PARA PLAN FREE:
    # Esperamos 15 segundos antes de conectar para que Render mate el bot anterior
    print(">>> Esperando liberación de conexión (15s)...")
    time.sleep(15)
    
    while True:
        try:
            bot.delete_webhook()
            print(">>> Conectando con Telegram...")
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            # Si hay conflicto 409, esperamos más tiempo para reintentar
            print(f"Conflicto: {e}. Reintentando en 10s...")
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
