# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: binary_engine.py (MOTOR DE BAJO NIVEL)
# =================================================================

class BinaryEngine:
    @staticmethod
    def convert_all(value):
        """Convierte un número a todas las bases principales."""
        try:
            # Detectamos si es un número decimal o un string numérico
            num = int(value)
            return {
                "DECIMAL": str(num),
                "BINARIO": bin(num)[2:],
                "HEX": hex(num)[2:].upper(),
                "OCTAL": oct(num)[2:]
            }
        except ValueError:
            # Si es texto, convertimos cada carácter a su representación binaria
            binary_text = ' '.join(format(ord(x), 'b') for x in value)
            hex_text = ' '.join(format(ord(x), 'x') for x in value).upper()
            return {
                "TEXTO": value,
                "BINARIO": binary_text,
                "HEX": hex_text,
                "INFO": "Conversión de caracteres (ASCII)"
            }
