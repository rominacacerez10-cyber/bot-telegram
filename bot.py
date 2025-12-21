import os
import telebot
import requests
import io
import json
import base64
from datetime import datetime
from pymongo import MongoClient

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN, threaded=False) # Desactivamos hilos para evitar el error 409
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

def encrypt_adyen(card, month, year, cvv, adyen_key):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {"number": card, "cvc": cvv, "expiryMonth": month, "expiryYear": year, "generationtime": gen_time}
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except: return {"success": False}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ **BOT ACTIVO**\nUsa `/adyen CC|MES|ANO|CVV KEY`", parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        parts = message.text.split()
        datos = parts[1].split('|')
        res = encrypt_adyen(datos[0], datos[1], datos[2], datos[3], parts[2])
        bot.reply_to(message, f"`{res['encrypted']}`", parse_mode="Markdown")
    except: bot.reply_to(message, "❌ Error en formato.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith('.txt'): # Dos puntos agregados correctamente
        msg = bot.reply_to(message, "📩 Envía la **ADYEN_KEY**:")
        bot.register_next_step_handler(msg, process_txt, message.document)

def process_txt(message, doc):
    key = message.text
    file_info = bot.get_file(doc.file_id)
    downloaded = bot.download_file(file_info.file_path).decode('utf-8')
    results = []
    for line in downloaded.splitlines()[:50]:
        try:
            d = line.replace('|',' ').split()
            res = encrypt_adyen(d[0], d[1], d[2], d[3], key)
            results.append(f"{line} -> {res['encrypted']}")
        except: list
    output = io.BytesIO("\n".join(results).encode())
    output.name = "res.txt"
    bot.send_document(message.chat.id, output)

if __name__ == "__main__":
    print("🚀 Matando conexiones previas...")
    bot.remove_webhook() # Limpieza total de webhooks
    print("🚀 Iniciando polling limpio...")
    bot.polling(none_stop=True, interval=0, timeout=20)
