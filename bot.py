import telebot
import os
from flask import Flask, request

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
# Asegúrate de que esta URL coincida exactamente con la de tu Dashboard de Render
URL_PROYECTO = "https://cjkiller-bot.onrender.com" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- COMANDOS ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ **SISTEMA ESTABILIZADO**\nCJkiller v20.5 ahora funciona mediante Webhook para evitar conflictos.", parse_mode="Markdown")

@bot.message_handler(commands=['shk'])
def shk(message):
    bot.reply_to(message, "🔍 Procesando SHK en modo estable...")

# --- RUTA DEL WEBHOOK ---
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook_setup():
    bot.remove_webhook()
    # Esto le dice a Telegram a dónde enviar los mensajes
    bot.set_webhook(url=URL_PROYECTO + '/' + TOKEN)
    return "Configuración Webhook: EXITOSA", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
