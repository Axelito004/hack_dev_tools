import curses
import time
import locale
import random

# Configurar soporte para caracteres especiales
locale.setlocale(locale.LC_ALL, '')

def draw_shell(stdscr):
    # --- 1. CONFIGURACIÓN ---
    curses.curs_set(0)
    stdscr.nodelay(False)
    curses.start_color()
    stdscr.keypad(True)

    # Colores
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) # Banner
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) # Texto
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # Autores
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Selector (Fondo Azul)

    # --- 2. COMPONENTES VISUALES ---
    header_inst = "--- FUNDACITE && MINCYT ---"
    
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
    espaciado_letras = 1 
    subtitle = "Hack-Dev Tools"
    authors = "By: (AXL-HACKING)AG Castillo Giménez && Ing. Josue Ordoñez"
    
    opciones = [
        "[ 1 ] - Fundamentos de Bash y Supervivencia",
        "[ 2 ] - Preservación y Adquisición de Evidencia",
        "[ 3 ] - Recuperación de Datos y Análisis (Data Carving)",
        "[ 4 ] - Análisis Forense de Memoria Volátil (RAM)",
        "[ 5 ] - Forense de Redes y Análisis de Tráfico",
        "[ Salir ] - Cerrar Sistema"
    ]

    # --- ANCHO FIJO PARA EL SELECTOR ---
    ANCHO_SELECTOR = 75 # Esto define qué tan ancha será la barra azul
    fila_seleccionada = 0

    while True:
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()

        ancho_total_banner = sum(len(letras[l][0]) for l in palabra) + (espaciado_letras * (len(palabra) - 1))
        start_y = max(1, (alto // 2) - 11)
        banner_x = max(0, (ancho // 2) - (ancho_total_banner // 2))

        try:
            # Header
            header_x = max(0, (ancho // 2) - (len(header_inst) // 2))
            stdscr.addstr(start_y, header_x, header_inst, curses.color_pair(2) | curses.A_DIM)

            # Banner Glitch
            x_cursor = banner_x
            y_banner = start_y + 2
            for caracter in palabra:
                if caracter in letras:
                    for i in range(6):
                        if y_banner + i < alto:
                            contenido = letras[caracter][i]
                            if caracter in "ITE":
                                lista_char = list(contenido)
                                for idx, c in enumerate(lista_char):
                                    if c not in " ╚═╗║" and random.random() > 0.85:
                                        lista_char[idx] = random.choice(["?", "!", "0", "1", "▒", "X"])
                                contenido = "".join(lista_char)
                            stdscr.addstr(y_banner + i, x_cursor, contenido, curses.color_pair(1) | curses.A_BOLD)
                    x_cursor += len(letras[caracter][0]) + espaciado_letras

            # Subtítulo y Autores
            y_aux = y_banner + 7
            stdscr.addstr(y_aux, max(0, (ancho // 2) - (len(subtitle) // 2)), subtitle, curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(y_aux + 1, max(0, (ancho // 2) - (len(authors) // 2)), authors, curses.color_pair(3))

            # --- 3. MENÚ CON SELECTOR ENSANCHADO ---
            y_menu = y_aux + 4
            for idx, opc in enumerate(opciones):
                if y_menu + idx < alto:
                    # Rellenamos la opción con espacios para que la barra azul sea ancha
                    # .center(ANCHO_SELECTOR) hace que el texto quede centrado en la barra azul
                    opcion_formateada = opc.center(ANCHO_SELECTOR)
                    
                    x_opc = max(0, (ancho // 2) - (ANCHO_SELECTOR // 2))
                    
                    if idx == fila_seleccionada:
                        # Al aplicar el color 4 aquí, se pinta todo el bloque de 75 caracteres
                        stdscr.addstr(y_menu + idx, x_opc, opcion_formateada, curses.color_pair(4) | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_menu + idx, x_opc, opcion_formateada, curses.color_pair(2))

        except curses.error:
            pass

        stdscr.refresh()
        tecla = stdscr.getch()

        if tecla == curses.KEY_UP and fila_seleccionada > 0:
            fila_seleccionada -= 1
        elif tecla == curses.KEY_DOWN and fila_seleccionada < len(opciones) - 1:
            fila_seleccionada += 1
        elif tecla in [10, 13, curses.KEY_ENTER]:
            if fila_seleccionada == len(opciones) - 1: break
            stdscr.clear()
            msg = f">> ACCESO AUTORIZADO: CARGANDO NIVEL {fila_seleccionada + 1} ..."
            stdscr.addstr(alto // 2, max(0, (ancho // 2) - (len(msg) // 2)), msg, curses.color_pair(3) | curses.A_BLINK)
            stdscr.refresh()
            time.sleep(1.2)

if __name__ == "__main__":
    curses.wrapper(draw_shell)