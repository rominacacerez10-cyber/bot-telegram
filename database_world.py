import requests

# Tu lista local (puedes seguir agregando miles de líneas aquí)
BIN_DATA = {
    "415231": {"b": "BANAMEX", "c": "MEXICO 🇲🇽", "t": "VISA", "l": "PLATINUM"},
    # ... tus otros BINs
}

def lookup_bin(bin_val):
    key = str(bin_val)[:6]
    
    # 1. Intento de búsqueda local
    local_result = BIN_DATA.get(key)
    if local_result:
        return {
            "b": local_result['b'],
            "c": local_result['c'],
            "t": local_result['t'],
            "l": local_result['l'],
            "SOURCE": "LOCAL_DB 🏛️"
        }

    # 2. BÚSQUEDA GLOBAL (Si no está en la local)
    try:
        # Usamos una API gratuita para obtener datos reales al 1000%
        response = requests.get(f"https://lookup.binlist.net/{key}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "b": data.get("bank", {}).get("name", "UNKNOWN BANK").upper(),
                "c": f"{data.get('country', {}).get('name', 'UNKNOWN')} {data.get('country', {}).get('emoji', '')}".upper(),
                "t": f"{data.get('scheme', '???')} - {data.get('type', '???')}".upper(),
                "l": data.get("brand", "STANDARD").upper(),
                "SOURCE": "CLOUD_NETWORK 🛰️"
            }
    except:
        pass

    # 3. Respuesta si nada funciona
    return {
        "b": "NOT FOUND", "c": "UNKNOWN", "t": "UNKNOWN", "l": "STANDARD", "SOURCE": "NONE"
    }

class Database:
    @staticmethod
    def check_vip(user_id): return True
