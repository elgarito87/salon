import sqlite3

DB_FILE = 'students.db'

# Initialize database and create table if not exists

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        name TEXT PRIMARY KEY,
        personality TEXT,
        tastes TEXT,
        extra_info TEXT
    )''')
    conn.commit()
    conn.close()


def load_students():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name, personality, tastes, extra_info FROM students')
    rows = c.fetchall()
    conn.close()
    return [
        {
            'name': row[0],
            'personality': row[1],
            'tastes': row[2],
            'extra_info': row[3] or ''
        } for row in rows
    ]


def save_students(students):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM students')
    for s in students:
        c.execute(
            'INSERT OR REPLACE INTO students (name, personality, tastes, extra_info) VALUES (?, ?, ?, ?)',
            (s['name'], s.get('personality', ''), s.get('tastes', ''), s.get('extra_info', ''))
        )
    conn.commit()
    conn.close()


def add_student(student):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO students (name, personality, tastes, extra_info) VALUES (?, ?, ?, ?)',
            (student['name'], student.get('personality', ''), student.get('tastes', ''), student.get('extra_info', ''))
        )
        conn.commit()
    finally:
        conn.close()
