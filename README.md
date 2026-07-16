**Shield AI - Detector de Deepfakes de Audio**

  Shield AI es una herramienta cliente-servidor diseñada para analizar grabaciones de voz en tiempo real y detectar si el audio pertenece a un humano o ha sido generado sintéticamente por una Inteligencia Artificial.
  El proyecto utiliza un motor de análisis espectral impulsado por redes neuronales a través de Hugging Face y está estructurado para poder integrarse como una extensión de navegador web.

**Características principales**

  Captura de audio en tiempo real: Grabación nativa desde el navegador usando MediaRecorder.

Análisis con IA: Integración del modelo pre-entrenado Vansh180/deepfake-audio-wav2vec2 especializado en clasificación de audio.

Microservicio backend: API construida con FastAPI para la recepción, procesamiento y limpieza de los archivos multimedia.

Interfaz asíncrona: Arquitectura de frontend dividida (HTML, CSS, JS) preparada para compilarse como extensión de Google Chrome/Microsoft Edge.

**Requisitos previos**

Para ejecutar este proyecto en tu máquina local, necesitarás tener instalado:

Python 3.8 o superior.

Gestor de paquetes pip.

**Instalación y Dependencias**

Es muy recomendable utilizar un entorno virtual para no crear conflictos con otros proyectos de Python en tu sistema.

Clonar el repositorio:

git clone https://github.com/guillebort/antiDeepfakes.git
cd antiDeepfakes

Crear y activar un entorno virtual (Opcional pero recomendado):

En Windows:

python -m venv venv
venv\Scripts\activate

En macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Instalar las librerías necesarias:
Ejecuta el siguiente comando para instalar el framework web, el servidor y las herramientas de Inteligencia Artificial (PyTorch y Transformers):

pip install fastapi uvicorn transformers torch python-multipart

Nota: python-multipart es estrictamente necesario para que FastAPI pueda procesar y entender los archivos de audio .webm que envía el navegador web.

**Cómo ejecutar el proyecto**

La arquitectura de este proyecto es cliente-servidor, lo que significa que requiere levantar dos procesos independientes: el "cerebro" (Backend IA) y la "cara" (Frontend Web).

Necesitarás abrir dos terminales distintas, ambas ubicadas en la raíz de la carpeta del proyecto.

**1. Iniciar el Servidor de IA (Backend)**

En tu primera terminal, levanta la API de FastAPI ejecutando:

python -m uvicorn main:app --reload

El parámetro --reload reiniciará el servidor automáticamente si haces cambios en el archivo main.py.

Sabrás que el motor está activo cuando la consola imprima: Motor IA listo y a la escucha y confirme que está operando en el puerto 8000.

**2️. Iniciar la Interfaz Web (Frontend)**

IMPORTANTE: Evita utilizar extensiones como Live Server de Visual Studio Code. Estas herramientas vigilan la carpeta y, al detectar los archivos de audio temporales que crea la IA al analizar, recargarán tu página web automáticamente, destruyendo los resultados en pantalla.

Para evitar este problema, en tu segunda terminal, levanta un servidor estático nativo utilizando Python:

python -m http.server 5500


**3. Realizar tu primer escaneo**

Abre tu navegador web preferido (Chrome, Edge, Brave...).

Accede a la URL local: http://localhost:5500/popup.html

Concede los permisos de micrófono cuando el navegador te lo solicite.

Haz clic en  "Iniciar Escaneo", habla durante 3 segundos y revisa el veredicto en la pantalla (puedes ver los datos matemáticos crudos en la terminal de tu Backend).

**Estructura del proyecto**

main.py - Microservicio backend con FastAPI y lógica del modelo Wav2Vec2.

popup.html - Estructura visual de la interfaz del cliente.

style.css - Estilos y animaciones de la interfaz.

popup.js - Lógica de grabación, manejo del DOM y peticiones fetch asíncronas.

README.md - Documentación del proyecto.

**Autor**

Guillermo Bort Hurtado
