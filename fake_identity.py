# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: fake_identity.py (GENERADOR DE IDENTIDADES)
# =================================================================

import requests

class FakeID:
    @staticmethod
    def generate(country_code="US"):
        """Genera una identidad falsa completa con imagen y datos."""
        try:
            # Puedes cambiar 'randomuser.me' por otra API si lo deseas.
            # 'nat' (nationality) asegura que la identidad sea de un país específico.
            response = requests.get(f"https://randomuser.me/api/?nat={country_code}&inc=name,location,email,login,phone,picture&noinfo", timeout=5)
            if response.status_code == 200:
                data = response.json()['results'][0]
                
                # Formato de nombre
                name = f"{data['name']['first']} {data['name']['last']}".upper()
                
                # Dirección completa
                location = data['location']
                address = f"{location['street']['name']} {location['street']['number']}, {location['city']}, {location['state']}, {location['postcode']}".upper()
                
                # Datos de cuenta
                username = data['login']['username']
                password = data['login']['password'] # ¡Precaución al usar contraseñas generadas!
                
                return {
                    "FULL NAME": name,
                    "ADDRESS": address,
                    "EMAIL": data['email'].upper(),
                    "PHONE": data['phone'],
                    "USERNAME": username,
                    "PASSWORD": password,
                    "PHOTO_URL": data['picture']['large']
                }
        except Exception as e:
            print(f"Error generando identidad: {e}")
            return None
        return None
