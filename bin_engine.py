import requests

class BinLookup:
    @staticmethod
    def get_info(bin_number):
        """Consulta la información del banco y país del BIN."""
        try:
            # Usamos una API confiable para obtener datos del BIN
            response = requests.get(f"https://lookup.binlist.net/{bin_number}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "brand": data.get("scheme", "UNK").upper(),
                    "type": data.get("type", "UNK").upper(),
                    "level": data.get("brand", "UNK").upper(),
                    "bank": data.get("bank", {}).get("name", "UNK").upper(),
                    "country": data.get("country", {}).get("name", "UNK").upper(),
                    "flag": data.get("country", {}).get("emoji", "🌐")
                }
        except:
            pass
        # Retorno por defecto si la API falla o no encuentra el BIN
        return {"brand": "STRIPE", "type": "CREDIT", "level": "GOLD", "bank": "BCO CENTRAL", "country": "USA", "flag": "🇺🇸"}
