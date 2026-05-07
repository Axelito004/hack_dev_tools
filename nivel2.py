import curses
import time
import os
import textwrap
import random
import hashlib


# --- MOTOR DE VOZ IA (EDGE-TTS - LOQUENDO) BLINDADO ---
def hablar(texto, rate=280, esperar=False, matar_previo=False):
    try:
        # TUMBA AL REPRODUCTOR Y A LA IA (Evita el Broken Pipe)
        if matar_previo:
            os.system("pkill -9 mpg123 >/dev/null 2>&1")
            os.system("pkill -f edge-tts >/dev/null 2>&1")

        texto_limpio = texto.replace('"', '').replace("'", "")
        
        # Traductor de velocidad: Convertimos la velocidad vieja al formato de Edge-TTS
        if rate == 200:
            velocidad = "+15%"  
        elif rate == 240:
            velocidad = "+25%"  
        elif rate >= 280:
            velocidad = "+120%"  
        else:
            velocidad = "+15%"

        # Envolvemos todo el comando en () y redirigimos el stderr al abismo
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
        elif char == ':': res.append('dos puntos')
        elif char == ';': res.append('punto y coma')
        elif char == '>': res.append('mayor que')
        elif char == '<': res.append('menor que')
        elif char == '&': res.append('ampersand')
        elif char == '|': res.append('tuberia')
        elif char == '\\': res.append('barra invertida')
        elif char == "'": res.append('comilla simple')
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

def alerta_bloq_mayus(stdscr):
    alto, ancho = stdscr.getmaxyx()
    curses.curs_set(0)
    stdscr.clear()
    msg1 = "¡ ALERTA DE SINTAXIS !"
    msg2 = "SE HA DETECTADO UNA MAYÚSCULA INCORRECTA."
    msg3 = "ES PROBABLE QUE TENGAS EL [BLOQ MAYÚS] ACTIVADO."
    stdscr.addstr(alto//2 - 3, ancho//2 - len(msg1)//2, msg1, curses.color_pair(11) | curses.A_BLINK | curses.A_BOLD)
    stdscr.addstr(alto//2 - 1, ancho//2 - len(msg2)//2, msg2, curses.color_pair(12))
    stdscr.addstr(alto//2, ancho//2 - len(msg3)//2, msg3, curses.color_pair(12) | curses.A_BOLD)
    stdscr.refresh()
    hablar("Alerta. Bloqueo de mayúsculas detectado.", esperar=True, matar_previo=True)
    curses.flushinp()
    stdscr.getch()

# --- ANIMACIONES ---
def animacion_fallo(stdscr):
    curses.curs_set(0)
    alto, ancho = stdscr.getmaxyx()
    hablar("Misión fallida. Límite de errores excedido. Bloqueo del sistema iniciado.", rate=200, esperar=False, matar_previo=True)
    for _ in range(8):
        stdscr.bkgd(' ', curses.color_pair(11))
        stdscr.clear()
        stdscr.addstr(alto//2, ancho//2 - 20, "!!! SISTEMA BLOQUEADO - OPERACIÓN ABORTADA !!!", curses.color_pair(5) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.3)
        stdscr.bkgd(' ', curses.color_pair(2))
        stdscr.clear()
        stdscr.refresh()
        time.sleep(0.3)

def animacion_extraccion(stdscr):
    curses.curs_set(0)
    alto, ancho = stdscr.getmaxyx()
    stdscr.clear()
    archivos = ["passwords.txt", "syslog.bak", "SAM_database", "config.json", "browser_history.db", "id_rsa", "shadow"]
    hablar("Inyección exitosa. Extrayendo datos del objetivo.", rate=200, esperar=False, matar_previo=True)
    for i in range(101):
        stdscr.clear()
        stdscr.addstr(alto//2 - 2, ancho//2 - 14, "--- EXTRACCIÓN EN PROGRESO ---", curses.color_pair(12) | curses.A_BOLD)
        barra = "█" * (i // 4) + "-" * (25 - (i // 4))
        stdscr.addstr(alto//2, ancho//2 - 18, f"Progreso: [{barra}] {i}%", curses.color_pair(3))
        if i % 4 == 0:
            stdscr.addstr(alto//2 + 2, ancho//2 - 15, f"Descargando: {random.choice(archivos)}", curses.color_pair(10))
        stdscr.refresh()
        time.sleep(0.04)

def animacion_matrix(stdscr):
    curses.curs_set(0)
    alto, ancho = stdscr.getmaxyx()
    chars = "01@#$%&*KALI-LINUX"
    start_t = time.time()
    hablar("Borrando huellas. Encriptación finalizada.", rate=200, esperar=False)
    stdscr.clear()
    while time.time() - start_t < 4.0:
        for _ in range(40):
            y = random.randint(0, alto-2)
            x = random.randint(0, ancho-2)
            stdscr.addstr(y, x, random.choice(chars), curses.color_pair(3))
        stdscr.refresh()
        time.sleep(0.05)

# --- COMANDOS DEL NIVEL ---
comandos_ducky = [
    {"cmd": "lsusb", "desc": "Lista dispositivos USB para detectar el Arduino Uno original.", "out": "Bus 001 Device 004: ID 2341:0043 Arduino SA Uno"},
    {"cmd": "dmesg | tail", "desc": "Revisa los registros del kernel para confirmar la asignacion del puerto.", "out": "[ 124.56] usb 1-1: New USB device found... ttyACM0"},
    {"cmd": "apt install dfu-programmer", "desc": "Instala la herramienta tactica para flashear el chip de Atmel.", "out": "[Ok] dfu-programmer instalado correctamente."},
    {"cmd": "mkdir operacion_ducky", "desc": "Crea un directorio seguro para los archivos de la operacion.", "out": "[Directorio creado con exito]"},
    {"cmd": "cd operacion_ducky", "desc": "Ingresa al area de trabajo del proyecto.", "out": "root@kali:~/operacion_ducky#"},
    {"cmd": "wget http://server.local/Arduino-keyboard.hex", "desc": "Descarga el firmware HID modificado para el Arduino.", "out": "200 OK - Arduino-keyboard.hex guardado"},
    {"cmd": "nano payload.txt", "desc": "Abre el editor de texto para escribir el DuckyScript.", "out": "[Editor GNU Nano abierto]"},
    {"cmd": "cat payload.txt", "desc": "Audita el contenido del payload antes de compilarlo.", "out": "DELAY 1000\nSTRING Hola Academia Kali!\nENTER"},
    {"cmd": "java -jar duckencode.jar -i payload.txt -o inject.bin", "desc": "Compila el texto plano a un archivo binario inyectable.", "out": "DuckyScript to bin conversion... DONE"},
    {"cmd": "ls -la", "desc": "Verifica que el archivo binario se genero correctamente.", "out": "-rw-r--r-- 1 root root  145 Apr 15 inject.bin"},
    {"cmd": "echo \"Modo DFU Activado\"", "desc": "Simula el puenteo manual de pines en el Arduino.", "out": "Modo DFU Activado por el Operador"},
    {"cmd": "lsusb", "desc": "Verifica que el chip entro en modo de flasheo profundo.", "out": "Bus 001 Device 005: ID 03eb:2fef Atmel Corp. atmega16u2 DFU"},
    {"cmd": "dfu-programmer atmega16u2 erase", "desc": "Borra el firmware de comunicacion serial original de fabrica.", "out": "Erasing flash...  Success"},
    {"cmd": "dfu-programmer atmega16u2 flash Arduino-keyboard.hex", "desc": "Flashea el firmware que camuflara la placa como un teclado.", "out": "Flashing...  Success"},
    {"cmd": "dfu-programmer atmega16u2 reset", "desc": "Reinicia el microcontrolador para armar el inyector.", "out": "Resetting USB to switch operation mode..."}
]

# --- FLUJO PRINCIPAL DEL NIVEL 2 ---
def iniciar(stdscr):
    # Colores
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    alto, ancho = stdscr.getmaxyx()
    mx = int(ancho * 0.1)

    # 1. DISCLAIMER
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(2, mx, "=== NIVEL 2: ADVERTENCIA LEGAL Y ÉTICA ===", curses.color_pair(11) | curses.A_BOLD)
    texto_disc = "Esta simulación es una herramienta de carácter estrictamente educativo. Las técnicas para convertir un Arduino Uno en un Rubber Ducky permiten ejecutar código arbitrario como si fuera un teclado humano. El usuario es capaz de usarlo para lo que le convenga, siempre y cuando lo haga bajo sus propias consecuencias."
    draw_text_wrapped(stdscr, 4, mx, texto_disc, ancho - mx*2, curses.color_pair(2))
    stdscr.refresh()
    
    # Bloqueamos Python hasta que la IA termine de hablar, luego limpiamos el buffer
    hablar("Advertencia legal y ética. Esta simulación es de carácter estrictamente educativo. El usuario es capaz de usarlo para lo que le convenga, siempre y cuando lo haga bajo sus propias consecuencias.", rate=200, esperar=True, matar_previo=True)
    curses.flushinp() 
    
    stdscr.addstr(alto-4, mx, "[ PRESIONA ENTER PARA CONTINUAR ]", curses.color_pair(10) | curses.A_BLINK)
    stdscr.refresh()
    while stdscr.getch() not in [10, 13]: pass

    # 2. LISTA DE COMPRA
    stdscr.clear()
    stdscr.addstr(2, mx, "=== LISTA DE LA COMPRA ===", curses.color_pair(12) | curses.A_BOLD)
    ascii_arduino = """
    ┌──────────────────────────────────────────────────────────┐        SCL SDA AREF GND 13 12 ~11~10 ~9  8    7 ~6 ~5  4 ~3  2  1>  0<
    │  ● ● ● ●     ╔══════════════╗  ╔══════════════════════╗  │         [ ] [ ] [ ]  [ ] [ ][ ] [ ][ ][ ][ ]  [ ][ ][ ][ ][ ][ ] [ ] [ ]
    │ DIGITAL      ║  ATMEGA16U2  ║  ║    ATMEGA328P-PU     ║  │       +-----------------------------------------------------------------+
    │              ║  ████████    ║  ║  ● ○ ○ ○ ○ ●  ○ ●    ║  │  +----+                                     RST SCK MISO  [ ][ ][ ]     |
    │  ● ● ● ●     ╚══════════════╝  ╚══════════════════════╝  │  |USB |    [ ][ ] GND/RST2                  GND MOSI 5V   [ ][ ][ ]     |
    │                                                          │  +----+    [ ][ ] MOSI2/SCK2                                            |
    │  ● ● ● ● ●   [RESET]    ●PWR ●TX ●RX ●L                  │  |         [ ][ ] 5V/MISO2       +---------------+                      |
    │ ANALOG IN    ┌──┐    ╔════╗ ┌──────────┐                 │  |                               | A R D U I N O |                      |
    │              │○││    ║USB ║ │  POWER   │                 │  +----+                          +---------------+                      |
    │  ●VIN ●GND ●GND ●5V ●3.3V ●AREF    │CONN│                │  |PWR |                                                       UNO_R3     \\
    └──────────────────────────────────────────────────────────┘  +----+                                                                   \\
        MADE IN ITALY  arduino.cc  Open Source Hardware                |                                                                   |
                                                                        | [ ]  [ ]  [ ]  [ ] [ ] [ ] [ ] [ ]    [ ] [ ] [ ] [ ] [ ] [ ]     |
                                                                        | N/C IOREF RST  3V3 5V  GND GND Vin    A0  A1  A2  A3  A4  A5      |
                                                                        +-------------------------------------------------------------------+
"""

    # --- CONTROL DE RENDERIZADO DEL PLANO ASCII ---
    # Verificamos si la terminal es lo suficientemente ancha (144 chars + márgenes)
    if ancho < 160:
        alerta_ancho = "⚠️ ADVERTENCIA: TERMINAL MUY ESTRECHA ⚠️\n\nEl plano de ingeniería es demasiado grande. Por favor, MAXIMIZA la ventana de tu terminal en Kali Linux para poder visualizar la arquitectura del Arduino correctamente."
        draw_text_wrapped(stdscr, 6, mx, alerta_ancho, ancho - mx*2, curses.color_pair(11) | curses.A_BLINK | curses.A_BOLD)
    else:
        # Dibujamos el ASCII línea por línea SIN usar textwrap para no deformarlo
        y_dibujo = 4
        for linea in ascii_arduino.strip("\n").split("\n"):
            try:
                stdscr.addstr(y_dibujo, max(0, ancho//2 - 72), linea, curses.color_pair(4))
                y_dibujo += 1
            except curses.error:
                pass
            
    stdscr.refresh()
    
    hablar("Lista de la compra. Para la vida real necesitarás una placa Arduino Uno estándar y un cable USB.", rate=200, esperar=True, matar_previo=True)
    curses.flushinp()
    
    stdscr.addstr(alto-4, mx, "[ PRESIONA ENTER PARA CONTINUAR ]", curses.color_pair(10) | curses.A_BLINK)
    stdscr.refresh()
    while stdscr.getch() not in [10, 13]: pass

    # 3. TUTORIAL DUCKYSCRIPT
    instrucciones = [
        ("Presiona tecla Windows más R para abrir Ejecutar:", "GUI r"),
        ("Para redactar texto como un fantasma, escribe:", "STRING Cadena de texto"),
        ("Para confirmar la ejecución, teclea:", "ENTER")
    ]
    
    for msg, cmd in instrucciones:
        input_user = ""
        exito_tut = False
        stdscr.clear()
        stdscr.addstr(2, mx, "=== ENTRENAMIENTO DE PAYLOAD (DUCKYSCRIPT) ===", curses.color_pair(12) | curses.A_BOLD)
        stdscr.addstr(4, mx, msg, curses.color_pair(2))
        stdscr.addstr(6, mx, f"Comando requerido: {cmd}", curses.color_pair(4) | curses.A_BOLD)
        stdscr.refresh()
        
        hablar(msg + f" Escribe, {deletrear(cmd)}", rate=200, esperar=True, matar_previo=True)
        curses.flushinp() # Evita que el usuario escriba mientras la IA habla
        curses.curs_set(1)
        
        while not exito_tut:
            stdscr.move(8, mx)
            stdscr.clrtoeol()
            stdscr.addstr(8, mx, "> " + input_user, curses.color_pair(3))
            stdscr.refresh()
            
            k = stdscr.getch()
            if k in [10, 13]:
                if input_user.strip() == cmd:
                    exito_tut = True
                    curses.curs_set(0)
                    hablar("Correcto", rate=240, esperar=True, matar_previo=True)
                    curses.flushinp()
                else:
                    input_user = ""
            elif k in [127, 8, curses.KEY_BACKSPACE]:
                input_user = input_user[:-1]
            elif 32 <= k <= 126:
                char = chr(k)
                if len(input_user) < len(cmd) and char == cmd[len(input_user)]:
                    input_user += char
                else:
                    input_user = ""
                    hablar("Error", rate=280, esperar=False, matar_previo=True)

    # 4. MISIÓN PRINCIPAL - MUERTE SÚBITA
    errores_restantes = 10
    
    for idx, m in enumerate(comandos_ducky):
        input_user = ""
        exito = False
        
        while not exito:
            stdscr.clear()
            
            # Condición de Derrota
            if errores_restantes <= 0:
                animacion_fallo(stdscr)
                return # Devuelve al index
            
            color_reloj = curses.color_pair(11) | curses.A_BLINK if errores_restantes <= 3 else curses.color_pair(11)
            stdscr.addstr(2, mx, f"FASE: {idx+1}/{len(comandos_ducky)} | OPERACIÓN RUBBER DUCKY", curses.color_pair(12) | curses.A_BOLD)
            stdscr.addstr(2, ancho - mx - 25, f"VIDAS: {errores_restantes}/10", color_reloj)
            
            stdscr.addstr(4, mx, "COMANDO:", curses.A_BOLD)
            stdscr.addstr(5, mx, m['cmd'], curses.color_pair(4) | curses.A_BOLD)
            draw_text_wrapped(stdscr, 7, mx, f"INFO: {m['desc']}\n\n--- SALIDA ESPERADA ---\nroot@kali:~# {m['cmd']}\n{m['out']}", ancho-mx*2, curses.color_pair(2))
            stdscr.addstr(alto-4, mx, "KALI-ACADEMY# ", curses.A_BOLD)
            stdscr.refresh()

            # Reproduce audio y bloquea teclado
            curses.curs_set(0)
            texto_unido = f"Comando: {m['cmd']}. Explicación: {m['desc']}."
            hablar(texto_unido, rate=200, esperar=True, matar_previo=True)
            curses.flushinp() # Borramos el buffer de teclado por si tecleó mientras hablaba
            curses.curs_set(1)

            # Bucle interno de escritura
            while True:
                stdscr.move(alto-4, mx + 14)
                stdscr.clrtoeol()
                stdscr.addstr(alto-4, mx + 14, input_user, curses.color_pair(3) | curses.A_BOLD)
                stdscr.refresh()

                k = stdscr.getch()

                if k in [10, 13]: 
                    if input_user.strip() == m['cmd']:
                        exito = True
                        curses.curs_set(0)
                        hablar("Correcto", rate=240, esperar=True, matar_previo=True) 
                        curses.flushinp()
                        break # Pasa al siguiente comando
                    else: input_user = ""
                elif k in [127, 8, curses.KEY_BACKSPACE]:
                    input_user = input_user[:-1]
                elif k == curses.KEY_F1:
                    hablar(f"Repito deletreo: {deletrear(m['cmd'])}.", rate=200, esperar=False, matar_previo=True)
                elif 32 <= k <= 126:
                    char = chr(k)
                    pos_actual = len(input_user)
                    
                    if pos_actual < len(m['cmd']) and char == m['cmd'][pos_actual]:
                        input_user += char
                    else:
                        if char.isalpha() and char.isupper() and pos_actual < len(m['cmd']) and m['cmd'][pos_actual].islower():
                            alerta_bloq_mayus(stdscr)
                        
                        input_user = "" 
                        errores_restantes -= 1
                        
                        if errores_restantes > 0:
                            hablar(f"Error. Te quedan {errores_restantes} vidas", rate=280, esperar=False, matar_previo=True) 
                        break # Rompe el bucle de escritura para actualizar la UI y redibujar

                elif k == 27: # ESC para salir
                    return

    # 5. ANIMACIONES DE VICTORIA
    animacion_extraccion(stdscr)
    animacion_matrix(stdscr)

    # 6. PANTALLA FINAL DE INTELIGENCIA TÁCTICA
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(2, mx, "=== REPORTE TÁCTICO FINAL ===", curses.color_pair(10) | curses.A_BOLD)
    pros_cons = """
    VENTAJAS DEL MÉTODO ARDUINO:
    [+] Costo: Extremadamente barato comparado con pendrives inyectores comerciales.
    [+] Sigilo Digital: Es detectado a bajo nivel como un Teclado (Bypassa Antivirus).
    [+] Personalizable: Código abierto y librerías accesibles.
    
    DESVENTAJAS:
    [-] Aspecto Físico: Es una placa expuesta y un cable, altamente sospechoso en la vida real.
    [-] Preparación: Requiere puentear pines manualmente para entrar en modo DFU.
    [-] Capacidad: Memoria muy limitada para scripts complejos.
    """
    draw_text_wrapped(stdscr, 4, mx, pros_cons, ancho - mx*2, curses.color_pair(2))
    stdscr.refresh()
    
    hablar("Misión completada. Análisis táctico. Ventajas: Costo muy bajo, alta disponibilidad y evita las defensas antivirus. Desventajas: Aspecto físico altamente sospechoso y requiere flasheo manual del chip.", rate=200, esperar=True, matar_previo=True)
    curses.flushinp()
    
    stdscr.addstr(alto-4, mx, "[ MISIÓN FINALIZADA. PRESIONA ENTER PARA VOLVER AL MENÚ ]", curses.color_pair(10) | curses.A_BLINK)
    stdscr.refresh()
    while stdscr.getch() not in [10, 13]: pass
    return