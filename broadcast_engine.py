# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: broadcast_engine.py (MANDO CENTRALIZADO)
# =================================================================

import time

class BroadcastManager:
    @staticmethod
    def send_global(bot, user_list, message_text):
        """Envía un mensaje a todos los usuarios registrados."""
        success = 0
        failed = 0
        
        for user_id in user_list:
            try:
                # Diseño de mensaje oficial del sistema
                header = "<b>📢 COMUNICADO OFICIAL OMNIPOTENTE</b>\n"
                header += "─" * 25 + "\n"
                bot.send_message(user_id, f"{header}{message_text}", parse_mode="HTML")
                success += 1
                time.sleep(0.05) # Pequeña pausa para evitar Flood
            except:
                failed += 1
                
        return success, failed
