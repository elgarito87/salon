# Classroom Feedback App

Esta aplicación permite simular un salón de clases donde cada estudiante, con una personalidad y gustos definidos, proporciona retroalimentación sobre cómo le gustaría aprender un tema específico.
Utiliza la API de OpenAI para generar las respuestas de los estudiantes.
Los perfiles de los alumnos ahora se guardan en una base de datos
`SQLite` llamada `students.db`.
El módulo `student_db.py` crea esta base de datos de forma automática la primera
vez que ejecutes la aplicación.

La aplicación se ha probado con Python 3.10 como versión mínima recomendada.

## Configuración

1.  Clona este repositorio (una vez que lo subas a GitHub).
2.  Crea un entorno virtual e instala las dependencias:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  Configura tu clave de API de OpenAI como una variable de entorno llamada `OPENAI_API_KEY` (obligatorio). La aplicación no se ejecutará si no la proporcionas.
    *   En Windows (PowerShell): `$env:OPENAI_API_KEY="tu_clave_aqui"`
    *   En Linux/macOS: `export OPENAI_API_KEY="tu_clave_aqui"`
    *   Asegúrate de reemplazar `"tu_clave_aqui"` con tu clave real.
4.  Ejecuta la aplicación: `python classroom_app.py`
5.  Para una interfaz gráfica sencilla de captura de estudiantes, ejecuta
    `python student_gui.py`.
6.  Para una interfaz con asientos interactivos y generación de
    retroalimentación, ejecuta
    `python classroom_seating_gui.py`.

## Uso

-   Agrega estudiantes con sus perfiles.
-   Introduce un tema de aprendizaje.
-   Observa la retroalimentación personalizada de cada estudiante.

## Advertencia de Seguridad de la API Key

NO subas tu clave de API de OpenAI directamente en el código a repositorios públicos como GitHub. Utiliza variables de entorno como se describe en la sección de configuración. El script `classroom_app.py` incluye advertencias y un ejemplo de cómo cargar la clave desde una variable de entorno.
