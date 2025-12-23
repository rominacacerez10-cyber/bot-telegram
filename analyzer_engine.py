# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: analyzer_engine.py (ANÁLISIS DE PENETRACIÓN)
# =================================================================

class BinAnalyzer:
    @staticmethod
    def get_score(data):
        """Calcula el puntaje de un BIN basado en su tipo y nivel."""
        score = 0
        advice = ""
        
        # Lógica de Puntaje
        b_type = data.get('t', '').upper()
        b_level = data.get('l', '').upper()
        
        if "CREDIT" in b_type: score += 50
        if "DEBIT" in b_type: score += 20
        
        if any(x in b_level for x in ["PLATINUM", "BUSINESS", "CORPORATE"]): score += 30
        if any(x in b_level for x in ["INFINITE", "WORLD", "SIGNATURE"]): score += 45
        if "PREPAID" in b_type: score -= 20
        
        # Generar Consejo
        if score >= 80: advice = "💎 NIVEL DIOS: ALTA PROBABILIDAD EN TODO."
        elif score >= 50: advice = "✅ NIVEL ALTO: IDEAL PARA SERVICIOS STREAMING."
        elif score >= 30: advice = "⚠️ NIVEL MEDIO: USAR CON PROXIES RESIDENCIALES."
        else: advice = "❌ NIVEL BAJO: PROBABLEMENTE SOLO PARA PRUEBAS."
        
        return {"SCORE": f"{score}/100", "ADVICE": advice}
