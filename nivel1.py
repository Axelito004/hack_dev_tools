import curses
import pyttsx3
import time

# Configuración del motor de voz
engine = pyttsx3.init('espeak')
# ACELERAMOS LA VOZ: 280-300 es ideal para que no haya lag al teclear
engine.setProperty('rate', 280) 

def hablar(texto, blocking=True):
    engine.say(texto)
    if blocking:
        engine.runAndWait()

def iniciar(stdscr):
    # --- BASE DE DATOS DE 50 COMANDOS ESENCIALES ---
    lecciones = [
        # NAVEGACIÓN Y ARCHIVOS
        {"cmd": "pwd", "desc": "Muestra la ruta del directorio actual."},
        {"cmd": "ls -la", "desc": "Lista todos los archivos, incluyendo ocultos y permisos."},
        {"cmd": "cd /tmp", "desc": "Cambia al directorio temporal del sistema."},
        {"cmd": "mkdir evidence", "desc": "Crea un directorio para almacenar hallazgos."},
        {"cmd": "touch case.txt", "desc": "Crea un archivo vacío para notas del caso."},
        {"cmd": "cp case.txt case_bak.txt", "desc": "Copia archivos de evidencia."},
        {"cmd": "mv case.txt evidence/", "desc": "Mueve archivos a carpetas específicas."},
        {"cmd": "rm case_bak.txt", "desc": "Elimina archivos (¡Cuidado en forense!)."},
        {"cmd": "cat /etc/hostname", "desc": "Visualiza el nombre de la máquina."},
        {"cmd": "head -n 5 /etc/passwd", "desc": "Muestra las primeras 5 líneas de un archivo."},
        
        # BUSQUEDA Y FILTRADO
        {"cmd": "grep 'root' /etc/passwd", "desc": "Busca un patrón específico en un texto."},
        {"cmd": "find /home -name '*.jpg'", "desc": "Busca archivos por nombre y extensión."},
        {"cmd": "locate binary", "desc": "Encuentra archivos rápidamente usando una base de datos."},
        {"cmd": "which python3", "desc": "Muestra la ruta del ejecutable de un programa."},
        {"cmd": "history | tail", "desc": "Muestra los últimos comandos ejecutados."},
        
        # SISTEMA Y HARDWARE
        {"cmd": "uname -a", "desc": "Muestra información completa del Kernel y sistema."},
        {"cmd": "lscpu", "desc": "Muestra la arquitectura y detalles del procesador."},
        {"cmd": "lsblk", "desc": "Lista los dispositivos de bloque (discos y particiones)."},
        {"cmd": "df -h", "desc": "Muestra el espacio libre en los discos en formato humano."},
        {"cmd": "du -sh *", "desc": "Calcula el tamaño de carpetas y archivos."},
        {"cmd": "free -m", "desc": "Muestra el estado de la memoria RAM en Megabytes."},
        {"cmd": "uptime", "desc": "Indica cuánto tiempo lleva encendido el sistema."},
        {"cmd": "dmesg | grep usb", "desc": "Muestra mensajes del kernel sobre dispositivos USB."},
        
        # PROCESOS Y RECURSOS
        {"cmd": "top", "desc": "Monitor de procesos en tiempo real (Presiona 'q' para salir)."},
        {"cmd": "ps aux", "desc": "Instantánea de todos los procesos en ejecución."},
        {"cmd": "kill -9 1234", "desc": "Fuerza el cierre de un proceso por su ID."},
        {"cmd": "htop", "desc": "Monitor de procesos interactivo y visual."},
        
        # REDES Y CONECTIVIDAD
        {"cmd": "ip addr", "desc": "Muestra las interfaces de red y direcciones IP."},
        {"cmd": "ping -c 4 8.8.8.8", "desc": "Prueba la conectividad hacia Google."},
        {"cmd": "nmcli device", "desc": "Gestiona conexiones de red desde terminal."},
        {"cmd": "ifconfig", "desc": "Herramienta clásica para configurar interfaces (obsoleta pero vital)."},
        {"cmd": "netstat -tuln", "desc": "Muestra puertos abiertos y servicios escuchando."},
        {"cmd": "ss -ant", "desc": "Muestra estadísticas de sockets TCP (sucesor de netstat)."},
        {"cmd": "ssh user@host", "desc": "Inicia conexión segura remota."},
        {"cmd": "scp file.txt user@host:/tmp", "desc": "Copia archivos de forma segura entre hosts."},
        {"cmd": "curl -I google.com", "desc": "Obtiene las cabeceras HTTP de un sitio."},
        
        # SEGURIDAD Y FORENSE
        {"cmd": "sudo -l", "desc": "Lista los privilegios del usuario actual."},
        {"cmd": "chmod +x script.sh", "desc": "Otorga permisos de ejecución a un archivo."},
        {"cmd": "chown root:root file", "desc": "Cambia el propietario y grupo de un archivo."},
        {"cmd": "whoami", "desc": "Muestra el nombre del usuario actual."},
        {"cmd": "id", "desc": "Muestra el UID y GID del usuario."},
        {"cmd": "last", "desc": "Muestra los últimos usuarios que iniciaron sesión."},
        {"cmd": "shred -u file.txt", "desc": "Sobreescribe y elimina un archivo de forma segura."},
        {"cmd": "md5sum file.txt", "desc": "Calcula el hash MD5 para verificar integridad."},
        {"cmd": "sha256sum file.txt", "desc": "Calcula el hash SHA256 (estándar forense)."},
        {"cmd": "dd if=/dev/sdb of=img.raw", "desc": "Crea una imagen bit a bit de un disco (Forense puro)."},
        
        # GESTIÓN DE PAQUETES Y LOGS
        {"cmd": "sudo apt update", "desc": "Actualiza la lista de paquetes de los repositorios."},
        {"cmd": "tail -f /var/log/syslog", "desc": "Monitorea logs del sistema en tiempo real."},
        {"cmd": "journalctl -xe", "desc": "Muestra errores detallados del sistema (systemd)."},
        {"cmd": "alias cls='clear'", "desc": "Crea un atajo personalizado para comandos."},
        {"cmd": "exit", "desc": "Cierra la sesión actual de la terminal."}
    ]

    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    hablar("Iniciando maratón de cincuenta comandos. La velocidad y precisión son clave.")
    
    tiempo_inicio = time.time()
    
    for idx, lecc in enumerate(lecciones):
        comando_objetivo = lecc['cmd']
        input_usuario = ""
        
        while input_usuario != comando_objetivo:
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            
            # --- INTERFAZ ---
            tiempo_actual = time.time() - tiempo_inicio
            stdscr.addstr(1, 2, f"⏱️ TIEMPO: {tiempo_actual:.2f}s", curses.color_pair(10))
            stdscr.addstr(1, ancho - 25, f"PROGRESO: {idx+1}/50")
            
            stdscr.addstr(4, 5, ">> UTILIDAD:", curses.color_pair(3))
            stdscr.addstr(5, 5, lecc['desc'], curses.color_pair(2))
            
            stdscr.addstr(8, 5, "TECLEA:", curses.color_pair(2))
            stdscr.addstr(8, 15, comando_objetivo, curses.color_pair(2) | curses.A_DIM)

            # Entrada de usuario
            stdscr.addstr(11, 5, "KALI@UNEFA:~$ ", curses.color_pair(3) | curses.A_BOLD)
            for i, char in enumerate(input_usuario):
                color = curses.color_pair(3)
                if i >= len(comando_objetivo) or char != comando_objetivo[i]:
                    color = curses.color_pair(11)
                stdscr.addstr(11, 20 + i, char, color | curses.A_BOLD)

            stdscr.refresh()

            key = stdscr.getch()

            if key in (curses.KEY_BACKSPACE, 127, 8):
                input_usuario = input_usuario[:-1]
            elif 32 <= key <= 126:
                char_tecleado = chr(key)
                input_usuario += char_tecleado
                # FEEDBACK AUDITIVO POR LETRA
                engine.say(char_tecleado)
                engine.runAndWait()
            elif key == 27:
                return

        # Sonido de éxito corto
        engine.say("Correcto")
        engine.runAndWait()

    # --- RESUMEN FINAL ---
    tiempo_total = time.time() - tiempo_inicio
    stdscr.clear()
    msg_final = f"MARATÓN COMPLETADA EN {tiempo_total:.2f} SEGUNDOS."
    stdscr.addstr(alto // 2, (ancho // 2) - (len(msg_final) // 2), msg_final, curses.color_pair(3) | curses.A_BOLD)
    stdscr.refresh()
    hablar(f"Increíble, Ángel. Has completado los cincuenta comandos en {int(tiempo_total)} segundos. Eres un experto.")
    stdscr.getch()