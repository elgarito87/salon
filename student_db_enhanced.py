import sqlite3
import random
import string

DB_FILE = 'students.db'

def init_db():
    """Inicializa la base de datos y crea las tablas si no existen"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Crear tabla de estudiantes con matrícula
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        personality TEXT,
        tastes TEXT,
        extra_info TEXT,
        seat_number INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Crear tabla de retroalimentación histórica
    c.execute('''CREATE TABLE IF NOT EXISTS feedback_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_matricula TEXT,
        topic TEXT,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_matricula) REFERENCES students (matricula)
    )''')
    
    conn.commit()
    conn.close()

def generate_matricula():
    """Genera una matrícula única en formato EST-XXXXX"""
    while True:
        # Generar matrícula con formato EST- + 5 dígitos
        matricula = "EST-" + ''.join(random.choices(string.digits, k=5))
        
        # Verificar que no exista
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM students WHERE matricula = ?', (matricula,))
        exists = c.fetchone()[0] > 0
        conn.close()
        
        if not exists:
            return matricula

def load_students():
    """Carga todos los estudiantes desde la base de datos"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT matricula, name, personality, tastes, extra_info, seat_number 
                 FROM students ORDER BY created_at''')
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            'matricula': row[0],
            'name': row[1],
            'personality': row[2] or '',
            'tastes': row[3] or '',
            'extra_info': row[4] or '',
            'seat_number': row[5]
        } for row in rows
    ]

def add_student(student_data):
    """Agrega un nuevo estudiante con matrícula automática"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    matricula = generate_matricula()
    
    try:
        c.execute('''INSERT INTO students 
                     (matricula, name, personality, tastes, extra_info, seat_number) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (matricula,
                   student_data['name'],
                   student_data.get('personality', ''),
                   student_data.get('tastes', ''),
                   student_data.get('extra_info', ''),
                   student_data.get('seat_number')))
        conn.commit()
        return matricula
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_student_seat(matricula, seat_number):
    """Actualiza el número de asiento de un estudiante"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE students SET seat_number = ? WHERE matricula = ?', 
              (seat_number, matricula))
    conn.commit()
    conn.close()

def get_student_by_matricula(matricula):
    """Obtiene un estudiante por su matrícula"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT matricula, name, personality, tastes, extra_info, seat_number 
                 FROM students WHERE matricula = ?''', (matricula,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'matricula': row[0],
            'name': row[1],
            'personality': row[2] or '',
            'tastes': row[3] or '',
            'extra_info': row[4] or '',
            'seat_number': row[5]
        }
    return None

def save_feedback(student_matricula, topic, feedback):
    """Guarda la retroalimentación en el historial"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO feedback_history 
                 (student_matricula, topic, feedback) 
                 VALUES (?, ?, ?)''',
              (student_matricula, topic, feedback))
    conn.commit()
    conn.close()

def get_feedback_history(student_matricula):
    """Obtiene el historial de retroalimentación de un estudiante"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT topic, feedback, created_at 
                 FROM feedback_history 
                 WHERE student_matricula = ? 
                 ORDER BY created_at DESC''', (student_matricula,))
    rows = c.fetchall()
    conn.close()
    
    return [
        {
            'topic': row[0],
            'feedback': row[1],
            'date': row[2]
        } for row in rows
    ]

def get_students_count():
    """Obtiene el número total de estudiantes registrados"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM students')
    count = c.fetchone()[0]
    conn.close()
    return count

def clear_all_seats():
    """Limpia todos los asientos asignados"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE students SET seat_number = NULL')
    conn.commit()
    conn.close()
