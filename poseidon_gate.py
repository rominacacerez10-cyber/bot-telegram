import requests
import random
import time

class PoseidonGate:
    """
    🔱 POSEIDON GATEWAY - AUTHORIZE.NET 🔱
    TYPE: CHARGE $0.01 (REAL AUTH)
    """
    @staticmethod
    def check_poseidon(cc, mm, yy, cvv):
        # Credenciales de tu Sandbox Authorize.Net
        api_login = "TU_API_LOGIN_ID"
        trans_key = "TU_TRANSACTION_KEY"
        
        # Endpoint de Producción/Sandbox
        url = "https://apitest.authorize.net/xml/v1/request.api"
        
        # Payload XML (Más robusto que JSON para AuthNet)
        payload = f"""
        <createTransactionRequest xmlns="AnetApi/xml/v1/schema/AnetApiSchema.xsd">
            <merchantAuthentication>
                <name>{api_login}</name>
                <transactionKey>{trans_key}</transactionKey>
            </merchantAuthentication>
            <transactionRequest>
                <transactionType>authCaptureTransaction</transactionType>
                <amount>0.01</amount>
                <payment>
                    <creditCard>
                        <cardNumber>{cc}</cardNumber>
                        <expirationDate>{yy}-{mm}</expirationDate>
                        <cardCode>{cvv}</cardCode>
                    </creditCard>
                </payment>
                <billTo>
                    <firstName>Test</firstName>
                    <lastName>User</lastName>
                    <address>123 Main St</address>
                    <city>New York</city>
                    <state>NY</state>
                    <zip>10001</zip>
                    <country>USA</country>
                </billTo>
            </transactionRequest>
        </createTransactionRequest>
        """
        
        try:
            # Headers para simular navegador real
            headers = {'Content-Type': 'text/xml'}
            r = requests.post(url, data=payload, headers=headers, timeout=20)
            
            # Limpiamos la respuesta (AuthNet devuelve texto con BOM a veces)
            response = r.text
            
            # --- ANÁLISIS DE RESULTADOS ---
            if "<responseCode>1</responseCode>" in response:
                # Code 1 = Approved
                return {"status": "LIVE ✅", "msg": "Transaction Approved", "charge": "$0.01"}
            elif "<responseCode>4</responseCode>" in response:
                # Code 4 = Held for Review (A veces es Live)
                text = response.split("<errorText>")[1].split("</errorText>")[0]
                return {"status": "LIVE 🟡 (Held)", "msg": text, "charge": "$0.00"}
            else:
                # Intentamos sacar el error exacto
                try:
                    error_text = response.split("<errorText>")[1].split("</errorText>")[0]
                except:
                    error_text = "Declined / Invalid Data"
                return {"status": "DEAD ❌", "msg": error_text.upper(), "charge": "$0.00"}

        except Exception as e:
            return {"status": "ERROR ⚠️", "msg": f"SYSTEM: {str(e)}", "charge": "N/A"}
