# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: gate_control.py (CONTROL DE ACCESO GLOBAL)
# =================================================================

class GateKeeper:
    # Estado inicial: Abierto (True)
    is_open = True
    maintenance_msg = "⚠️ <b>BOT EN MANTENIMIENTO CRÍTICO.</b>\n<i>El Admin ha cerrado el acceso temporalmente.</i>"

    @classmethod
    def toggle_gate(cls):
        """Cambia el estado del bot entre Abierto y Cerrado."""
        cls.is_open = not cls.is_open
        return cls.is_open

    @classmethod
    def check_gate(cls, user_id, admin_id):
        """Verifica si el usuario puede pasar por la puerta."""
        if user_id == admin_id:
            return True
        return cls.is_open
