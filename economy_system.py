# economy_system.py - SISTEMA DE MONETIZACIÓN Y FIDELIZACIÓN
import random
import string
from datetime import datetime, timedelta

class Economy:
    @staticmethod
    def generate_key(prefix="CJK", length=12):
        """Genera una llave única de alta seguridad."""
        chars = string.ascii_uppercase + string.digits
        key = f"{prefix}-{''.join(random.choice(chars) for _ in range(length))}"
        return key

    @staticmethod
    def calculate_rank(hits):
        """Asigna rangos basados en el rendimiento del usuario."""
        if hits > 1000: return "🔥 LEYENDA OMNIPOTENT"
        if hits > 500: return "💎 ELITE"
        if hits > 100: return "🎖️ VETERANO"
        return "🔰 RECLUTA"

# Lógica masiva de recompensas por referidos aquí...
