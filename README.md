# Classroom Feedback App

Esta aplicación permite simular un salón de clases donde cada estudiante, con una personalidad y gustos definidos, proporciona retroalimentación sobre cómo le gustaría aprender un tema específico.
Utiliza la API de OpenAI para generar las respuestas de los estudiantes.

## Configuración

1.  Clona este repositorio (una vez que lo subas a GitHub).
2.  Crea un entorno virtual e instala las dependencias:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  (Recomendado) Configura tu clave de API de OpenAI como una variable de entorno llamada `OPENAI_API_KEY`.
    *   En Windows (PowerShell): `$env:OPENAI_API_KEY="tu_clave_aqui"`
    *   En Linux/macOS: `export OPENAI_API_KEY="tu_clave_aqui"`
    *   Asegúrate de reemplazar `"tu_clave_aqui"` con tu clave real.
4.  Ejecuta la aplicación: `python classroom_app.py`

## Uso

-   Agrega estudiantes con sus perfiles.
-   Introduce un tema de aprendizaje.
-   Observa la retroalimentación personalizada de cada estudiante.

## Advertencia de Seguridad de la API Key

NO subas tu clave de API de OpenAI directamente en el código a repositorios públicos como GitHub. Utiliza variables de entorno como se describe en la sección de configuración. El script `classroom_app.py` incluye advertencias y un ejemplo de cómo cargar la clave desde una variable de entorno.
