import curses
import time
import os
import textwrap
import random

# --- MOTOR DE VOZ ASÍNCRONO/SÍNCRONO ---
def hablar(texto, rate=200, esperar=False):
    try:
        texto_limpio = texto.replace('"', '').replace("'", "")
        comando_bash = f'espeak-ng -s {rate} -v es -g 2 "{texto_limpio}" 2>/dev/null'
        
        if not esperar:
            comando_bash += ' &' 
            
        os.system(comando_bash)
    except:
        pass

def format_time(segundos):
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

def calcular_rango(errores):
    if errores == 0: return "S+ (PERFECTO)"
    elif errores <= 3: return "S (ÉLITE)"
    elif errores <= 10: return "A (AVANZADO)"
    elif errores <= 20: return "B (COMPETENTE)"
    else: return "C (REQUIERE PRÁCTICA)"

def alerta_bloq_mayus(stdscr):
    alto, ancho = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.clear()
    
    msg1 = "¡ ALERTA DE SINTAXIS !"
    msg2 = "SE HA DETECTADO UNA MAYÚSCULA INCORRECTA."
    msg3 = "ES PROBABLE QUE TENGAS EL [BLOQ MAYÚS] ACTIVADO."
    msg4 = "KALI LINUX ES ESTRICTAMENTE SENSIBLE A MAYÚSCULAS/MINÚSCULAS."
    
    stdscr.addstr(alto//2 - 3, ancho//2 - len(msg1)//2, msg1, curses.color_pair(11) | curses.A_BLINK | curses.A_BOLD)
    stdscr.addstr(alto//2 - 1, ancho//2 - len(msg2)//2, msg2, curses.color_pair(12))
    stdscr.addstr(alto//2, ancho//2 - len(msg3)//2, msg3, curses.color_pair(12) | curses.A_BOLD)
    stdscr.addstr(alto//2 + 1, ancho//2 - len(msg4)//2, msg4, curses.color_pair(2))
    
    stdscr.addstr(alto//2 + 4, ancho//2 - 20, "[ PRESIONA CUALQUIER TECLA PARA CONTINUAR ]", curses.color_pair(10))
    stdscr.refresh()
    hablar("Alerta. Bloqueo de mayúsculas detectado.", esperar=True)
    stdscr.getch()

# --- BASE DE DATOS DE COMANDOS ---
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

misiones_extremo_final = [
    {"cmd": "find / -type f -perm -4000 -exec ls -l {} \\;", "desc": "Busca binarios SUID para escalar privilegios.", "out": "-rwsr-xr-x 1 root root 64K /usr/bin/passwd"},
    {"cmd": "iptables -A INPUT -p tcp --dport 22 -j ACCEPT", "desc": "Agrega regla de Firewall para permitir trafico SSH.", "out": "[Regla IPTABLES aplicada]"},
    {"cmd": "awk -F: '{ print $1 }' /etc/passwd", "desc": "Corta un archivo y muestra solo la columna de usuarios.", "out": "root\nkali\npostgres"},
    {"cmd": "sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config", "desc": "Reemplaza configuracion crítica para asegurar el servidor SSH.", "out": "[Archivo sshd_config actualizado]"},
    {"cmd": "hydra -l root -P pass.txt ssh://192.168.1.1", "desc": "Ataque de fuerza bruta remoto por protocolo SSH.", "out": "[22][ssh] host: 192.168.1.1   login: root   password: 12345"},
    {"cmd": "sqlmap -u \"http://target.com/vuln.php?id=1\" --dbs", "desc": "Inyeccion SQL automatizada para extraer bases de datos.", "out": "available databases [2]:\n[*] information_schema\n[*] users_db"},
    {"cmd": "tar -czvf backup.tar.gz /var/www/html/", "desc": "Comprime toda la carpeta web en un archivo gz.", "out": "backup.tar.gz creado con exito"},
    {"cmd": "ssh -L 8080:localhost:80 user@192.168.1.50", "desc": "Creacion de un tunel cifrado (Port Forwarding) via SSH.", "out": "Welcome to Ubuntu 22.04 LTS"},
    {"cmd": "grep -rnw '/var/log/' -e 'Failed password'", "desc": "Busca intentos de inicio de sesion fallidos en todos los logs.", "out": "/var/log/auth.log:35: Failed password for invalid user"},
    {"cmd": "chown -R www-data:www-data /var/www/html", "desc": "Cambia el propietario recursivamente de la carpeta web.", "out": "[Permisos y propietario cambiados]"},
    {"cmd": "systemctl restart NetworkManager.service", "desc": "Reinicia el servicio maestro de la red en Linux.", "out": "[Servicio reiniciado]"},
    {"cmd": "wget -r -np -nH --cut-dirs=1 http://target.com/files/", "desc": "Clona de forma recursiva un directorio abierto en una web.", "out": "Downloaded: 45 files, 15M in 2s"},
    {"cmd": "tcpdump -i eth0 -w capture.pcap port 80", "desc": "Captura trafico de red (Sniffing) y lo guarda en un archivo PCAP.", "out": "tcpdump: listening on eth0, link-type EN10MB"},
    {"cmd": "nc -lvnp 4444 -e /bin/bash", "desc": "Abre un puerto con Netcat para recibir una Reverse Shell.", "out": "Listening on [0.0.0.0] (family 0, port 4444)"},
    {"cmd": "hashcat -m 1000 hashes.txt rockyou.txt", "desc": "Ataque de diccionario a hashes NTLM usando Hashcat.", "out": "e10adc3949ba59abbe56e057f20f883e:123456"}
]

for m in misiones_facil: m['diff'] = "FÁCIL"
for m in misiones_medio: m['diff'] = "MEDIO"
for m in misiones_dificil: m['diff'] = "DIFÍCIL"
for m in misiones_extremo_final: m['diff'] = "EXTREMO"

# Tiempos límite en segundos para el modo CONTRARRELOJ
limites_tiempo = {
    "FÁCIL": 300,   # 5 min
    "MEDIO": 780,   # 13 min
    "DIFÍCIL": 1320, # 22 min
    "EXTREMO": 2100 # 35 min
}

# --- GENERADOR DE CERTIFICADO ---
def generar_comprobante(stdscr, estadisticas):
    curses.curs_set(1)
    stdscr.clear()
    alto, ancho = stdscr.getmaxyx()
    mx = ancho // 2
    
    stdscr.addstr(alto//2 - 6, mx - 20, "REGISTRO DE OPERADOR FINALIZADO", curses.A_BOLD)
    stdscr.addstr(alto//2 - 4, mx - 20, "Ingresa tu nombre para el acta oficial:", curses.color_pair(10))
    
    nombre = ""
    while True:
        stdscr.addstr(alto//2 - 2, mx - 20, " > " + nombre + " " * 30, curses.A_UNDERLINE)
        stdscr.move(alto//2 - 2, mx - 17 + len(nombre))
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
    tiempo_total = 0
    for nivel, data in estadisticas.items():
        if data['tiempo'] > 0:
            modo_texto = "CONTRARRELOJ" if data['modo'] == "CONTRARRELOJ" else "CLÁSICO"
            reporte_tiempos += f"   - NIVEL {nivel} | MODO: {modo_texto} | Rango: {data['rango']} | Errores cometidos: {data['errores']} | Tiempo: {format_time(data['tiempo'])}\n"
            tiempo_total += data['tiempo']

    fecha_hora_actual = time.strftime("%d/%m/%Y - %H:%M:%S")

    contenido = f"""
    =======================================================
            COMPROBANTE DE CAPACITACION TACTICA
                    FUNDACITE YARACUY
    =======================================================
    FECHA Y HORA DE EMISION: {fecha_hora_actual}
    
    OPERADOR: {nombre.upper()}      

    ESTADISTICAS DE RENDIMIENTO:
{reporte_tiempos}
    TIEMPO TOTAL EN OPERACIÓN: {format_time(tiempo_total)}

    ¡FELICIDADES! HAS COMPLETADO TU CAPACITACION EN KALI-LINUX (BASH)
    SIGUE CON TU PROGRESO PARA QUE TE CONVIERTAS EN TODO UN OPERADOR
    Y HACKER ETICO, {nombre.upper()}!
    
    ESTADO: CERTIFICADO POR Ing. Josue Ordoñez & A.G. Castillo Gimenez
    =======================================================
    """
    
    try:
        with open(path_final, "w") as f:
            f.write(contenido)
        stdscr.addstr(alto//2 + 2, mx - 20, "¡CERTIFICADO GUARDADO EXITOSAMENTE!", curses.color_pair(3) | curses.A_BOLD)
    except:
        stdscr.addstr(alto//2 + 2, mx - 20, "ERROR AL GUARDAR EL CERTIFICADO", curses.color_pair(11))
    
    curses.curs_set(0)
    stdscr.addstr(alto//2 + 4, mx - 20, "Presiona ENTER para volver al INICIO", curses.A_BLINK)
    stdscr.refresh()
    stdscr.getch()

# --- MOTOR DE MISIONES ---
def ejecutar_nivel(stdscr, comandos, nombre_nivel, modo="CLASICO", tiempo_limite=0):
    start_time_nivel = time.time()
    errores_nivel = 0
    
    for idx, m in enumerate(comandos):
        input_user = ""
        exito = False
        voz_lista = False
        
        while not exito:
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            mx = int(ancho * 0.1)
            
            tiempo_transcurrido = time.time() - start_time_nivel
            
            # --- LÓGICA DE TIEMPO SEGÚN EL MODO ---
            if modo == "CONTRARRELOJ":
                tiempo_restante = tiempo_limite - tiempo_transcurrido
                if tiempo_restante <= 0:
                    curses.curs_set(0)
                    stdscr.clear()
                    stdscr.addstr(alto//2, ancho//2 - 12, "¡ TIEMPO AGOTADO !", curses.color_pair(11) | curses.A_BLINK | curses.A_BOLD)
                    stdscr.refresh()
                    hablar("Tiempo agotado. Misión fracasada.", rate=200, esperar=True)
                    time.sleep(1)
                    return False, 0, errores_nivel
                
                color_reloj = curses.color_pair(11) | curses.A_BLINK if tiempo_restante <= 10 else curses.color_pair(10)
                str_tiempo = f"TIEMPO RESTANTE: {format_time(tiempo_restante)}"
            else:
                color_reloj = curses.color_pair(10)
                str_tiempo = f"TIEMPO: {format_time(tiempo_transcurrido)}"

            etiqueta_dif = f" [{m.get('diff', '')}]" if nombre_nivel == "MODO EXTREMO" else ""
            
            stdscr.addstr(2, mx, f"MODULO: {nombre_nivel}{etiqueta_dif} | FASE: {idx+1}/{len(comandos)} | MODO: {modo}", curses.color_pair(12) | curses.A_BOLD)
            stdscr.addstr(2, ancho - mx - 40, f"ERRORES: {errores_nivel} | {str_tiempo}", color_reloj)
            
            stdscr.addstr(4, mx, "COMANDO:", curses.A_BOLD)
            stdscr.addstr(5, mx, m['cmd'], curses.color_pair(4) | curses.A_BOLD)
            y_act = draw_text_wrapped(stdscr, 7, mx, f"INFO: {m['desc']}\n\n--- SALIDA ESPERADA ---\nroot@kali:~# {m['cmd']}\n{m['out']}", ancho-mx*2, curses.color_pair(2))

            stdscr.addstr(alto-4, mx, "KALI-ACADEMY# ", curses.A_BOLD)

            if not voz_lista:
                curses.curs_set(0)
                stdscr.addstr(alto-4, mx + 14, "[ ESCUCHANDO LA VOZ... ]", curses.color_pair(12) | curses.A_BLINK)
                stdscr.refresh()

                hablar(f"Comando. {m['cmd']}.", rate=200, esperar=True)
                hablar(f"Explicación. {m['desc']}", rate=200, esperar=True)
                
                curses.flushinp() 
                voz_lista = True
                
                stdscr.move(alto-4, mx)
                stdscr.clrtoeol()
                stdscr.addstr(alto-4, mx, "KALI-ACADEMY# ", curses.A_BOLD)

            for i, c in enumerate(input_user):
                stdscr.addstr(alto-4, mx + 14 + i, c, curses.color_pair(3) | curses.A_BOLD)

            curses.curs_set(1)
            stdscr.move(alto-4, mx + 14 + len(input_user))
            stdscr.refresh()

            stdscr.timeout(100)
            k = stdscr.getch()

            if k in [10, 13]: 
                if input_user.strip() == m['cmd']:
                    exito = True
                    curses.curs_set(0)
                    hablar("Correcto", rate=240, esperar=True) 
                else: input_user = ""
            elif k in [127, 8, curses.KEY_BACKSPACE]:
                input_user = input_user[:-1]
            elif 32 <= k <= 126:
                char = chr(k)
                pos_actual = len(input_user)
                
                if pos_actual < len(m['cmd']) and char == m['cmd'][pos_actual]:
                    input_user += char
                else:
                    if char.isalpha() and char.isupper() and pos_actual < len(m['cmd']) and m['cmd'][pos_actual].islower():
                        alerta_bloq_mayus(stdscr)
                    
                    input_user = "" 
                    errores_nivel += 1
                    hablar("Error", rate=280, esperar=False) 
            elif k == 27: 
                curses.curs_set(0)
                return False, 0, 0
            
    stdscr.timeout(-1)
    curses.curs_set(0)
    tiempo_final = time.time() - start_time_nivel
    return True, tiempo_final, errores_nivel

def iniciar(stdscr):
    estadisticas = {
        "FÁCIL": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""},
        "MEDIO": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""},
        "DIFÍCIL": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""},
        "EXTREMO": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""}
    }
    
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True: # BUCLE PRINCIPAL DE MODOS
        curses.curs_set(0)
        
        # --- AQUÍ ESTÁ LA SOLUCIÓN ---
        # Obtenemos las dimensiones de la pantalla antes de dibujar cualquier menú
        alto, ancho = stdscr.getmaxyx() 
        
        modos_juego = [
            (" MODO CLÁSICO (Sin presión de tiempo) ", "CLASICO", 10), 
            (" MODO CONTRARRELOJ (Muerte Súbita) ", "CONTRARRELOJ", 11),
            (" [ SALIR DE LA ACADEMIA ] ", "SALIR", 2)
        ]
        
        sel_modo = 0
        while True:
            stdscr.clear()
            stdscr.addstr(2, (ancho//2)-15, "--- ACADEMIA KALI YARACUY ---", curses.A_BOLD)
            stdscr.addstr(4, (ancho//2)-14, "SELECCIONA EL MODO DE JUEGO", curses.color_pair(4))
            
            for i, (txt, _, col) in enumerate(modos_juego):
                estilo_base = curses.color_pair(col)
                estilo = estilo_base | curses.A_REVERSE if i == sel_modo else estilo_base
                stdscr.addstr(6+i, (ancho//2)-len(txt)//2, txt, estilo)
                
            k = stdscr.getch()
            if k == curses.KEY_UP and sel_modo > 0: sel_modo -= 1
            elif k == curses.KEY_DOWN and sel_modo < len(modos_juego)-1: sel_modo += 1
            elif k in [10, 13]: break
            
        modo_elegido = modos_juego[sel_modo][1]
        
        if modo_elegido == "SALIR":
            break
            
        while True: # BUCLE SECUNDARIO DE DIFICULTADES
            stdscr.clear()
            # Volvemos a obtener dimensiones por si el usuario redimensionó la terminal
            alto, ancho = stdscr.getmaxyx() 
            
            niveles = [
                (" 1. NIVEL RECLUTA (Facil) ", misiones_facil, "FÁCIL", 10),
                (" 2. NIVEL AGENTE (Medio) ", misiones_medio, "MEDIO", 12),
                (" 3. NIVEL ESPECIALISTA (Dificil) ", misiones_dificil, "DIFÍCIL", 11),
                (" 4. MODO EXTREMO (Aleatorio + Bosses) ", None, "EXTREMO", 5), 
                (" [ VOLVER AL MENU DE MODOS ] ", None, "VOLVER", 2)
            ]
            
            sel_dif = 0
            while True:
                stdscr.clear()
                stdscr.addstr(2, (ancho//2)-15, "--- ACADEMIA KALI YARACUY ---", curses.A_BOLD)
                stdscr.addstr(4, (ancho//2)-22, f"MODO: {modo_elegido} - SELECCIONA DIFICULTAD", curses.color_pair(4))
                
                for i, (txt, _, _, col) in enumerate(niveles):
                    estilo_base = curses.color_pair(col)
                    estilo = estilo_base | curses.A_REVERSE if i == sel_dif else estilo_base
                    stdscr.addstr(6+i, (ancho//2)-18, txt.center(36), estilo)
                    
                k = stdscr.getch()
                if k == curses.KEY_UP and sel_dif > 0: sel_dif -= 1
                elif k == curses.KEY_DOWN and sel_dif < len(niveles)-1: sel_dif += 1
                elif k in [10, 13]: break
            
            clave = niveles[sel_dif][2]
            
            if clave == "VOLVER": 
                break # Rompe el bucle de dificultad y vuelve a preguntar por Clásico/Contrarreloj
            
            nombre_str = niveles[sel_dif][0].strip()
            lista_cmds = niveles[sel_dif][1]
            
            if clave == "EXTREMO":
                combinacion = misiones_facil + misiones_medio + misiones_dificil
                random.shuffle(combinacion)
                lista_cmds = combinacion + misiones_extremo_final
                nombre_str = "MODO EXTREMO"

            tiempo_limite_nivel = limites_tiempo[clave] if modo_elegido == "CONTRARRELOJ" else 0

            exito, duracion, errores = ejecutar_nivel(stdscr, lista_cmds, nombre_str, modo=modo_elegido, tiempo_limite=tiempo_limite_nivel)
            
            if exito:
                estadisticas[clave]['tiempo'] = duracion
                estadisticas[clave]['errores'] = errores
                estadisticas[clave]['rango'] = calcular_rango(errores)
                estadisticas[clave]['modo'] = modo_elegido
                
                opcs = [" PASAR A OTRO NIVEL ", " FINALIZAR Y GENERAR COMPROBANTE "]
                res = 0
                while True:
                    curses.curs_set(0)
                    stdscr.clear()
                    stdscr.addstr(alto//2-4, (ancho//2)-15, f"¡FASE {clave} COMPLETADA!", curses.color_pair(10) | curses.A_BOLD)
                    stdscr.addstr(alto//2-2, (ancho//2)-15, f"Rango Obtenido: {estadisticas[clave]['rango']}", curses.color_pair(12))
                    
                    for i, o in enumerate(opcs):
                        stdscr.addstr(alto//2+i, (ancho//2)-15, o, curses.A_REVERSE if i == res else curses.A_NORMAL)
                    k = stdscr.getch()
                    if k == curses.KEY_UP: res = 0
                    elif k == curses.KEY_DOWN: res = 1
                    elif k in [10, 13]: break
                
                if res == 1:
                    generar_comprobante(stdscr, estadisticas)
                    return # Cierra todo el sistema al generar el comprobante
    estadisticas = {
        "FÁCIL": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""},
        "MEDIO": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""},
        "DIFÍCIL": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""},
        "EXTREMO": {"tiempo": 0, "errores": 0, "rango": "", "modo": ""}
    }
    
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while True: # BUCLE PRINCIPAL DE MODOS
        curses.curs_set(0)
        
        modos_juego = [
            (" MODO CLÁSICO (Sin presión de tiempo) ", "CLASICO", 10), 
            (" MODO CONTRARRELOJ (Muerte Súbita) ", "CONTRARRELOJ", 11),
            (" [ SALIR DE LA ACADEMIA ] ", "SALIR", 2)
        ]
        
        sel_modo = 0
        while True:
            stdscr.clear()
            stdscr.addstr(2, (ancho//2)-15, "--- ACADEMIA KALI YARACUY ---", curses.A_BOLD)
            stdscr.addstr(4, (ancho//2)-14, "SELECCIONA EL MODO DE JUEGO", curses.color_pair(4))
            
            for i, (txt, _, col) in enumerate(modos_juego):
                estilo_base = curses.color_pair(col)
                estilo = estilo_base | curses.A_REVERSE if i == sel_modo else estilo_base
                stdscr.addstr(6+i, (ancho//2)-len(txt)//2, txt, estilo)
                
            k = stdscr.getch()
            if k == curses.KEY_UP and sel_modo > 0: sel_modo -= 1
            elif k == curses.KEY_DOWN and sel_modo < len(modos_juego)-1: sel_modo += 1
            elif k in [10, 13]: break
            
        modo_elegido = modos_juego[sel_modo][1]
        
        if modo_elegido == "SALIR":
            break
            
        while True: # BUCLE SECUNDARIO DE DIFICULTADES
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            niveles = [
                (" 1. NIVEL RECLUTA (Facil) ", misiones_facil, "FÁCIL", 10),
                (" 2. NIVEL AGENTE (Medio) ", misiones_medio, "MEDIO", 12),
                (" 3. NIVEL ESPECIALISTA (Dificil) ", misiones_dificil, "DIFÍCIL", 11),
                (" 4. MODO EXTREMO (Aleatorio + Bosses) ", None, "EXTREMO", 5), 
                (" [ VOLVER AL MENU DE MODOS ] ", None, "VOLVER", 2)
            ]
            
            sel_dif = 0
            while True:
                stdscr.clear()
                stdscr.addstr(2, (ancho//2)-15, "--- ACADEMIA KALI YARACUY ---", curses.A_BOLD)
                stdscr.addstr(4, (ancho//2)-22, f"MODO: {modo_elegido} - SELECCIONA DIFICULTAD", curses.color_pair(4))
                
                for i, (txt, _, _, col) in enumerate(niveles):
                    estilo_base = curses.color_pair(col)
                    estilo = estilo_base | curses.A_REVERSE if i == sel_dif else estilo_base
                    stdscr.addstr(6+i, (ancho//2)-18, txt.center(36), estilo)
                    
                k = stdscr.getch()
                if k == curses.KEY_UP and sel_dif > 0: sel_dif -= 1
                elif k == curses.KEY_DOWN and sel_dif < len(niveles)-1: sel_dif += 1
                elif k in [10, 13]: break
            
            clave = niveles[sel_dif][2]
            
            if clave == "VOLVER": 
                break # Rompe el bucle de dificultad y vuelve a preguntar por Clásico/Contrarreloj
            
            nombre_str = niveles[sel_dif][0].strip()
            lista_cmds = niveles[sel_dif][1]
            
            if clave == "EXTREMO":
                combinacion = misiones_facil + misiones_medio + misiones_dificil
                random.shuffle(combinacion)
                lista_cmds = combinacion + misiones_extremo_final
                nombre_str = "MODO EXTREMO"

            tiempo_limite_nivel = limites_tiempo[clave] if modo_elegido == "CONTRARRELOJ" else 0

            exito, duracion, errores = ejecutar_nivel(stdscr, lista_cmds, nombre_str, modo=modo_elegido, tiempo_limite=tiempo_limite_nivel)
            
            if exito:
                estadisticas[clave]['tiempo'] = duracion
                estadisticas[clave]['errores'] = errores
                estadisticas[clave]['rango'] = calcular_rango(errores)
                estadisticas[clave]['modo'] = modo_elegido
                
                opcs = [" PASAR A OTRO NIVEL ", " FINALIZAR Y GENERAR COMPROBANTE "]
                res = 0
                while True:
                    curses.curs_set(0)
                    stdscr.clear()
                    stdscr.addstr(alto//2-4, (ancho//2)-15, f"¡FASE {clave} COMPLETADA!", curses.color_pair(10) | curses.A_BOLD)
                    stdscr.addstr(alto//2-2, (ancho//2)-15, f"Rango Obtenido: {estadisticas[clave]['rango']}", curses.color_pair(12))
                    
                    for i, o in enumerate(opcs):
                        stdscr.addstr(alto//2+i, (ancho//2)-15, o, curses.A_REVERSE if i == res else curses.A_NORMAL)
                    k = stdscr.getch()
                    if k == curses.KEY_UP: res = 0
                    elif k == curses.KEY_DOWN: res = 1
                    elif k in [10, 13]: break
                
                if res == 1:
                    generar_comprobante(stdscr, estadisticas)
                    return # Cierra todo el sistema al generar el comprobante