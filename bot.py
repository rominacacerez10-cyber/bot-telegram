import os
import telebot
import base64
import json
import time
import threading
import io
from flask import Flask
from datetime import datetime

# --- 1. SERVIDOR ANTICIERRE (Para Render Free) ---
app = Flask(__name__)
@app.route('/')
def index(): return "CJKiller Hardcore Edition is Online"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CONFIGURACIÓN ---
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

# --- 4. COMANDOS CON ESTÉTICA PERSONALIZADA ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    texto = (
        "| Hardcore:() |\n"
        "━━━━━━━━━━━━━━\n"
        "🔥 **CJKILLER BOT v2.0**\n"
        "━━━━━━━━━━━━━━\n"
        "💎 **Comandos Disponibles:**\n"
        "• `/adyen CC|MES|ANO|CVV` - Encriptar una CC.\n"
        "• `/chk CC|MES|ANO|CVV` - Probar tarjeta (Gate).\n"
        "• **Envía un .txt** - Procesamiento Masivo.\n"
        "━━━━━━━━━━━━━━\n"
        "👑 **Owner:** @TuUsuario"
    )
    bot.reply_to(message, texto, parse_mode="Markdown")

@bot.message_handler(commands=['adyen'])
def cmd_adyen(message):
    try:
        data = message.text.split()[1]
        p = data.split('|')
        res = encrypt_adyen(p[0], p[1], p[2], p[3])
        
        # Estética de respuesta personalizada
        response = (
            "| Hardcore:() |\n"
            f"━━━━━━━━━━━━━━\n"
            f"🔹 **CC:** `{data}`\n"
            "━━━━━━━━━━━━━━\n"
            "💎 **RESULTADO:**\n"
            f"`{res['encrypted']}`\n"
            "━━━━━━━━━━━━━━\n"
            "✅ **Generado con éxito.**"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ **Error:** Formato incorrecto. Usa `/adyen CC|MES|ANO|CVV`")

# --- 5. PROCESAMIENTO MASIVO (.TXT) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith('.txt'):
        bot.reply_to(message, "⏳ **Hardcore Processing...** Espere un momento.")
        
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path).decode('utf-8')
        
        results = []
        for line in downloaded.splitlines()[:100]: # Límite aumentado a 100
            try:
                d = line.replace('|', ' ').split()
                if len(d) >= 4:
                    res = encrypt_adyen(d[0], d[1], d[2], d[3])
                    if res["success"]:
                        results.append(f"{line} -> {res['encrypted']}")
            except: continue
        
        output = io.BytesIO("\n".join(results).encode())
        output.name = "hashes_hardcore.txt"
        bot.send_document(
            message.chat.id, 
            output, 
            caption=f"| Hardcore:() |\n━━━━━━━━━━━━━━\n✅ **Procesadas:** {len(results)}\n━━━━━━━━━━━━━━"
        )

# --- 6. ARRANQUE SEGURO ---
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Pausa de seguridad para que Render limpie el proceso anterior
    time.sleep(10)
    bot.remove_webhook()
    
    print("🚀 CJKiller Hardcore Edition Iniciado...")
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            print(f"⚠️ Reintentando... {e}")
            time.sleep(5)
