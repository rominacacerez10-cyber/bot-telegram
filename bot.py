import telebot
import os
import time
import threading
import requests
from flask import Flask

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "✅ **CJkiller v20.5 ESTABILIZADO**\nLa guerra de instancias ha terminado.")

@app.route('/')
def home():
    return "Bot is running"

def run_bot():
    # 1. FORZAMOS A TELEGRAM A MATAR CUALQUIER OTRA CONEXIÓN
    print(">>> Solicitando a Telegram limpiar conexiones viejas...")
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
        requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1")
    except:
        pass
    
    # 2. ESPERA LARGA PARA QUE RENDER MATE EL PROCESO ANTERIOR
    print(">>> Pausa de seguridad de 20 segundos...")
    time.sleep(20)

    while True:
        try:
            print(">>> Intentando tomar el control del bot...")
            bot.polling(none_stop=True, interval=3, timeout=30)
        except Exception as e:
            print(f"Conflicto aún presente: {e}. Reintentando...")
            time.sleep(15)

if __name__ == "__main__":
    # Iniciamos el bot en un hilo
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Servidor Flask para Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
