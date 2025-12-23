# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: scrapper_engine.py (EXTRACTOR DE DATOS)
# =================================================================

import re

class Scrapper:
    @staticmethod
    def extract_data(text):
        """Extrae BINs y tarjetas en formato CC|MM|YY|CVV del texto."""
        # Busca patrones de 15-16 dígitos seguidos de separadores y fechas
        cc_pattern = r'\b(?:\d[ -]*?){13,16}(?:[|/ -])\d{2}(?:[|/ -])(?:\d{2,4})(?:[|/ -])\d{3,4}\b'
        bin_pattern = r'\b\d{6}\b'
        
        cards = re.findall(cc_pattern, text)
        bins = re.findall(bin_pattern, text)
        
        # Limpiamos los resultados
        clean_cards = [c.replace(' ', '').replace('/', '|') for c in cards]
        clean_bins = list(set(bins)) # Sin duplicados
        
        return {
            "CARDS": clean_cards,
            "BINS": clean_bins,
            "TOTAL_C": len(clean_cards),
            "TOTAL_B": len(clean_bins)
        }
