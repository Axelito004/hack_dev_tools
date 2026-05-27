#!/usr/bin/env python3
"""
nivel3.py - Módulo Forense: Análisis y Sanitización de Metadatos.
Simulador de academia táctica de Kali Linux con TTS y ejecución real de herramientas.
Proporciona la función iniciar(stdscr) para ser llamada desde main.py.
"""

import curses
import os
import sys
import subprocess
import time
import signal
import threading
import shlex
from pathlib import Path

# ------------------------------- TTS engine ---------------------------------
_tts_proc = None
_tts_lock = threading.Lock()

def _kill_previous_tts():
    global _tts_proc
    with _tts_lock:
        if _tts_proc is not None:
            try:
                os.killpg(os.getpgid(_tts_proc.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
            _tts_proc = None

def hablar(texto, rate=280, esperar=False, matar_previo=False):
    global _tts_proc
    if matar_previo:
        _kill_previous_tts()
    if rate > 100:
        rate_str = f"+{rate - 100}%"
    elif rate < 100:
        rate_str = f"{rate - 100}%"
    else:
        rate_str = "+0%"
    try:
        edge = subprocess.Popen(
            ["edge-tts", "--text", texto, "--voice", "es-ES-AlvaroNeural",
             "--rate", rate_str, "--write-media", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        mpg = subprocess.Popen(
            ["mpg123", "-"],
            stdin=edge.stdout, stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        edge.stdout.close()
        with _tts_lock:
            _tts_proc = mpg
        if esperar:
            mpg.wait()
            with _tts_lock:
                _tts_proc = None
    except FileNotFoundError:
        pass

def deletrear(texto):
    simbolos = {
        '!': 'signo de exclamación', '"': 'comillas', '#': 'almohadilla',
        '$': 'dólar', '%': 'por ciento', '&': 'ampersand', '\'': 'apóstrofe',
        '(': 'paréntesis izquierdo', ')': 'paréntesis derecho', '*': 'asterisco',
        '+': 'más', ',': 'coma', '-': 'guion', '.': 'punto', '/': 'barra',
        ':': 'dos puntos', ';': 'punto y coma', '<': 'menor que', '=': 'igual',
        '>': 'mayor que', '?': 'interrogación', '@': 'arroba',
        '[': 'corchete izquierdo', '\\': 'barra invertida', ']': 'corchete derecho',
        '^': 'circunflejo', '_': 'guion bajo', '`': 'acento grave',
        '{': 'llave izquierda', '|': 'barra vertical', '}': 'llave derecha',
        '~': 'tilde', ' ': 'espacio'
    }
    partes = [simbolos.get(ch, ch.lower()) for ch in texto]
    hablar(", ".join(partes), rate=250, esperar=False, matar_previo=True)

# -------------------------- Curses UI utilities -----------------------------
def draw_menu(stdscr, options, current):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = "Módulo Forense: Análisis y Sanitización de Metadatos"
    stdscr.addstr(1, max(0, (w - len(title)) // 2), title, curses.A_BOLD)
    stdscr.addstr(2, max(0, (w - len("Selecciona herramienta:")) // 2), "Selecciona herramienta:")
    for idx, opt in enumerate(options):
        x = max(0, (w - len(opt)) // 2)
        y = 4 + idx
        attr = curses.A_REVERSE if idx == current else 0
        stdscr.addstr(y, x, opt, attr)
    stdscr.addstr(h-1, 0, "UP/DOWN: mover  ENTER: elegir  (o ESC para salir)", curses.A_DIM)
    stdscr.refresh()

def file_explorer(stdscr, modalidad):
    curses.curs_set(1)
    current_path = os.path.expanduser("~")
    cursor = 1
    scroll_offset = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        header = f"Explorador de archivos - Modalidad {modalidad}"
        stdscr.addstr(0, max(0, (w - len(header)) // 2), header, curses.A_BOLD)
        stdscr.addstr(1, 0, f"Directorio: {current_path}"[:w-1])
        if modalidad == 4:
            stdscr.addstr(2, 0, "Sugerencia: Busca un archivo .pdf para analizar", curses.A_DIM)
        try:
            entries = [".."] + sorted(os.listdir(current_path))
        except PermissionError:
            stdscr.addstr(4, 0, "Error: Permiso denegado. Pulse cualquier tecla para retroceder.")
            stdscr.refresh()
            stdscr.getch()
            parent = os.path.dirname(current_path)
            if parent != current_path:
                current_path = parent
            cursor = 1
            continue
        max_lines = h - 5
        start_idx = scroll_offset
        end_idx = min(len(entries), start_idx + max_lines)
        visible = entries[start_idx:end_idx]
        for i, entry in enumerate(visible):
            y = 4 + i
            if y >= h - 1:
                break
            full = os.path.join(current_path, entry)
            prefix = " 📁" if entry == ".." or os.path.isdir(full) else " 📄"
            line = f"{prefix} {entry}"[:w-1]
            attr = curses.A_REVERSE if (start_idx + i) == cursor else 0
            stdscr.addstr(y, 0, line, attr)
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and cursor > 0:
            cursor -= 1
            if cursor < scroll_offset:
                scroll_offset = cursor
        elif key == curses.KEY_DOWN and cursor < len(entries) - 1:
            cursor += 1
            if cursor >= scroll_offset + max_lines:
                scroll_offset = cursor - max_lines + 1
        elif key == ord('\n'):
            selected = entries[cursor]
            full = os.path.join(current_path, selected)
            if selected == "..":
                parent = os.path.dirname(current_path)
                if parent != current_path:
                    current_path = parent
                    cursor = 1
                    scroll_offset = 0
            elif os.path.isdir(full):
                current_path = full
                cursor = 1
                scroll_offset = 0
            else:
                curses.curs_set(0)
                return full
        elif key == 27:
            curses.curs_set(0)
            return None

def text_input_field(stdscr, prompt="> "):
    input_str = ""
    y, x = stdscr.getyx()
    while True:
        stdscr.move(y, 0)
        stdscr.clrtoeol()
        stdscr.addstr(y, 0, prompt + input_str)
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord('\n'):
            return input_str
        elif ch in (curses.KEY_BACKSPACE, 127):
            input_str = input_str[:-1] if input_str else ""
        elif ch == curses.KEY_F1:
            if input_str:
                deletrear(input_str)
        elif 32 <= ch <= 126:
            input_str += chr(ch)

def draw_fake_console(stdscr, text, title="Consola Forense"):
    h, w = stdscr.getmaxyx()
    split = h // 2
    for i in range(split, h):
        stdscr.move(i, 0)
        stdscr.clrtoeol()
    stdscr.hline(split, 0, curses.ACS_HLINE, w)
    stdscr.addstr(split, 2, f" {title} ")
    for i, line in enumerate(text.splitlines()):
        if split + 1 + i >= h - 1:
            break
        stdscr.addstr(split + 1 + i, 1, line[:w-2])
    stdscr.refresh()

def execute_and_show(stdscr, cmd):
    h, w = stdscr.getmaxyx()
    split = h // 2
    for i in range(split, h):
        stdscr.move(i, 0)
        stdscr.clrtoeol()
    stdscr.refresh()
    try:
        args = shlex.split(cmd)
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        output = result.stdout + ("\n--- STDERR ---\n" + result.stderr if result.stderr else "")
        if not output.strip():
            output = "(sin salida)"
    except FileNotFoundError:
        output = f"Error: Comando no encontrado. ¿Está instalado {args[0]}?"
    except subprocess.TimeoutExpired:
        output = "Error: El comando excedió el tiempo de espera (30 s)."
    except Exception as e:
        output = f"Error inesperado: {e}"
    draw_fake_console(stdscr, output)
    return output

def animate_start(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    msg = "Iniciando escáner forense"
    stdscr.addstr(h//2, max(0, (w - len(msg))//2), msg, curses.A_BOLD)
    stdscr.refresh()
    hablar("Iniciando escáner forense", esperar=False)
    for _ in range(3):
        time.sleep(0.3)
        stdscr.addstr(h//2+1, max(0, (w-10)//2), "[*.......]", curses.A_DIM)
        stdscr.refresh()
        time.sleep(0.3)
    stdscr.clear()

def failure_animation(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    msg = "¡FALLO DEL SISTEMA! Has agotado tus vidas."
    stdscr.addstr(h//2, max(0, (w - len(msg))//2), msg, curses.A_BOLD | curses.A_BLINK)
    stdscr.refresh()
    hablar("Fallo del sistema. La misión ha fracasado.", esperar=True)
    time.sleep(2)
    stdscr.clear()

def final_report(stdscr, modalidad, filepath, total_time):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    tool_names = {1: "ExifTool", 2: "MediaInfo", 3: "MAT2", 4: "PDF Tools"}
    tool = tool_names.get(modalidad, "Desconocida")
    mins, secs = divmod(total_time, 60)
    time_str = f"{mins:02d}:{secs:02d}"
    report = [
        f"Reporte de Inteligencia - {tool}",
        f"Archivo analizado: {filepath}",
        "",
        "Análisis completado con éxito.",
        "Los metadatos han sido procesados según los protocolos tácticos.",
        f"Tiempo total empleado: {time_str}",
    ]
    if modalidad == 1:
        report.append("Se aplicaron técnicas de extracción, geolocalización y borrado seguro.")
        report.append("Se analizaron: metadatos básicos, GPS, cámara, fechas y estructura de archivo.")
    elif modalidad == 2:
        report.append("Se inspeccionaron todos los streams multimedia y codecs asociados.")
        report.append("Se extrajo información de audio, video, capítulos y formato contenedor.")
    elif modalidad == 3:
        report.append("Se generó una copia anonimizada libre de metadatos sensibles.")
    elif modalidad == 4:
        report.append("Se evaluó la estructura del PDF y se detectaron posibles objetos maliciosos.")
    report.append("")
    report.append("Presiona cualquier tecla para volver al menú principal.")

    for i, line in enumerate(report):
        y = 2 + i
        if y < h - 1:
            x = max(0, (w - len(line)) // 2)
            attr = curses.A_BOLD if i == 0 else 0
            stdscr.addstr(y, x, line, attr)
    stdscr.refresh()
    hablar("Reporte de inteligencia generado. Misión cumplida.", esperar=False)
    stdscr.getch()

def update_timer_display(stdscr, start_time, line=0):
    h, w = stdscr.getmaxyx()
    elapsed = int(time.time() - start_time)
    mins, secs = divmod(elapsed, 60)
    timer_str = f"{mins:02d}:{secs:02d}"
    stdscr.move(line, w - 10)
    stdscr.clrtoeol()
    stdscr.addstr(line, w - len(timer_str) - 2, timer_str, curses.A_BOLD)
    stdscr.refresh()

def mission_loop(stdscr, missions, modalidad, filepath):
    lives = 10
    h, w = stdscr.getmaxyx()
    start_time = time.time()

    for i, (descripcion, cmd) in enumerate(missions):
        if lives <= 0:
            break

        stdscr.clear()
        stdscr.addstr(0, 0, f"Misión {i+1}/{len(missions)} - Modalidad {modalidad}", curses.A_BOLD)
        update_timer_display(stdscr, start_time, 0)
        stdscr.addstr(1, 0, descripcion)
        stdscr.addstr(3, 0, "Comando esperado:", curses.A_UNDERLINE)
        stdscr.addstr(4, 0, cmd, curses.A_BOLD)
        stdscr.move(6, 0)
        stdscr.clrtoeol()
        stdscr.addstr(6, 0, f"Vidas restantes: {lives}")
        stdscr.hline(7, 0, curses.ACS_HLINE, w)
        stdscr.refresh()

        hablar(f"Introduce el comando: {cmd}", esperar=False)

        correct = False
        while lives > 0 and not correct:
            update_timer_display(stdscr, start_time, 0)

            input_y = 8
            stdscr.move(input_y, 0)
            stdscr.clrtoeol()
            stdscr.addstr(input_y, 0, "> ")
            stdscr.refresh()
            user_input = text_input_field(stdscr, prompt="> ")

            if user_input.strip() == cmd.strip():
                stdscr.addstr(input_y+1, 0, "✅ Comando aceptado. Ejecutando...")
                stdscr.refresh()
                output = execute_and_show(stdscr, cmd)
                hablar("Comando procesado", esperar=False)

                stdscr.addstr(h-2, 0, "Presiona Enter para continuar...", curses.A_BOLD)
                stdscr.refresh()
                while True:
                    key = stdscr.getch()
                    if key == ord('\n'):
                        break
                correct = True
            else:
                stdscr.addstr(input_y+1, 0, "❌ Error: comando incorrecto.")
                stdscr.refresh()
                hablar("Error", esperar=False)
                lives -= 1
                time.sleep(1)
                stdscr.move(input_y+1, 0)
                stdscr.clrtoeol()
                stdscr.move(6, 0)
                stdscr.clrtoeol()
                stdscr.addstr(6, 0, f"Vidas restantes: {lives}")
                stdscr.refresh()

        if lives <= 0:
            failure_animation(stdscr)
            return False

    total_time = int(time.time() - start_time)
    final_report(stdscr, modalidad, filepath, total_time)
    return True

# --------------------------- Función principal ------------------------------
def iniciar(stdscr):
    """Función que debe ser llamada desde main.py: nivel3.iniciar(stdscr)"""
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    try:
        curses.start_color()
        curses.use_default_colors()
    except:
        pass

    while True:
        animate_start(stdscr)
        options = [
            "1. ExifTool (Análisis profundo multiplataforma)",
            "2. MediaInfo (Análisis rápido de multimedia)",
            "3. MAT2 (Anonimización y borrado de rastros)",
            "4. PDF Tools - pdfinfo/pdfid (Análisis forense de PDF)"
        ]
        current_opt = 0
        chosen = None
        while True:
            draw_menu(stdscr, options, current_opt)
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current_opt = (current_opt - 1) % len(options)
            elif key == curses.KEY_DOWN:
                current_opt = (current_opt + 1) % len(options)
            elif key == ord('\n'):
                chosen = current_opt + 1
                break
            elif key == 27:
                return

        filepath = file_explorer(stdscr, chosen)
        if filepath is None:
            continue

        # ========================= MISIONES EXPANDIDAS =========================
        if chosen == 1:  # ExifTool
            missions = [
                ("Ver todos los metadatos", f"exiftool {filepath}"),
                ("Buscar coordenadas GPS", f"exiftool -gps:all {filepath}"),
                ("Extraer información de cámara (fabricante, modelo, lente)", f"exiftool -make -model -lensid -lens {filepath}"),
                ("Mostrar fechas de creación y modificación", f"exiftool -createdate -modifydate -datetimeoriginal {filepath}"),
                ("Extraer metadatos XMP (Adobe, Dublin Core)", f"exiftool -xmp:all {filepath}"),
                ("Mostrar información de imagen (dimensiones, DPI, color)", f"exiftool -imagesize -xresolution -yresolution -colorspace {filepath}"),
                ("Extraer metadatos de copyright y autor", f"exiftool -copyright -artist -byline -creator {filepath}"),
                ("Listar todos los grupos de metadatos disponibles", f"exiftool -g {filepath}"),
                ("Mostrar solo metadatos EXIF", f"exiftool -exif:all {filepath}"),
                ("Mostrar metadatos en formato JSON (legible por máquina)", f"exiftool -j {filepath}"),
                ("Extraer thumbnail/ vista previa incrustada", f"exiftool -thumbnailimage -b {filepath}"),
                ("Borrar todos los metadatos (¡cuidado!)", f"exiftool -all= {filepath}"),
            ]
        elif chosen == 2:  # MediaInfo
            missions = [
                ("Resumen general del archivo multimedia", f"mediainfo {filepath}"),
                ("Información detallada y completa", f"mediainfo -f {filepath}"),
                ("Mostrar información en formato XML estructurado", f"mediainfo --Output=XML {filepath}"),
                ("Extraer solo información de video", f"mediainfo --Inform='Video;%CodecID%|%Format%|%Width%x%Height%|%FrameRate%|%BitRate%' {filepath}"),
                ("Extraer solo información de audio", f"mediainfo --Inform='Audio;%CodecID%|%Format%|%Channels%|%SamplingRate%|%BitRate%|%Language%' {filepath}"),
                ("Mostrar capítulos y estructura del contenedor", f"mediainfo --Inform='Menu;%Format%|%Chapters%' {filepath}"),
                ("Mostrar formato del contenedor y perfil", f"mediainfo --Inform='General;%Format%|%Format/Info%|%CodecID%|%FileSize%|%Duration%' {filepath}"),
                ("Extraer metadatos de pista de texto (subtítulos)", f"mediainfo --Inform='Text;%Format%|%Language%|%CodecID%' {filepath}"),
                ("Mostrar información en formato legible (viejo estilo)", f"mediainfo --Legacy {filepath}"),
                ("Verificar integridad y errores del archivo", f"mediainfo --LogFile=/dev/stdout {filepath}"),
            ]
        elif chosen == 3:  # MAT2
            missions = [
                ("Escanear metadatos sospechosos", f"mat2 -s {filepath}"),
                ("Generar copia anonimizada", f"mat2 {filepath}"),
            ]
        elif chosen == 4:  # PDF Tools
            missions = [
                ("Leer metadatos PDF (autor, fechas...)", f"pdfinfo {filepath}"),
                ("Escanear estructura PDF en busca de JavaScript/objetos maliciosos", f"pdfid {filepath}"),
            ]
        else:
            continue

        mission_loop(stdscr, missions, chosen, filepath)

if __name__ == "__main__":
    curses.wrapper(iniciar)