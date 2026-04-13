import curses
import os
import time
import datetime

def hablar(texto, rate=270):
    try:
        texto_limpio = texto.replace('"', '').replace("'", "")
        os.system(f'espeak-ng -s {rate} -v es "{texto_limpio}" 2>/dev/null')
    except:
        pass

def hablar_async(texto, rate=400):
    try:
        texto_limpio = texto.replace('"', '').replace("'", "")
        os.system('killall espeak-ng 2>/dev/null')
        os.system(f'espeak-ng -s {rate} -v es "{texto_limpio}" 2>/dev/null &')
    except:
        pass

def safe_addstr(stdscr, y, x, texto, estilo=0):
    try:
        alto, ancho = stdscr.getmaxyx()
        if 0 <= y < alto and 0 <= x < ancho:
            espacio_disponible = ancho - x
            stdscr.addstr(y, x, texto[:espacio_disponible], estilo)
    except:
        pass

def iniciar(stdscr):
    # --- BASE DE DATOS DE COMANDOS ---
    lecciones = [
        # NAVEGACIÓN Y ARCHIVOS
        {"cmd": "sudo", "desc": "Permite al usuario ejecutar comandos sin ningun tipo de restrccion", "ejemplo": "sudo apt upgrade (Actualiza todas las aplicaciones)"},
        {"cmd": "pwd", "desc": "Imprime la ruta absoluta del directorio de trabajo actual.", "ejemplo": "Uso: pwd (Verifica donde estas parado)"},
        {"cmd": "ls -la", "desc": "Lista contenido del directorio con atributos detallados y archivos ocultos.", "ejemplo": "Uso: ls -la /home/kali"},
        {"cmd": "cd /tmp", "desc": "Cambia el directorio actual a la carpeta de archivos temporales.", "ejemplo": "Uso: cd /var/log (Para revisar registros)"},
        {"cmd": "mkdir evidence", "desc": "Crea un nuevo directorio en la ruta actual para organizar hallazgos.", "ejemplo": "Uso: mkdir cases_2026"},
        {"cmd": "touch case.txt", "desc": "Crea un archivo vacio o actualiza la fecha de modificacion de uno existente.", "ejemplo": "Uso: touch notas_forenses.log"},
        {"cmd": "cp case.txt case_bak.txt", "desc": "Realiza una copia exacta de un archivo en una nueva ubicacion.", "ejemplo": "Uso: cp evidencia.dd /media/externo/"},
        {"cmd": "mv case.txt evidence/", "desc": "Mueve o renombra archivos y directorios dentro del sistema.", "ejemplo": "Uso: mv antiguo.txt nuevo_nombre.txt"},
        {"cmd": "rm case_bak.txt", "desc": "Elimina un archivo del sistema de archivos de forma permanente.", "ejemplo": "Nota: ¡No se puede recuperar facilmente!"},
        {"cmd": "cat /etc/hostname", "desc": "Concatena y muestra el contenido completo de un archivo en la terminal.", "ejemplo": "Uso: cat /etc/issue (Ver version del sistema)"},
        {"cmd": "cat /etc/os-release", "desc": "Informa sobre la Version de la distriucion de linux que se usa", "ejemplo": "Uso: cat /etc/os-release (Ver version del sistema)"},
        {"cmd": "head -n 5 /etc/passwd", "desc": "Muestra las primeras lineas de un archivo de texto.", "ejemplo": "Uso: head -n 10 /var/log/auth.log"},
        
        # BUSQUEDA Y FILTRADO
        {"cmd": "grep 'root' /etc/passwd", "desc": "Busca coincidencias de texto dentro de archivos o flujos de datos.", "ejemplo": "Uso: dmesg | grep -i usb"},
        {"cmd": "find /home -name '*.jpg'", "desc": "Busca archivos en una jerarquia de directorios segun criterios.", "ejemplo": "Uso: find / -user kali (Busca archivos del usuario)"},
        {"cmd": "locate binary", "desc": "Encuentra archivos rapidamente consultando una base de datos indexada.", "ejemplo": "Uso: updatedb (Para actualizar el indice)"},
        {"cmd": "which python3", "desc": "Localiza y muestra la ruta del archivo ejecutable de un programa.", "ejemplo": "Uso: which nmap"},
        {"cmd": "history | tail", "desc": "Muestra el historial de comandos ejecutados recientemente.", "ejemplo": "Uso: !102 (Repite el comando 102 del historial)"},
        
        # SISTEMA Y HARDWARE
        {"cmd": "uname -a", "desc": "Muestra informacion detallada del kernel, arquitectura y sistema operativo.", "ejemplo": "Uso: uname -r (Ver solo el kernel)"},
        {"cmd": "lscpu", "desc": "Despliega informacion detallada sobre la arquitectura de la CPU.", "ejemplo": "Muestra nucleos, hilos y cache del procesador."},
        {"cmd": "lsblk", "desc": "Lista informacion sobre todos los dispositivos de bloque disponibles.", "ejemplo": "Uso: lsblk -f (Ver sistemas de archivos)"},
        {"cmd": "df -h", "desc": "Muestra el espacio libre y utilizado en los discos en formato legible.", "ejemplo": "Uso: df -i (Ver disponibilidad de inodos)"},
        {"cmd": "du -sh *", "desc": "Estima y muestra el uso de espacio de archivos y directorios.", "ejemplo": "Uso: du -h --max-depth=1"},
        {"cmd": "free -m", "desc": "Muestra la cantidad de memoria RAM libre y usada en el sistema.", "ejemplo": "Uso: free -h (Formato humano)"},
        {"cmd": "uptime", "desc": "Indica cuanto tiempo ha estado encendido el sistema y la carga promedio.", "ejemplo": "Muestra usuarios logueados y carga de CPU."},
        {"cmd": "dmesg | grep usb", "desc": "Examina los mensajes del buffer del kernel sobre dispositivos de hardware.", "ejemplo": "Vital para detectar pendrives recien conectados."},
        
        # PROCESOS Y RECURSOS
        {"cmd": "top", "desc": "Monitor dinamico de procesos y recursos del sistema en tiempo real.", "ejemplo": "Presiona 'q' para salir, 'k' para matar un proceso."},
        {"cmd": "ps aux", "desc": "Muestra una instantanea de todos los procesos activos en el sistema.", "ejemplo": "Uso: ps aux | grep apache"},
        {"cmd": "kill -9 1234", "desc": "Envia una señal de terminacion forzosa a un proceso especifico.", "ejemplo": "Uso: killall firefox (Mata todas las instancias)"},
        {"cmd": "htop", "desc": "Visualizador de procesos interactivo y amigable para la terminal.", "ejemplo": "Requiere instalacion: sudo apt install htop"},
        
        # REDES Y CONECTIVIDAD
        {"cmd": "ip a", "desc": "Te Muestra tu propia direccion IP", "ejemplo": "Uso: ip a"},
        {"cmd": "ip addr", "desc": "Administra y visualiza direcciones IP e interfaces de red.", "ejemplo": "Uso: ip link set eth0 up"},
        {"cmd": "ping -c 4 8.8.8.8", "desc": "Envia paquetes de prueba ICMP para verificar conectividad.", "ejemplo": "Uso: ping google.com"},
        {"cmd": "nmcli device", "desc": "Herramienta de linea de comandos para controlar NetworkManager.", "ejemplo": "Uso: nmcli dev wifi list"},
        {"cmd": "ifconfig", "desc": "Configura y muestra interfaces de red (Herramienta clasica).", "ejemplo": "Muestra MAC, IP y mascara de subred."},
        {"cmd": "netstat -tuln", "desc": "Muestra puertos abiertos y servicios en escucha de red.", "ejemplo": "Uso: netstat -ap (Ver que programa usa el puerto)"},
        {"cmd": "ss -ant", "desc": "Investiga sockets y estadisticas de red TCP (Sucesor de netstat).", "ejemplo": "Mas rapido y detallado que herramientas antiguas."},
        {"cmd": "ssh user@host", "desc": "Inicia una conexion de terminal segura con un servidor remoto.", "ejemplo": "Uso: ssh -p 2222 admin@192.168.1.1"},
        {"cmd": "scp file.txt user@host:/tmp", "desc": "Copia archivos de forma segura entre hosts a traves de la red.", "ejemplo": "Uso: scp -r carpeta/ remoto:/backup"},
        {"cmd": "curl -I google.com", "desc": "Transfiere datos desde o hacia un servidor mediante diversos protocolos.", "ejemplo": "El parametro -I trae solo las cabeceras HTTP."},
        
        # SEGURIDAD Y FORENSE
        {"cmd": "sudo -l", "desc": "Lista los privilegios permitidos para el usuario actual mediante sudo.", "ejemplo": "Permite ver si puedes ejecutar comandos como root."},
        {"cmd": "chmod +x script.sh", "desc": "Cambia los permisos de acceso de un archivo (Otorga ejecucion).", "ejemplo": "Uso: chmod 777 file (¡Peligro: acceso total!)"},
        {"cmd": "chown root:root file", "desc": "Cambia el propietario y el grupo de un archivo o directorio.", "ejemplo": "Uso: chown -R kali:kali /home/kali/data"},
        {"cmd": "whoami", "desc": "Muestra el nombre del usuario efectivo vinculado a la sesion actual.", "ejemplo": "Util para verificar si el sudo funciono."},
        {"cmd": "id", "desc": "Imprime los identificadores de usuario y de grupo actuales.", "ejemplo": "Muestra UID, GID y grupos secundarios."},
        {"cmd": "last", "desc": "Muestra una lista de los ultimos usuarios conectados al sistema.", "ejemplo": "Uso: last -n 5 (Ver ultimos 5 logins)"},
        {"cmd": "shred -u file.txt", "desc": "Sobreescribe un archivo para ocultar su contenido y luego lo elimina.", "ejemplo": "Vital en forense para destruccion segura de datos."},
        {"cmd": "md5sum file.txt", "desc": "Calcula y verifica la huella digital MD5 de un archivo.", "ejemplo": "Verifica si un archivo fue alterado."},
        {"cmd": "sha256sum file.txt", "desc": "Genera el hash SHA256 para verificar la integridad de la evidencia.", "ejemplo": "Estandar forense para cadena de custodia."},
        {"cmd": "dd if=/dev/sdb of=img.raw", "desc": "Copia datos a bajo nivel (Bit a Bit) entre archivos y dispositivos.", "ejemplo": "Uso: dd status=progress (Ver avance de la copia)"},
        
        # GESTIÓN DE PAQUETES Y LOGS
        {"cmd": "sudo apt update", "desc": "Actualiza el indice de paquetes disponibles en los repositorios.", "ejemplo": "Paso previo obligatorio antes de instalar algo."},
        {"cmd": "tail -f /var/log/syslog", "desc": "Muestra el final de un archivo y sigue sus cambios en vivo.", "ejemplo": "Uso: tail -n 20 (Ver las ultimas 20 lineas)"},
        {"cmd": "journalctl -xe", "desc": "Consulta los registros del sistema gestionados por systemd.", "ejemplo": "Uso: journalctl -u ssh (Ver logs de SSH)"},
        {"cmd": "alias cls='clear'", "desc": "Crea un nombre alternativo o atajo para un comando complejo.", "ejemplo": "Uso: alias (Sin parametros para ver todos)"},
        {"cmd": "exit", "desc": "Termina la ejecucion de la shell o cierra la sesion actual.", "ejemplo": "Finaliza el proceso de terminal activo."}
    ]

    curses.start_color()
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)    
    curses.init_pair(12, curses.COLOR_CYAN, curses.COLOR_BLACK)   

    stdscr.clear()
    hablar("Iniciando fase de entrenamiento Bash Core. Escuche con atención cada comando.")
    
    tiempo_inicio = time.time()
    
    for idx, lecc in enumerate(lecciones):
        comando_objetivo = lecc['cmd']
        input_usuario = ""
        descripcion = lecc['desc']
        ejemplo = lecc.get('ejemplo', "Sin ejemplo adicional.")

        # --- FASE 1: EXPLICACIÓN ---
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()
        cy, cx = alto // 2, ancho // 2

        safe_addstr(stdscr, cy - 8, cx - 15, f"PROGRESO: {idx+1}/{len(lecciones)}", curses.color_pair(10))
        safe_addstr(stdscr, cy - 6, cx - (len(comando_objetivo)//2), comando_objetivo, curses.A_BOLD | curses.color_pair(3))
        safe_addstr(stdscr, cy - 3, cx - (len(descripcion)//2), descripcion, curses.color_pair(2))
        safe_addstr(stdscr, cy + 1, cx - (len(ejemplo)//2), ejemplo, curses.color_pair(12) | curses.A_DIM)
        safe_addstr(stdscr, cy + 8, cx - 12, "[ ESCUCHANDO ASISTENTE... ]", curses.A_BLINK)
        stdscr.refresh()

        hablar(f"Comando: {comando_objetivo.replace('-', ' guion ')}")
        hablar(descripcion)

        # --- FASE 2: ESCRITURA ESTRICTA ---
        while input_usuario != comando_objetivo:
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            cy, cx = alto // 2, ancho // 2

            timer_txt = f"⏱️ {time.time()-tiempo_inicio:.1f}s | NODO: {idx+1}"
            safe_addstr(stdscr, cy - 8, cx - (len(timer_txt)//2), timer_txt, curses.color_pair(10))
            safe_addstr(stdscr, cy - 6, cx - (len(comando_objetivo)//2), comando_objetivo, curses.A_BOLD | curses.color_pair(3))
            safe_addstr(stdscr, cy - 3, cx - (len(descripcion)//2), descripcion, curses.color_pair(2))
            safe_addstr(stdscr, cy + 1, cx - (len(ejemplo)//2), ejemplo, curses.color_pair(12) | curses.A_DIM)

            prompt = "KALI@UNEFA:~$ "
            ancho_total_fijo = len(prompt) + len(comando_objetivo)
            start_x = max(0, cx - (ancho_total_fijo // 2))
            
            safe_addstr(stdscr, cy + 6, start_x, prompt, curses.color_pair(3) | curses.A_BOLD)

            for i, char in enumerate(input_usuario):
                safe_addstr(stdscr, cy + 6, start_x + len(prompt) + i, char, curses.color_pair(3) | curses.A_BOLD)

            stdscr.refresh()

            key = stdscr.getch()
            if key in (curses.KEY_BACKSPACE, 127, 8):
                input_usuario = input_usuario[:-1]
            elif 32 <= key <= 126:
                char_tecleado = chr(key)
                
                if len(input_usuario) < len(comando_objetivo) and char_tecleado == comando_objetivo[len(input_usuario)]:
                    input_usuario += char_tecleado
                    if char_tecleado == " ":
                        hablar_async("espacio")
                    elif char_tecleado == "-":
                        hablar_async("guion")
                    else:
                        hablar_async(char_tecleado)
                else:
                    hablar_async("Letra incorrecta. Reiniciando.")
                    input_usuario = "" 
                    
            elif key == 27: 
                return

        hablar("Correcto", rate=350)

    # Detenemos el cronómetro al terminar los 50 comandos
    tiempo_total = time.time() - tiempo_inicio
    m = int(tiempo_total // 60)
    s = int(tiempo_total % 60)

    # --- FASE 3: CAPTURA DE IDENTIDAD ---
    nombre_estudiante = ""
    stdscr.clear()
    hablar("Entrenamiento superado. Ingrese su nombre y apellido para emitir el certificado.")

    while True:
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()
        cy, cx = alto // 2, ancho // 2

        titulo = "¡MARATÓN DE COMANDOS COMPLETADA CON EXITO!"
        instruccion = "Ingrese su Nombre y Apellido para el Certificado (Presione ENTER al terminar):"
        prompt_nombre = ">> "

        safe_addstr(stdscr, cy - 4, cx - (len(titulo)//2), titulo, curses.color_pair(3) | curses.A_BOLD)
        safe_addstr(stdscr, cy - 2, cx - (len(instruccion)//2), instruccion, curses.color_pair(2))
        
        # Centramos el input box del nombre
        start_x_nombre = max(0, cx - 20)
        safe_addstr(stdscr, cy, start_x_nombre, prompt_nombre + nombre_estudiante, curses.color_pair(10) | curses.A_BOLD)
        
        stdscr.refresh()
        key = stdscr.getch()

        # Si presiona ENTER (10 o 13) y ha escrito algo, avanzamos
        if key in [curses.KEY_ENTER, 10, 13]:
            if len(nombre_estudiante.strip()) > 0:
                break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            nombre_estudiante = nombre_estudiante[:-1]
        elif 32 <= key <= 126:
            nombre_estudiante += chr(key)

    # --- FASE 4: GENERACIÓN DEL REPORTE TXT ---
    stdscr.clear()
    
    try:
        escritorio = os.path.expanduser("~/Desktop")
        if not os.path.exists(escritorio):
            escritorio_es = os.path.expanduser("~/Escritorio")
            if os.path.exists(escritorio_es):
                escritorio = escritorio_es
            else:
                escritorio = os.path.expanduser("~") 

        fecha_obj = datetime.datetime.now()
        fecha_str = fecha_obj.strftime("%d/%m/%Y %I:%M:%S %p")
        # El nombre del archivo ahora incluye el nombre del estudiante formateado
        nombre_limpio = nombre_estudiante.strip().replace(" ", "_").upper()
        nombre_archivo = f"Certificado_Bash_{nombre_limpio}_{fecha_obj.strftime('%Y%m%d')}.txt"
        ruta_completa = os.path.join(escritorio, nombre_archivo)

        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write("=========================================================\n")
            f.write("       CERTIFICADO DE ENTRENAMIENTO - TACTICAL BASH      \n")
            f.write("                MINCYT YARACUY - UNEFA                   \n")
            f.write("=========================================================\n\n")
            f.write(f"FECHA Y HORA : {fecha_str}\n")
            f.write(f"MODULO       : Nivel 1 - Fundamentos de Bash y Supervivencia\n")
            f.write(f"RENDIMIENTO  : {len(lecciones)} Comandos superados al 100%\n")
            f.write(f"TIEMPO TOTAL : {m} minutos con {s} segundos\n\n")
            f.write("=========================================================\n")
            f.write("EVALUADOR / INSTRUCTOR:\n")
            f.write("Ángel Gustavo Castillo Giménez\n")
            f.write("Ing. Josue Ordoñez\n\n")
            # Inyectamos el nombre ingresado por el usuario
            f.write(f"OPERADOR CERTIFICADO : {nombre_estudiante.strip().upper()}\n")
            f.write("=========================================================\n")
            f.write(">> Sistema Automatizado de Evaluación Forense <<\n")

        msg_reporte = f">> Certificado guardado en: {ruta_completa} <<"
        safe_addstr(stdscr, cy, cx - (len(msg_reporte)//2), msg_reporte, curses.color_pair(10) | curses.A_BOLD)
    except:
        msg_error = ">> Error: No se pudo generar el reporte txt <<"
        safe_addstr(stdscr, cy, cx - (len(msg_error)//2), msg_error, curses.color_pair(11) | curses.A_BOLD)

    stdscr.refresh()
    hablar(f"Entrenamiento finalizado. Certificado emitido para {nombre_estudiante}. Guardado en el escritorio.")
    time.sleep(4)