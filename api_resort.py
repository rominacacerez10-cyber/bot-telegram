# api_resort.py - CONSULTA HÍBRIDA DE EMERGENCIA
import requests

class CloudLookup:
    @staticmethod
    def check_online(bin_num):
        """Consulta una API de respaldo si el BIN no está en la DB local."""
        try:
            # Usamos un servicio gratuito de alta velocidad como respaldo
            response = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return {
                    "b": data.get("bank", {}).get("name", "N/A").upper(),
                    "c": data.get("country", {}).get("name", "INTL").upper(),
                    "t": data.get("scheme", "N/A").upper(),
                    "l": data.get("type", "N/A").upper()
                }
        except:
            return None
        return None
