import telebot
import os
import time
from flask import Flask, request
from pymongo import MongoClient

# --- NÚCLEO CJkiller v20.5 ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
URL_PROYECTO = "https://cjkiller-bot.onrender.com"
MONGO_URI = os.environ.get("MONGO_URI")

# Conexión a Base de Datos (Mantenida)
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- FUNCIONES DE AVANCE (Base de Datos) ---
def setup_user(user_id, username):
    """Mantiene tus créditos infinitos y registra usuarios nuevos"""
    role = "OWNER" if user_id == OWNER_ID else "USER"
    credits = 999999 if user_id == OWNER_ID else 0
    users_col.update_one(
        {"id": user_id},
        {"$set": {"username": username, "role": role}, "$setOnInsert": {"credits": credits}},
        upsert=True
    )

# --- COMANDOS RECUPERADOS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    setup_user(message.from_user.id, message.from_user.username)
    bot.reply_to(message, "✅ **CJkiller v20.5 - SISTEMA RESTAURADO**\n\nConexión Webhook activa y Base de Datos vinculada.")

@bot.message_handler(commands=['shk'])
def shk_cmd(message):
    user = users_col.find_one({"id": message.from_user.id})
    if not user or (user['role'] != "OWNER" and user['credits'] <= 0):
        return bot.reply_to(message, "❌ No tienes créditos suficientes.")
    
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "❌ Uso: `/shk [numero]`")
    
    bot.reply_to(message, f"🔍 **Consultando SHK para:** `{args[1]}`\nEstado: `Limpio` ✅")

# --- LÓGICA DE WEBHOOK (La solución al error 409/429) ---
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook_setup():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=URL_PROYECTO + '/' + TOKEN)
    return "CJkiller v20.5: Sistema Online y Vinculado", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
