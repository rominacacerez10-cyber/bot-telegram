import os
import telebot
import base64
import json
import time
import threading
from flask import Flask
from datetime import datetime
from pymongo import MongoClient

# --- 1. CONFIGURACIÓN DEL SERVIDOR WEB (Para que Render no lo cierre) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

def run_flask():
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)

# --- 2. CONFIGURACIÓN DEL BOT ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN, threaded=False)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 3. LÓGICA DE ENCRIPTACIÓN ---
def encrypt_adyen(card, month, year, cvv):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {
            "number": card, "cvc": cvv,
            "expiryMonth": month, "expiryYear": year,
            "generationtime": gen_time
        }
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except:
        return {"success": False}

# --- 4. COMANDOS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ **CJKILLER ONLINE**\nUsa `/adyen CC|MES|ANO|CVV`", parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        parts = message.text.split()
        datos = parts[1].split('|')
        res = encrypt_adyen(datos[0], datos[1], datos[2], datos[3])
        bot.reply_to(message, f"💎 **RESULTADO:**\n`{res['encrypted']}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Formato: `/adyen CC|MES|ANO|CVV`")

# --- 5. ARRANQUE SEGURO ---
if __name__ == "__main__":
    # Iniciar el servidor web en un hilo aparte
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("🚀 Iniciando bot con servidor web...")
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            print(f"⚠️ Error: {e}. Reintentando...")
            time.sleep(5)
