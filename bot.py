import os
import telebot
import requests
import io
import json
import base64
from datetime import datetime
from pymongo import MongoClient
from telebot import types

# --- 1. CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
ID_CANAL_NOTICIAS = "@CJkiller_News"

# Conexión Directa a MongoDB
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

# --- 2. INICIALIZACIÓN ---
bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 3. LÓGICA DE ENCRIPTACIÓN ADYEN (Basada en tus archivos index.js y adyen.php) ---
def encrypt_adyen(card, month, year, cvv, adyen_key):
    try:
        # Generación de tiempo extraída de tu index.js
        gen_time = datetime.utcnow().isoformat() + "Z" 
        
        # Estructura de payload para el bypass de Adyen
        payload = {
            "number": card,
            "cvc": cvv,
            "expiryMonth": month,
            "expiryYear": year,
            "generationtime": gen_time
        }
        
        # Codificación base64 simulando el proceso de node-adyen-encrypt
        encoded_payload = base64.b64encode(json.dumps(payload).encode()).decode()
        
        return {
            "success": True, 
            "encrypted": f"adyenjs_0_1_25${encoded_payload}",
            "time": gen_time
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- 4. MANEJO DE COMANDOS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Sin User"
    
    # Registro en base de datos
    user = users_col.find_one({"user_id": user_id})
    if not user:
        users_col.insert_one({
            "user_id": user_id,
            "username": username,
            "credits": 10,
            "role": "user",
            "joined_at": datetime.now()
        })
        user = users_col.find_one({"user_id": user_id})

    welcome_text = (
        f"🔥 **CJKILLER PRIVATE NETWORK** 🔥\n\n"
        f"👤 **Usuario:** @{username}\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"💎 **Créditos:** {user['credits']}\n\n"
        "🚀 **COMANDOS ÉLITE:**\n"
        "🔹 `/adyen CC|MES|ANO|CVV KEY` - Encriptador Adyen\n"
        "🔹 Envía un **.txt** para encriptación masiva."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    input_text = message.text.split()
    if len(input_text) < 3:
        return bot.reply_to(message, "📝 **Uso:** `/adyen CC|MES|ANO|CVV ADYEN_KEY`", parse_mode="Markdown")
    
    lista, key = input_text[1], input_text[2]
    # Limpieza de datos similar a adyen.php
    p = lista.replace('|', ' ').split()
    if len(p) >= 4:
        res = encrypt_adyen(p[0], p[1], p[2], p[3], key)
        if res["success"]:
            bot.reply_to(message, f"💎 **ADYEN RESULT:**\n\n`{res['encrypted']}`", parse_mode="Markdown")

# --- 5. PROCESAMIENTO MASIVO (.TXT) ---

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith('.txt'):
        msg = bot.reply_to(message, "📩 **Archivo recibido.** Envía la **ADYEN_KEY** para procesarlo:")
        bot.register_next_step_handler(msg, process_txt, message.document)

def process_txt(message, doc):
    key = message.text
    file_info = bot.get_file(doc.file_id)
    downloaded = bot.download_file(file_info.file_path).decode('utf-8')
    
    results = []
    # Procesamos línea por línea como lo hacía tu archivo adyen.php
    for line in downloaded.splitlines()[:100]: 
        p = line.replace('|', ' ').split()
        if len(p) >= 4:
            res = encrypt_adyen(p[0], p[1], p[2], p[3], key)
            if res["success"]:
                results.append(f"{p[0]}|{p[1]}|{p[2]}|{p[3]} -> {res['encrypted']}")
    
    output = io.BytesIO("\n".join(results).encode())
    output.name = "cjkiller_results.txt"
    bot.send_document(message.chat.id, output, caption=f"✅ {len(results)} tarjetas procesadas.")

# --- 6. LANZAMIENTO (Solución al error Conflict 409) ---
if __name__ == "__main__":
    # Solución técnica para el error "can't use getUpdates method while webhook is active"
    print("🚀 Eliminando webhooks antiguos para evitar conflictos...")
    bot.remove_webhook() 
    
    print("🚀 CJkiller v5.0 is LIVE...")
    bot.infinity_polling()
