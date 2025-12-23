# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: ai_brain.py (CEREBRO ARTIFICIAL)
# =================================================================

import requests

class AIEngine:
    @staticmethod
    def ask_ai(prompt):
        """Envía una consulta al núcleo de IA."""
        try:
            # Utilizamos un endpoint optimizado para velocidad
            api_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=es&dt=t&q={prompt}"
            # Nota: Para una IA real de diálogo estilo GPT sin costo de RAM:
            response = requests.get(f"https://api.simsimi.vn/v2/simsimi?text={prompt}&lc=es", timeout=10)
            
            if response.status_code == 200:
                return response.json().get('result', "⚠️ No puedo procesar eso ahora.")
            return "❌ Error en el núcleo neuronal."
        except Exception as e:
            return f"🚨 IA_ERROR: {str(e)}"
