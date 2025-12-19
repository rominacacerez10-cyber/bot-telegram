import requests
import time
import urllib.parse
import urllib3

# Esto evita mensajes de advertencia al conectar con la API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "8106789282:AAF09T8dWH6fy0swDLpyXtbpwY3zJqQBDJw"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def enviar_mensaje(chat_id, texto):
    try:
        payload = {'chat_id': chat_id, 'text': texto, 'parse_mode': 'HTML'}
        # Aquí ya no usamos 'proxies=PROXIES' porque Render tiene conexión libre
        requests.get(URL + "sendMessage", params=payload, timeout=10)
    except:
        pass

def ejecutar_checker(cards):
    try:
        # Codificamos las tarjetas como en tu Sh.php original
        cards_encoded = urllib.parse.quote(cards)
        api_url = f"https://arturo.alwaysdata.net/MultiHilos/peticion2.php?cards={cards_encoded}"
        
        # Hacemos la petición directa. ¡En Render esto no dará Error 403!
        response = requests.get(api_url, verify=False, timeout=20)
        return response.text
    except Exception as e:
        return f"<b>⚠️ Error de conexión:</b>\n<code>{str(e)}</code>"

print("🚀 Bot iniciado en Render. Esperando mensajes...")

last_update_id = 0
while True:
    try:
        # Revisamos si hay mensajes nuevos en Telegram
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
                        
                        # Ejecutamos la lógica que antes hacía el archivo Sh.php
                        resultado = ejecutar_checker(cards)
                        enviar_mensaje(chat_id, resultado)
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
