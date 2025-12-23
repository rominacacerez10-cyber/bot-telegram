# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: extrapolator_engine.py (EXTRAPOLACIÓN AVANZADA)
# =================================================================

import random
from validator_engine import Validator

class Extrapolator:
    @staticmethod
    def extrapolate(full_card, quantity=10):
        """Genera variaciones basadas en un número de tarjeta real."""
        # Limpiamos el número (nos quedamos con los primeros 12 o 13 dígitos)
        base = "".join(filter(str.isdigit, str(full_card)))[:12]
        generated = []
        
        if len(base) < 6: return None

        while len(generated) < quantity:
            # Creamos un número nuevo basado en la raíz de la original
            new_card = base
            while len(new_card) < 15:
                new_card += str(random.randint(0, 9))
            
            # Buscamos el dígito de control de Luhn
            for i in range(10):
                final_card = new_card + str(i)
                if Validator.luhn_check(final_card) and final_card != full_card:
                    generated.append(final_card)
                    break
                    
        return list(set(generated)) # Retorna sin duplicados
