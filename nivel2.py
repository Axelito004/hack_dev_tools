import curses
import os
import subprocess
import time
import textwrap

def preparar_evidencia():
    nombre_archivo = "evidencia_001.img"
    if not os.path.exists(nombre_archivo):
        os.system(f"dd if=/dev/zero of={nombre_archivo} bs=1M count=10 2>/dev/null")
        os.system(f"echo 'FLAG{{UNEFA_YARACUY_FORENSE_2026}}' >> {nombre_archivo}")
    return nombre_archivo

def limpiar_evidencia():
    os.system("rm -f evidencia_001.img backup_evidencia.img 2>/dev/null")

def draw_text_wrapped(stdscr, y, x, text, width, color):
    lineas = textwrap.wrap(text, width)
    for i, linea in enumerate(lineas):
        try:
            stdscr.addstr(y + i, x, linea, color)
        except curses.error:
            pass
    return y + len(lineas)

def iniciar(stdscr):
    curses.start_color()
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
    curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)    

    archivo_evidencia = preparar_evidencia()

    misiones = [
        {
            "titulo": "FASE 1: INTEGRIDAD DE LA EVIDENCIA (HASHING)",
            "contexto": "En forense, necesitamos asegurar que el archivo no ha sido manipulado. Usaremos un algoritmo matemático para sacar su 'huella digital'.",
            "anatomia": [
                ("sha256sum", "Es la herramienta que calcula la huella matemática."),
                ("evidencia_001.img", "Es el archivo sospechoso que vamos a analizar.")
            ],
            "comando_esperado": "sha256sum evidencia_001.img"
        },
        {
            "titulo": "FASE 2: DUPLICACIÓN BIT A BIT (CLONADO)",
            "contexto": "Nunca trabajamos sobre la evidencia original para no dañarla. Vamos a crear una copia exacta de respaldo.",
            "anatomia": [
                ("cp", "Comando base de Linux para Copiar (Copy)."),
                ("evidencia_001.img", "El archivo de ORIGEN (lo que queremos copiar)."),
                ("backup_evidencia.img", "El archivo de DESTINO (el nuevo clon que crearemos).")
            ],
            "comando_esperado": "cp evidencia_001.img backup_evidencia.img"
        },
        {
            "titulo": "FASE 3: BÚSQUEDA DE METADATOS OCULTOS",
            "contexto": "El sospechoso ocultó una bandera de texto dentro del disco binario. Vamos a extraer todo el texto y a filtrarlo.",
            "anatomia": [
                ("strings", "Extrae todo el texto legible oculto en el archivo binario."),
                ("|", "Se llama 'Pipe' (tubería). Pasa el resultado al siguiente comando."),
                ("grep FLAG", "Filtra la avalancha de texto y solo te muestra la línea que dice 'FLAG'.")
            ],
            "comando_esperado": "strings evidencia_001.img | grep FLAG"
        }
    ]

    for idx, mision in enumerate(misiones):
        input_usuario = ""
        salida_terminal = ""
        ejecutado = False
        fase_superada = False

        while True:
            stdscr.clear()
            alto, ancho = stdscr.getmaxyx()
            mx = int(ancho * 0.1)
            ancho_t = ancho - (mx * 2)

            stdscr.addstr(2, mx, f">> SISTEMA FORENSE - NODO {idx+1}/{len(misiones)}", curses.color_pair(10) | curses.A_BOLD)
            stdscr.addstr(4, mx, mision['titulo'], curses.color_pair(3) | curses.A_BOLD)
            y_act = draw_text_wrapped(stdscr, 6, mx, mision['contexto'], ancho_t, curses.color_pair(2))

            y_act += 2
            stdscr.addstr(y_act, mx, ">> ANATOMIA DEL COMANDO:", curses.color_pair(10))
            y_act += 1
            for parte, explicacion in mision['anatomia']:
                stdscr.addstr(y_act, mx + 3, parte, curses.color_pair(4) | curses.A_BOLD)
                stdscr.addstr(y_act, mx + 3 + len(parte) + 2, f"-> {explicacion}", curses.color_pair(2))
                y_act += 1

            y_act += 1
            stdscr.addstr(y_act, mx, ">> ACCIÓN REQUERIDA:", curses.color_pair(10))
            stdscr.addstr(y_act + 1, mx, "Escribe exactamente este comando y presiona ENTER:", curses.color_pair(2))
            stdscr.addstr(y_act + 2, mx + 3, mision['comando_esperado'], curses.color_pair(3) | curses.A_BOLD)

            if ejecutado:
                y_act += 4
                stdscr.addstr(y_act, mx, "--- RESULTADO EN EL KERNEL ---", curses.color_pair(4) | curses.A_BOLD)
                lineas = salida_terminal.split('\n')[-6:] 
                for i, l in enumerate(lineas):
                    try:
                        stdscr.addstr(y_act + 1 + i, mx, l[:ancho_t], curses.color_pair(2))
                    except:
                        pass

            y_prompt = alto - 4
            prompt = "ROOT@FORENSE:~# "
            stdscr.addstr(y_prompt, mx, prompt, curses.color_pair(11) | curses.A_BOLD)
            
            if fase_superada:
                msg_avanzar = "[ PULSA ENTER PARA CONTINUAR ]"
                stdscr.addstr(y_prompt, mx + len(prompt), msg_avanzar, curses.color_pair(10) | curses.A_BLINK)
                stdscr.refresh()
                k = stdscr.getch()
                if k in [10, 13]: 
                    break 
                continue

            for i, char in enumerate(input_usuario):
                color = curses.color_pair(3)
                if i >= len(mision['comando_esperado']) or char != mision['comando_esperado'][i]:
                    color = curses.color_pair(11)
                stdscr.addstr(y_prompt, mx + len(prompt) + i, char, color | curses.A_BOLD)

            stdscr.refresh()
            
            k = stdscr.getch()

            if k in (127, 8, curses.KEY_BACKSPACE):
                input_usuario = input_usuario[:-1]
            elif 32 <= k <= 126:
                input_usuario += chr(k)
            elif k in [10, 13]: 
                if input_usuario.strip() == "": continue
                
                stdscr.addstr(y_prompt + 2, mx, "[*] Procesando en el Kernel de Kali...", curses.color_pair(10) | curses.A_BLINK)
                stdscr.refresh()
                
                try:
                    res = subprocess.run(input_usuario, shell=True, capture_output=True, text=True, timeout=5)
                    salida_terminal = res.stdout + res.stderr
                    ejecutado = True
                    
                    if " ".join(input_usuario.split()) == mision['comando_esperado']:
                        salida_terminal += "\n\n[+] OPERACIÓN CONFIRMADA: Evidencia asegurada."
                        fase_superada = True
                    else:
                        salida_terminal += "\n\n[-] ERROR: Comando incorrecto. Revise la sintaxis y los colores."
                        input_usuario = "" 
                except Exception as e:
                    salida_terminal = f"Error: {str(e)}"
                    input_usuario = ""

            elif k == 27: 
                limpiar_evidencia()
                return

    # --- PANTALLA FINAL: EXPLICACIÓN MODO "NIÑO DE PRIMARIA" ---
    stdscr.clear()
    alto, ancho = stdscr.getmaxyx()
    mx = int(ancho * 0.1)
    ancho_t = ancho - (mx * 2)

    titulo_final = "=== RESUMEN DE LA MISIÓN ==="
    stdscr.addstr(2, max(0, (ancho // 2) - (len(titulo_final) // 2)), titulo_final, curses.color_pair(10) | curses.A_BOLD)

    texto_explicativo = (
        "¡Lo lograste! Acabas de actuar como un verdadero detective digital. "
        "Para que nunca se te olvide lo que hiciste hoy, imagínalo así:\n\n"
        "1. EL CANDADO MÁGICO (sha256sum):\n"
        "Imagina que el archivo sospechoso es un diario secreto. El comando 'sha256sum' "
        "le puso un candado mágico que toma una foto de cada letra adentro. Si el malo "
        "intenta borrar o cambiar una sola coma del diario, el candado se rompe y nos avisa. "
        "¡Así demostramos frente a un juez que nadie tocó la evidencia!\n\n"
        "2. LA COPIA DEL VIDEOJUEGO (cp):\n"
        "Nunca, pero NUNCA, jugamos con la evidencia original. Usamos el comando 'cp' para hacer "
        "un clon exacto, como cuando guardas la partida en un videojuego antes de ir a pelear "
        "contra un jefe. Así, si nos equivocamos investigando y rompemos algo, el archivo "
        "original sigue a salvo en su cajita de cristal.\n\n"
        "3. EL PERRITO SABUESO (strings + grep):\n"
        "El malo rompió una carta y la tiró a la basura (el archivo .img). El comando 'strings' "
        "es como una lupa gigante que rescata todas las letras legibles de esa basura. "
        "Pero como leer tanta basura da pereza, usamos 'grep', que actúa como un perrito sabueso "
        "entrenado. Le dijimos: '¡Busca la palabra FLAG!' y él fue corriendo a traernos justo lo que queríamos.\n\n"
        ">> Presiona ENTER para volver al menú principal..."
    )

    draw_text_wrapped(stdscr, 4, mx, texto_explicativo, ancho_t, curses.color_pair(2))
    stdscr.refresh()

    while True:
        k = stdscr.getch()
        if k in [10, 13]:
            break

    limpiar_evidencia()