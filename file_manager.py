# =================================================================
# PROJECT: CJKILLER OMNIPOTENT
# MODULE: file_manager.py (GESTIÓN DE ARCHIVOS DEL NÚCLEO)
# =================================================================

import os

class SystemExplorer:
    @staticmethod
    def get_project_tree():
        """Escanea el directorio del proyecto y mide su volumen."""
        files_info = {}
        total_lines = 0
        
        # Listamos solo archivos .py para medir el bot
        for file in os.listdir('.'):
            if file.endswith('.py'):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = len(f.readlines())
                    size = os.path.getsize(file) / 1024 # KB
                    files_info[file] = f"{lines} LNS | {size:.1f} KB"
                    total_lines += lines
        
        return files_info, total_lines
