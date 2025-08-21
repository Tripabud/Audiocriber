# Aplicación de Transcripción de Audio con Streamlit

Esta es una aplicación web simple creada con Streamlit que permite a los usuarios subir un archivo de audio y obtener una transcripción de texto con diarización de hablantes (identificando quién habla).

La aplicación utiliza la API de AssemblyAI para el reconocimiento de voz.

## Prerrequisitos

Antes de empezar, asegúrate de tener lo siguiente instalado:

1.  **Python 3.8+**
2.  **FFmpeg**: Esta es una dependencia crucial para la biblioteca `pydub`, que se encarga de convertir diferentes formatos de audio a WAV. 
    -   **Windows**: Descárgalo desde [el sitio oficial de FFmpeg](https://ffmpeg.org/download.html) y añade la carpeta `bin` a tu PATH del sistema.
    -   **macOS**: `brew install ffmpeg`
    -   **Linux (Debian/Ubuntu)**: `sudo apt update && sudo apt install ffmpeg`

## Cómo Configurar y Ejecutar el Proyecto

### 1. Clona o descarga este repositorio

Crea una carpeta y guarda los archivos `app.py`, `requirements.txt` y `README.md` dentro.

### 2. Crea un Entorno Virtual

Es una buena práctica aislar las dependencias de tu proyecto.

```bash
python -m venv venv
```

Activa el entorno:
-   **Windows**: `venv\Scripts\activate`
-   **macOS/Linux**: `source venv/bin/activate`

### 3. Instala las Dependencias

Con tu entorno virtual activado, instala las bibliotecas necesarias:

```bash
pip install -r requirements.txt
```

### 4. Configura tu Clave de API de AssemblyAI

La aplicación necesita una clave de API para comunicarse con AssemblyAI.

1.  **Obtén una clave**: Regístrate gratis en [AssemblyAI](https://www.assemblyai.com/dashboard/signup) para obtener tu clave de API.
2.  **Establece la variable de entorno**: La forma más segura de manejar tu clave es a través de una variable de entorno llamada `ASSEMBLYAI_API_KEY`.

    -   **Windows (PowerShell)**:
        ```powershell
        $env:ASSEMBLYAI_API_KEY="TU_CLAVE_AQUI"
        ```
        *(Nota: Para que sea permanente, búscala en "Editar las variables de entorno del sistema")*

    -   **macOS/Linux**:
        ```bash
        export ASSEMBLYAI_API_KEY="TU_CLAVE_AQUI"
        ```
        *(Añade esta línea a tu `.bashrc` o `.zshrc` para que sea permanente)*

### 5. Ejecuta la Aplicación Streamlit

Una vez que todo está configurado, ejecuta el siguiente comando en tu terminal:

```bash
streamlit run app.py
```

Se abrirá una nueva pestaña en tu navegador con la aplicación en funcionamiento.
