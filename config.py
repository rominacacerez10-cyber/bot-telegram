# config.py - CONFIGURACIÓN CENTRAL DE SEGURIDAD v35.0
import os

# 1. CREDENCIALES DEL BOT (Obtenidas de @BotFather)
TOKEN = "8106789282:AAGnVn2lzYyYsi2iJhszWjt_nS47fxibAv4"

# 2. IDENTIDAD DEL ADMINISTRADOR (Tu ID de Telegram)
# Según tus instrucciones anteriores, tu ID es:
ADMIN_ID = 7447432617

# 3. CANALES DE LOGS Y AUDITORÍA
# Canal donde el bot enviará reportes de ataques y errores
LOG_CHANNEL = -1002319403816

# 4. CONFIGURACIÓN DE BASE DE DATOS (MongoDB)
# Reemplaza con tu cadena de conexión real
MONGO_URI = "mongodb+srv://admin:<sbI8ojgXZsKHEJKu>@cluster0.gprhwkr.mongodb.net/?appName=Cluster0"

# 5. PARÁMETROS DEL SISTEMA
VERSION = "35.0 OMNIPOTENT"
DB_NAME = "cjk_database"
MAX_THREADS = 5000  # Capacidad de procesamiento extremo

# 6. CONFIGURACIÓN DE SEGURIDAD (Firewall)
ANTI_SPAM_COOLDOWN = 1.5  # Segundos entre comandos
BAN_THRESHOLD = 5         # Intentos de ataque antes de ban permanente
