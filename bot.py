import os, telebot, base64, json, time, threading, io, random
from flask import Flask
from datetime import datetime
from pymongo import MongoClient
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ 1. CONFIGURACIÓN DE ÉLITE ] ---
TOKEN = "8106789282:AAFI6CEgWuL-nq5jpSf3vSD8pzIlwLvoBLQ"
ADMIN_ID = 7012561892 
LOG_CHANNEL = -1002434567890 
REQUIRED_CHANNEL = "@TuCanalOficial" 
MONGO_URI = "mongodb+srv://admin:S47qBJK9Sjghm11t@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

bot = telebot.TeleBot(TOKEN, threaded=False)
db = MongoClient(MONGO_URI)['cjkiller_db']
users_col = db['users']
last_msg_time = {}

# --- [ 2. SERVIDOR WEB ANTICIERRE ] ---
app = Flask(__name__)
@app.route('/')
def index(): return "CJKILLER SUPREME ENGINE: ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# --- [ 3. LÓGICA TÉCNICA (ADYEN & FAKE) ] ---
def encrypt_adyen(card, month, year, cvv):
    try:
        gen_time = datetime.utcnow().isoformat() + "Z" 
        payload = {"number": card, "cvc": cvv, "expiryMonth": month, "expiryYear": year, "generationtime": gen_time}
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        return {"success": True, "hash": f"adyenjs_0_1_25${encoded}"}
    except: return {"success": False}

def get_fake_data():
    names = ["John", "Robert", "Michael", "William", "David"]
    lasts = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    cities = ["New York, NY", "Los Angeles, CA", "Chicago, IL"]
    return {
        "name": f"{random.choice(names)} {random.choice(lasts)}",
        "email": f"{random.choice(names).lower()}{random.randint(100,999)}@gmail.com",
        "address": f"{random.randint(100, 9999)} {random.choice(['Main St', 'Park Ave'])}",
        "city": random.choice(cities),
        "zip": random.randint(10001, 99999)
    }

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(REQUIRED_CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True

# --- [ 4. MENÚS INTERACTIVOS ] ---
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💎 Adyen Hash", callback_data="adyen_req"),
        InlineKeyboardButton("🌍 Fake Data", callback_data="run_fake"),
        InlineKeyboardButton("👤 Perfil", callback_data="show_me"),
        InlineKeyboardButton("🔗 Referidos", callback_data="show_ref"),
        InlineKeyboardButton("📢 Canal Oficial", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@','')}")
    )
    return markup

# --- [ 5. MOTOR DE SEGURIDAD Y COMANDOS ] ---
@bot.message_handler(func=lambda m: True)
def handle_supreme(message):
    uid = message.from_user.id
    current_time = time.time()

    if not message.text: return

    # A. Marketing Automático
    if not is_subscribed(uid) and uid != ADMIN_ID:
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("📢 Unirse al Canal", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@','')}"))
        return bot.send_message(message.chat.id, "⚠️ **ACCESO RESTRINGIDO**\n\nDebes ser miembro de nuestro canal oficial para usar el bot.", reply_markup=markup)

    # B. Seguridad Anti-Spam
    if uid != ADMIN_ID:
        if uid in last_msg_time and current_time - last_msg_time[uid] < 5:
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            return
        last_msg_time[uid] = current_time

    # C. Procesador de Comandos
    text = message.text
    if text.startswith('/start'):
        user = users_col.find_one({"user_id": uid})
        if not user:
            args = text.split()
            ref_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
            user = {"user_id": uid, "credits": 15, "referrals": 0, "role": "Premium Member"}
            if ref_id and ref_id != uid:
                users_col.update_one({"user_id": ref_id}, {"$inc": {"credits": 5, "referrals": 1}})
                try: bot.send_message(ref_id, "🔥 **Bonus:** Alguien se unió con tu link. +5 Créditos.")
                except: pass
            users_col.insert_one(user)
        
        welcome_img = "https://i.imgur.com/rXyY4v3.jpeg" 
        bot.send_photo(message.chat.id, welcome_img, caption=(
            "╔═════════════════════╗\n"
            "      ⚔️ **CJKILLER SUPREME** ⚔️\n"
            "╚═════════════════════╝\n"
            f"👤 **Bienvenido:** @{message.from_user.username}\n"
            f"💰 **Balance:** {user.get('credits', 0)} créditos\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🚀 _El motor de élite está listo para operar._"
        ), reply_markup=main_menu(), parse_mode="Markdown")

    elif text.startswith('/adyen'):
        try:
            parts = text.split()
            if len(parts) < 2: return bot.reply_to(message, "❌ Use: `/adyen CC|MM|YY|CVV`")
            cc_data = parts[1]
            p = cc_data.split('|')
            res = encrypt_adyen(p[0], p[1], p[2], p[3])
            bot.reply_to(message, f"💎 **ADYEN HASH:**\n`{res['hash']}`", parse_mode="Markdown")
            bot.send_message(LOG_CHANNEL, f"🚩 **LOG:** @{message.from_user.username} -> `{cc_data}`")
        except: bot.reply_to(message, "❌ Formato incorrecto.")

    elif text.startswith('/fake'):
        f = get_fake_data()
        bot.reply_to(message, f"🌍 **DATOS:**\n👤 `{f['name']}`\n📧 `{f['email']}`\n📍 `{f['city']} {f['zip']}`", parse_mode="Markdown")

    elif text.startswith('/me'):
        u = users_col.find_one({"user_id": uid})
        bot.reply_to(message, f"| Hardcore:() |\n━━━━━━━━━━━━━\n🆔 **ID:** `{uid}`\n💰 **Créditos:** {u['credits']}\n👑 **Rango:** {'OWNER' if uid == ADMIN_ID else 'USER'}", parse_mode="Markdown")

    elif text.startswith('/addcredits') and uid == ADMIN_ID:
        try:
            _, tid, amt = text.split()
            users_col.update_one({"user_id": int(tid)}, {"$inc": {"credits": int(amt)}})
            bot.reply_to(message, f"✅ +{amt} créditos cargados a `{tid}`")
        except: pass

# --- [ 6. CALLBACKS ] ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "adyen_req":
        bot.send_message(call.message.chat.id, "💡 Envía: `/adyen CC|MM|YY|CVV`")
    elif call.data == "run_fake":
        f = get_fake_data()
        bot.send_message(call.message.chat.id, f"🌍 **FAKE:**\n👤 `{f['name']}`\n📧 `{f['email']}`\n📍 `{f['city']}`")
    elif call.data == "show_me":
        u = users_col.find_one({"user_id": call.from_user.id})
        bot.send_message(call.message.chat.id, f"👤 **Perfil:**\n💰 Créditos: {u['credits']}")
    elif call.data == "show_ref":
        link = f"https://t.me/{bot.get_me().username}?start={call.from_user.id}"
        bot.send_message(call.message.chat.id, f"🔗 **TU LINK:**\n`{link}`\n\nGana 5 créditos por invitado.")

# --- [ 7. ARRANQUE LIMPIO Y SEGURO ] ---
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.remove_webhook() # Evita el conflicto 409
    time.sleep(2) 
    print(f"🔥 CJKILLER SUPREME LIVE")
    bot.polling(none_stop=True, interval=1, timeout=20)
