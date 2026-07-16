from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. Añade esta importación
from transformers import pipeline
import shutil
import os

app = FastAPI(
    title="Shield AI - Deepfake Audio Detector",
    description="API de microservicios para analizar espectrogramas y detectar voz sintética."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conexiones desde cualquier puerto (ej. tu web en 5500)
    allow_credentials=True,
    allow_methods=["*"],  # Permite métodos GET, POST, etc.
    allow_headers=["*"],  # Permite el envío de archivos (multipart/form-data)
)

print("Cargando motor de análisis espectral de audio...")
# Inicializamos el modelo de IA capaz de procesar señales de audio
audio_classifier = pipeline(
    "audio-classification", 
    model="Vansh180/deepfake-audio-wav2vec2"
)
print("Motor IA listo y a la escucha.")

@app.post("/scan-audio")
async def scan_audio_file(file: UploadFile = File(...)):
    # 1. Bloque de seguridad: Validar que solo nos envíen audio
    extensiones_permitidas = ('.wav', '.mp3', '.flac')
    if not (file.filename.endswith(".wav") or file.filename.endswith(".mp3") or file.filename.endswith(".flac") or file.filename.endswith(".webm")):
        raise HTTPException(status_code=400, detail="Formato bloqueado. Solo se permite WAV, MP3, FLAC o WEBM.")
    
    # 2. Descargar el archivo de la red a la memoria del servidor
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    print(f"\n[RED] -> Recibido archivo binario: {file.filename}")
    print("[IA] -> Extrayendo características y analizando espectro...")
    
    try:
        # 3. La IA procesa el archivo de audio
        # El modelo analiza las frecuencias y devuelve sus predicciones
        resultados = audio_classifier(temp_file_path)
        
        # 4. Limpieza: Borramos el archivo del servidor para no saturar el disco
        os.remove(temp_file_path)
        
        print("[IA] -> Análisis completado con éxito.")
        
        # 👇 CHIVATO AÑADIDO: Imprimir resultados en la terminal 👇
        print("\n" + "="*50)
        print(f"🧠 VEREDICTO DE LA IA:")
        print(resultados)
        print("="*50 + "\n")
        # 👆 ================================================== 👆
        
        # 5. Estructuramos la respuesta para el cliente
        return {
            "status": "success",
            "file_scanned": file.filename,
            "analysis_results": resultados
        }
        
    except Exception as e:
        # Limpieza del archivo temporal
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        # ¡NUEVO! Imprimir el error exacto en la terminal para poder diagnosticarlo
        import traceback
        print("\n❌ [ERROR CRÍTICO EN LA IA] Detalles del fallo:")
        traceback.print_exc()
        print("-" * 50)
        
        raise HTTPException(status_code=500, detail=str(e))