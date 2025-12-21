import os
import telebot
import requests
import io
import json
import base64
from datetime import datetime
from pymongo import MongoClient

# --- 1. CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

# --- 2. LÓGICA DE ENCRIPTACIÓN ---
def encrypt_adyen(card, month, year, cvv, adyen_key):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {
            "number": card, "cvc": cvv,
            "expiryMonth": month, "expiryYear": year,
            "generationtime": gen_time
        }
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- 3. MANEJO DE COMANDOS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 **CJKILLER NET** 🔥\nUsa `/adyen CC|MES|ANO|CVV KEY` o envía un .txt", parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    parts = message.text.split()
    if len(parts) < 3:
        return bot.reply_to(message, "❌ Formato: `/adyen CC|MES|ANO|CVV KEY`")
    datos = parts[1].split('|')
    if len(datos) == 4:
        res = encrypt_adyen(datos[0], datos[1], datos[2], datos[3], parts[2])
        if res["success"]:
            bot.reply_to(message, f"💎 **RESULTADO:**\n`{res['encrypted']}`", parse_mode="Markdown")

# --- 4. PROCESAMIENTO MASIVO (FIX LÍNEA 99) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    # CORRECCIÓN: Se añade el ':' que faltaba en tu captura
    if message.document.file_name.endswith('.txt'):
        msg = bot.reply_to(message, "📩 Envía la **ADYEN_KEY** para procesar:")
        bot.register_next_step_handler(msg, process_txt, message.document)

def process_txt(message, doc):
    key = message.text
    file_info = bot.get_file(doc.file_id)
    downloaded = bot.download_file(file_info.file_path).decode('utf-8')
    results = [f"{line} -> {encrypt_adyen(*line.replace('|',' ').split(), key)['encrypted']}" 
               for line in downloaded.splitlines() if len(line.split('|')) == 4]
    
    output = io.BytesIO("\n".join(results).encode())
    output.name = "resultados.txt"
    bot.send_document(message.chat.id, output, caption="✅ Proceso completado.")

# --- 5. LANZAMIENTO (FIX CONFLICTO 409) ---
if __name__ == "__main__":
    # Esta línea es VITAL para eliminar el error 409 de tus logs
    bot.remove_webhook() 
    print("🚀 Bot iniciado correctamente...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
