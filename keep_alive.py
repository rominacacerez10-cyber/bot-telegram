# keep_alive.py - SISTEMA ANTI-SUSPENSIÓN
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "⚡ OMNIPOTENT v35.0: SISTEMA ACTIVO Y OPERATIVO"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Inicia un hilo separado para el servidor web."""
    t = Thread(target=run)
    t.start()
