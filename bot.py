import os
import telebot
import base64
import json
import time
import threading
from flask import Flask
from datetime import datetime

# --- SERVIDOR WEB ---
app = Flask(__name__)
@app.route('/')
def index(): return "Bot Live"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
bot = telebot.TeleBot(TOKEN, threaded=False)

def encrypt_adyen(card, month, year, cvv):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {"number": card, "cvc": cvv, "expiryMonth": month, "expiryYear": year, "generationtime": gen_time}
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "encrypted": f"adyenjs_0_1_25${encoded}"}
    except: return {"success": False}

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "✅ Online")

@bot.message_handler(commands=['adyen'])
def adyen(m):
    try:
        p = m.text.split()[1].split('|')
        res = encrypt_adyen(p[0], p[1], p[2], p[3])
        bot.reply_to(m, f"`{res['encrypted']}`", parse_mode="Markdown")
    except: bot.reply_to(m, "❌ Formato incorrecto")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    
    # EL SECRETO: Limpieza simple y espera larga para que Telegram cierre el conflicto
    print("⏳ Esperando 10 segundos para limpiar sesiones viejas...")
    bot.remove_webhook()
    time.sleep(10) 
    
    print("🚀 Iniciando...")
    while True:
        try:
            # interval=5 para no saturar y evitar el error 409
            bot.polling(none_stop=True, interval=5, timeout=20)
        except Exception as e:
            print(f"⚠️ Conflicto: {e}. Reintentando en 15s...")
            time.sleep(15)
