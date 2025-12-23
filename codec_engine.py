# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: codec_engine.py (TRADUCTOR UNIVERSAL DE DATOS)
# =================================================================

import base64
import urllib.parse

class CodecEngine:
    @staticmethod
    def encode_all(text):
        """Convierte texto plano a múltiples formatos de seguridad."""
        return {
            "BASE64": base64.b64encode(text.encode()).decode(),
            "HEX": text.encode().hex(),
            "URL": urllib.parse.quote(text)
        }

    @staticmethod
    def decode_auto(data):
        """Intenta descifrar qué formato es y devuelve el texto plano."""
        results = {}
        # Intento Base64
        try:
            results["FROM_B64"] = base64.b64decode(data).decode()
        except: pass
        
        # Intento Hex
        try:
            results["FROM_HEX"] = bytes.fromhex(data).decode()
        except: pass
        
        # Intento URL
        try:
            decoded_url = urllib.parse.unquote(data)
            if decoded_url != data:
                results["FROM_URL"] = decoded_url
        except: pass
            
        return results
