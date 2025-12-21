import os
import telebot
import base64
import json
import time
import threading
from flask import Flask
from datetime import datetime
from pymongo import MongoClient

# --- 1. WEB SERVER (Mantiene el bot vivo en Render) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "CJkiller Bot is Online"

def run_flask():
    # Render usa el puerto 10000 por defecto
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

# Importante: threaded=False para evitar múltiples hilos peleando por el Token
bot = telebot.TeleBot(TOKEN, threaded=False)

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

# --- 5. ARRANQUE CON LIMPIEZA AGRESIVA ---
if __name__ == "__main__":
    # Iniciar Flask en segundo plano
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("🚀 Limpiando sesiones muertas en Telegram...")
    # El secreto para quitar el error 409 es borrar el Webhook Y los mensajes pendientes
    bot.remove_webhook(drop_pending_updates=True)
    time.sleep(2) # Pausa de seguridad
    
    print("🚀 Iniciando Polling...")
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"⚠️ Error detectado: {e}")
            # Si hay conflicto, esperamos más tiempo para que la otra sesión expire
            time.sleep(10)
