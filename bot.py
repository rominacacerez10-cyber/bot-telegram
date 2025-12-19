import telebot
from flask import Flask
import threading
import os

# 1. Configuración del Bot con tu Token verificado
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
bot = telebot.TeleBot(TOKEN)

# 2. Configuración de Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot en linea"

# 3. Comandos del Bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ ¡Bot encendido y listo!")

@bot.message_handler(commands=['chk'])
def chk_card(message):
    try:
        input_data = message.text.split(maxsplit=1)[1]
        bot.reply_to(message, f"🔍 **Procesando:** `{input_data}`")
    except:
        bot.reply_to(message, "❌ Envía: `/chk tarjeta|mes|año|cvv`")

# 4. Iniciar el bot en un hilo para que no bloquee a Gunicorn
def run_bot():
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

# Iniciamos el hilo inmediatamente
bot_thread = threading.Thread(target=run_bot)
bot_thread.daemon = True
bot_thread.start()

# No usamos app.run() aquí, Gunicorn se encarga
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
