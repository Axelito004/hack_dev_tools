import curses
import time
import os
import subprocess
import textwrap

# --- MOTOR DE VOZ IA (BLINDADO) ---
def hablar(texto, rate=280, esperar=False, matar_previo=False):
    try:
        if matar_previo:
            os.system("pkill -9 mpg123 >/dev/null 2>&1")
            os.system("pkill -f edge-tts >/dev/null 2>&1")

        texto_limpio = texto.replace('"', '').replace("'", "")
        
        if rate == 200: velocidad = "+15%"  
        elif rate == 240: velocidad = "+25%"  
        elif rate >= 280: velocidad = "+40%"  
        else: velocidad = "+15%"

        comando_bash = f'(edge-tts --voice es-MX-JorgeNeural --rate="{velocidad}" --text "{texto_limpio}" | mpg123 -q -) 2>/dev/null'
        
        if not esperar:
            comando_bash += ' &' 
            
        os.system(comando_bash)
    except:
        pass

def deletrear(cmd):
    res = []
    for char in cmd:
        if char == ' ': res.append('espacio')
        elif char == '-': res.append('guion')
        elif char == '/': res.append('barra')
        elif char == '.': res.append('punto')
        elif char == '*': res.append('asterisco')
        elif char == '_': res.append('guion bajo')
        elif char == '>': res.append('mayor que')
        elif char == '<': res.append('menor que')
        elif char == '|': res.append('tuberia')
        elif char == '\\': res.append('barra invertida')
        elif char == '"': res.append('comillas dobles')
        elif char.isalpha():
            if char.isupper(): res.append(f'letra {char.lower()} mayúscula')
            else: res.append(f'letra {char.lower()}')
        elif char.isdigit():
            res.append(f'número {char}')
        else: res.append(char)
    return " . ".join(res)

# --- UI TÁCTICA ---
def dibujar_marco_terminal(stdscr, mx, ancho, alto, titulo, salida_texto=""):
    """Dibuja un marco ASCII para mostrar resultados."""
    stdscr.addstr(3, mx, f"┌── {titulo} " + "─" * (ancho - mx*2 - len(titulo) - 5) + "┐", curses.color_pair(4))
    for i in range(4, 9):
        stdscr.addstr(i, mx, "│", curses.color_pair(4))
        stdscr.addstr(i, ancho - mx - 1, "│", curses.color_pair(4))
    stdscr.addstr(9, mx, "├" + "─" * (ancho - mx*2 - 2) + "┤", curses.color_pair(4))
    
    for i in range(10, alto-5):
        stdscr.addstr(i, mx, "│", curses.color_pair(4))
        stdscr.addstr(i, ancho - mx - 1, "│", curses.color_pair(4))
    stdscr.addstr(alto-5, mx, "└" + "─" * (ancho - mx*2 - 2) + "┘", curses.color_pair(4))
    
    if salida_texto:
        y_out = 10
        for linea in salida_texto.strip().split('\n')[:(alto-16)]: 
            try:
                linea_truncada = linea[:ancho-mx*2-4]
                stdscr.addstr(y_out, mx + 2, linea_truncada, curses.color_pair(2))
                y_out += 1
            except curses.error: pass

# --- FASE 0: TUTORIAL DE RECONOCIMIENTO (ip a) ---
def fase_reconocimiento_inicial(stdscr):
    alto, ancho = stdscr.getmaxyx()
    mx = int(ancho * 0.05)
    
    input_user = ""
    exito_ip = False
    salida_ip = ""

    hablar("Fase cero iniciada. Antes de atacar una red, debes conocer tu propia configuración. Ejecuta el comando I P A para descubrir tu interfaz y tu segmento de red.", rate=200, esperar=False, matar_previo=True)

    # 1. Obligar a ejecutar 'ip a'
    while not exito_ip:
        stdscr.clear()
        stdscr.addstr(1, mx, "FASE 0: RECONOCIMIENTO DE RED LOCAL", curses.color_pair(12) | curses.A_BOLD)
        dibujar_marco_terminal(stdscr, mx, ancho, alto, "SISTEMA NATIVO", salida_ip)
        
        stdscr.addstr(5, mx + 2, "OBJETIVO:", curses.color_pair(12) | curses.A_BOLD)
        stdscr.addstr(6, mx + 2, "Descubre tu IP, rango de red y nombre de tarjeta de red.", curses.color_pair(2))
        stdscr.addstr(7, mx + 2, "COMANDO :", curses.color_pair(12) | curses.A_BOLD)
        stdscr.addstr(8, mx + 2, "ip a", curses.color_pair(3) | curses.A_BOLD)

        stdscr.addstr(alto-3, mx, "root@auditor:~# " + input_user, curses.color_pair(3) | curses.A_BOLD)
        stdscr.refresh()

        k = stdscr.getch()
        if k in [10, 13]:
            if input_user.strip() == "ip a":
                try:
                    resultado = subprocess.run("ip a", shell=True, capture_output=True, text=True, timeout=5)
                    salida_ip = resultado.stdout
                except:
                    salida_ip = "[ERROR AL LEER INTERFACES]"
                
                # Mostrar resultado real
                stdscr.clear()
                stdscr.addstr(1, mx, "FASE 0: RECONOCIMIENTO DE RED LOCAL", curses.color_pair(12) | curses.A_BOLD)
                dibujar_marco_terminal(stdscr, mx, ancho, alto, "SISTEMA NATIVO (RESULTADO)", salida_ip)
                stdscr.addstr(alto-3, mx, ">>> ANALIZA LA SALIDA DE ARRIBA <<<", curses.color_pair(10) | curses.A_BLINK | curses.A_BOLD)
                stdscr.addstr(alto-2, mx, "[ PRESIONA ENTER CUANDO ESTÉS LISTO PARA CONFIGURAR EL RADAR ]", curses.color_pair(12))
                stdscr.refresh()
                
                hablar("Comando procesado. Analiza la salida. Busca tu interfaz activa, como eth0 o wlan0, y tu dirección I P.", rate=200, esperar=False, matar_previo=True)
                while stdscr.getch() not in [10, 13]: pass
                exito_ip = True
            else:
                input_user = ""
                hablar("Comando incorrecto. Escribe i p espacio a.", rate=280, esperar=False)
        elif k in [127, 8, curses.KEY_BACKSPACE]: input_user = input_user[:-1]
        elif 32 <= k <= 126: input_user += chr(k)

    # 2. Configurar Variables
    interfaz, ip_obj, red = "", "", ""
    curses.curs_set(1)
    
    hablar("Introduce los datos encontrados en el análisis anterior.", rate=200, esperar=False)
    
    # Pedir Interfaz
    while True:
        stdscr.clear()
        stdscr.addstr(alto//2 - 4, mx, "=== CONFIGURACIÓN DE PARÁMETROS TÁCTICOS ===", curses.color_pair(12) | curses.A_BOLD)
        stdscr.addstr(alto//2 - 2, mx, "1. Interfaz de Red (Ej. eth0, wlan0): > " + interfaz, curses.color_pair(2))
        stdscr.refresh()
        k = stdscr.getch()
        if k in [10, 13] and interfaz: break
        elif k in [127, 8, curses.KEY_BACKSPACE]: interfaz = interfaz[:-1]
        elif 32 <= k <= 126: interfaz += chr(k)

    # Pedir IP Objetivo
    while True:
        stdscr.clear()
        stdscr.addstr(alto//2 - 4, mx, "=== CONFIGURACIÓN DE PARÁMETROS TÁCTICOS ===", curses.color_pair(12) | curses.A_BOLD)
        stdscr.addstr(alto//2 - 2, mx, f"1. Interfaz de Red: {interfaz}", curses.color_pair(3))
        stdscr.addstr(alto//2, mx, "2. IP de un Equipo Objetivo (Ej. 192.168.1.1): > " + ip_obj, curses.color_pair(2))
        stdscr.refresh()
        k = stdscr.getch()
        if k in [10, 13] and ip_obj: break
        elif k in [127, 8, curses.KEY_BACKSPACE]: ip_obj = ip_obj[:-1]
        elif 32 <= k <= 126: ip_obj += chr(k)

    # Pedir Red
    while True:
        stdscr.clear()
        stdscr.addstr(alto//2 - 4, mx, "=== CONFIGURACIÓN DE PARÁMETROS TÁCTICOS ===", curses.color_pair(12) | curses.A_BOLD)
        stdscr.addstr(alto//2 - 2, mx, f"1. Interfaz de Red: {interfaz}", curses.color_pair(3))
        stdscr.addstr(alto//2, mx, f"2. IP de Equipo Objetivo: {ip_obj}", curses.color_pair(3))
        stdscr.addstr(alto//2 + 2, mx, "3. Rango de Red (Ej. 192.168.1.0/24): > " + red, curses.color_pair(2))
        stdscr.refresh()
        k = stdscr.getch()
        if k in [10, 13] and red: break
        elif k in [127, 8, curses.KEY_BACKSPACE]: red = red[:-1]
        elif 32 <= k <= 126: red += chr(k)

    return interfaz.strip(), ip_obj.strip(), red.strip()

# --- MOTOR DE EJECUCIÓN DEL MÓDULO ---
def ejecutar_modulo(stdscr, comandos, titulo):
    alto, ancho = stdscr.getmaxyx()
    mx = int(ancho * 0.05)

    for idx, m in enumerate(comandos):
        input_user = ""
        exito = False
        voz_lista = False
        salida_real = ""
        
        while not exito:
            stdscr.clear()
            curses.curs_set(0)
            
            stdscr.addstr(1, mx, f"MÓDULO: {titulo} | Comando: {idx+1}/{len(comandos)}", curses.color_pair(12) | curses.A_BOLD)
            
            dibujar_marco_terminal(stdscr, mx, ancho, alto, "TERMINAL ACTIVA", salida_real)
            
            stdscr.addstr(5, mx + 2, "OBJETIVO:", curses.color_pair(12) | curses.A_BOLD)
            stdscr.addstr(6, mx + 2, m['desc'], curses.color_pair(2))
            stdscr.addstr(7, mx + 2, "COMANDO :", curses.color_pair(12) | curses.A_BOLD)
            stdscr.addstr(8, mx + 2, m['cmd'], curses.color_pair(3) | curses.A_BOLD)

            stdscr.addstr(alto-3, mx, "root@auditor:~# ", curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(alto-1, mx, "[ F1: DELETREAR | ESC: VOLVER AL MENÚ ]", curses.color_pair(4) | curses.A_BOLD)

            if input_user:
                stdscr.addstr(alto-3, mx + 16, input_user, curses.color_pair(3) | curses.A_BOLD)

            if not voz_lista:
                hablar(f"Objetivo: {m['desc']}. Escribe: {m['cmd']}.", rate=200, esperar=False, matar_previo=True)
                voz_lista = True

            curses.curs_set(1)
            stdscr.refresh()
            k = stdscr.getch()

            if k in [10, 13]: 
                if input_user.strip() == m['cmd']:
                    curses.curs_set(0)
                    stdscr.addstr(alto-3, mx + 16, "[ EJECUTANDO... POR FAVOR ESPERA ]", curses.color_pair(12) | curses.A_BLINK)
                    stdscr.refresh()
                    
                    try:
                        # Timeout extendido a 60s para comandos pesados de nmap
                        resultado = subprocess.run(m['cmd'], shell=True, text=True, capture_output=True, timeout=60)
                        if resultado.stdout: salida_real = resultado.stdout
                        elif resultado.stderr: salida_real = f"[WARN] {resultado.stderr}"
                        else: salida_real = "[Comando ejecutado sin salida]"
                    except subprocess.TimeoutExpired:
                        salida_real = "[ERROR] Ejecución abortada. Tardó más de 60 segundos."
                    except Exception as e:
                        salida_real = f"Error fatal: {str(e)}"
                    
                    stdscr.clear()
                    stdscr.addstr(1, mx, f"MÓDULO: {titulo} | Comando: {idx+1}/{len(comandos)}", curses.color_pair(12) | curses.A_BOLD)
                    dibujar_marco_terminal(stdscr, mx, ancho, alto, "RESULTADOS DE AUDITORÍA", salida_real)
                    stdscr.addstr(alto-3, mx, f"root@auditor:~# {m['cmd']}", curses.color_pair(3))
                    stdscr.addstr(alto-1, mx, "[ PRESIONA ENTER PARA CONTINUAR AL SIGUIENTE COMANDO ]", curses.color_pair(10) | curses.A_BLINK)
                    stdscr.refresh()
                    
                    hablar("Procesado. Revisa la consola.", rate=240, esperar=False, matar_previo=True) 
                    while stdscr.getch() not in [10, 13]: pass
                    exito = True 
                else: 
                    input_user = ""
                    hablar("Error tipográfico.", rate=280, esperar=False, matar_previo=True)
            elif k in [127, 8, curses.KEY_BACKSPACE]: input_user = input_user[:-1]
            elif k == curses.KEY_F1: hablar(f"Deletreo: {deletrear(m['cmd'])}", rate=200, esperar=False, matar_previo=True)
            elif k == 27: return # ESC para salir al menú
            elif 32 <= k <= 126: input_user += chr(k)

# --- MENÚ PRINCIPAL ---
def iniciar(stdscr):
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Obligamos a pasar por la Fase 0
    interfaz, ip_obj, red = fase_reconocimiento_inicial(stdscr)

    # Base de Datos de Comandos Generada Dinámicamente
    # Base de Datos de Comandos Generada Dinámicamente (Versión Extendida)
    mods = {
        "1": {
            "nombre": "BASH (Herramientas Nativas de Red y SO)",
            "cmds": [
                {"cmd": "ip a", "desc": "Muestra las interfaces de red, direcciones IP y estados (UP/DOWN)."},
                {"cmd": "ip route", "desc": "Muestra la tabla de enrutamiento. Busca la linea 'default via' para hallar tu router."},
                {"cmd": "ip neigh", "desc": "Muestra la caché ARP local. Lista direcciones IP y sus direcciones MAC correspondientes."},
                {"cmd": f"ping -c 4 {ip_obj}", "desc": "Envía 4 paquetes ICMP Echo Request para comprobar si el objetivo responde."},
                {"cmd": f"traceroute {ip_obj}", "desc": "Mapea los saltos de enrutadores intermedios hasta llegar a la IP objetivo."},
                {"cmd": "ss -tuln", "desc": "Lista todos los puertos TCP y UDP que están a la escucha en tu propia máquina."},
                {"cmd": "netstat -rn", "desc": "Muestra la tabla de enrutamiento del kernel en formato numérico."},
                {"cmd": f"dig {ip_obj}", "desc": "Interroga servidores DNS para extraer información detallada de resolución de nombres."},
                {"cmd": f"whois {ip_obj}", "desc": "Consulta bases de datos públicas para ver a quién le pertenece una IP o dominio."},
                {"cmd": f"sudo macchanger -r {interfaz}", "desc": "Falsifica tu dirección MAC asignando una aleatoria para evadir filtros de red."}
            ]
        },
        "2": {
            "nombre": "NMAP MASTERCLASS (Escaneo y Evasión)",
            "cmds": [
                {"cmd": f"nmap {ip_obj}", "desc": "Escaneo estándar. Revisa el estado de los 1000 puertos más comunes del objetivo."},
                {"cmd": f"nmap -sn {red}", "desc": "Ping Sweep. Mapea qué IPs están vivas en toda la red sin escanear puertos."},
                {"cmd": f"nmap -Pn {ip_obj}", "desc": "Omitir Ping. Fuerza el escaneo asumiendo que el host está vivo (Bypassa firewalls de Windows)."},
                {"cmd": f"sudo nmap -sS {ip_obj}", "desc": "TCP SYN Scan (Escaneo Sigiloso). Rápido y deja menos rastros en los logs del servidor."},
                {"cmd": f"sudo nmap -sU {ip_obj}", "desc": "UDP Scan. Busca puertos UDP abiertos (como DNS 53, SNMP 161). Es lento pero letal."},
                {"cmd": f"nmap -p 21,22,80,443 {ip_obj}", "desc": "Escaneo por lista. Analiza únicamente los puertos FTP, SSH, HTTP y HTTPS."},
                {"cmd": f"nmap -p- {ip_obj}", "desc": "Escaneo absoluto. Revisa los 65535 puertos existentes. No deja nada a la imaginación."},
                {"cmd": f"nmap -sV {ip_obj}", "desc": "Version Detection. Interroga los servicios para saber su versión exacta (Ej. Apache 2.4.49)."},
                {"cmd": f"sudo nmap -O {ip_obj}", "desc": "OS Detection. Analiza la huella TCP/IP para adivinar el Sistema Operativo (Windows, Linux, etc)."},
                {"cmd": f"nmap -A {ip_obj}", "desc": "Aggressive Scan. Activa OS, Version, Scripts por defecto y traceroute a la vez."},
                {"cmd": f"nmap -T4 {ip_obj}", "desc": "Plantilla Agresiva (Timing). Acelera el escaneo reduciendo tiempos de espera de respuesta."},
                {"cmd": f"nmap -D RND:10 {ip_obj}", "desc": "Ataque Decoy. Oculta tu IP generando tráfico desde 10 IPs falsas hacia el objetivo."},
                {"cmd": f"nmap -f {ip_obj}", "desc": "Fragmentación. Divide los paquetes en partes diminutas para evadir firewalls e IDS."},
                {"cmd": f"nmap --script default,safe {ip_obj}", "desc": "Nmap Scripting Engine. Corre scripts seguros y por defecto para buscar fallas básicas."},
                {"cmd": f"nmap --script vuln {ip_obj}", "desc": "Auditoría de Vulnerabilidades. Usa la base de datos de Nmap para detectar exploits (CVEs)."},
                {"cmd": f"nmap -oN reporte_nmap.txt {ip_obj}", "desc": "Output Normal. Guarda todo el resultado del escaneo en un archivo de texto."},
                {"cmd": f"nmap -oX reporte_nmap.xml {ip_obj}", "desc": "Output XML. Guarda el reporte en XML, ideal para importar a Metasploit."}
            ]
        },
        "3": {
            "nombre": "ARP-SCAN (Mapeo de Capa 2 / LAN)",
            "cmds": [
                {"cmd": f"sudo arp-scan -I {interfaz} --localnet", "desc": "Fuerza un paquete ARP Request a toda la red local pidiendo a todos que se identifiquen."},
                {"cmd": f"sudo arp-scan -I {interfaz} {red}", "desc": "Escanea una subred específica que podría ser diferente a tu LAN actual."},
                {"cmd": f"sudo arp-scan --retry=5 -I {interfaz} --localnet", "desc": "Aumenta los reintentos a 5. Ideal para redes Wifi ruidosas donde se pierden paquetes."},
                {"cmd": f"sudo arp-scan --ignoredups -I {interfaz} --localnet", "desc": "Filtra la salida para ocultar respuestas duplicadas del mismo equipo."},
                {"cmd": f"sudo arp-scan --bandwidth=5000 -I {interfaz} --localnet", "desc": "Reduce el ancho de banda del escaneo para ser más sigiloso y no saturar switches."}
            ]
        },
        "4": {
            "nombre": "TCPDUMP (Análisis y Sniffing de Paquetes)",
            "cmds": [
                {"cmd": f"sudo tcpdump -i {interfaz} -c 10", "desc": "Pone la tarjeta en modo promiscuo y captura los próximos 10 paquetes."},
                {"cmd": f"sudo tcpdump -i {interfaz} -n -c 20", "desc": "Desactiva la resolución de nombres DNS. Acelera la captura mostrando solo IPs numéricas."},
                {"cmd": f"sudo tcpdump -i {interfaz} host {ip_obj} -c 15", "desc": "Escucha únicamente el tráfico que entra o sale de la IP del objetivo."},
                {"cmd": f"sudo tcpdump -i {interfaz} port 80 or port 443", "desc": "Captura tráfico Web (HTTP y HTTPS) de forma exclusiva."},
                {"cmd": f"sudo tcpdump -i {interfaz} icmp", "desc": "Captura exclusivamente pings y mensajes de control ICMP en la red."},
                {"cmd": f"sudo tcpdump -i {interfaz} -w captura_red.pcap", "desc": "Modo silencioso: Graba todo el tráfico capturado en un archivo para analizar en Wireshark."},
                {"cmd": f"sudo tcpdump -r captura_red.pcap", "desc": "Modo forense: Lee e imprime el tráfico guardado previamente en un archivo .pcap."},
                {"cmd": f"sudo tcpdump -i {interfaz} -A -c 5", "desc": "Modo ASCII. Intenta leer e imprimir el texto plano dentro de los paquetes (robos de credenciales)."},
                {"cmd": f"sudo tcpdump -i {interfaz} -XX -c 3", "desc": "Hexdump. Muestra los cabezales y la carga útil en formato Hexadecimal profundo."}
            ]
        }
    }

    # Bucle del Menú Principal
    while True:
        curses.curs_set(0)
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()
        mx = ancho // 2

        stdscr.addstr(2, mx - 20, "=== KALI ACADEMY: MÓDULO REDES ===", curses.color_pair(10) | curses.A_BOLD)
        stdscr.addstr(4, mx - 20, f"Interfaz: {interfaz} | Red: {red}", curses.color_pair(3))
        
        stdscr.addstr(6, mx - 20, "[1] NATIVO: Bash Network Tools", curses.color_pair(2))
        stdscr.addstr(7, mx - 20, "[2] NMAP  : Masterclass Completa (12 Comandos)", curses.color_pair(2))
        stdscr.addstr(8, mx - 20, "[3] ARP   : arp-scan (Descubrimiento físico)", curses.color_pair(2))
        stdscr.addstr(9, mx - 20, "[4] PCAP  : tcpdump (Sniffer de red)", curses.color_pair(2))
        stdscr.addstr(11, mx - 20, "[5] SALIR DE LA ACADEMIA DE REDES", curses.color_pair(11) | curses.A_BOLD)
        
        stdscr.addstr(13, mx - 20, "Selecciona un módulo (1-5): ", curses.color_pair(12))
        stdscr.refresh()

        k = stdscr.getch()
        opcion = chr(k) if 32 <= k <= 126 else ""

        if opcion in mods:
            ejecutar_modulo(stdscr, mods[opcion]["cmds"], mods[opcion]["nombre"])
        elif opcion == "5":
            break

if __name__ == "__main__":
    curses.wrapper(iniciar)