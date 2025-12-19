import requests
import time
import urllib.parse
import urllib3
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Desactivar advertencias de certificados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "8106789282:AAF09T8dWH6fy0swDLpyXtbpwY3zJqQBDJw"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# --- LÓGICA DEL BOT ---

def enviar_mensaje(chat_id, texto):
    try:
        payload = {'chat_id': chat_id, 'text': texto, 'parse_mode': 'HTML'}
        requests.get(URL + "sendMessage", params=payload, timeout=10)
    except:
        pass

def ejecutar_checker(cards):
    try:
        cards_encoded = urllib.parse.quote(cards)
        api_url = f"https://arturo.alwaysdata.net/MultiHilos/peticion2.php?cards={cards_encoded}"
        # Render permite la conexión directa sin Error 403
        response = requests.get(api_url, verify=False, timeout=25)
        return response.text
    except Exception as e:
        return f"<b>⚠️ Error:</b>\n<code>{str(e)}</code>"

def iniciar_bot():
    print("🚀 Bot CJkiller iniciado en Render...")
    last_update_id = 0
    while True:
        try:
            res = requests.get(URL + f"getUpdates?offset={last_update_id + 1}", timeout=10).json()
            if res.get("ok") and res.get("result"):
                for update in res["result"]:
                    last_update_id = update["update_id"]
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        msg = update["message"]["text"]
                        if msg.startswith(("/chk", ".chk")):
                            cards = msg.replace("/chk ", "").replace(".chk ", "").strip()
                            enviar_mensaje(chat_id, "<b>⌛ Procesando tarjetas...</b>")
                            resultado = ejecutar_checker(cards)
                            enviar_mensaje(chat_id, resultado)
            time.sleep(1)
        except:
            time.sleep(5)

# --- SERVIDOR WEB PARA EL PLAN GRATUITO DE RENDER ---

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot esta vivo")

def ejecutar_servidor():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Iniciamos el bot en un hilo separado
    threading.Thread(target=iniciar_bot, daemon=True).start()
    # Iniciamos el servidor web que pide Render para el plan Free
    ejecutar_servidor()
