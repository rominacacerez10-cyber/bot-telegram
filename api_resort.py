# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: api_resort.py (MOTOR DE CONSULTA HÍBRIDO)
# =================================================================

import requests

class CloudLookup:
    @staticmethod
    def check_bin(bin_number):
        """Consulta profundidad de BIN en API de alta precisión."""
        try:
            # Usamos una API de respaldo confiable
            response = requests.get(f"https://lookup.binlist.net/{bin_number}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "b": data.get('bank', {}).get('name', 'N/A').upper(),
                    "c": data.get('country', {}).get('name', 'N/A').upper(),
                    "t": data.get('type', 'N/A').upper(),
                    "l": data.get('level', 'N/A').upper() or data.get('brand', 'N/A').upper()
                }
        except:
            return None
        return None

    @staticmethod
    def check_ip(ip_address):
        """Rastreo de IP para detectar Proxy/VPN y geolocalización."""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,isp,proxy", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return {
                        "PAIS": data['country'].upper(),
                        "CIUDAD": data['city'].upper(),
                        "ISP": data['isp'].upper(),
                        "PROXY/VPN": "SÍ 🚨" if data.get('proxy') else "NO ✅"
                    }
        except:
            return None
        return None
