import telebot
from flask import Flask
import os

# 1. Configuración básica
app = Flask(__name__)
TOKEN = "8106789282:AAHQ8vaNTeS0p8DVb4L1khGbahTDPy0nNgU" # Tu token verificado
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return "Servidor activo"

# 2. Comando de prueba
@bot.message_handler(commands=['chk'])
def check(message):
    bot.reply_to(message, "✅ ¡Bot funcionando correctamente!")

# 3. Función de arranque simplificada (SIN THREADING para evitar duplicidad)
if __name__ == "__main__":
    import threading
    # Usamos un nombre de hilo específico para evitar choques
    t = threading.Thread(target=lambda: bot.infinity_polling(timeout=20, long_polling_timeout=10))
    t.daemon = True
    t.start()
    
    # Render usa el puerto 10000 por defecto
    app.run(host="0.0.0.0", port=10000)
