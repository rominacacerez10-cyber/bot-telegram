# admin_dashboard.py - PANEL DE CONTROL MAESTRO (BOTONES)
from telebot import types

class AdminDashboard:
    @staticmethod
    def main_menu():
        """Genera el menú principal de administración."""
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [
            types.InlineKeyboardButton("🔑 Generar Key", callback_data="adm_gen_key"),
            types.InlineKeyboardButton("📊 Estadísticas", callback_data="adm_stats"),
            types.InlineKeyboardButton("📩 Ver Tickets", callback_data="adm_tickets"),
            types.InlineKeyboardButton("📢 Broadcast", callback_data="adm_broadcast"),
            types.InlineKeyboardButton("🛡️ Firewall Status", callback_data="adm_firewall"),
            types.InlineKeyboardButton("⚙️ Configuración", callback_data="adm_settings")
        ]
        markup.add(*btns)
        return markup

    @staticmethod
    def key_options():
        """Opciones para crear llaves VIP."""
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton("1 Día", callback_data="key_1d"),
            types.InlineKeyboardButton("7 Días", callback_data="key_7d"),
            types.InlineKeyboardButton("30 Días", callback_data="key_30d"),
            types.InlineKeyboardButton("⬅️ Volver", callback_data="adm_main")
        )
        return markup
