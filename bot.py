import telebot
from flask import Flask
import os

# 1. Configuración de Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor CJkiller Activo"

# 2. Configuración del Bot (Usa tu último Token verificado)
#
TOKEN = "8106789282:AAHQ8vaNTeS0p8DVb4L1khGbahTDPy0nNgU"
bot = telebot.TeleBot(TOKEN)

# 3. Comandos del Bot
@bot.message_handler(commands=['start', 'chk'])
def send_welcome(message):
    bot.reply_to(message, "✅ ¡Bot CJkiller funcionando correctamente en Render!")

# 4. Bloque de ejecución para Render
if __name__ == "__main__":
    # Importante: No usamos threading aquí para evitar el error 409 Conflict
    # El puerto 10000 es el estándar de Render
    app.run(host="0.0.0.0", port=10000)
