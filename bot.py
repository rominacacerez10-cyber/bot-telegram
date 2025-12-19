import telebot
from flask import Flask
import threading
import os

# 1. Configuración de Flask para Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

# 2. Configuración de tu Bot (PON TU NUEVO TOKEN AQUÍ)
TOKEN = "8106789282:ASHQ8vaNTeS0p8DVb4L1khGbahTDPy0nNgU"
bot = telebot.TeleBot(TOKEN)

# 3. Tus comandos (Ejemplo del comando /chk)
@bot.message_handler(commands=['start', 'chk'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Bot CJkiller activo y respondiendo.")

# --- Puedes agregar aquí el resto de tus funciones y decoradores ---

# 4. Bloque de arranque (Lo que evita el bloqueo entre Flask y el Bot)
if __name__ == "__main__":
    def run_bot():
        print("🚀 Intentando conectar con Telegram...")
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Error en el bot: {e}")

    # Arrancar el Bot en un hilo separado
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Arrancar Flask en el puerto que pide Render
    print("🌐 Arrancando servidor Flask...")
    app.run(host="0.0.0.0", port=10000)
