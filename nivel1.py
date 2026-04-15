import curses
import time
import os
import textwrap

# --- MOTOR DE VOZ ASÍNCRONO ---
def hablar(texto, rate=280):
    try:
        texto_limpio = texto.replace('"', '').replace("'", "")
        os.system(f'espeak-ng -s {rate} -v es "{texto_limpio}" 2>/dev/null &')
    except:
        pass

def format_time(segundos):
    """Convierte segundos en formato MM:SS"""
    mins = int(segundos // 60)
    secs = int(segundos % 60)
    return f"{mins:02d}:{secs:02d}"

def draw_text_wrapped(stdscr, y, x, text, width, color):
    y_actual = y
    for parrafo in text.split('\n'):
        lineas = textwrap.wrap(parrafo, width)
        for linea in lineas:
            try:
                stdscr.addstr(y_actual, x, linea, color)
            except curses.error: pass
            y_actual += 1
    return y_actual

# --- BASE DE DATOS DE COMANDOS (EJEMPLOS PARA LLENAR) ---
misiones_facil = [
    {"cmd": "clear", "desc": "Limpia la terminal para empezar de cero.", "out": "[Pantalla limpia]"},
    {"cmd": "pwd", "desc": "Muestra la ruta de la carpeta actual.", "out": "/home/kali"},
    {"cmd": "whoami", "desc": "Muestra el nombre del usuario actual.", "out": "root"},
    {"cmd": "ls", "desc": "Lista los archivos y carpetas visibles.", "out": "Desktop  Documents  Downloads"},
    {"cmd": "top", "desc": "Muestra los procesos en tiempo real.", "out": "PID USER PR NI VIRT RES SHR S %CPU"},
    {"cmd": "id", "desc": "Muestra tus identificadores de usuario.", "out": "uid=0(root) gid=0(root) groups=0(root)"},
    {"cmd": "uptime", "desc": "Indica cuanto tiempo lleva encendido el equipo.", "out": "up 2 hours, 15 minutes"},
    {"cmd": "hostname", "desc": "Muestra el nombre del equipo en la red.", "out": "kali-yaracuy"},
    {"cmd": "date", "desc": "Imprime la fecha y hora del sistema.", "out": "Wed Apr 15 10:00:00 2026"},
    {"cmd": "cal", "desc": "Muestra el calendario del mes actual.", "out": "April 2026"},
    {"cmd": "df", "desc": "Muestra el espacio libre en los discos.", "out": "/dev/sda1 50G 20G 30G 40% /"},
    {"cmd": "free", "desc": "Muestra el estado de la memoria RAM.", "out": "Mem: 8GB used: 2GB free: 6GB"},
    {"cmd": "groups", "desc": "Lista los grupos a los que perteneces.", "out": "root sudo audio video"},
    {"cmd": "history", "desc": "Muestra los ultimos comandos escritos.", "out": "1 ls  2 pwd  3 clear"},
    {"cmd": "arch", "desc": "Muestra la arquitectura del procesador.", "out": "x86_64"}
]
misiones_medio = [
    {"cmd": "ls -la", "desc": "Lista archivos ocultos y permisos.", "out": "drwxr-xr-x 2 root root 4096 ."},
    {"cmd": "mkdir evidencia", "desc": "Crea una carpeta llamada evidencia.", "out": "[Carpeta creada]"},
    {"cmd": "touch nota.txt", "desc": "Crea un archivo de texto vacio.", "out": "[Archivo creado]"},
    {"cmd": "cat /etc/passwd", "desc": "Lee la lista de usuarios del sistema.", "out": "root:x:0:0:root:/root:/bin/bash"},
    {"cmd": "cp nota.txt copia.txt", "desc": "Copia un archivo a una nueva ubicacion.", "out": "[Copiado con exito]"},
    {"cmd": "mv nota.txt dato.txt", "desc": "Renombra o mueve un archivo.", "out": "[Movido con exito]"},
    {"cmd": "rm dato.txt", "desc": "Borra un archivo permanentemente.", "out": "[Eliminado]"},
    {"cmd": "sudo su", "desc": "Cambia al modo superusuario con poder total.", "out": "root@kali#"},
    {"cmd": "chmod +x script.sh", "desc": "Otorga permisos de ejecucion.", "out": "[Permisos actualizados]"},
    {"cmd": "grep root /etc/passwd", "desc": "Busca la palabra root en un archivo.", "out": "root:x:0:0:root..."},
    {"cmd": "ls | grep txt", "desc": "Filtra solo archivos de texto.", "out": "nota.txt  copia.txt"},
    {"cmd": "ps aux", "desc": "Lista todos los programas ejecutandose.", "out": "root 1 0.0 0.1 168012 9904"},
    {"cmd": "kill -9 1234", "desc": "Fuerza el cierre de un programa por su ID.", "out": "[Proceso terminado]"},
    {"cmd": "ping -c 4 google.com", "desc": "Prueba conexion enviando 4 paquetes.", "out": "4 packets transmitted, 4 received"},
    {"cmd": "ifconfig eth0", "desc": "Configuracion de la tarjeta de red.", "out": "inet 192.168.1.15"},
    {"cmd": "iwconfig", "desc": "Estado de la red inalambrica wifi.", "out": "wlan0 IEEE 802.11"},
    {"cmd": "uname -a", "desc": "Muestra la version del sistema linux.", "out": "Linux kali 6.6.0-amd64"},
    {"cmd": "tail -n 5 /var/log/syslog", "desc": "Lee las ultimas 5 lineas del registro.", "out": "Apr 15 10:05:01 systemd..."},
    {"cmd": "tar -cvf backup.tar /etc", "desc": "Empaqueta archivos en un comprimido.", "out": "backup.tar [OK]"},
    {"cmd": "find . -name \"*.jpg\"", "desc": "Busca todas las fotos en esta carpeta.", "out": "./foto1.jpg"},
    {"cmd": "echo \"Hacked\" > msg.txt", "desc": "Escribe un mensaje en un archivo nuevo.", "out": "[Mensaje guardado]"},
    {"cmd": "cat msg.txt >> log.txt", "desc": "Añade texto al final de otro archivo.", "out": "[Contenido anexado]"},
    {"cmd": "apt list --installed", "desc": "Lista todos los programas instalados.", "out": "binwalk/kali-rolling,now"},
    {"cmd": "du -sh /home", "desc": "Muestra el tamaño de la carpeta personal.", "out": "2.4G /home"},
    {"cmd": "locate password", "desc": "Busca archivos llamados password.", "out": "/var/lib/mysql/password.key"}
]
misiones_dificil = [
    # --- REDES (NMAP) ---
    {"cmd": "nmap 192.168.1.1", "desc": "Escaneo de puertos basicos.", "out": "PORT STATE SERVICE\n80/tcp open http"},
    {"cmd": "nmap -sP 192.168.1.0/24", "desc": "Descubre equipos encendidos en la red.", "out": "Host 192.168.1.15 is up"},
    {"cmd": "nmap -sV 192.168.1.1", "desc": "Detecta versiones de software abierto.", "out": "80/tcp open http Apache 2.4.50"},
    {"cmd": "nmap -O 192.168.1.1", "desc": "Intenta detectar el sistema operativo.", "out": "OS: Linux 5.x"},
    {"cmd": "nmap -A 192.168.1.1", "desc": "Escaneo agresivo completo.", "out": "Vulnerabilities, OS, Versions..."},
    {"cmd": "nmap -p 80,443 192.168.1.1", "desc": "Analiza solo puertos web.", "out": "80/tcp open, 443/tcp open"},
    {"cmd": "nmap -Pn 192.168.1.1", "desc": "Escaneo saltando el bloqueo de ping.", "out": "Scanning without ping..."},
    {"cmd": "nmap --script vuln 192.168.1.1", "desc": "Busca vulnerabilidades conocidas.", "out": "VULNERABLE: CVE-2021-3177"},
    {"cmd": "nmap -sU 192.168.1.1", "desc": "Escaneo de puertos UDP.", "out": "53/udp open domain"},
    {"cmd": "nmap -T4 192.168.1.1", "desc": "Aumenta la velocidad del escaneo.", "out": "[Escaneo rapido completado]"},
    {"cmd": "nmap -oN scan.txt 192.168.1.1", "desc": "Guarda el reporte en un archivo.", "out": "[Guardado en scan.txt]"},
    {"cmd": "nmap -sS 192.168.1.1", "desc": "Escaneo sigiloso para evitar firewalls.", "out": "[SYN Scan completado]"},
    # --- OSINT ---
    {"cmd": "sherlock usuario", "desc": "Busca un usuario en redes sociales.", "out": "[*] Checking Instagram... Found!"},
    {"cmd": "whois google.com", "desc": "Muestra datos del dueño del dominio.", "out": "Registrar: MarkMonitor Inc."},
    {"cmd": "nslookup google.com", "desc": "Traduce dominio a direccion IP.", "out": "Address: 142.250.189.174"},
    {"cmd": "theHarvester -d unefa.edu.ve -b google", "desc": "Recolecta correos de una institucion.", "out": "Emails found: 12"},
    {"cmd": "dig google.com ANY", "desc": "Informacion tecnica de servidores DNS.", "out": "google.com. IN MX 10..."},
    {"cmd": "photon -u http://target.com", "desc": "Rastrea archivos y correos de un sitio.", "out": "Found 45 scripts, 12 emails"},
    {"cmd": "subfinder -d target.com", "desc": "Encuentra subdominios ocultos.", "out": "dev.target.com, api.target.com"},
    {"cmd": "amass enum -d target.com", "desc": "Mapea toda la presencia en internet.", "out": "ASN: 15169 Google LLC"},
    {"cmd": "socialscan usuario", "desc": "Verifica disponibilidad en plataformas.", "out": "Instagram: Taken, Twitter: Free"},
    {"cmd": "h8mail -t victima@mail.com", "desc": "Busca si una clave fue filtrada.", "out": "Found in 2 breaches: Adobe, Canva"},
    {"cmd": "holehe victima@mail.com", "desc": "Verifica registros de un correo.", "out": "Registered on: Twitter, Netflix"},
    {"cmd": "dnsrecon -d target.com", "desc": "Auditoria completa de registros DNS.", "out": "SRV, TXT, A, AAAA records found"},
    {"cmd": "ctfr -d target.com", "desc": "Busca subdominios por certificados.", "out": "Found: staging.target.com"},
    # --- METADATOS (EXIFTOOL) ---
    {"cmd": "exiftool evidencia.jpg", "desc": "Muestra datos ocultos de una foto.", "out": "Make: Samsung, Model: S21"},
    {"cmd": "exiftool -gps:all evidencia.jpg", "desc": "Muestra las coordenadas GPS de la foto.", "out": "GPS: 10.342 N, 68.583 W"},
    {"cmd": "exiftool -all= evidencia.jpg", "desc": "Limpia todos los metadatos del archivo.", "out": "[Archivo limpiado]"},
    {"cmd": "exiftool -Make -Model evidencia.jpg", "desc": "Muestra la marca y el modelo de camara.", "out": "Samsung SM-G991B"},
    {"cmd": "exiftool \"-DateTimeOriginal\" evidencia.jpg", "desc": "Muestra fecha y hora de captura.", "out": "2026:04:15 10:30:00"},
    {"cmd": "exiftool -htmldump foto.jpg > info.html", "desc": "Crea un reporte visual en HTML.", "out": "[Reporte info.html generado]"},
    {"cmd": "exiftool -r folder/", "desc": "Analiza todas las fotos de una carpeta.", "out": "[15 archivos analizados]"},
    {"cmd": "exiftool -Artist=\"Agente\" foto.jpg", "desc": "Cambia el nombre del autor en la foto.", "out": "[Actualizado: Agente]"},
    {"cmd": "exiftool -CommonState foto.jpg", "desc": "Muestra metadatos de estado comunes.", "out": "File Size: 2.4MB"},
    {"cmd": "exiftool -ThumbnailImage -b foto.jpg > min.jpg", "desc": "Extrae la miniatura oculta.", "out": "[Miniatura guardada]"},
    # --- FORENSE Y RECUPERACION ---
    {"cmd": "binwalk firmware.bin", "desc": "Analiza archivos dentro de un binario.", "out": "0x0 PNG image data"},
    {"cmd": "binwalk -e firmware.bin", "desc": "Extrae el contenido de un binario.", "out": "[Extraccion finalizada]"},
    {"cmd": "foremost -i disco.img", "desc": "Recupera archivos borrados de un disco.", "out": "Extracting: jpg, pdf, zip"},
    {"cmd": "foremost -t jpg -i disco.img", "desc": "Recupera solo imagenes JPG borradas.", "out": "15 images recovered"},
    {"cmd": "scalpel disco.img -o salida", "desc": "Talla archivos de un disco dañado.", "out": "[Recuperacion avanzada OK]"},
    {"cmd": "testdisk /dev/sdb", "desc": "Repara particiones y discos dañados.", "out": "[Analizando particiones...]"},
    {"cmd": "photorec /dev/sdb", "desc": "Recupera fotos de memorias formateadas.", "out": "[Recuperando archivos...]"},
    {"cmd": "dd if=/dev/sdb of=disco.img", "desc": "Clona un disco bit a bit para analisis.", "out": "512MB copied [OK]"},
    {"cmd": "md5sum disco.img", "desc": "Genera la huella digital del archivo.", "out": "a1b2c3d4e5f6..."},
    {"cmd": "sha256sum disco.img", "desc": "Genera una huella de seguridad maxima.", "out": "e3b0c44298fc..."},
    {"cmd": "bulk_extractor disco.img -o res", "desc": "Extrae correos e IPs de un disco.", "out": "Emails found: 142"},
    {"cmd": "chkrootkit", "desc": "Busca virus y espias en el sistema.", "out": "Searching for rootkits..."},
    {"cmd": "rkhunter --check", "desc": "Auditoria contra puertas traseras.", "out": "System check: OK"},
    {"cmd": "lsblk", "desc": "Muestra discos conectados al equipo.", "out": "sda, sdb, nvme0n1"},
    {"cmd": "fdisk -l", "desc": "Lista las particiones y sus tamaños.", "out": "/dev/sda1 20G Linux"}
]

# --- GENERADOR DE CERTIFICADO ---
def generar_comprobante(stdscr, tiempos_logrados):
    curses.curs_set(1)
    stdscr.clear()
    alto, ancho = stdscr.getmaxyx()
    mx = ancho // 2
    
    stdscr.addstr(alto//2 - 6, mx - 20, "REGISTRO DE OPERADOR FINALIZADO", curses.A_BOLD)
    stdscr.addstr(alto//2 - 4, mx - 20, "Ingresa tu nombre para el acta oficial:", curses.color_pair(10))
    
    nombre = ""
    while True:
        stdscr.addstr(alto//2 - 2, mx - 20, " > " + nombre + " " * 30, curses.A_UNDERLINE)
        stdscr.refresh()
        k = stdscr.getch()
        if k in [10, 13] and len(nombre.strip()) > 2: break
        elif k in [127, 8, curses.KEY_BACKSPACE]: nombre = nombre[:-1]
        elif 32 <= k <= 126 and len(nombre) < 30: nombre += chr(k)

    user = os.getlogin()
    ruta = f"/home/{user}/Escritorio/"
    if not os.path.exists(ruta): ruta = f"/home/{user}/Desktop/"
    
    path_final = f"{ruta}Certificado_{nombre.replace(' ', '_')}.txt"
    
    reporte_tiempos = ""
    for nivel, segs in tiempos_logrados.items():
        if segs > 0:
            reporte_tiempos += f"   - NIVEL {nivel}: {format_time(segs)}\n"

    contenido = f"""
    =======================================================
               COMPROBANTE DE CAPACITACION TACTICA
                    FUNDACITE YARACUY
    =======================================================
    
    OPERADOR: {nombre.upper()}      

    ESTADISTICAS DE RENDIMIENTO:
    {reporte_tiempos}
    TIEMPO TOTAL: {format_time(sum(tiempos_logrados.values()))}

    FELICIDADES! HAS COMPLETADO TU CAPACITACION EN KALI-lINUZ (BASH)
    SIGUE CON TU PROGRESO PARA QUE TE CONVIERTAS EN TODO UN OPERADOR
    Y HACKER, {nombre.upper()}!
    
    ESTADO: CERTIFICADO POR Ing.Joue Ordonez & AG Castillo Gimenez
    =======================================================
    """
    
    try:
        with open(path_final, "w") as f:
            f.write(contenido)
        stdscr.addstr(alto//2 + 2, mx - 20, "¡CERTIFICADO GUARDADO!", curses.color_pair(3) | curses.A_BOLD)
    except:
        stdscr.addstr(alto//2 + 2, mx - 20, "ERROR AL GUARDAR", curses.color_pair(11))
    
    stdscr.addstr(alto//2 + 4, mx - 20, "Presiona ENTER para volver al INICIO", curses.A_BLINK)
    stdscr.refresh()
    stdscr.getch()
    curses.curs_set(0)

# --- MOTOR DE MISIONES ---
def ejecutar_nivel(stdscr, comandos, nombre_nivel):
    start_time_nivel = time.time()
    for idx, m in enumerate(comandos):
        input_user = ""
        exito = False
        voz_lista = False
        
        while not exito:
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            mx = int(ancho * 0.1)
            tiempo_actual = time.time() - start_time_nivel

            stdscr.addstr(2, mx, f"MODULO: {nombre_nivel} | FASE: {idx+1}/{len(comandos)}", curses.color_pair(12) | curses.A_BOLD)
            stdscr.addstr(2, ancho - mx - 20, f"TIEMPO: {format_time(tiempo_actual)}", curses.color_pair(10))
            
            stdscr.addstr(4, mx, "COMANDO:", curses.A_BOLD)
            stdscr.addstr(5, mx, m['cmd'], curses.color_pair(4) | curses.A_BOLD)
            y_act = draw_text_wrapped(stdscr, 7, mx, f"INFO: {m['desc']}\n\n--- SALIDA ESPERADA ---\nroot@kali:~# {m['cmd']}\n{m['out']}", ancho-mx*2, curses.color_pair(2))

            stdscr.addstr(alto-4, mx, "KALI-ACADEMY# ", curses.A_BOLD)
            
            # Dibujado del input
            for i, c in enumerate(input_user):
                stdscr.addstr(alto-4, mx + 14 + i, c, curses.color_pair(3) | curses.A_BOLD)

            stdscr.refresh()
            if not voz_lista:
                hablar(f"Comando {m['cmd']}. {m['desc']}")
                voz_lista = True

            stdscr.timeout(100)
            k = stdscr.getch()

            if k in [10, 13]: # ENTER
                if input_user.strip() == m['cmd']:
                    exito = True
                    hablar("Correcto", rate=400)
                else: input_user = ""
            elif k in [127, 8, curses.KEY_BACKSPACE]:
                input_user = input_user[:-1]
            elif 32 <= k <= 126:
                char = chr(k)
                # --- LOGICA DE ERROR: BORRADO TOTAL ---
                pos_actual = len(input_user)
                if pos_actual < len(m['cmd']) and char == m['cmd'][pos_actual]:
                    input_user += char
                else:
                    input_user = "" # RESET TOTAL SI FALLA
                    hablar("Error", rate=500)
            elif k == 27: return False, 0
            
    stdscr.timeout(-1)
    return True, time.time() - start_time_nivel

def iniciar(stdscr):
    tiempos_totales = {"FÁCIL": 0, "MEDIO": 0, "DIFÍCIL": 0}
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()
        niveles = [
            (" 1. NIVEL RECLUTA (Facil) ", misiones_facil, "FÁCIL", 10),
            (" 2. NIVEL AGENTE (Medio) ", misiones_medio, "MEDIO", 12),
            (" 3. NIVEL ESPECIALISTA (Dificil) ", misiones_dificil, "DIFÍCIL", 11),
            (" [ VOLVER AL MENU PRINCIPAL ] ", None, None, 2)
        ]
        
        sel = 0
        while True:
            stdscr.clear()
            stdscr.addstr(2, (ancho//2)-15, "--- ACADEMIA KALI YARACUY ---", curses.A_BOLD)
            for i, (txt, _, _, col) in enumerate(niveles):
                estilo = curses.A_REVERSE if i == sel else curses.A_NORMAL
                stdscr.addstr(6+i, (ancho//2)-18, txt.center(36), estilo | curses.color_pair(col))
            k = stdscr.getch()
            if k == curses.KEY_UP and sel > 0: sel -= 1
            elif k == curses.KEY_DOWN and sel < len(niveles)-1: sel += 1
            elif k in [10, 13]: break
        
        if niveles[sel][1] is None: break
        
        nombre_str, lista_cmds, clave, _ = niveles[sel]
        exito, duracion = ejecutar_nivel(stdscr, lista_cmds, nombre_str)
        
        if exito:
            tiempos_totales[clave] = duracion
            opcs = [" PASAR A OTRO NIVEL ", " FINALIZAR Y GENERAR COMPROBANTE "]
            res = 0
            while True:
                stdscr.clear()
                stdscr.addstr(alto//2-2, (ancho//2)-10, "¡FASE COMPLETADA!", curses.color_pair(10) | curses.A_BOLD)
                for i, o in enumerate(opcs):
                    stdscr.addstr(alto//2+i, (ancho//2)-15, o, curses.A_REVERSE if i == res else curses.A_NORMAL)
                k = stdscr.getch()
                if k == curses.KEY_UP: res = 0
                elif k == curses.KEY_DOWN: res = 1
                elif k in [10, 13]: break
            
            if res == 1:
                generar_comprobante(stdscr, tiempos_totales)
                break