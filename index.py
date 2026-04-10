import curses
import time
import locale
import random
import pyttsx3
import nivel1  # Asegúrate de que nivel1.py esté en la misma carpeta

# Configurar soporte para caracteres especiales (UTF-8)
locale.setlocale(locale.LC_ALL, '')

def hablar(texto):
    """Función de voz optimizada para Kali Linux"""
    try:
        engine = pyttsx3.init('espeak')
        engine.setProperty('rate', 145) # Velocidad elegante
        
        # Intentar cargar voz en español
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id:
                engine.setProperty('voice', voice.id)
                break
        
        engine.say(texto)
        engine.runAndWait()
    except:
        pass # Si el audio falla, el sistema no se detiene

def draw_shell(stdscr):
    # --- 1. BIENVENIDA AUDITIVA INSTITUCIONAL ---
    stdscr.clear()
    msg_pantalla = ">> ESTABLECIENDO CONEXION SEGURA..."
    msg_voz = "Conexión establecida. Bienvenido, Aspirante. Sistema Fundacite y Minsit Yaracuy en línea."
    
    alto, ancho = stdscr.getmaxyx()
    
    # Dibujar mensaje de carga centrado
    x_boot = max(0, (ancho // 2) - (len(msg_pantalla) // 2))
    y_boot = max(0, alto // 2)
    
    try:
        stdscr.addstr(y_boot, x_boot, msg_pantalla, curses.A_BOLD)
        stdscr.refresh()
    except:
        pass

    hablar(msg_voz)

    # --- 2. CONFIGURACIÓN DE CURSES ---
    curses.curs_set(0)
    stdscr.nodelay(False)
    curses.start_color()
    stdscr.keypad(True)

    # Colores
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) # Banner
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) # Texto
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # Autores
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Selector Ancho

    # --- 3. DEFINICIÓN DEL BANNER (MODULAR CON GLITCH) ---
    letras = {
        'F': ["███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "██║     ", "╚═╝     "],
        'U': ["██╗   ██╗", "██║   ██║", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
        'N': ["███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"],
        'D': ["██████╗ ", "██╔══██╗", "██║  ██║", "██║  ██║", "██████╔╝", "╚═════╝ "],
        'A': ["  █████╗  ", " ██╔══██╗ ", " ███████║ ", " ██╔══██║ ", " ██║  ██║ ", " ╚═╝  ╚═╝ "],
        'C': [" ██████╗ ", "██╔════╝ ", "██║      ", "██║      ", "╚██████╗ ", " ╚═════╝ "],
        # LETRAS CON GLITCH (I, T, E)
        'I': ["█?█", "▒█▒", "▓█▓", "░█░", "█#█", "╚?╝"],
        'T': ["█▓▒░▓█░█", "╚═?██╔═?", "  ▒██║  ", "  ▓██║  ", "  ░██║  ", "  ╚?╝   "],
        'E': ["█?█?█?█╗", "██╔═░══╝", "█▒███╗  ", "██╔?═╝  ", "███?███╗", "╚═░════╝"]
    }

    palabra = "FUNDACITE"
    header_inst = "--- FUNDACITE && MINCYT ---"
    subtitle = "Hack-Dev Tools | Yaracuy"
    authors = "By: (AXL-HACKING)AG Castillo Giménez && Ing. Josue Ordoñez"
    
    opciones = [
        "[ 1 ] - Fundamentos de Bash y Supervivencia",
        "[ 2 ] - Preservación y Adquisición de Evidencia",
        "[ 3 ] - Recuperación de Datos y Análisis (Data Carving)",
        "[ 4 ] - Análisis Forense de Memoria Volátil (RAM)",
        "[ 5 ] - Forense de Redes y Análisis de Tráfico",
        "[ Salir ] - Cerrar Sistema"
    ]

    ANCHO_SELECTOR = 75
    fila_seleccionada = 0

    # --- 4. BUCLE PRINCIPAL DE LA INTERFAZ ---
    while True:
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()

        # Cálculos de centrado
        ancho_total_banner = sum(len(letras[l][0]) for l in palabra) + (len(palabra) - 1)
        start_y = max(0, (alto // 2) - 11)
        banner_x = max(0, (ancho // 2) - (ancho_total_banner // 2))

        try:
            # Dibujar Header Institucional
            hx = max(0, (ancho // 2) - (len(header_inst) // 2))
            stdscr.addstr(start_y, hx, header_inst, curses.color_pair(2) | curses.A_DIM)

            # Dibujar Banner con Glitch Dinámico
            x_cursor = banner_x
            y_banner = start_y + 2
            for caracter in palabra:
                if caracter in letras:
                    for i in range(6):
                        if y_banner + i < alto:
                            contenido = letras[caracter][i]
                            # Efecto glitch para I, T, E
                            if caracter in "ITE":
                                lista_char = list(contenido)
                                for idx, c in enumerate(lista_char):
                                    if c not in " ╚═╗║" and random.random() > 0.88:
                                        lista_char[idx] = random.choice(["?", "X", "1", "0", "▒"])
                                contenido = "".join(lista_char)
                            
                            stdscr.addstr(y_banner + i, x_cursor, contenido, curses.color_pair(1) | curses.A_BOLD)
                    x_cursor += len(letras[caracter][0]) + 1

            # Subtítulo y Autores
            y_info = y_banner + 7
            if y_info + 1 < alto:
                stdscr.addstr(y_info, max(0, (ancho // 2) - (len(subtitle) // 2)), subtitle, curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(y_info + 1, max(0, (ancho // 2) - (len(authors) // 2)), authors, curses.color_pair(3))

            # Menú con Selector Ancho
            y_menu = y_info + 4
            for idx, opc in enumerate(opciones):
                if y_menu + idx < alto:
                    opcion_formateada = opc.center(ANCHO_SELECTOR)
                    mx = max(0, (ancho // 2) - (ANCHO_SELECTOR // 2))
                    
                    if idx == fila_seleccionada:
                        stdscr.addstr(y_menu + idx, mx, opcion_formateada, curses.color_pair(4) | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_menu + idx, mx, opcion_formateada, curses.color_pair(2))

        except curses.error:
            pass

        stdscr.refresh()

        # --- 5. CONTROL DE ENTRADA ---
        tecla = stdscr.getch()

        if tecla == curses.KEY_UP and fila_seleccionada > 0:
            fila_seleccionada -= 1
        elif tecla == curses.KEY_DOWN and fila_seleccionada < len(opciones) - 1:
            fila_seleccionada += 1
        elif tecla in [10, 13, curses.KEY_ENTER]:
            # Opción Salir
            if fila_seleccionada == 5:
                break
            
            # Opción Nivel 1
            if fila_seleccionada == 0:
                stdscr.clear()
                msg = ">> ACCEDIENDO AL NODO 01: BASH_CORE..."
                stdscr.addstr(alto // 2, max(0, (ancho // 2) - (len(msg) // 2)), msg, curses.color_pair(3) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(1)
                
                # Lanzar Nivel 1
                nivel1.iniciar(stdscr)
                
                # Al volver, resetear terminal
                stdscr.clear()
                curses.curs_set(0)
            else:
                # Otros niveles
                stdscr.clear()
                msg = f">> ERROR: MODULO {fila_seleccionada + 1} EN DESARROLLO <<"
                stdscr.addstr(alto // 2, max(0, (ancho // 2) - (len(msg) // 2)), msg, curses.color_pair(1) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(1.2)

if __name__ == "__main__":
    curses.wrapper(draw_shell)