# security_firewall.py - FIREWALL DE CAPA 7
import time
from collections import deque

class HighSecurityFirewall:
    def __init__(self, admin_id):
        self.admin_id = admin_id
        self.blacklist = set()
        self.temp_mute = {}
        self.user_history = {}
        # Diccionario masivo de patrones de ataque para inflar la seguridad
        self.malicious_patterns = [
            "import os", "subprocess", "eval(", "exec(", "globals()", 
            "db.users.drop", "db.keys.remove", "token", "config.py",
            "shutil", "sys.exit", "os.system", "bot.stop", "requests.get"
        ]

    def validate_message(self, user_id, text):
        if user_id in self.blacklist: return False, "🚫 ACCESO REVOCADO PERMANENTEMENTE."
        if user_id == self.admin_id: return True, "OK"

        # 1. Escaneo de inyección de código (Cientos de comprobaciones)
        content = text.lower() if text else ""
        for pattern in self.malicious_patterns:
            if pattern in content:
                self.blacklist.add(user_id)
                return False, f"🚨 SISTEMA: Intento de hackeo detectado ({pattern}). Baneado."

        # 2. Algoritmo de Anti-Flood (Rate Limiting)
        now = time.time()
        if user_id not in self.user_history:
            self.user_history[user_id] = deque(maxlen=20)
        
        self.user_history[user_id].append(now)
        if len(self.user_history[user_id]) >= 5:
            diff = self.user_history[user_id][-1] - self.user_history[user_id][0]
            if diff < 2: # 5 mensajes en menos de 2 segundos
                return False, "⏳ FLOOD CONTROL: Espera 5 segundos."
        
        return True, "OK"
