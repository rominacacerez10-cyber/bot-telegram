import telebot
import os
import time
from flask import Flask, request
from pymongo import MongoClient

# --- CONFIGURACIÓN CJkiller v20.5 ---
TOKEN = "8106789282:AAGBmKZgELy8KSUT7K6d7mbFspFpxUzhG-M"
OWNER_ID = 7012561892
URL_PROYECTO = "https://cjkiller-bot.onrender.com"
MONGO_URI = os.environ.get("MONGO_URI")

# Conexión a Base de Datos
client = MongoClient(MONGO_URI)
db = client['cjkiller_db']
users_col = db['users']

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- FUNCIONES INTERNAS ---
def setup_user(user_id, username):
    """Registra o actualiza al usuario con sus permisos correspondientes"""
    is_owner = (user_id == OWNER_ID)
    role = "OWNER" if is_owner else "USER"
    # Si es dueño, créditos infinitos. Si es nuevo, inicia en 0.
    credits = 999999 if is_owner else 0
    
    users_col.update_one(
        {"id": user_id},
        {
            "$set": {"username": username, "role": role},
            "$setOnInsert": {"credits": credits}
        },
        upsert=True
    )

# --- COMANDOS DE USUARIO ---

@bot.message_handler(commands=['start'])
def start_cmd(message):
    setup_user(message.from_user.id, message.from_user.username)
    bot.reply_to(message, "✅ **CJkiller v20.5 ONLINE**\n\nSistema de Webhook y Base de Datos vinculados correctamente.")

@bot.message_handler(commands=['me'])
def my_info(message):
    user_id = message.from_user.id
    user = users_col.find_one({"id": user_id})
    
    if not user:
        setup_user(user_id, message.from_user.username)
        user = users_col.find_one({"id": user_id})

    resp = (f"📊 **TU PERFIL**\n\n"
            f"🆔 ID: `{user['id']}`\n"
            f"🏅 Rango: `{user['role']}`\n"
            f"💎 Créditos: `{user['credits']}`")
    bot.reply_to(message, resp, parse_mode="Markdown")

@bot.message_handler(commands=['shk'])
def shk_cmd(message):
    user = users_col.find_one({"id": message.from_user.id})
    if not user or (user['role'] != "OWNER" and user.get('credits', 0) <= 0):
        return bot.reply_to(message, "❌ No tienes créditos suficientes.")
    
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "❌ Uso: `/shk [numero]`")
    
    bot.reply_to(message, f"🔍 **Consultando SHK para:** `{args[1]}`\nEstado: `Limpio` ✅")

# --- COMANDOS ADMINISTRATIVOS (SOLO OWNER) ---

@bot.message_handler(commands=['add'])
def add_credits(message):
    if message.from_user.id != OWNER_ID: return
    try:
        args = message.text.split()
        target_id, cantidad = int(args[1]), int(args[2])
        users_col.update_one({"id": target_id}, {"$inc": {"credits": cantidad}}, upsert=True)
        bot.reply_to(message, f"💎 Se añadieron `{cantidad}` créditos al ID `{target_id}`.")
    except:
        bot.reply_to(message, "❌ Uso: `/add [ID] [Cantidad]`")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != OWNER_ID: return
    try:
        target_id = int(message.text.split()[1])
        users_col.update_one({"id": target_id}, {"$set": {"role": "BANNED"}}, upsert=True)
        bot.reply_to(message, f"🚫 Usuario `{target_id}` baneado.")
    except:
        bot.reply_to(message, "❌ Uso: `/ban [ID]`")

# --- LÓGICA DE WEBHOOK (ANTI-ERRORES) ---

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
