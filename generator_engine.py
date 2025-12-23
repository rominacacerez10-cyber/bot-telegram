import random
from validator_engine import Validator

class CCGen:
    @staticmethod
    def generate(bin_format, quantity=10):
        """Genera tarjetas válidas matemáticamente basadas en un BIN."""
        generated = []
        # Limpiamos el BIN de espacios o caracteres extraños
        prefix = str(bin_format).replace(" ", "").split("|")[0][:6]
        
        while len(generated) < quantity:
            # Creamos un número de 16 dígitos
            card = prefix
            while len(card) < 15:
                card += str(random.randint(0, 9))
            
            # Calculamos el dígito de control (Luhn)
            for i in range(10):
                if Validator.luhn_check(card + str(i)):
                    # Generamos fecha y CVV aleatorio para completar el formato
                    month = str(random.randint(1, 12)).zfill(2)
                    year = random.randint(2026, 2031)
                    cvv = str(random.randint(100, 999))
                    generated.append(f"{card}{i}|{month}|{year}|{cvv}")
                    break
                    
        return generated
