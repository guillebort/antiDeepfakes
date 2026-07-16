from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from transformers import pipeline
import shutil
import os

app = FastAPI(
    title="Shield AI - Deepfake Audio Detector",
    description="API de microservicios para analizar espectrogramas y detectar voz sintética."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir conexiones desde cualquier puerto 
    allow_credentials=True,
    allow_methods=["*"],  # Permitir métodos GET, POST, etc.
    allow_headers=["*"],  # Permitir el envío de archivos 
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
    # validar que solo nos envíen audio
    extensiones_permitidas = ('.wav', '.mp3', '.flac')
    if not (file.filename.endswith(".wav") or file.filename.endswith(".mp3") or file.filename.endswith(".flac") or file.filename.endswith(".webm")):
        raise HTTPException(status_code=400, detail="Formato bloqueado. Solo se permite WAV, MP3, FLAC o WEBM.")
    
    # descargar el archivo de la red a la memoria del servidor
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    print(f"\n[RED] -> Recibido archivo binario: {file.filename}")
    print("[IA] -> Extrayendo características y analizando espectro...")
    
    try:
        # la ia procesa el archivo de audio
        # El modelo analiza las frecuencias y devuelve sus predicciones
        resultados = audio_classifier(temp_file_path)
        
        #Borramos el archivo del servidor para no saturar el disco
        os.remove(temp_file_path)
        
        print("[IA] -> Análisis completado con éxito.")
        
        # Imprimimos los resultados en la terminal 
        print("\n" + "="*50)
        print(f"VEREDICTO DE LA IA:")
        print(resultados)
        print("="*50 + "\n")
        
        # Estructuramos la respuesta
        return {
            "status": "success",
            "file_scanned": file.filename,
            "analysis_results": resultados
        }
        
    except Exception as e:
        # Limpieza del archivo temporal
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        #Imprimimos el error exacto en la terminal para poder diagnosticarlo
        import traceback
        print("\n[ERROR CRÍTICO EN LA IA] Detalles del fallo:")
        traceback.print_exc()
        print("-" * 50)
        
        raise HTTPException(status_code=500, detail=str(e))
