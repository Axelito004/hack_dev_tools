import curses
import time
import locale
import random
import pyttsx3
import nivel1
import nivel2 
import nivel3 
import os

# Configurar soporte para caracteres especiales (UTF-8)
locale.setlocale(locale.LC_ALL, '')

def hablar(texto, rate=200):
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
    """Dibuja texto solo si está dentro de los límites de la pantalla"""
    try:
        alto, ancho = stdscr.getmaxyx()
        if 0 <= y < alto and 0 <= x < ancho:
            espacio_disponible = ancho - x
            stdscr.addstr(y, x, texto[:espacio_disponible], estilo)
    except:
        pass

def draw_shell(stdscr):
    # --- 1. BIENVENIDA AUDITIVA ---
    stdscr.clear()
    msg_pantalla = ">> ESTABLECIENDO CONEXION SEGURA CON EL NODO CENTRAL..."
    msg_voz = "Conexión establecida. Bienvenido, Aspirante. Sistema de hackeo Fundasite Yaracuy en línea."
    
    alto, ancho = stdscr.getmaxyx()
    
    # Centrado absoluto del mensaje de carga
    x_boot = max(0, (ancho // 2) - (len(msg_pantalla) // 2))
    y_boot = max(0, alto // 2)
    
    try:
        stdscr.addstr(y_boot, x_boot, msg_pantalla, curses.A_BOLD | curses.A_BLINK)
        stdscr.refresh()
    except:
        pass

    hablar(msg_voz)

    # --- 2. CONFIGURACIÓN DE CURSES ---
    curses.curs_set(0)
    stdscr.nodelay(False)
    # ACTIVAMOS EL TIMEOUT PARA LA ANIMACIÓN (150ms)
    stdscr.timeout(150)
    curses.start_color()
    stdscr.keypad(True)

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)  
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK) # COLOR GLITCH

    # --- 3. BANNER ---
    letras = {
        'F': ["███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "██║     ", "╚═╝     "],
        'U': ["██╗   ██╗", "██║   ██║", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
        'N': ["███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"],
        'D': ["██████╗ ", "██╔══██╗", "██║  ██║", "██║  ██║", "██████╔╝", "╚═════╝ "],
        'A': ["  █████╗  ", " ██╔══██╗ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
        'C': [" ██████╗ ", "██╔════╝ ", "██║      ", "██║      ", "╚██████╗ ", " ╚═════╝ "],
        'I': ["█?█", "▒█▒", "▓█▓", "░█░", "█#█", "╚?╝"],
        'T': ["█▓▒░▓█░█", "╚═?██╔═?", "  ▒██║  ", "  ▓██║  ", "  ░██║  ", "  ╚?╝   "],
        'E': ["█?█?█?█╗", "██╔═░══╝", "█▒███╗  ", "██╔?═╝  ", "███?███╗", "╚═░════╝"]
    }

    palabra = "FUNDACITE"
    header_inst = "--- FUNDACITE && MINCYT YARACUY ---"
    subtitle = "Pasos basicos en Terminal & Herremientas Forenses"
    # ACTUALIZACIÓN DE IDENTIDAD SEGÚN TU PREFERENCIA PROFESIONAL
    authors = "Desarrollado por: Angel Gustavo Castillo Giménez && Ing. Josue Ordoñez"
    
    opciones = [
        " 1. Fundamentos de Bash y Supervivencia ",
        " 2. Preservación y Adquisición de Evidencia ",
        " 3. Recuperación de Datos y Análisis ",
        " 4. Análisis Forense de Memoria RAM ",
        " 5. Forense de Redes y Tráfico ",
        " [ SALIR DEL SISTEMA ] "
    ]

    ANCHO_SELECTOR = 60
    fila_seleccionada = 0

    # --- 4. BUCLE PRINCIPAL ---
    while True:
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()

        bloque_alto = 18
        start_y = max(0, (alto // 2) - (bloque_alto // 2))

        ancho_total_banner = sum(len(letras[l][0]) for l in palabra) + (len(palabra) - 1)
        banner_x = max(0, (ancho // 2) - (ancho_total_banner // 2))

        try:
            # Header
            hx = max(0, (ancho // 2) - (len(header_inst) // 2))
            stdscr.addstr(start_y, hx, header_inst, curses.color_pair(2) | curses.A_DIM)

            # Banner Principal
            x_cursor = banner_x
            y_banner = start_y + 2
            for caracter in palabra:
                for i in range(6):
                    if y_banner + i < alto:
                        contenido = letras[caracter][i]
                        if caracter in "ITE" and random.random() > 0.9:
                            lista_char = list(contenido)
                            for idx, c in enumerate(lista_char):
                                if c not in " ╚═╗║": 
                                    lista_char[idx] = random.choice(["?", "!", "1", "0"])
                            contenido = "".join(lista_char)
                        stdscr.addstr(y_banner + i, x_cursor, contenido, curses.color_pair(1) | curses.A_BOLD)
                x_cursor += len(letras[caracter][0]) + 1

            # --- TEXTO GLITCH: POWERED BY I.A. ---
            texto_base = "p o w e r e d   b y   I . A ."
            caracteres_glitch = "!<>-_\\/[]{}—=+*^?#_01"
            texto_animado = ""
            
            for char in texto_base:
                if char != " " and random.random() < 0.15:
                    texto_animado += random.choice(caracteres_glitch)
                else:
                    texto_animado += char
                    
            # Se ubica alineado a la derecha del banner
            stdscr.addstr(y_banner + 6, max(0, banner_x + ancho_total_banner - len(texto_base)), texto_animado, curses.color_pair(10) | curses.A_DIM)

            # Info Centrada
            y_info = y_banner + 8
            stdscr.addstr(y_info, max(0, (ancho // 2) - (len(subtitle) // 2)), subtitle, curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(y_info + 1, max(0, (ancho // 2) - (len(authors) // 2)), authors, curses.color_pair(3))

            # Menú Centrado
            y_menu = y_info + 4
            for idx, opc in enumerate(opciones):
                if y_menu + idx < alto:
                    opc_txt = opc.center(ANCHO_SELECTOR)
                    mx = max(0, (ancho // 2) - (ANCHO_SELECTOR // 2))
                    
                    if idx == fila_seleccionada:
                        stdscr.addstr(y_menu + idx, mx, opc_txt, curses.color_pair(4) | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_menu + idx, mx, opc_txt, curses.color_pair(2))

        except curses.error:
            pass

        stdscr.refresh()

        # LECTURA DE TECLADO ASÍNCRONA
        tecla = stdscr.getch()
        
        # Si no se presiona nada, repite el bucle para continuar la animación
        if tecla == -1:
            continue

        if tecla == curses.KEY_UP and fila_seleccionada > 0:
            fila_seleccionada -= 1
        elif tecla == curses.KEY_DOWN and fila_seleccionada < len(opciones) - 1:
            fila_seleccionada += 1
        elif tecla in [10, 13, curses.KEY_ENTER]:
            if fila_seleccionada == 5: break
            
            # DESACTIVAR TIMEOUT ANTES DE ENTRAR AL MÓDULO PARA NO ROMPER SU TECLADO
            stdscr.timeout(-1)
            
            if fila_seleccionada == 0:
                stdscr.clear()
                nivel1.iniciar(stdscr)
                curses.curs_set(0)
            elif fila_seleccionada == 1:
                stdscr.clear()
                nivel2.iniciar(stdscr)
                curses.curs_set(0)
            elif fila_seleccionada == 2:
                stdscr.clear()
                nivel3.iniciar(stdscr)
                curses.curs_set(0)
            else:
                stdscr.clear()
                msg = f">> MODULO {fila_seleccionada + 1} EN DESARROLLO <<"
                stdscr.addstr(alto // 2, max(0, (ancho // 2) - (len(msg) // 2)), msg, curses.color_pair(1) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(1)
                
            # REACTIVAR ANIMACIÓN AL VOLVER AL MENÚ
            stdscr.timeout(150)

if __name__ == "__main__":
    curses.wrapper(draw_shell)