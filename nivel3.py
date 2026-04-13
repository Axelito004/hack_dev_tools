import curses
import os
import subprocess
import time
import textwrap
import zipfile

def preparar_evidencia():
    """Crea una imagen binaria corrupta con un archivo ZIP real oculto adentro"""
    nombre_archivo = "evidencia_002.img"
    if not os.path.exists(nombre_archivo):
        # 1. Creamos un archivo de texto con la bandera
        with open("secreto.txt", "w") as f:
            f.write("FLAG{UNEFA_DATA_CARVING_MASTER}")
        
        # 2. Lo comprimimos en un ZIP real
        with zipfile.ZipFile("archivo_oculto.zip", "w") as zf:
            zf.write("secreto.txt")
        
        # 3. Borramos el txt original
        os.remove("secreto.txt")
        
        # 4. Creamos 2MB de basura, inyectamos el ZIP, y metemos 1MB más de basura
        os.system(f"dd if=/dev/urandom of={nombre_archivo} bs=1M count=2 2>/dev/null")
        os.system(f"cat archivo_oculto.zip >> {nombre_archivo}")
        os.system(f"dd if=/dev/urandom bs=1M count=1 >> {nombre_archivo} 2>/dev/null")
        
        # 5. Borramos el ZIP suelto
        os.remove("archivo_oculto.zip")
    return nombre_archivo

def limpiar_evidencia():
    """Limpia el disco de trabajo forense"""
    os.system("rm -f evidencia_002.img 2>/dev/null")
    os.system("rm -rf rescate_datos 2>/dev/null")

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

    # Borramos evidencia vieja por si acaso y creamos la nueva
    limpiar_evidencia()
    preparar_evidencia()

    # --- BASE DE DATOS DEL NIVEL 3 (CARVING) ---
    misiones = [
        {
            "titulo": "FASE 1: ESCANEO DE FIRMAS (RECONOCIMIENTO)",
            "contexto": "El sospechoso intentó destruir sus datos. A simple vista, el archivo es pura basura binaria. Usaremos una herramienta que escanea la 'firma' (el ADN) de los archivos para ver si hay algo oculto en su interior.",
            "anatomia": [
                ("binwalk", "Herramienta que escanea archivos en busca de firmas y códigos incrustados."),
                ("evidencia_002.img", "Nuestro archivo de evidencia dañado.")
            ],
            "comando_esperado": "binwalk evidencia_002.img"
        },
        {
            "titulo": "FASE 2: DATA CARVING (LA EXTRACCIÓN)",
            "contexto": "¡Bingo! Binwalk detectó un archivo ZIP enterrado entre la basura. Ahora usaremos Foremost para ignorar el daño del disco y 'tallar' o extraer físicamente ese archivo basándose en su estructura.",
            "anatomia": [
                ("foremost", "Programa del gobierno de EE.UU. para recuperar archivos perdidos."),
                ("-i evidencia_002.img", "La (i) significa Input. Le pasamos el archivo dañado."),
                ("-o rescate_datos", "La (o) significa Output. Crea esta carpeta y guarda allí lo recuperado.")
            ],
            "comando_esperado": "foremost -i evidencia_002.img -o rescate_datos"
        },
        {
            "titulo": "FASE 3: VERIFICACIÓN DEL RESCATE",
            "contexto": "Foremost ha terminado la operación. Automáticamente debió crear una carpeta llamada 'rescate_datos' y dentro de ella, una carpeta por cada tipo de archivo que haya logrado resucitar (en este caso, un directorio 'zip').",
            "anatomia": [
                ("ls", "Lista el contenido de un directorio."),
                ("rescate_datos/zip/", "La ruta donde Foremost guardó nuestro archivo resucitado.")
            ],
            "comando_esperado": "ls rescate_datos/zip/"
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

            # 1. HEADER Y CONTEXTO
            stdscr.addstr(2, mx, f">> SISTEMA FORENSE - NODO {idx+1}/{len(misiones)}", curses.color_pair(10) | curses.A_BOLD)
            stdscr.addstr(4, mx, mision['titulo'], curses.color_pair(3) | curses.A_BOLD)
            y_act = draw_text_wrapped(stdscr, 6, mx, mision['contexto'], ancho_t, curses.color_pair(2))

            # 2. ANATOMÍA DEL COMANDO
            y_act += 2
            stdscr.addstr(y_act, mx, ">> ANATOMIA DEL COMANDO:", curses.color_pair(10))
            y_act += 1
            for parte, explicacion in mision['anatomia']:
                stdscr.addstr(y_act, mx + 3, parte, curses.color_pair(4) | curses.A_BOLD)
                stdscr.addstr(y_act, mx + 3 + len(parte) + 2, f"-> {explicacion}", curses.color_pair(2))
                y_act += 1

            # 3. INSTRUCCIÓN EXPLÍCITA
            y_act += 1
            stdscr.addstr(y_act, mx, ">> ACCIÓN REQUERIDA:", curses.color_pair(10))
            stdscr.addstr(y_act + 1, mx, "Escribe exactamente este comando y presiona ENTER:", curses.color_pair(2))
            stdscr.addstr(y_act + 2, mx + 3, mision['comando_esperado'], curses.color_pair(3) | curses.A_BOLD)

            # 4. SALIDA REAL DEL SISTEMA
            if ejecutado:
                y_act += 4
                stdscr.addstr(y_act, mx, "--- RESULTADO EN EL KERNEL ---", curses.color_pair(4) | curses.A_BOLD)
                # Binwalk da una salida tipo tabla, mostramos unas cuantas líneas más (8)
                lineas = salida_terminal.split('\n')[-9:] 
                for i, l in enumerate(lineas):
                    try:
                        stdscr.addstr(y_act + 1 + i, mx, l[:ancho_t], curses.color_pair(2))
                    except:
                        pass

            # 5. ZONA DE ENTRADA CON VALIDACIÓN DE COLORES
            y_prompt = alto - 4
            prompt = "ROOT@FORENSE:~# "
            stdscr.addstr(y_prompt, mx, prompt, curses.color_pair(11) | curses.A_BOLD)
            
            # Control de pase a la siguiente fase
            if fase_superada:
                msg_avanzar = "[ PULSA ENTER PARA CONTINUAR ]"
                stdscr.addstr(y_prompt, mx + len(prompt), msg_avanzar, curses.color_pair(10) | curses.A_BLINK)
                stdscr.refresh()
                k = stdscr.getch()
                if k in [10, 13]: 
                    break 
                continue

            # Dibujo dinámico de teclas (Verde = bien / Rojo = mal)
            for i, char in enumerate(input_usuario):
                color = curses.color_pair(3)
                if i >= len(mision['comando_esperado']) or char != mision['comando_esperado'][i]:
                    color = curses.color_pair(11)
                stdscr.addstr(y_prompt, mx + len(prompt) + i, char, color | curses.A_BOLD)

            stdscr.refresh()
            
            # --- CAPTURA DE TECLADO ---
            k = stdscr.getch()

            if k in (127, 8, curses.KEY_BACKSPACE):
                input_usuario = input_usuario[:-1]
            elif 32 <= k <= 126:
                input_usuario += chr(k)
            elif k in [10, 13]: # ENTER
                if input_usuario.strip() == "": continue
                
                # Indicador de procesamiento visual
                stdscr.addstr(y_prompt + 2, mx, "[*] Procesando en el Kernel de Kali...", curses.color_pair(10) | curses.A_BLINK)
                stdscr.refresh()
                
                try:
                    # Ejecución real en el OS
                    res = subprocess.run(input_usuario, shell=True, capture_output=True, text=True, timeout=10)
                    salida_terminal = res.stdout + res.stderr
                    ejecutado = True
                    
                    if " ".join(input_usuario.split()) == mision['comando_esperado']:
                        salida_terminal += "\n\n[+] OPERACIÓN CONFIRMADA: Proceso completado exitosamente."
                        fase_superada = True
                    else:
                        salida_terminal += "\n\n[-] ERROR: Comando incorrecto. Revise la sintaxis y los colores."
                        input_usuario = "" 
                except Exception as e:
                    salida_terminal = f"Error: {str(e)}"
                    input_usuario = ""

            elif k == 27: # ESC
                limpiar_evidencia()
                return

    # --- PANTALLA FINAL: EXPLICACIÓN MODO "NIÑO DE PRIMARIA" ---
    stdscr.clear()
    alto, ancho = stdscr.getmaxyx()
    mx = int(ancho * 0.1)
    ancho_t = ancho - (mx * 2)

    titulo_final = "=== RESUMEN DE LA MISIÓN: RESURRECCIÓN DE DATOS ==="
    stdscr.addstr(2, max(0, (ancho // 2) - (len(titulo_final) // 2)), titulo_final, curses.color_pair(10) | curses.A_BOLD)

    texto_explicativo = (
        "¡Eres un mago de la informática forense! Acabas de resucitar un archivo "
        "que el sistema operativo creía muerto. Para que lo entiendas súper fácil, "
        "imagina que el disco duro es una gran caja de arena:\n\n"
        "1. LA MÁQUINA DE RAYOS X (binwalk):\n"
        "El malo tiró su juguete (el archivo secreto) en la gran caja de arena y luego "
        "lo cubrió con muchísima tierra y basura. A simple vista solo ves arena. "
        "El comando 'binwalk' es como ponerte unos lentes de Rayos X. Escanea la arena y te dice: "
        "'¡Oye! En la esquina izquierda detecto la forma de un carrito de juguete (un ZIP)'.\n\n"
        "2. LAS PINZAS MÁGICAS (foremost):\n"
        "Ya sabemos dónde está el juguete gracias a los Rayos X, pero si metemos una pala "
        "podríamos romperlo. 'foremost' es como unas pinzas quirúrgicas gigantes. "
        "Mete las pinzas en la arena ignorando toda la basura, agarra el juguete con mucho "
        "cuidado y lo saca limpiecito para guardarlo en la carpeta de rescate.\n\n"
        "3. EL TESORO RESCATADO (ls):\n"
        "Finalmente, abrimos el cofre de rescate y ¡Ta-Da! Ahí está nuestro archivo, "
        "listo para ser usado como evidencia contra el sospechoso en la corte.\n\n"
        ">> Presiona ENTER para volver al menú principal..."
    )

    draw_text_wrapped(stdscr, 5, mx, texto_explicativo, ancho_t, curses.color_pair(2))
    stdscr.refresh()

    while True:
        k = stdscr.getch()
        if k in [10, 13]:
            break

    limpiar_evidencia()