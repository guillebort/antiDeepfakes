const contenedorInicio = document.getElementById('contenedor-inicio');
const consolaResultados = document.getElementById('consola-resultados');
const btnGrabar = document.getElementById('btn-grabar');
const btnReiniciar = document.getElementById('btn-reiniciar');
let fragmentosAudio = [];

// grabar
btnGrabar.addEventListener('click', async () => {
    btnGrabar.disabled = true; 
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = evento => fragmentosAudio.push(evento.data);
        
        mediaRecorder.onstop = async () => {
            contenedorInicio.style.display = "none";
            
            consolaResultados.style.display = "block";
            consolaResultados.innerHTML = "<h2>Analizando espectro de audio...</h2><p>El servidor IA está procesando la señal.</p>";
            
            const archivoAudio = new Blob(fragmentosAudio, { type: 'audio/webm' });
            fragmentosAudio = []; 
            const formData = new FormData();
            formData.append("file", archivoAudio, "grabacion.webm");

            try {
                const respuesta = await fetch("http://127.0.0.1:8000/scan-audio", {
                    method: "POST",
                    body: formData
                });

                if (!respuesta.ok) throw new Error(`Error del servidor: ${respuesta.status}`);

                const resultadoIA = await respuesta.json();
                let resultados = resultadoIA.analysis_results || resultadoIA; 
                if (!Array.isArray(resultados)) resultados = [resultados];

                const topResultado = resultados[0];
                const etiqueta = topResultado.label ? topResultado.label.toLowerCase() : "desconocido";
                const probabilidad = topResultado.score ? (topResultado.score * 100).toFixed(1) : "0";

                let mensajeFinal = "";
                
                // mostramos el resultado
                if (etiqueta.includes("spoof") || etiqueta.includes("fake")) {
                    mensajeFinal = `
                        <div style="color: #d63031;">
                            <h1 style="font-size: 40px; margin: 0;">DEEPFAKE DETECTADO</h1>
                            <p style="font-size: 22px; color: #333;">Probabilidad de voz sintética generada por IA:</p>
                            <h2 style="font-size: 48px; margin: 10px 0;">${probabilidad}%</h2>
                        </div>
                    `;
                } else if (etiqueta.includes("bonafide") || etiqueta.includes("real")) {
                    mensajeFinal = `
                        <div style="color: #27ae60;">
                            <h1 style="font-size: 40px; margin: 0;">VOZ HUMANA</h1>
                            <p style="font-size: 22px; color: #333;">Probabilidad de voz auténtica:</p>
                            <h2 style="font-size: 48px; margin: 10px 0;">${probabilidad}%</h2>
                        </div>
                    `;
                } else {
                    mensajeFinal = `
                        <div style="color: #2980b9;">
                            <h1 style="font-size: 40px; margin: 0;">Veredicto: ${topResultado.label || 'Desconocido'}</h1>
                            <p style="font-size: 22px; color: #333;">Nivel de confianza:</p>
                            <h2 style="font-size: 48px; margin: 10px 0;">${probabilidad}%</h2>
                        </div>
                    `;
                }
                
                consolaResultados.innerHTML = mensajeFinal;
                
                btnReiniciar.style.display = "block";

            } catch (error) {
                consolaResultados.innerHTML = `<h2 style="color: #d63031;">Fallo de conexión</h2><p>${error.message}</p>`;
                btnReiniciar.style.display = "block";
            }
        };

        mediaRecorder.start();
        btnGrabar.textContent = "Grabando (3s)...";
        btnGrabar.classList.add("grabando");

        setTimeout(() => {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop()); 
        }, 3000);

    } catch (error) {
        alert(`Fallo al iniciar el micrófono: ${error.message}`);
    }
});

// accion al reiniciar
btnReiniciar.addEventListener('click', () => {
    btnReiniciar.style.display = "none";
    consolaResultados.style.display = "none";
    contenedorInicio.style.display = "block";
    
    btnGrabar.textContent = "🎙️ Iniciar Escaneo";
    btnGrabar.classList.remove("grabando");
    btnGrabar.disabled = false; 
});
