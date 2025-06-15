import json
import os
import tkinter as tk
from tkinter import messagebox

STUDENTS_FILE = "students.json"
MAX_STUDENTS = 0  # 0 means unlimited


def load_students():
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_students(students):
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=4, ensure_ascii=False)


def add_student():
    global students
    name = name_entry.get().strip()
    personality = personality_entry.get().strip()
    tastes = tastes_entry.get().strip()
    extra = extra_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "El nombre no puede estar vacío.")
        return

    if any(s['name'].lower() == name.lower() for s in students):
        messagebox.showerror("Error", f"Ya existe un estudiante llamado '{name}'.")
        return

    if MAX_STUDENTS > 0 and len(students) >= MAX_STUDENTS:
        messagebox.showwarning(
            "Límite alcanzado",
            f"Se alcanzó el máximo de estudiantes ({MAX_STUDENTS}).")
        return

    students.append({
        "name": name,
        "personality": personality,
        "tastes": tastes,
        "extra_info": extra
    })
    save_students(students)
    students_listbox.insert(tk.END, name)
    name_entry.delete(0, tk.END)
    personality_entry.delete(0, tk.END)
    tastes_entry.delete(0, tk.END)
    extra_entry.delete(0, tk.END)
    messagebox.showinfo("Éxito", f"Estudiante '{name}' agregado.")


def set_limit():
    global MAX_STUDENTS
    val = limit_entry.get().strip()
    if not val:
        MAX_STUDENTS = 0
        limit_label.config(text="Límite: sin límite")
        return
    try:
        num = int(val)
        if num < 0:
            raise ValueError
        MAX_STUDENTS = num
        limit_label.config(text=f"Límite: {num if num != 0 else 'sin límite'}")
    except ValueError:
        messagebox.showerror("Error", "Introduce un número válido (0 para sin límite).")


def load_to_listbox():
    students_listbox.delete(0, tk.END)
    for s in students:
        students_listbox.insert(tk.END, s['name'])


students = load_students()

root = tk.Tk()
root.title("Gestión de Estudiantes")

# Campos de entrada
form_frame = tk.Frame(root)
form_frame.pack(padx=10, pady=10, fill=tk.X)

name_label = tk.Label(form_frame, text="Nombre:")
name_label.grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1, sticky="we")

personality_label = tk.Label(form_frame, text="Personalidad:")
personality_label.grid(row=1, column=0, sticky="e")
personality_entry = tk.Entry(form_frame)
personality_entry.grid(row=1, column=1, sticky="we")

tastes_label = tk.Label(form_frame, text="Gustos:")
tastes_label.grid(row=2, column=0, sticky="e")
tastes_entry = tk.Entry(form_frame)
tastes_entry.grid(row=2, column=1, sticky="we")

extra_label = tk.Label(form_frame, text="Extra:")
extra_label.grid(row=3, column=0, sticky="e")
extra_entry = tk.Entry(form_frame)
extra_entry.grid(row=3, column=1, sticky="we")

add_button = tk.Button(form_frame, text="Agregar", command=add_student)
add_button.grid(row=4, column=0, columnspan=2, pady=5)

form_frame.columnconfigure(1, weight=1)

# Lista de estudiantes
list_frame = tk.Frame(root)
list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

students_listbox = tk.Listbox(list_frame)
students_listbox.pack(fill=tk.BOTH, expand=True)
load_to_listbox()

# Límite de estudiantes
limit_frame = tk.Frame(root)
limit_frame.pack(padx=10, pady=10)

limit_label = tk.Label(limit_frame, text="Límite: sin límite")
limit_label.pack(side=tk.LEFT)
limit_entry = tk.Entry(limit_frame, width=5)
limit_entry.pack(side=tk.LEFT, padx=5)
limit_button = tk.Button(limit_frame, text="Establecer", command=set_limit)
limit_button.pack(side=tk.LEFT)

root.mainloop()
