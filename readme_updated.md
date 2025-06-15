# 🏫 Salón de Clases Virtual - Sistema de Gestión Estudiantil

Una aplicación completa para simular un salón de clases donde cada estudiante, con personalidad y gustos únicos, recibe retroalimentación personalizada sobre temas de aprendizaje. La aplicación utiliza la API de OpenAI para generar respuestas inteligentes y cuenta con un sistema completo de gestión estudiantil.

## ✨ Características Principales

- **🎫 Sistema de Matrícula Automática**: Cada estudiante recibe una matrícula única (formato EST-XXXXX)
- **🪑 Gestión Visual de Asientos**: Interfaz gráfica que simula un salón real con asientos interactivos
- **🧠 Retroalimentación Personalizada**: Utiliza OpenAI para generar respuestas adaptadas a cada estudiante
- **📚 Historial Completo**: Guarda todo el historial de retroalimentación por estudiante
- **💾 Base de Datos Persistente**: Toda la información se guarda automáticamente en SQLite
- **📊 Estadísticas del Sistema**: Visualiza métricas de uso y ocupación

## 🔧 Requisitos del Sistema

- Python 3.10 o superior
- Clave API de OpenAI
- Bibliotecas: `openai`, `tkinter`, `sqlite3`

## 🚀 Instalación y Configuración

1. Clona este repositorio.
2. Crea un entorno virtual e instala las dependencias:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements_updated.txt
    ```
3. Configura la clave de API de OpenAI en la variable de entorno `OPENAI_API_KEY`.
    * Windows (PowerShell): `$env:OPENAI_API_KEY="tu_clave_aqui"`
    * Linux/macOS: `export OPENAI_API_KEY="tu_clave_aqui"`
4. Inicia la aplicación desde la línea de comandos:
    `python classroom_app.py`
5. Si prefieres una interfaz con asientos y control visual, ejecuta:
    `python enhanced_classroom_gui.py`

## 🖥️ Uso Básico

- Agrega o edita estudiantes con sus perfiles.
- Selecciona un tema de aprendizaje.
- Consulta la retroalimentación generada para cada estudiante.
- Revisa el historial y las métricas en la interfaz gráfica.

## 🔐 Advertencia de Seguridad

No incluyas tu clave de API de OpenAI en repositorios públicos. Utiliza siempre variables de entorno para mantenerla privada.
