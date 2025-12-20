import telebot
import requests
import time
import random
import os
import threading
from pymongo import MongoClient
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
MONGO_URI = os.environ.get("MONGO_URI")

# Conexión a MongoDB (Ya configurada en Render)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- LÓGICA DE USUARIOS ---
def get_user(user_id):
    user = users_col.find_one({"id": user_id})
    if not user and user_id == OWNER_ID:
        user = {"id": OWNER_ID, "credits": 999999, "role": "OWNER"}
        users_col.insert_one(user)
    return user

# --- COMANDOS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    get_user(message.from_user.id)
    bot.reply_to(message, "🚀 **CJkiller v20.5 ONLINE**\n\nEl bot ya recibe tus mensajes correctamente desde Render.", parse_mode="Markdown")

@bot.message_handler(commands=['gen'])
def gen_cmd(message):
    user = get_user(message.from_user.id)
    if not user:
        bot.reply_to(message, "❌ No tienes acceso.")
        return
    bot.reply_to(message, "💳 Generando... (Ejemplo activo)")

# --- INTEGRACIÓN CON RENDER ---
@app.route('/')
def home():
    return "Servidor CJkiller Vivo"

def run_bot_polling():
    """Esta función mantiene al bot escuchando mensajes en segundo plano"""
    while True:
        try:
            bot.remove_webhook()
            print("Iniciando escucha de mensajes (Polling)...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Error en polling: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # 1. Lanzamos el bot en un hilo separado
    threading.Thread(target=run_bot_polling, daemon=True).start()
    
    # 2. Iniciamos el servidor Flask para que Render no apague el servicio
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
