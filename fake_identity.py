import random

class FakeID:
    @staticmethod
    def generate(country_code="US"):
        """Generador de Identidades Nivel Extremo"""
        try:
            # Diccionarios de datos para asegurar que siempre haya contenido
            nombres = ["James", "Robert", "John", "Michael", "David", "Mary", "Patricia", "Jennifer", "Linda"]
            apellidos = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
            ciudades = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia"]
            calles = ["Maple St", "Oak St", "Washington Blvd", "Lakeview Dr", "Park Ave"]

            # Construcción del objeto de datos
            data = {
                "NOMBRE": random.choice(nombres),
                "APELLIDO": random.choice(apellidos),
                "EDAD": str(random.randint(19, 75)),
                "GENERO": random.choice(["Masculino", "Femenino"]),
                "CIUDAD": random.choice(ciudades),
                "DIRECCION": f"{random.randint(100, 9999)} {random.choice(calles)}",
                "ZIP_CODE": str(random.randint(10000, 99999)),
                "S_SOCIAL": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
                "PHOTO_URL": "https://randomuser.me/api/portraits/men/1.jpg"
            }
            
            return data

        except Exception as e:
            # Si algo falla internamente, enviamos un log al terminal de Render
            print(f"Error interno en generador: {e}")
            return None
