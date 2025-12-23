# server_monitor.py - VIGILANCIA DE RECURSOS
import psutil
import os

class Monitor:
    @staticmethod
    def get_stats():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"💻 CPU: {cpu}% | 🧠 RAM: {ram}%"

    @staticmethod
    def auto_clean():
        """Limpia logs antiguos para liberar espacio."""
        if os.path.exists("error.log"):
            os.remove("error.log")
