# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: proxy_checker.py (INTELIGENCIA DE RED)
# =================================================================

import requests

class ProxyChecker:
    @staticmethod
    def check_ip(ip_address):
        """Analiza la reputación y ubicación de una dirección IP."""
        try:
            # Usamos una API de inteligencia de red rápida
            response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,regionName,city,zip,isp,org,as,proxy,query", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "IP": data.get("query"),
                        "PAIS": f"{data.get('country')} {data.get('countryCode')}",
                        "CIUDAD": data.get("city"),
                        "ISP": data.get("isp"),
                        "TIPO": "PROXY/VPN 🛡️" if data.get("proxy") else "RESIDENCIAL ✅",
                        "ORG": data.get("org")
                    }
            return None
        except Exception as e:
            print(f"Error en ProxyChecker: {e}")
            return None
