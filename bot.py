import telebot
from flask import Flask
import threading
import os

# 1. Configuración de Flask para Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor CJkiller Activo"

# 2. Configuración del Bot con tu nuevo Token verificado
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
bot = telebot.TeleBot(TOKEN, threaded=False) # Desactivamos hilos internos para evitar conflictos

# 3. Comandos básicos
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "✅ ¡Bot CJkiller en línea! Usa /chk seguido de tu tarjeta.")

@bot.message_handler(commands=['chk'])
def chk_card(message):
    try:
        input_data = message.text.split(maxsplit=1)[1]
        bot.reply_to(message, f"🔍 **Analizando:** `{input_data}`\n⏳ Procesando...")
    except IndexError:
        bot.reply_to(message, "❌ Formato: `/chk numero|mes|año|cvv`")

# 4. Función de ejecución
def run_bot():
    print("🚀 Intentando conectar con Telegram...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # Iniciamos el bot en un hilo separado
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    # Puerto estándar de Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
