import curses
import time
import os
import textwrap
import random

# --- MOTOR DE VOZ ---
def hablar(texto, rate=280):
    try:
        texto_limpio = texto.replace('"', '').replace("'", "")
        os.system(f'espeak-ng -s {rate} -v es "{texto_limpio}" 2>/dev/null &')
    except:
        pass

def format_time(segundos):
    return f"{int(segundos // 60):02d}:{int(segundos % 60):02d}"

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

# --- BASE DE DATOS EXTENDIDA (Basada en Ing. Román) ---
misiones_ducky = [
    {
        "cmd": "sudo apt install default-jre -y",
        "desc": "Instala el entorno Java necesario para codificar el ataque.",
        "out": "[+] Java Runtime Environment (JRE) configurado."
    },
    {
        "cmd": "wget https://github.com/libreria_usb",
        "desc": "Descarga el motor de compilación para los scripts de inyección.",
        "out": "[+] Descarga finalizada: ducky-encoder.jar"
    },
    {
        "cmd": "echo 'GUI r' > script.txt",
        "desc": "Inicia el Ducky Script. Este comando abre la ventana de Ejecutar en Windows.",
        "out": "[+] Archivo script.txt creado con comando GUI r"
    },
    {
        "cmd": "echo 'STRING cmd /c \"echo TREE C:\\ > exploit.bat && start exploit.bat\"' >> script.txt",
        "desc": "Inyecta una cadena que crea un archivo .bat en la víctima y lo ejecuta de inmediato.",
        "out": "[+] Payload de persistencia .bat añadido al script."
    },
    {
        "cmd": "java -jar ducky-encoder.jar -i script.txt -o inject.bin",
        "desc": "Transforma el código malicioso en el binario inject.bin listo para el hardware.",
        "out": "Encoding... OK!\n[+] Archivo binario generado."
    }
]

def simulacion_ataque(stdscr):
    alto, ancho = stdscr.getmaxyx()
    curses.init_pair(20, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(21, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    
    # 1. EFECTO GLITCH / LLUVIA DE CARACTERES (Simulando la inyección rápida)
    hablar("Inyectando carga útil. Ejecutando script automatizado.")
    start_sim = time.time()
    while time.time() - start_sim < 3: # 3 segundos de locura
        stdscr.clear()
        for _ in range(100):
            y, x = random.randint(0, alto-1), random.randint(0, ancho-1)
            char = random.choice("!@#$%^&*()_+{}:<>?abcdef0123456789")
            color = random.choice([curses.color_pair(10), curses.color_pair(20), curses.color_pair(2)])
            try:
                stdscr.addch(y, x, char, color)
            except: pass
        stdscr.refresh()
        time.sleep(0.05)

    # 2. MENSAJE CRÍTICO
    stdscr.clear()
    msg_vuln = "¡ERES VULNERABLE!"
    stdscr.addstr(alto//2 - 2, (ancho//2) - (len(msg_vuln)//2), msg_vuln, curses.color_pair(20) | curses.A_BOLD | curses.A_BLINK)
    stdscr.refresh()
    hablar("Sistema comprometido. Eres vulnerable.")
    time.sleep(2)

    # 3. DISCLAIMER Y ADVERTENCIA
    stdscr.clear()
    disclaimer = (
        "AVISO DE SEGURIDAD:\n\n"
        "El uso de herramientas HID como USB Rubber Ducky puede comprometer "
        "un sistema en cuestion de segundos sin dejar rastro. Como estudiantes "
        "de CiberSeguridad, tienen la responsabilidad ética de usar este "
        "conocimiento solo para la defensa y auditoría autorizada."
    )
    y_disc = draw_text_wrapped(stdscr, alto//3, ancho//2 - 25, disclaimer, 50, curses.color_pair(2))
    
    # ADVERTENCIA EN AMARILLO Y MAYÚSCULAS
    adv = "ÚSALA BAJO TUS PROPIAS CONSECUENCIAS"
    stdscr.addstr(y_disc + 2, (ancho//2) - (len(adv)//2), adv, curses.color_pair(21) | curses.A_BOLD)
    
    stdscr.addstr(alto-4, (ancho//2) - 10, "[ ENTER PARA CONTINUAR ]", curses.A_BLINK)
    stdscr.refresh()
    
    while True:
        k = stdscr.getch()
        if k in [10, 13]: break

def ejecutar_modulo(stdscr, comandos, titulo):
    start_time = time.time()
    for idx, m in enumerate(comandos):
        input_user = ""
        exito = False
        voz_lista = False
        
        while not exito:
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            mx = int(ancho * 0.1)
            t_act = time.time() - start_time

            stdscr.addstr(2, mx, f"MODULO 2: {titulo} | {idx+1}/{len(comandos)}", curses.color_pair(10) | curses.A_BOLD)
            stdscr.addstr(2, ancho - mx - 15, f"T: {format_time(t_act)}", curses.color_pair(10))
            
            stdscr.addstr(4, mx, "COMANDO OBJETIVO:", curses.A_BOLD)
            stdscr.addstr(5, mx, m['cmd'], curses.color_pair(4) | curses.A_BOLD)
            
            y_act = draw_text_wrapped(stdscr, 7, mx, f"ANÁLISIS: {m['desc']}", ancho-mx*2, curses.color_pair(2))
            
            y_act += 2
            stdscr.addstr(y_act, mx, "--- OUTPUT ESPERADO EN KALI ---", curses.A_DIM)
            stdscr.addstr(y_act+1, mx, f"root@kali:~# {m['cmd']}", curses.color_pair(2))
            draw_text_wrapped(stdscr, y_act+2, mx, m['out'], ancho-mx*2, curses.color_pair(3))

            stdscr.addstr(alto-4, mx, "HID-ACADEMY# ", curses.A_BOLD)
            
            # Dibujar input
            for i, c in enumerate(input_user):
                stdscr.addstr(alto-4, mx + 13 + i, c, curses.color_pair(3) | curses.A_BOLD)

            stdscr.refresh()

            if not voz_lista:
                hablar(f"Instrucción: {m['desc']}")
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
                # ERROR CRÍTICO: BORRADO TOTAL
                pos = len(input_user)
                if pos < len(m['cmd']) and char == m['cmd'][pos]:
                    input_user += char
                else:
                    input_user = "" 
                    hablar("Error", rate=500)
            elif k == 27: return False, 0
            
    return True, time.time() - start_time

def iniciar(stdscr):
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    exito, duracion = ejecutar_modulo(stdscr, misiones_ducky, "ATAQUE HID - RUBBER DUCKY")
    
    if exito:
        simulacion_ataque(stdscr)