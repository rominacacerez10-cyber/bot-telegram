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
    """Asegura que tú tengas créditos infinitos en la DB"""
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
    bot.reply_to(message, f"🚀 **CJkiller v20.5 ONLINE**\n\nHola {nombre}, el bot está listo y la conexión ha sido limpiada. \nPrueba `/shk 450012` ahora.", parse_mode="Markdown")

@bot.message_handler(commands=['shk'])
def shk_cmd(message):
    # Verificación de seguridad (Solo el dueño)
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "❌ **Uso:** `/shk 450012xxxx`", parse_mode="Markdown")
    
    target = args[1]
    sent_msg = bot.reply_to(message, "🔍 **Consultando SHK...**", parse_mode="Markdown")
    
    # Simulación de proceso estable
    time.sleep(1.5)
    
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=sent_msg.message_id,
        text=f"✅ **RESULTADO SHK**\n\n**BIN/CC:** `{target}`\n**ESTADO:** `Limpio` \n**DETALLE:** `Conexión estable en Render`",
        parse_mode="Markdown"
    )

# --- INTEGRACIÓN CON RENDER (AJUSTE FINAL ANTI-CONFLICTO) ---

@app.route('/')
def home():
    return "CJkiller Bot is Live and Healthy"

def run_bot_polling():
    """Mantiene al bot escuchando y soluciona el error 409 de conflicto"""
    while True:
        try:
            # Forzamos la limpieza de webhooks para evitar el error 'Conflict'
            bot.remove_webhook()
            print(">>> Conexión limpia. Iniciando Polling sin conflictos...")
            # infinity_polling con timeout ajustado para Render
            bot.infinity_polling(timeout=40, long_polling_timeout=20, restart_on_change=True)
        except Exception as e:
            # Si hay un error de conexión, espera 5 segundos y reintenta solo
            print(f"Reintentando conexión por error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # 1. Hilo para el Bot con daemon=True para que no bloquee el cierre
    threading.Thread(target=run_bot_polling, daemon=True).start()
    
    # 2. Servidor Flask para que Render mantenga el servicio 'Live'
    port = int(os.environ.get("PORT", 10000))
