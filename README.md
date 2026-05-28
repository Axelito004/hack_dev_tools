# 🛡️ Kali Academy Tactical Simulator

[![Estado](https://img.shields.io/badge/Estado-Operativo-green.svg)]()
[![Plataforma](https://img.shields.io/badge/Plataforma-Kali_Linux-blue.svg)]()
[![Licencia](https://img.shields.io/badge/Licencia-Educativa-orange.svg)]()

**Kali Academy** es un entorno interactivo y táctico desarrollado en Python para el entrenamiento de operadores en ciberseguridad, administración de sistemas y respuesta a incidentes. A través de una interfaz de terminal inmersiva (TUI) y un motor de voz de IA, los estudiantes aprenden y ejecutan comandos reales en un entorno controlado y auditable.

Desarrollado para la capacitación técnica en **FUNDACITE Yaracuy** / **Laboratorio Interactivo Arístides Bastidas**.

---

## 🚀 Módulos de Entrenamiento (El Plan de Estudios)

El simulador cuenta con 4 niveles de progresión táctica, diseñados para llevar al estudiante desde cero hasta la auditoría avanzada:

### 🟢 Nivel 1: Entrenamiento Básico (Bash y Sistema)
* **Objetivo:** Dominio de la terminal de Linux, navegación, permisos y gestión de procesos.
* **Mecánicas:** Modos de juego clásico, contrarreloj (muerte súbita) y "A ciegas" (entrenamiento auditivo puro).

### 🟡 Nivel 2: Entrenamiento en BASH (SANBOX)
* **Objetivo:** pONER EN PRACTICA LOS COMANDOS DE TERMINAL APRENDIDOS EN EL MODULO UNI
* **Mecánicas:** Simulador de practica de ejecucion de comandos bajo presión de tiempo con límite de 10 vidas.

### 🟠 Nivel 3: Análisis Forense de Archivos
* **Objetivo:** Análisis profundo de metadatos en archivos reales (Imágenes, PDF, Multimedia) y respuesta a incidentes.
* **Mecánicas:** Explorador de archivos integrado. Ejecución **real** sobre los archivos del usuario en un entorno aislado (`/tmp/academia_sandbox`).
* **Herramientas dominadas:** `exiftool`, `mat2` (Anonimización), `mediainfo`, `pdfinfo` y `pdfid`.

### 🔴 Nivel 4: Análisis forense de redes y tráfico
* **Objetivo:** Reconocimiento avanzado de redes, descubrimiento de hosts, escaneo de vulnerabilidades e intercepción de paquetes.
* **Mecánicas:** Fase 0 obligatoria para identificar el rango de red (`ip a`). Ejecución real contra equipos de la LAN con reportes capturados en pantalla.
* **Herramientas dominadas:** `nmap` (12 comandos tácticos), `arp-scan` (Capa 2), `tcpdump` (Sniffing crudo).

---

## 🛠️ Requisitos y Dependencias

Para que el simulador ejecute comandos reales, procese el audio y formatee la pantalla, el sistema anfitrión (Kali Linux / Debian) debe tener instaladas las siguientes herramientas:

### 1. Dependencias del Sistema Operativo
Abre tu terminal y ejecuta este comando para instalar todas las herramientas forenses y de red necesarias:
```bash
sudo apt update -y

sudo apt update --fix-missing

sudo apt install -y exiftool mediainfo mat2 poppler-utils pdfid mpg123

sudo apt install -y espeak-ng binwalk foremost python3-pip

pip install pyttsx3 --break-system-packages 2>/dev/null || pip3 install pyttsx3 2>/dev/null
sudo apt-get install mpg123
pip install gTTS --break-system-packages
sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install gtts
pipx install edge-tts

git clone [https://github.com/Axelito004/hack_dev_tools.git](https://github.com/Axelito004/hack_dev_tools.git)
```
## 👾 PARA EJECUTAR 

```bash
# 1. Entrar al directorio del proyecto
cd hack_dev_tools

# 2. Para ejecutar programa
sudo python3 main.py

```
## ⚠️ Advertencia Legal, Términos de Uso y Exención de Responsabilidad

**LEER DETENIDAMENTE ANTES DE CLONAR, INSTALAR O EJECUTAR ESTE SOFTWARE.**

Este proyecto, **Kali Academy Tactical Simulator**, junto con todos sus módulos, scripts y técnicas documentadas, ha sido desarrollado **exclusivamente con fines académicos, de investigación y formación profesional** en ciberseguridad, respuesta a incidentes (Blue Teaming) y Hacking Ético.

Al descargar o utilizar esta herramienta, usted (el Usuario) acepta incondicionalmente los siguientes términos:

1. **Propósito Estrictamente Educativo:** El software incluye la automatización de herramientas reales de escaneo de redes, intercepción de tráfico y ejecución de payloads. Su único objetivo es enseñar a los operadores cómo defenderse contra estas técnicas entendiendo cómo funcionan.
2. **Exención Absoluta de Responsabilidad:** Los desarrolladores (Ing. Josué Ordóñez, A.G. Castillo Giménez), el Laboratorio Interactivo Arístides Bastidas, FUNDACITE Yaracuy, y cualquier entidad u organización afiliada **NO ASUMEN NINGUNA RESPONSABILIDAD** directa, indirecta, penal, civil, incidental o consecuente por el uso, mal uso, o incapacidad de uso de esta herramienta.
3. **Responsabilidad Exclusiva del Usuario:** El usuario asume el 100% de la responsabilidad por sus acciones. El usuario garantiza y se compromete a que **solo ejecutará estos módulos en entornos controlados (Sandboxes) o en redes, dispositivos y sistemas sobre los cuales tiene propiedad absoluta o autorización explícita y por escrito** para auditar.
4. **Cumplimiento de la Ley:** El uso de herramientas de escaneo (como Nmap o arp-scan) o la interceptación de tráfico (tcpdump) contra infraestructuras de terceros sin consentimiento es un delito tipificado en las leyes nacionales e internacionales de delitos informáticos.
5. **Condición "Tal Cual" (As-Is):** Este software se proporciona "tal cual", sin garantías de ningún tipo, expresas o implícitas. Los creadores no garantizan que el código esté libre de errores o que su ejecución no pueda causar alteraciones no deseadas, pérdida temporal de conectividad o pérdida de datos en el sistema anfitrión.

**Si no está de acuerdo con estos términos, debe eliminar inmediatamente cualquier copia de este código de sus sistemas.**

## 👨‍💻 **Creadores:** 
- Ing. Josué Ordóñez (TUTOR) & (AXL-HACKING)A.G. Castillo Giménez (DESARROLLADOR) | Laboratorio Interactivo Arístides Bastidas (FUNDACITE Yaracuy).

## 📖 **Documentación:** [Leer el Manual de Usuario detallado aquí](#) *(Enlace disponible próximamente)*
