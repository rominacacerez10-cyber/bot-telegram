# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: validator_engine.py (MATEMÁTICA PURA)
# =================================================================

class Validator:
    @staticmethod
    def luhn_check(card_number):
        """Verifica si un número de tarjeta es válido matemáticamente."""
        card_number = str(card_number).strip().replace(" ", "")
        if not card_number.isdigit():
            return False
            
        digits = [int(d) for d in card_number]
        # El algoritmo de Luhn: duplicar cada segundo dígito desde la derecha
        for i in range(len(digits) - 2, -1, -2):
            val = digits[i] * 2
            if val > 9:
                val -= 9
            digits[i] = val
            
        return sum(digits) % 10 == 0
