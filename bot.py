import os
import telebot
import requests
import io
import json
import base64
from datetime import datetime
from pymongo import MongoClient
from telebot import types

# --- 1. CONFIGURACIÓN E IDENTIDAD ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
ID_CANAL_NOTICIAS = "@CJkiller_News"

# ENLACE DE MONGODB
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

# --- 2. INICIALIZACIÓN ---
bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 3. LÓGICA DE ENCRIPTACIÓN ADYEN (Arquitectura de tus archivos) ---
def encrypt_adyen(card, month, year, cvv, adyen_key):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z"
        # Estructura de bypass basada en la lógica de index.js
        payload = f"{card}|{month}|{year}|{cvv}|{gen_time}"
        encoded_data = base64.b64encode(payload.encode()).decode()
        return {
            "success": True, 
            "encrypted": f"adyenjs_0_1_25${encoded_data}",
            "time": gen_time
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- 4. COMANDOS ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    
    # Registro silencioso en DB
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({
            "user_id": user_id,
            "username": username,
            "credits": 10,  # Regalo inicial de créditos
            "role": "user",
            "joined_at": datetime.now()
        })

    welcome_text = (
        f"🔥 **CJKILLER PRIVATE NETWORK v5.0** 🔥\n\n"
        f"👤 **Usuario:** @{username}\n"
        f"🆔 **ID:** `{user_id}`\n\n"
        "🚀 **COMANDOS DISPONIBLES:**\n"
        "🔹 `/adyen CC|MES|ANO|CVV KEY` - Encriptador Elite\n"
        "🔹 Envía un archivo `.txt` para encriptación masiva."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    input_text = message.text.split()
    if len(input_text) < 3:
        return bot.reply_to(message, "📝 Uso: `/adyen CC|MES|ANO|CVV ADYEN_KEY`", parse_mode="Markdown")
    
    lista, key = input_text[1], input_text[2]
    p = lista.split('|')
    if len(p) == 4:
        res = encrypt_adyen(p[0], p[1], p[2], p[3], key)
        if res["success"]:
            bot.reply_to(message, f"💎 **ADYEN ENCRYPTED**\n\n`{res['encrypted']}`", parse_mode="Markdown")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith('.txt'):
        msg = bot.reply_to(message, "📩 Envíame la **ADYEN_KEY** para este archivo:")
        bot.register_next_step_handler(msg, process_txt, message.document)

def process_txt(message, doc):
    key = message.text
    file_info = bot.get_file(doc.file_id)
    downloaded = bot.download_file(file_info.file_path).decode('utf-8')
    
    results = []
    for line in downloaded.splitlines()[:100]: # Límite de 100 líneas por archivo
        p = line.replace('|', ' ').split()
        if len(p) >= 4:
            res = encrypt_adyen(p[0], p[1], p[2], p[3], key)
            if res["success"]:
                results.append(f"{p[0]}|{p[1]}|{p[2]}|{p[3]} -> {res['encrypted']}")
    
    output = io.BytesIO("\n".join(results).encode())
    output.name = "cjkiller_mass_adyen.txt"
    bot.send_document(message.chat.id, output, caption=f"✅ {len(results)} Tarjetas procesadas.")

# --- 5. RUN ---
if __name__ == "__main__":
    print("🚀 CJkiller v5.0 is LIVE...")
    bot.infinity_polling()
