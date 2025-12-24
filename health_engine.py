# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: health_engine.py (MONITOR DE ESTADO)
# =================================================================

import requests

class GateHealth:
    @staticmethod
    def check_status(pk):
        """Verifica si la llave pública (PK) actual sigue activa."""
        try:
            # Intentamos una petición vacía a Stripe para ver si la PK es válida
            url = f"https://api.stripe.com/v1/tokens"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            # Mandamos un número de tarjeta inválido a propósito solo para ver la respuesta del server
            data = {'card[number]': '4242', 'key': pk}
            
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 401:
                return "DEAD ❌ (Invalid PK)"
            elif response.status_code == 400:
                # 400 es bueno aquí, significa que la PK es válida pero la tarjeta (4242) no.
                return "ALIVE ✅"
            else:
                return f"UNKNOWN ⚠️ ({response.status_code})"
        except:
            return "ERROR 🚫 (Connection Failed)"
