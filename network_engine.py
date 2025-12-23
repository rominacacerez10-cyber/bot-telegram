# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: network_engine.py (MONITOR DE INFRAESTRUCTURA)
# =================================================================

import socket
import requests
import time

class NetMonitor:
    @staticmethod
    def check_host(url):
        """Verifica si un sitio web responde y mide su tiempo de reacción."""
        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            latency = round((time.time() - start) * 1000, 2)
            return {
                "STATUS": "ONLINE ✅" if response.status_code == 200 else f"ERROR {response.status_code} ⚠️",
                "LATENCY": f"{latency}ms",
                "SERVER": response.headers.get("Server", "HIDDEN")
            }
        except:
            return {"STATUS": "OFFLINE ❌", "LATENCY": "N/A", "SERVER": "N/A"}

    @staticmethod
    def port_scan(host, port):
        """Escanea un puerto específico en un host."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            result = s.connect_ex((host, int(port)))
            s.close()
            return "OPEN 🔓" if result == 0 else "CLOSED 🔒"
        except:
            return "ERROR 🚫"
