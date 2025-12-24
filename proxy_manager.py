# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: proxy_manager.py
# =================================================================

import random

class ProxyManager:
    # Lista inicial vacía para que no de error
    PROXIES = []

    @staticmethod
    def get_proxy():
        """Devuelve None si no hay proxies, evitando que el bot muera."""
        if not ProxyManager.PROXIES:
            return None
        proxy = random.choice(ProxyManager.PROXIES)
        return {"http": proxy, "https": proxy}

    @staticmethod
    def add_proxies_from_text(text):
        """Añade proxies a la lista actual."""
        new_proxies = text.splitlines()
        ProxyManager.PROXIES.extend([p.strip() for p in new_proxies if p.strip()])
        return len(new_proxies)
