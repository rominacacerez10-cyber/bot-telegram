# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: bin_scrapper.py (RECOLECTOR DE DATOS)
# =================================================================

import re

class BinScrapper:
    @staticmethod
    def extract_bins(text):
        """Busca patrones de 6 dígitos que parezcan BINs en un texto."""
        # Busca secuencias de 6 dígitos que empiecen por 3, 4, 5 o 6
        bins_found = re.findall(r'\b([3456]\d{5})\b', text)
        # Elimina duplicados
        return list(set(bins_found))
