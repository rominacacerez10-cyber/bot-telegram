# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: document_engine.py (GENERADOR VISUAL DE IDENTIDAD)
# =================================================================

from PIL import Image, ImageDraw, ImageFont
import io

class IDGenerator:
    @staticmethod
    def create_membership(name, country, city, user_id):
        # Creamos una imagen azul oscuro estilo "VIP Card"
        img = Image.new('RGB', (800, 450), color=(10, 20, 40))
        canvas = ImageDraw.Draw(img)
        
        # Dibujamos bordes dorados
        canvas.rectangle([20, 20, 780, 430], outline=(212, 175, 55), width=5)
        
        # Insertamos el texto
        # Nota: Si no tienes una fuente .ttf, usará la básica
        text_content = f"""
        OFFICIAL IDENTIFICATION
        -----------------------
        NAME: {name.upper()}
        REGION: {country.upper()}
        CITY: {city.upper()}
        ID: {user_id}
        STATUS: VERIFIED
        """
        
        canvas.text((60, 100), text_content, fill=(255, 255, 255))
        
        # Guardamos en memoria para enviar por Telegram
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr
