import curses
import time
import locale
import random
import pyttsx3
import nivel1  

# Configurar soporte para caracteres especiales (UTF-8)
locale.setlocale(locale.LC_ALL, '')

def hablar(texto, rate=300):
    """
    Usa el motor del sistema directamente para evitar errores de memoria 
    en Python 3.13 y asegurar la velocidad de 290.
    """
    try:
        # Limpiamos el texto de caracteres que puedan romper el comando bash
        texto_limpio = texto.replace('"', '').replace("'", "")
        # Ejecución directa de espeak-ng
        os.system(f'espeak-ng -s {rate} -v es "{texto_limpio}"')
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
    curses.start_color()
    stdscr.keypad(True)

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)  

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
    authors = "Desarrollado por: Ángel Gustavo Castillo Giménez && Ing. Josue Ordoñez"
    
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

        # Cálculo de la "Masa Visual" para centrar todo el bloque verticalmente
        # (Banner + Info + Menú = aprox 18 líneas)
        bloque_alto = 18
        start_y = max(0, (alto // 2) - (bloque_alto // 2))

        # Centrado del Banner
        ancho_total_banner = sum(len(letras[l][0]) for l in palabra) + (len(palabra) - 1)
        banner_x = max(0, (ancho // 2) - (ancho_total_banner // 2))

        try:
            # Header
            hx = max(0, (ancho // 2) - (len(header_inst) // 2))
            stdscr.addstr(start_y, hx, header_inst, curses.color_pair(2) | curses.A_DIM)

            # Banner Glitch
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

            # Info Centrada
            y_info = y_banner + 7
            stdscr.addstr(y_info, max(0, (ancho // 2) - (len(subtitle) // 2)), subtitle, curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(y_info + 1, max(0, (ancho // 2) - (len(authors) // 2)), authors, curses.color_pair(3))

            # Menú Centrado
            y_menu = y_info + 4
            for idx, opc in enumerate(opciones):
                if y_menu + idx < alto:
                    # Centramos el texto dentro del selector y el selector en la pantalla
                    opc_txt = opc.center(ANCHO_SELECTOR)
                    mx = max(0, (ancho // 2) - (ANCHO_SELECTOR // 2))
                    
                    if idx == fila_seleccionada:
                        stdscr.addstr(y_menu + idx, mx, opc_txt, curses.color_pair(4) | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_menu + idx, mx, opc_txt, curses.color_pair(2))

        except curses.error:
            pass

        stdscr.refresh()

        tecla = stdscr.getch()
        if tecla == curses.KEY_UP and fila_seleccionada > 0:
            fila_seleccionada -= 1
        elif tecla == curses.KEY_DOWN and fila_seleccionada < len(opciones) - 1:
            fila_seleccionada += 1
        elif tecla in [10, 13, curses.KEY_ENTER]:
            if fila_seleccionada == 5: break
            if fila_seleccionada == 0:
                stdscr.clear()
                nivel1.iniciar(stdscr)
                curses.curs_set(0)
            else:
                stdscr.clear()
                msg = f">> MODULO {fila_seleccionada + 1} EN DESARROLLO <<"
                stdscr.addstr(alto // 2, max(0, (ancho // 2) - (len(msg) // 2)), msg, curses.color_pair(1) | curses.A_BOLD)
                stdscr.refresh()
                time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(draw_shell)