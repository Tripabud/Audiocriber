
import streamlit as st
import assemblyai as aai
import os
import tempfile
from pydub import AudioSegment

# --- CONFIGURACIÓN INICIAL ---

# Título de la página y favicon
st.set_page_config(page_title="Transcripción de Audio", page_icon="🎙️")

# Leer la clave de API desde los secretos de Streamlit o una variable de entorno
# Es la forma más segura de manejar claves de API.
# Importar el tipo de error específico de Streamlit
from streamlit.errors import StreamlitAPIException

try:
    # Intenta obtener la clave desde los secretos de Streamlit (para despliegue en la nube)
    aai.settings.api_key = st.secrets["ASSEMBLYAI_API_KEY"]
except (KeyError, StreamlitAPIException):
    # Si falla (porque el archivo no existe localmente o la clave no está),
    # usa la variable de entorno como alternativa.
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# --- INTERFAZ DE USUARIO ---

st.title("🎙️ Transcripción de Audio con Diarización")

# --- ESTILOS CSS MODERNOS (TEMA OSCURO) ---
st.markdown("""    
<style>
/* Color de fondo principal */
.stApp {
    background-color: #0f172a; /* Azul noche */
}

/* Color y fuente del título principal */
h1 {
    color: #f8fafc; /* Blanco casi puro */
    font-family: 'sans-serif';
}

/* Estilo de botones */
.stButton>button {
    color: #f8fafc; /* Texto blanco */
    background-color: #2563eb; /* Azul vibrante */
    border-radius: 8px;
    border: none;
    padding: 12px 24px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #1d4ed8; /* Azul más oscuro al pasar el mouse */
}

/* Estilo del área de texto de la transcripción */
.stTextArea textarea {
    background-color: #1e293b; /* Azul-gris oscuro */
    color: #e2e8f0; /* Gris claro */
    border-radius: 8px;
    border: 1px solid #334155;
    font-size: 16px;
}

/* Estilo del file uploader */
.stFileUploader label {
    color: #cbd5e1; /* Gris azulado */
    font-size: 18px;
    font-weight: bold;
}

/* Ocultar el menú de hamburguesa de Streamlit y el footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# Comprobar si la clave de API está configurada
if not aai.settings.api_key:
    st.error("¡Clave de API de AssemblyAI no encontrada! Por favor, configúrala como se indica en el README.")
    st.stop()

# Componente para subir archivos
uploaded_file = st.file_uploader(
    "Elige un archivo de audio...",
    type=['wav', 'mp3', 'm4a', 'opus', 'ogg', 'flac', 'aac']
)

# Almacenar la transcripción en el estado de la sesión para que persista
if 'transcription_result' not in st.session_state:
    st.session_state['transcription_result'] = None

if uploaded_file is not None:
    # Usar un spinner para dar feedback al usuario durante el procesamiento
    with st.spinner('Procesando audio y transcribiendo... Esto puede tardar unos minutos.'):
        try:
            # Crear un archivo temporal para trabajar con él de forma segura
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # --- PROCESAMIENTO DE AUDIO ---
            # Convertir el audio a formato WAV si no lo es, ya que es un estándar robusto.
            # Pydub necesita la ruta del archivo para una conversión fiable.
            st.write("Convirtiendo audio a formato WAV (si es necesario).")
            audio = AudioSegment.from_file(tmp_file_path)
            
            # Guardar el audio convertido en otro archivo temporal WAV
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp_file:
                audio.export(wav_tmp_file.name, format="wav")
                wav_file_path = wav_tmp_file.name

            # --- TRANSCRIPCIÓN CON DIARIZACIÓN ---
            st.write("Enviando a la API de AssemblyAI para transcripción.")
            transcriber = aai.Transcriber()
            
            # Configurar la transcripción para que identifique hablantes y MEJORE LA PRECISIÓN
            config = aai.TranscriptionConfig(
                speaker_labels=True,
                language_code="es",  # ¡IMPORTANTE! Especifica el idioma del audio
                punctuate=True,      # Habilita la puntuación automática
                format_text=True     # Habilita el formateo de texto (ej. números)
            )

            # Realizar la transcripción
            transcript = transcriber.transcribe(wav_file_path, config)

            # --- MANEJO DE RESPUESTA ---
            if transcript.status == aai.TranscriptStatus.error:
                st.error(f"Error en la transcripción: {transcript.error}")
                st.session_state['transcription_result'] = None
            else:
                st.write("¡Transcripción completada!")
                # Formatear la salida con etiquetas de hablante
                lines = []
                for utterance in transcript.utterances:
                    # El nombre del hablante es una letra (A, B, C...)
                    speaker_label = f"Hablante {utterance.speaker}"
                    lines.append(f"{speaker_label}: {utterance.text}")
                
                st.session_state['transcription_result'] = "\n".join(lines)

        except Exception as e:
            st.error(f"Ha ocurrido un error inesperado: {e}")
            st.session_state['transcription_result'] = None
        finally:
            # Limpiar los archivos temporales
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
            if 'wav_file_path' in locals() and os.path.exists(wav_file_path):
                os.remove(wav_file_path)

# Mostrar la transcripción y el botón de descarga si existe un resultado
if st.session_state['transcription_result']:
    st.subheader("Transcripción Completa")
    st.text_area("Resultado", st.session_state['transcription_result'], height=300)

    # Botón para descargar el archivo .txt
    st.download_button(
        label="📥 Guardar Transcripción (.txt)",
        data=st.session_state['transcription_result'],
        file_name=f"{uploaded_file.name.split('.')[0]}_transcripcion.txt",
        mime="text/plain"
    )
