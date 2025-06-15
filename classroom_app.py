import openai
import json
import os

# --- Configuración de la API de OpenAI ---
# ADVERTENCIA DE SEGURIDAD IMPORTANTE:
# La clave API proporcionada se usa aquí temporalmente para desarrollo.
# ¡NO SUBAS ESTA CLAVE A GITHUB DIRECTAMENTE EN EL CÓDIGO!
# Utiliza variables de entorno para producción y repositorios públicos.

# Intenta cargar la clave desde una variable de entorno primero (RECOMENDADO)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    # Si no se encuentra en variable de entorno, usa la clave proporcionada
    # SOLO PARA DESARROLLO LOCAL Y CON CONOCIMIENTO DEL RIESGO.
    # REEMPLAZA ESTO ANTES DE COMPARTIR O SUBIR A GITHUB.
    PROVIDED_API_KEY = "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" # Clave proporcionada por el USER
    print("--------------------------------------------------------------------------------")
    print("ADVERTENCIA DE SEGURIDAD MUY IMPORTANTE:")
    print("Estás utilizando una clave API de OpenAI directamente en el código.")
    print("Esto es EXTREMADAMENTE INSEGURO si este código se comparte o sube a GitHub.")
    print("La clave podría ser robada y usada maliciosamente, generando costos para ti.")
    print("POR FAVOR, configura la variable de entorno OPENAI_API_KEY y elimina la clave del código.")
    print("Ejemplo en PowerShell: $env:OPENAI_API_KEY=\"tu_clave_real_aqui\"")
    print("Ejemplo en bash/zsh: export OPENAI_API_KEY=\"tu_clave_real_aqui\"")
    print("El script continuará usando la clave hardcodeada por ahora, bajo tu responsabilidad.")
    print("--------------------------------------------------------------------------------\n")
    OPENAI_API_KEY = PROVIDED_API_KEY
else:
    print("Clave API de OpenAI cargada desde la variable de entorno OPENAI_API_KEY.")

if not OPENAI_API_KEY:
    print("Error fatal: No se pudo obtener la clave API de OpenAI.")
    print("Configura la variable de entorno OPENAI_API_KEY o asegúrate de que la clave esté disponible.")
    exit()

try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    # Prueba de conexión simple para validar la clave
    client.models.list()
    print("Conexión con OpenAI establecida y clave API validada.")
except openai.AuthenticationError:
    print("--------------------------------------------------------------------------------")
    print("Error de Autenticación con OpenAI:")
    print("La clave API proporcionada o configurada no es válida o ha caducado.")
    print("Por favor, verifica tu clave API de OpenAI.")
    print("Puedes obtener una nueva clave desde https://platform.openai.com/api-keys")
    print("Asegúrate de que la clave tenga los permisos necesarios y fondos suficientes si aplica.")
    print("--------------------------------------------------------------------------------")
    exit()
except Exception as e:
    print(f"Error inesperado al inicializar el cliente de OpenAI: {e}")
    exit()


STUDENTS_FILE = "students.json"
MAX_STUDENTS = 0 # 0 significa sin límite, se puede cambiar

def load_students():
    """Carga los estudiantes desde el archivo JSON."""
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Advertencia: El archivo {STUDENTS_FILE} está corrupto o no es un JSON válido. Empezando con una lista vacía.")
        return []

def save_students(students):
    """Guarda los estudiantes en el archivo JSON."""
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=4, ensure_ascii=False)

def add_student(students_list):
    """Agrega un nuevo estudiante a la lista."""
    global MAX_STUDENTS
    if MAX_STUDENTS > 0 and len(students_list) >= MAX_STUDENTS:
        print(f"Se ha alcanzado el número máximo de estudiantes ({MAX_STUDENTS}). No se pueden agregar más.")
        return

    print("\n--- Agregar Nuevo Estudiante ---")
    name = input("Nombre del estudiante: ").strip()
    if not name:
        print("El nombre no puede estar vacío.")
        return

    if any(s['name'].lower() == name.lower() for s in students_list):
        print(f"Error: Ya existe un estudiante con el nombre '{name}'. Los nombres deben ser únicos.")
        return

    personality = input("Personalidad (ej: curioso, analítico, creativo, escéptico): ").strip()
    tastes = input("Gustos (ej: videojuegos, lectura de ciencia ficción, debates filosóficos): ").strip()
    extra_info = input("Información extra (opcional): ").strip()

    students_list.append({
        "name": name,
        "personality": personality,
        "tastes": tastes,
        "extra_info": extra_info
    })
    save_students(students_list)
    print(f"Estudiante '{name}' agregado exitosamente.")

def view_students(students_list):
    """Muestra la lista de estudiantes."""
    if not students_list:
        print("\nNo hay estudiantes registrados.")
        return
    print("\n--- Lista de Estudiantes ---")
    for i, student in enumerate(students_list):
        print(f"{i+1}. Nombre: {student['name']}")
        print(f"   Personalidad: {student['personality']}")
        print(f"   Gustos: {student['tastes']}")
        if student['extra_info']:
            print(f"   Extra: {student['extra_info']}")
        print("-" * 20)

def get_feedback_from_student(student, topic):
    """Obtiene retroalimentación de un estudiante sobre un tema usando OpenAI."""
    prompt_messages = [
        {"role": "system", "content": f"Eres un estudiante llamado {student['name']}. Tu personalidad es '{student['personality']}' y tus gustos principales son '{student['tastes']}'. {('Información adicional sobre ti: ' + student['extra_info']) if student['extra_info'] else ''} Debes responder en primera persona desde la perspectiva de {student['name']}."},
        {"role": "user", "content": f"El tema que se va a enseñar es: \"{topic}\". Considerando tu personalidad y gustos, ¿cómo te gustaría que te enseñaran este tema? Describe tu método de aprendizaje ideal para \"{topic}\", qué tipo de actividades preferirías, qué te motivaría y qué cosas evitarías. Sé específico y creativo en tu respuesta."}
    ]

    try:
        print(f"Generando retroalimentación para {student['name']}...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Puedes cambiar a gpt-4 si tienes acceso y lo prefieres
            messages=prompt_messages,
            temperature=0.7,
            max_tokens=300, # Aumentado un poco para respuestas más completas
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        feedback = response.choices[0].message.content.strip()
        return feedback
    except openai.APIError as e:
        print(f"Error de API de OpenAI al obtener retroalimentación para {student['name']}: {e}")
    except openai.RateLimitError:
        print(f"Error: Se ha excedido el límite de peticiones a OpenAI para {student['name']}. Intenta más tarde.")
    except Exception as e:
        print(f"Error inesperado al contactar OpenAI para {student['name']}: {e}")
    return "No se pudo generar la retroalimentación debido a un error."

def get_all_feedback(students_list):
    """Pide un tema y obtiene retroalimentación de todos los estudiantes."""
    if not students_list:
        print("\nNo hay estudiantes registrados para pedir retroalimentación.")
        return

    topic = input("\nIntroduce el tema sobre el que quieres retroalimentación: ").strip()
    if not topic:
        print("El tema no puede estar vacío.")
        return

    print(f"\n--- Retroalimentación sobre el tema: '{topic}' ---")
    for student in students_list:
        print(f"\n--- {student['name']} ---")
        feedback = get_feedback_from_student(student, topic)
        print(f"{feedback}")
        print("-" * 30)

def set_max_students_limit():
    """Permite al usuario definir el número máximo de estudiantes."""
    global MAX_STUDENTS
    while True:
        try:
            current_limit = 'sin límite' if MAX_STUDENTS == 0 else str(MAX_STUDENTS)
            num_str = input(f"Introduce el número máximo de estudiantes (actual: {current_limit}, 0 para sin límite): ").strip()
            num = int(num_str)
            if num < 0:
                print("El número no puede ser negativo.")
            else:
                MAX_STUDENTS = num
                new_limit = 'sin límite' if MAX_STUDENTS == 0 else str(MAX_STUDENTS)
                print(f"Número máximo de estudiantes establecido en: {new_limit}.")
                # Opcional: si se reduce el límite, no se eliminan estudiantes existentes por encima del nuevo límite
                # pero no se podrán agregar más hasta estar por debajo.
                break
        except ValueError:
            print("Por favor, introduce un número entero válido.")


def main_menu():
    """Función principal que maneja el menú de la aplicación."""
    students_data = load_students()

    while True:
        print("\n========= Menú Principal ========")
        print("1. Agregar estudiante")
        print("2. Ver lista de estudiantes")
        print("3. Obtener retroalimentación sobre un tema")
        print("4. Establecer/Ver máximo número de estudiantes")
        print("5. Salir")
        print("===============================")

        choice = input("Selecciona una opción (1-5): ").strip()

        if choice == '1':
            add_student(students_data)
        elif choice == '2':
            view_students(students_data)
        elif choice == '3':
            get_all_feedback(students_data)
        elif choice == '4':
            set_max_students_limit()
            current_limit = 'sin límite' if MAX_STUDENTS == 0 else str(MAX_STUDENTS)
            print(f"Límite actual de estudiantes: {current_limit}")
        elif choice == '5':
            print("Saliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige un número del 1 al 5.")

if __name__ == "__main__":
    # Pequeña bienvenida e instrucciones iniciales
    print("Bienvenido a la Aplicación de Retroalimentación del Salón de Clases Virtual")
    print("-----------------------------------------------------------------------")
    if os.getenv("OPENAI_API_KEY"):
        print("Usando clave API de OpenAI desde variable de entorno.")
    else:
        print("ADVERTENCIA: Revisa los mensajes sobre la configuración de la API Key de OpenAI.")
    print("Puedes empezar agregando estudiantes y luego pedir retroalimentación sobre un tema.")

    main_menu()
