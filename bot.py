import os
import telebot
import base64
import json
import time
import threading
from flask import Flask
from datetime import datetime

# --- 1. SERVIDOR WEB (Para mantener el bot vivo en Render) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "CJKiller Bot is Active with New Token"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CONFIGURACIÓN ---
# Token actualizado satisfactoriamente
TOKEN = "8106789282:AAFI6CEgWuL-nq5jpSf3vSD8pzIlwLvoBLQ"
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
    bot.reply_to(message, "🔥 **CJKILLER ONLINE**\n\nEl bot se ha reiniciado correctamente con el nuevo Token.\nUsa `/adyen CC|MES|ANO|CVV`", parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        parts = message.text.split()
        datos = parts[1].split('|')
        res = encrypt_adyen(datos[0], datos[1], datos[2], datos[3])
        if res["success"]:
            bot.reply_to(message, f"💎 **RESULTADO:**\n`{res['encrypted']}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Formato: `/adyen CC|MES|ANO|CVV`")

# --- 5. ARRANQUE SEGURO ---
if __name__ == "__main__":
    # Iniciar servidor web en segundo plano
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("⏳ Esperando 10 segundos para estabilizar la nueva clave...")
    time.sleep(10)
    
    # Limpiamos cualquier rastro previo en Telegram
    bot.remove_webhook()
    
    print("🚀 Bot iniciado con éxito...")
    while True:
        try:
            # Intervalo de 3 segundos para evitar bloqueos por saturación
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"⚠️ Reintentando... {e}")
            time.sleep(5)
