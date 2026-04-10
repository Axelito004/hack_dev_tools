import pyttsx3

def probar_sistema():
    print("[*] Iniciando prueba de voz...")
    try:
        engine = pyttsx3.init()
        
        # Listar voces disponibles
        voices = engine.getProperty('voices')
        print(f"[*] Voces encontradas: {len(voices)}")
        
        for index, voice in enumerate(voices):
            print(f"    - Voz {index}: {voice.name} [{voice.languages}]")

        msg = "Probando sistema de audio de la UNEFA. Acceso autorizado."
        print(f"[*] Intentando decir: '{msg}'")
        
        engine.say(msg)
        engine.runAndWait()
        print("[+] Prueba finalizada sin errores.")
        
    except Exception as e:
        print(f"[!] ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    probar_sistema()