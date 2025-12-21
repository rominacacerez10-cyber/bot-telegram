import os
import telebot
import requests
import io
import json
import base64
import time
from datetime import datetime
from pymongo import MongoClient

# --- 1. CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

# Inicializamos el bot sin hilos para evitar el error de conflicto 409
bot = telebot.TeleBot(TOKEN, threaded=False)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 2. LÓGICA DE ENCRIPTACIÓN ADYEN ---
def encrypt_adyen(card, month, year, cvv, adyen_key):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {
            "number": card,
            "cvc": cvv,
            "expiryMonth": month,
            "expiryYear": year,
            "generationtime": gen_time
        }
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- 3. MANEJO DE COMANDOS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user = users_col.find_one({"user_id": user_id})
    if not user:
        users_col.insert_one({"user_id": user_id, "credits": 10, "joined_at": datetime.now()})
    
    bot.reply_to(message, "🔥 **CJKILLER NET ACTIVADO** 🔥\n\nUsa `/adyen CC|MES|ANO|CVV KEY` o envía un .txt", parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            return bot.reply_to(message, "❌ Formato: `/adyen CC|MES|ANO|CVV KEY`")
        
        datos = parts[1].split('|')
        res = encrypt_adyen(datos[0], datos[1], datos[2], datos[3], parts[2])
        if res["success"]:
            bot.reply_to(message, f"💎 **RESULTADO:**\n`{res['encrypted']}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Error al procesar.")

# --- 4. PROCES
