# visual_engine.py - MOTOR VISUAL MULTI-TEMA
# Este módulo gestiona la interfaz "Cyber" de alta densidad.

class Visuals:
    # --- PALETAS DE ESTILO ---
    THEMES = {
        "OMNIPOTENT": {"top": "👑", "wall": "║", "cor": "╔", "sep": "═"},
        "MATRIX": {"top": "📟", "wall": "┃", "cor": "┏", "sep": "━"},
        "RED_ALERT": {"top": "🚨", "wall": "│", "cor": "┌", "sep": "─"}
    }
    
    CURRENT_THEME = "OMNIPOTENT"

    @classmethod
    def get_header(cls):
        t = cls.THEMES[cls.CURRENT_THEME]
        return (
            f"<b>{t['cor']}{t['sep']*26}{t['cor'].replace('╔','╗').replace('┏','┓').replace('┌','┐')}\n"
            f"{t['wall']}    {t['top']} CJKILLER OMNIPOTENT    {t['wall']}\n"
            f"{t['cor'].replace('╔','╚').replace('┏','┗').replace('┌','└')}{t['sep']*26}{t['cor'].replace('╔','╝').replace('┏','┛').replace('┌','┘')}</b>"
        )

    @classmethod
    def format_table(cls, title, data_dict):
        """Genera tablas ASCII de alta precisión."""
        t = cls.THEMES[cls.CURRENT_THEME]
        header = cls.get_header()
        table = f"{header}\n<code>{t['cor']}{t['sep']*26}{t['cor'].replace('╔','╗').replace('┏','┓').replace('┌','┐')}</code>\n"
        table += f"<code>{t['wall']} {title.center(24)} {t['wall']}</code>\n"
        table += f"<code>{t['cor'].replace('╔','╠').replace('┏','┣').replace('┌','├')}{t['sep']*26}{t['cor'].replace('╔','╣').replace('┏','┫').replace('┌','┤')}</code>\n"
        
        for key, val in data_dict.items():
            line = f"{key}: {val}"
            table += f"<code>{t['wall']} {line.ljust(24)} {t['wall']}</code>\n"
            
        table += f"<code>{t['cor'].replace('╔','╚').replace('┏','┗').replace('┌','└')}{t['sep']*26}{t['cor'].replace('╔','╝').replace('┏','┛').replace('┌','┘')}</code>"
        return table
