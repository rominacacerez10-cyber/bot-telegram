import telebot
import os
import threading
from pymongo import MongoClient
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
MONGO_URI = os.environ.get("MONGO_URI")

# Base de Datos
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- COMANDOS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if user_id == OWNER_ID:
        users_col.update_one({"id": user_id}, {"$set": {"role": "OWNER", "credits": 9999}}, upsert=True)
    
    bot.reply_to(message, "🚀 **CJkiller v20.5 ONLINE**\n\nEl bot ya te escucha. ¡Prueba un comando!", parse_mode="Markdown")

# --- MANTENER VIVO EN RENDER ---
@app.route('/')
def home():
    return "Servidor CJkiller Activo"

def run_bot():
    """Función para que el bot escuche mensajes sin detener el servidor"""
    bot.remove_webhook()
    print("Bot iniciando Polling...")
    bot.infinity_polling(timeout=60)

if __name__ == "__main__":
    # 1. Lanzamos el bot en un hilo separado (Esto es lo que te faltaba)
    threading.Thread(target=run_bot, daemon=True).start()
    
    # 2. Iniciamos Flask en el puerto que pide Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
