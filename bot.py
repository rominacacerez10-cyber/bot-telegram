import telebot
import os
import time
import threading
import requests
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892

# Desactivamos el threading interno para evitar choques
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'shk'])
def handle_commands(message):
    if message.text.startswith('/start'):
        bot.reply_to(message, "✅ **CJkiller v20.5 ESTABLE**\nConexión única establecida.")
    elif message.text.startswith('/shk'):
        if message.from_user.id == OWNER_ID:
            bot.reply_to(message, "🔍 Consultando... (Conexión limpia)")

@app.route('/')
def home():
    return "Bot status: OK"

def run_bot():
    """Bucle de conexión con limpieza de Webhook forzada"""
    while True:
        try:
            # LIMPIEZA TOTAL: Matamos cualquier rastro de conexiones previas
            print(">>> Limpiando servidores de Telegram...")
            requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=True")
            time.sleep(5) 
            
            print(">>> Iniciando polling exclusivo...")
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            # Si hay conflicto 409, esperamos 15 segundos para que Render mate el proceso viejo
            print(f"Conflicto detectado: {e}. Esperando cierre de proceso anterior...")
            time.sleep(15)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
