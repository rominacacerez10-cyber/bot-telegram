# =================================================================
# PROJECT: CJKILLER OMNIPOTENT ARCHITECT v35.0
# TOTAL INFRASTRUCTURE: +5000 DISTRIBUTED LINES
# STATUS: EXTREME POWER ACTIVE
# =================================================================

import telebot
import telebot
import time
from config import TOKEN, ADMIN_ID
from visual_engine import Visuals
from database_world import Database
from gate_control import GateKeeper  # <-- Esta es la pieza que te falta
from security_firewall import firewall
from datetime import datetime
from fake_identity import FakeID
from generator_engine import CCGen
from proxy_checker import ProxyChecker
from scrapper_engine import Scrapper
bot = telebot.TeleBot(TOKEN)

# --- CAPA DE SEGURIDAD (EL ESCUDO) ---
def check_access(message):
    # Revisa baneos y spam
    allowed, reason = firewall.validate_message(message.from_user.id, message.text)
    if not allowed:
        bot.reply_to(message, reason)
        return False
    
    # Revisa si el bot está en mantenimiento
    if not GateKeeper.check_gate(message.from_user.id, ADMIN_ID):
        bot.reply_to(message, GateKeeper.maintenance_msg, parse_mode="HTML")
        return False
        
    return True

# --- IMPORTACIÓN DE MÓDULOS DE ÉLITE ---
from config import TOKEN, ADMIN_ID, LOG_CHANNEL
from visual_engine import Visuals
from security_firewall import firewall
from database_world import lookup_bin
from api_resort import CloudLookup
from economy_system import Economy
from server_monitor import Monitor
from keep_alive import keep_alive
from fake_identity import FakeID
from api_resort import CloudLookup
from ai_brain import AIEngine
from file_manager import SystemExplorer
from bin_scrapper import BinScrapper

# [DEF 1] INICIALIZACIÓN DE POTENCIA (5000 THREADS)
# Esto permite que el bot procese ataques y consultas masivas sin lag.
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=5000)

# -----------------------------------------------------------------
# [MIDDLEWARE] FIREWALL DE CAPA 7
# -----------------------------------------------------------------
def check_access(message):
    uid = message.from_user.id
    is_safe, reason = firewall.validate_message(uid, message.text or "")
    if not is_safe:
        bot.reply_to(message, f"<b>🛡️ FIREWALL: {reason}</b>", parse_mode="HTML")
        return False
    return True

# -----------------------------------------------------------------
# [ADMIN] /SCRAP - RECOLECTOR DE DATOS MASIVO
# -----------------------------------------------------------------
@bot.message_handler(commands=['scrap'])
def handle_scrap(message):
    if message.from_user.id != ADMIN_ID: return # Solo tú puedes usarlo
    
    try:
        # El bot analiza el mensaje al que estás respondiendo
        if not message.reply_to_message or not message.reply_to_message.text:
            return bot.reply_to(message, "⚠️ <b>ERROR:</b> Responde a un mensaje que contenga datos.", parse_mode="HTML")

        msg_wait = bot.reply_to(message, "📡 <code>EXTRAYENDO INTELIGENCIA...</code>", parse_mode="HTML")
        
        # Ejecutamos el scrapper
        data = Scrapper.extract_data(message.reply_to_message.text)
        
        if data['TOTAL_C'] == 0 and data['TOTAL_B'] == 0:
            return bot.edit_message_text("❌ No se encontró información útil.", message.chat.id, msg_wait.message_id)

        # Preparamos el reporte
        report = f"<b>📡 REPORTE DE EXTRACCIÓN</b>\n"
        report += f"<b>Tarjetas:</b> {data['TOTAL_C']}\n"
        report += f"<b>BINs Detectados:</b> {data['TOTAL_B']}\n"
        report += "─" * 20 + "\n"
        
        if data['CARDS']:
            report += "<b>LISTA DE CC:</b>\n"
            # Mostramos las primeras 10 para no saturar
            report += "\n".join([f"<code>{c}</code>" for c in data['CARDS'][:10]])
            if data['TOTAL_C'] > 10: report += f"\n<i>...y {data['TOTAL_C']-10} más.</i>"
        
        bot.edit_message_text(report, message.chat.id, msg_wait.message_id, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"🚨 <b>DEBUG:</b> <code>{str(e)}</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [COMMAND] /PROXY - ANALIZADOR DE SEGURIDAD DE RED
# -----------------------------------------------------------------
@bot.message_handler(commands=['proxy', 'ip'])
def handle_proxy(message):
    if not check_access(message): return
    
    try:
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ <b>USO:</b> <code>/proxy [DIRECCION_IP]</code>", parse_mode="HTML")

        target_ip = args[1]
        msg_wait = bot.reply_to(message, "📡 <code>RASTREANDO PAQUETES...</code>", parse_mode="HTML")
        
        # Ejecutamos el escaneo
        result = ProxyChecker.check_ip(target_ip)

        if result:
            output = Visuals.format_table(f"IP SCAN: {target_ip}", result)
            bot.edit_message_text(output, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        else:
            bot.edit_message_text("❌ Error: No se pudo obtener información de esa IP.", message.chat.id, msg_wait.message_id)

    except Exception as e:
        bot.reply_to(message, f"🚨 <b>DEBUG:</b> <code>{str(e)}</code>", parse_mode="HTML")

from extrapolator_engine import Extrapolator

# -----------------------------------------------------------------
# [VIP] /EXTRA - EXTRAPOLADOR DE ALTA PRECISIÓN
# -----------------------------------------------------------------
@bot.message_handler(commands=['extra', 'ex'])
def handle_extra(message):
    if not check_access(message): return
    
    try:
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ <b>USO:</b> <code>/extra [CARD_COMPLETA]</code>", parse_mode="HTML")

        full_card = args[1].split('|')[0] # Toma solo el número si viene con fecha
        msg_wait = bot.reply_to(message, "🧬 <code>EXTRAPOLANDO ADN BANCARIO...</code>", parse_mode="HTML")
        
        # 1. Obtenemos info del BIN
        info = lookup_bin(full_card[:6])
        
        # 2. Generamos las variaciones
        variations = Extrapolator.extrapolate(full_card, 15)

        if variations:
            # Reutilizamos la fecha y CVV de la original si el usuario los puso
            # o generamos unos nuevos pro.
            parts = args[1].split('|')
            date_cvv = f"|{parts[1]}|{parts[2]}|{parts[3]}" if len(parts) > 3 else "|01|2028|000"
            
            response = f"<b>🧬 EXTRAPOLACIÓN EXITOSA</b>\n"
            response += f"<b>BASE:</b> <code>{full_card[:6]}xxxxxx{full_card[-4:]}</code>\n"
            response += f"<b>BANK:</b> {info['b']} | {info['c']}\n"
            response += "─" * 20 + "\n"
            response += "\n".join([f"<code>{v}{date_cvv}</code>" for v in variations])
            
            bot.edit_message_text(response, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        else:
            bot.edit_message_text("❌ Error al procesar la tarjeta.", message.chat.id, msg_wait.message_id)

    except Exception as e:
        bot.reply_to(message, f"🚨 <b>DEBUG:</b> <code>{str(e)}</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [ADMIN] /SCRAP - EXTRACTOR DE BINS EN MASA
# -----------------------------------------------------------------
@bot.message_handler(commands=['scrap'])
def scrap_bins_command(message):
    if message.from_user.id != ADMIN_ID: return
    
    try:
        # Si el comando tiene texto después o es un reenviado
        target_text = ""
        if message.reply_to_message:
            target_text = message.reply_to_message.text
        else:
            target_text = message.text.split(None, 1)[1]
            
        msg_wait = bot.reply_to(message, "📡 <code>ESCANEANDO TEXTO...</code>", parse_mode="HTML")
        
        # Extracción
        found_bins = BinScrapper.extract_bins(target_text)
        
        if not found_bins:
            return bot.edit_message_text("❌ No se encontraron BINs válidos.", message.chat.id, msg_wait.message_id)
            
        # Validamos el primero de la lista como ejemplo de lo que encontró
        example_bin = found_bins[0]
        info = lookup_bin(example_bin)
        
        results = {
            "BINS_DETECTADOS": len(found_bins),
            "LISTA_PREVIA": f"{', '.join(found_bins[:5])}...",
            "ULTIMO_ANALISIS": example_bin,
            "BANCO_EJEMPLO": info['b'],
            "ESTADO": "LISTOS PARA DB ✅"
        }
        
        output = Visuals.format_table("BIN SCRAPPER V1", results)
        bot.edit_message_text(output, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        
    except Exception:
        bot.reply_to(message, "⚠️ <code>USO: Responde a un mensaje con /scrap o usa /scrap [texto]</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [VIP] /CHECK - VALIDACIÓN EXTREMA DE TARJETAS
# -----------------------------------------------------------------
@bot.message_handler(commands=['check', 'chk'])
def check_card_command(message):
    if not check_access(message): return
    
    try:
        full_card = message.text.split()[1]
        bin_val = full_card[:6]
        
        msg_wait = bot.reply_to(message, "🔍 <code>ANALIZANDO ESTRUCTURA...</code>", parse_mode="HTML")
        
        # 1. Validación Matemática
        is_valid = Validator.luhn_check(full_card)
        luhn_status = "VÁLIDA ✅" if is_valid else "INVÁLIDA ❌"
        
        # 2. Búsqueda de Info (Usando tu database_world mejorada)
        info = lookup_bin(bin_val)
        
        results = {
            "CARD": f"{full_card[:6]}xxxxxx{full_card[-4:]}",
            "LUHN": luhn_status,
            "BANK": info['b'],
            "COUNTRY": info['c'],
            "LEVEL": info['l'],
            "SOURCE": info['SOURCE']
        }
        
        output = Visuals.format_table("CC VALIDATOR", results)
        bot.edit_message_text(output, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        
    except IndexError:
        bot.reply_to(message, "⚠️ <code>USO: /check [NUMERO_TARJETA]</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"🚨 <b>ERROR:</b> <code>{str(e)}</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [ADMIN] /GATE - CIERRE PERIMETRAL DE EMERGENCIA
# -----------------------------------------------------------------
@bot.message_handler(commands=['gate', 'lock'])
def toggle_gate_command(message):
    if message.from_user.id != ADMIN_ID: return
    
    status = GateKeeper.toggle_gate()
    state_text = "ABIERTO ✅" if status else "CERRADO 🔒"
    
    gate_data = {
        "SISTEMA": "GATE_KEEPER v2",
        "ESTADO_ACTUAL": state_text,
        "ACCESO_ADMIN": "INMUNE 👑",
        "NOTIFICACIÓN": "ENVIADA A USUARIOS"
    }
    
    output = Visuals.format_table("CONTROL DE ACCESO", gate_data)
    bot.send_message(message.chat.id, output, parse_mode="HTML")

# -----------------------------------------------------------------
# [ADMIN] /FILES - EXPLORADOR DE CÓDIGO FUENTE
# -----------------------------------------------------------------
@bot.message_handler(commands=['files', 'root'])
def list_files_command(message):
    if message.from_user.id != ADMIN_ID: return
    
    files_data, total_lns = SystemExplorer.get_project_tree()
    
    # Añadimos el conteo total a los datos para la tabla
    files_data[">>> TOTAL LINES"] = f"{total_lns} LNS 👑"
    
    output = Visuals.format_table("PROJECT ARCHITECTURE", files_data)
    bot.send_message(message.chat.id, output, parse_mode="HTML")

# -----------------------------------------------------------------
# [VIP/ADMIN] /IA - CONSULTA AL NÚCLEO NEURONAL
# -----------------------------------------------------------------
@bot.message_handler(commands=['ia', 'ask'])
def ai_command(message):
    if not check_access(message): return
    
    # Verificación de rango (IA es solo para VIP o Admin)
    is_vip = Database.check_vip(message.from_user.id)
    if not is_vip and message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "⭐ <b>EL ACCESO A LA IA ES EXCLUSIVO PARA USUARIOS VIP.</b>", parse_mode="HTML")
    
    try:
        user_query = message.text.split(None, 1)[1]
        msg_wait = bot.reply_to(message, "🧠 <code>PENSANDO...</code>", parse_mode="HTML")
        
        # Llamada al cerebro
        ai_response = AIEngine.ask_ai(user_query)
        
        # Formato visual imponente
        response_data = {
            "PREGUNTA": user_query[:30] + "...",
            "IA_RESPONSE": ai_response,
            "ENGINE": "NEURAL_V2"
        }
        
        output = Visuals.format_table("AI INTELLIGENCE", response_data)
        bot.edit_message_text(output, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        
    except IndexError:
        bot.reply_to(message, "⚠️ <code>USO: /ia [TU PREGUNTA]</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [ADMIN] /BROADCAST - DIFUSIÓN GLOBAL OMNIPOTENTE
# -----------------------------------------------------------------
@bot.message_handler(commands=['broadcast', 'bc'])
def broadcast_command(message):
    # Verificación de rango supremo
    if message.from_user.id != ADMIN_ID: return
    
    try:
        # Extraer el mensaje (todo lo que va después de /bc)
        broadcast_msg = message.text.split(None, 1)[1]
        
        # Obtener todos los IDs de la base de datos que ya tenemos
        all_users = users_col.find({}, {"_id": 1})
        
        count_success = 0
        count_error = 0
        
        bot.send_message(message.chat.id, "🚀 <b>INICIANDO DIFUSIÓN GLOBAL...</b>", parse_mode="HTML")
        
        for user in all_users:
            try:
                # Formatear el mensaje con la estética del bot
                final_text = (
                    f"{Visuals.get_header()}\n\n"
                    f"📢 <b>COMUNICADO OFICIAL:</b>\n\n"
                    f"<code>{broadcast_msg}</code>\n\n"
                    f"<i>Atentamente: Admin Supremo</i>"
                )
                bot.send_message(user['_id'], final_text, parse_mode="HTML")
                count_success += 1
                time.sleep(0.1) # Evitar baneo de Telegram por spam rápido
            except:
                count_error += 1
                continue
        
        # Reporte final para el Admin
        report = {
            "ENVIADOS": count_success,
            "FALLIDOS": count_error,
            "TOTAL": count_success + count_error,
            "ESTADO": "COMPLETADO ✅"
        }
        
        output = Visuals.format_table("BROADCAST REPORT", report)
        bot.send_message(message.chat.id, output, parse_mode="HTML")
        
    except IndexError:
        bot.reply_to(message, "⚠️ <code>USO: /bc [MENSAJE]</code>", parse_mode="HTML")
    
# -----------------------------------------------------------------
# [ADMIN] /STATUS - MONITOR DE SALUD DEL NÚCLEO
# -----------------------------------------------------------------
@bot.message_handler(commands=['status', 'health'])
def status_command(message):
    if message.from_user.id != ADMIN_ID: return
    
    stats = Monitor.get_stats()
    output = Visuals.format_table("SERVER HEALTH", stats)
    
    bot.send_message(message.chat.id, output, parse_mode="HTML")

# -----------------------------------------------------------------
# [USER] /BAL - CONSULTA DE CRÉDITOS
# -----------------------------------------------------------------
@bot.message_handler(commands=['bal', 'money'])
def balance_command(message):
    if not check_access(message): return
    
    balance = Economy.get_balance(message.from_user.id)
    
    bal_data = {
        "USUARIO": f"@{message.from_user.username}",
        "CRÉDITOS": f"{balance} CC",
        "MÉTODO": "OFFICIAL_WALLET",
        "ESTADO": "ACTUALIZADO ✅"
    }
    
    output = Visuals.format_table("MI BILLETERA", bal_data)
    bot.send_message(message.chat.id, output, parse_mode="HTML")

# -----------------------------------------------------------------
# [ADMIN] /ADD - CARGA DE SALDO MANUAL
# -----------------------------------------------------------------
@bot.message_handler(commands=['add'])
def add_credits_command(message):
    if message.from_user.id != ADMIN_ID: return
    
    try:
        # Uso: /add [ID_USUARIO] [CANTIDAD]
        args = message.text.split()
        target_id = int(args[1])
        amount = int(args[2])
        
        Economy.add_credits(target_id, amount)
        
        bot.reply_to(message, f"💰 <b>TRANSACCIÓN EXITOSA:</b> Se han añadido {amount} créditos al ID <code>{target_id}</code>.", parse_mode="HTML")
    except:
        bot.reply_to(message, "⚠️ <code>USO: /add [USER_ID] [CANTIDAD]</code>", parse_mode="HTML")
# -----------------------------------------------------------------
# [TOOL] /IP - RASTREO Y SEGURIDAD DE CONEXIÓN
# -----------------------------------------------------------------
@bot.message_handler(commands=['ip'])
def track_ip_command(message):
    if not check_access(message): return
    
    try:
        ip_addr = message.text.split()[1]
        bot.send_message(message.chat.id, "🛰️ <code>RASTREANDO DIRECCIÓN...</code>", parse_mode="HTML")
        
        intel = CloudLookup.check_ip(ip_addr)
        
        if intel:
            output = Visuals.format_table(f"IP INTEL: {ip_addr}", intel)
            bot.send_message(message.chat.id, output, parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ <b>IP NO VÁLIDA O FUERA DE RANGO.</b>", parse_mode="HTML")
            
    except:
        bot.reply_to(message, "⚠️ <code>USO: /ip [DIRECCIÓN-IP]</code>", parse_mode="HTML")

# -----------------------------------------------------------------
# [ADMIN] /UNBAN - RESTAURACIÓN DE ACCESO TOTAL
# -----------------------------------------------------------------
@bot.message_handler(commands=['unban'])
def unban_user(message):
    # Verificación de seguridad de alta jerarquía
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ <b>ERROR: ACCESO DENEGADO.</b>", parse_mode="HTML")
    
    try:
        # Extraer el ID del usuario a desbloquear
        target_id = int(message.text.split()[1])
        
        # 1. Eliminar de la Blacklist permanente
        if target_id in firewall.blacklist:
            firewall.blacklist.remove(target_id)
        
        # 2. Limpiar historial de Flood para evitar bloqueos inmediatos
        if target_id in firewall.user_history:
            firewall.user_history[target_id].clear()
            
        # 3. Respuesta visual con el motor de Visuals
        unban_info = {
            "USUARIO ID": target_id,
            "ESTADO": "RESTABLECIDO ✅",
            "FIREWALL": "BYPASSED",
            "MOTIVO": "ADMIN_FORCE"
        }
        
        output = Visuals.format_table("PERDÓN CONCEDIDO", unban_info)
        bot.send_message(message.chat.id, output, parse_mode="HTML")
        
    except (IndexError, ValueError):
        bot.reply_to(message, "⚠️ <code>USO: /unban [USER_ID]</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>ERROR DE NÚCLEO:</b> <code>{e}</code>", parse_mode="HTML")    


def check_access(message):
    # Primero chequea el Firewall de Capa 7 que ya tenemos
    allowed, reason = firewall.validate_message(message.from_user.id, message.text)
    if not allowed:
        bot.reply_to(message, reason)
        return False
    
    # Luego chequea si la puerta global está abierta (Tú siempre pasas)
    if not GateKeeper.check_gate(message.from_user.id, ADMIN_ID):
        bot.reply_to(message, GateKeeper.maintenance_msg, parse_mode="HTML")
        return False
        
    return True

# -----------------------------------------------------------------
# [COMMAND] /START - INTERFAZ CYBER DE BIENVENIDA
# -----------------------------------------------------------------
@bot.message_handler(commands=['start'])
def welcome_command(message):
    if not check_access(message): return
    
    # Renderizado de Tabla de Usuario
    user_data = {
        "USER": f"@{message.from_user.username}",
        "ID": message.from_user.id,
        "RANK": "ADMIN" if message.from_user.id == ADMIN_ID else "USER",
        "STATUS": "ACTIVE ✅"
    }
    
    output = Visuals.format_table("ACCESS GRANTED", user_data)
    bot.send_message(message.chat.id, output, parse_mode="HTML")

# -----------------------------------------------------------------
# [COMMAND] /PRECISION - MOTOR HÍBRIDO DE BINS
# -----------------------------------------------------------------
@bot.message_handler(commands=['gen', 'g'])
def handle_gen(message):
    if not check_access(message): return # Tu aduana de seguridad
    
    try:
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "⚠️ <b>USO:</b> <code>/gen [BIN] [CANTIDAD]</code>", parse_mode="HTML")

        bin_input = args[1]
        cantidad = int(args[2]) if len(args) > 2 else 10
        if cantidad > 40: cantidad = 40 # Límite para evitar spam

        msg_wait = bot.reply_to(message, "⚙️ <code>FORJANDO ESTRUCTURAS...</code>", parse_mode="HTML")
        
        # Obtenemos info del BIN para que el mensaje se vea pro
        info = lookup_bin(bin_input[:6])
        
        # Llamamos a nuestro nuevo generador
        lista_cards = CCGen.generate(bin_input, cantidad)

        if lista_cards:
            # Formateamos la respuesta final
            response = f"<b>🔥 GENERACIÓN COMPLETADA</b>\n"
            response += f"<b>BIN:</b> <code>{bin_input[:6]}</code> | {info['b']}\n"
            response += f"<b>PAÍS:</b> {info['c']}\n"
            response += "─" * 20 + "\n"
            response += "\n".join([f"<code>{cc}</code>" for cc in lista_cards])
            
            bot.edit_message_text(response, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        else:
            bot.edit_message_text("❌ Error al procesar el BIN.", message.chat.id, msg_wait.message_id)

    except Exception as e:
        bot.reply_to(message, f"🚨 <b>DEBUG:</b> <code>{str(e)}</code>", parse_mode="HTML")

# [COMMAND] /FAKE - GENERADOR AVANZADO
@bot.message_handler(commands=['fake'])
def fake_identity_command(message):
    if not check_access(message): return

    try:
        args = message.text.split()
        country_code = args[1].upper() if len(args) > 1 else "US"
        
        msg_wait = bot.send_message(message.chat.id, "🛰️ <code>GENERANDO IDENTIDAD...</code>", parse_mode="HTML")

        fake_data = FakeID.generate(country_code)

        if fake_data:
            # Sacamos la foto para que no estorbe en la tabla
            photo_url = fake_data.pop("PHOTO_URL", None)
            output = Visuals.format_table(f"FIDE ID: {country_code}", fake_data)

            try:
                # Intenta enviar la foto
                bot.send_photo(message.chat.id, photo_url, caption=output, parse_mode="HTML")
                bot.delete_message(message.chat.id, msg_wait.message_id)
            except:
                # SI LA FOTO FALLA (Error 400), envía solo el texto
                bot.edit_message_text(output, message.chat.id, msg_wait.message_id, parse_mode="HTML")
        else:
            bot.edit_message_text("❌ <b>ERROR:</b> Datos vacíos.", message.chat.id, msg_wait.message_id, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"🚨 <b>DEBUG:</b> <code>{str(e)}</code>", parse_mode="HTML")
# -----------------------------------------------------------------
# [ADMIN] /PANEL - CONTROL TOTAL DE INFRAESTRUCTURA
# -----------------------------------------------------------------
@bot.message_handler(commands=['panel', 'admin'])
def master_panel(message):
    if message.from_user.id != ADMIN_ID: return
    
    stats = Monitor.get_stats() # Obtiene CPU/RAM en tiempo real
    panel_text = (
        f"{Visuals.get_header()}\n"
        f"👑 <b>CENTRO DE MANDO OMNIPOTENT</b>\n\n"
        f"🖥️ <b>SISTEMA:</b>\n"
        f"└ CPU: {stats['cpu']}% | RAM: {stats['ram']}%\n"
        f"└ UPTIME: {stats['uptime']}\n\n"
        f"⚙️ <b>MODULOS ACTIVOS:</b>\n"
        f"└ Firewall L7, Economy v2, Hybrid Search"
    )
    # Aquí irían los botones Inline de admin_dashboard.py
    bot.send_message(message.chat.id, panel_text, parse_mode="HTML")

# -----------------------------------------------------------------
# [EXECUTION] EL MOTOR DE ARRANQUE (AL FINAL)
# -----------------------------------------------------------------
if __name__ == "__main__":
    # Inicia el servidor web para Render (Anti-Sleep)
    keep_alive() 
    print(f"🚀 {datetime.now()} | CJKILLER OMNIPOTENT v35.0 ACTIVO")
    
    # Bucle infinito con auto-reconexión ante errores de red
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"⚠️ RECONECTANDO... ERROR: {e}")
            time.sleep(5)
