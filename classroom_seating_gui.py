import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import classroom_app as ca

students = ca.load_students()

ROWS = 4
COLUMNS = 5
seat_buttons = []
seat_assignments = {}

MAX_STUDENTS = ca.MAX_STUDENTS

def update_seat_button(seat_index):
    btn = seat_buttons[seat_index]
    student = seat_assignments.get(seat_index)
    if student:
        btn.config(text=student['name'], bg='lightgreen')
    else:
        btn.config(text=f"Asiento {seat_index+1}", bg='SystemButtonFace')

def save_and_refresh():
    ca.save_students(list(seat_assignments.values()))
    for i in range(len(seat_buttons)):
        update_seat_button(i)

def add_or_edit_student(seat_index):
    global MAX_STUDENTS
    if MAX_STUDENTS > 0 and len(seat_assignments) >= MAX_STUDENTS and seat_index not in seat_assignments:
        messagebox.showwarning("Límite alcanzado", f"Se alcanzó el máximo de estudiantes ({MAX_STUDENTS}).")
        return

    student = seat_assignments.get(seat_index, {})
    name = simpledialog.askstring("Nombre", "Nombre del estudiante:", initialvalue=student.get('name', ''))
    if not name:
        return
    personality = simpledialog.askstring("Personalidad", "Personalidad:", initialvalue=student.get('personality', '')) or ''
    tastes = simpledialog.askstring("Gustos", "Gustos:", initialvalue=student.get('tastes', '')) or ''
    extra = simpledialog.askstring("Extra", "Información extra:", initialvalue=student.get('extra_info', '')) or ''
    seat_assignments[seat_index] = {
        'name': name,
        'personality': personality,
        'tastes': tastes,
        'extra_info': extra
    }
    save_and_refresh()

def generate_feedback():
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showerror("Error", "Debes ingresar un tema en el pizarrón.")
        return
    if not seat_assignments:
        messagebox.showinfo("Sin estudiantes", "No hay estudiantes registrados.")
        return
    output.delete('1.0', tk.END)
    output.insert(tk.END, f"--- Retroalimentación sobre '{topic}' ---\n")
    for idx, student in seat_assignments.items():
        output.insert(tk.END, f"\n--- {student['name']} ---\n")
        feedback = ca.get_feedback_from_student(student, topic)
        output.insert(tk.END, feedback + "\n" + '-'*30 + "\n")

def set_limit():
    global MAX_STUDENTS
    val = simpledialog.askstring("Límite", "Número máximo de estudiantes (0 sin límite):")
    if val is None:
        return
    try:
        num = int(val)
        if num < 0:
            raise ValueError
        MAX_STUDENTS = num
        ca.MAX_STUDENTS = num
        limit_label.config(text=f"Límite: {num if num != 0 else 'sin límite'}")
    except ValueError:
        messagebox.showerror("Error", "Introduce un número válido.")

root = tk.Tk()
root.title("Salón de Clases Interactivo")

board_frame = tk.Frame(root)
board_frame.pack(pady=10)

board_label = tk.Label(board_frame, text="Tema en el pizarrón:")
board_label.pack(side=tk.LEFT)

topic_entry = tk.Entry(board_frame, width=40)
topic_entry.pack(side=tk.LEFT, padx=5)

feedback_btn = tk.Button(board_frame, text="Generar Retroalimentación", command=generate_feedback)
feedback_btn.pack(side=tk.LEFT)

limit_label = tk.Label(root, text="Límite: sin límite")
limit_label.pack(pady=5)

seats_frame = tk.Frame(root)
seats_frame.pack(padx=10, pady=10)

for r in range(ROWS):
    for c in range(COLUMNS):
        index = r*COLUMNS + c
        btn = tk.Button(seats_frame, text=f"Asiento {index+1}", width=12, height=2,
                         command=lambda i=index: add_or_edit_student(i))
        btn.grid(row=r, column=c, padx=5, pady=5)
        seat_buttons.append(btn)

output = scrolledtext.ScrolledText(root, width=60, height=15)
output.pack(padx=10, pady=10)

limit_btn = tk.Button(root, text="Establecer límite", command=set_limit)
limit_btn.pack(pady=5)

for idx, student in enumerate(students):
    if idx < ROWS*COLUMNS:
        seat_assignments[idx] = student

save_and_refresh()

root.mainloop()
