import telebot
import requests
import urllib.parse
from flask import Flask
from threading import Thread
import os

# Configuración
TOKEN = "8106789282:AAF09T8dWH6fy0swDLpyXtbpwY3zJqQBDJw"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot esta vivo"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def ejecutar_checker(cards):
    try:
        cards_clean = cards.strip()
        cards_encoded = urllib.parse.quote(cards_clean)
        api_url = f"https://arturo.alwaysdata.net/MultiHilos/peticion2.php?cards={cards_encoded}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Timeout de 30 segundos para evitar que se quede "pegado"
        response = requests.get(api_url, headers=headers, verify=False, timeout=30)
        return response.text if response.text.strip() else "❌ API sin respuesta."
    except Exception as e:
        return f"❌ Error: {str(e)}"

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    try:
        input_text = message.text.split(maxsplit=1)
        if len(input_text) < 2:
            bot.reply_to(message, "📝 Formato: /chk tarjeta")
            return
        
        sent_message = bot.reply_to(message, "⌛ Procesando tarjetas...")
        resultado = ejecutar_checker(input_text[1])
        bot.edit_message_text(resultado, message.chat.id, sent_message.message_id, parse_mode='HTML')
    except Exception as e:
        print(f"Error en handler: {e}")

if __name__ == "__main__":
    # Iniciar servidor web para Render
    Thread(target=run_flask).start()
    print("🚀 Bot CJkiller iniciado en Render...")
    bot.infinity_polling() 

# Cambio final
