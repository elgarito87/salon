import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import classroom_app as ca
import student_db_enhanced as db

class ClassroomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Salón de Clases Virtual - Sistema de Gestión Estudiantil")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar base de datos
        db.init_db()
        
        # Variables
        self.students = {}  # Dict: seat_number -> student_data
        self.ROWS = 5
        self.COLUMNS = 6
        self.seat_buttons = []
        self.selected_seat = None
        
        self.setup_ui()
        self.load_students()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="🏫 Salón de Clases Virtual", 
                              font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 10))
        
        # Frame superior - Pizarrón y controles
        top_frame = ttk.LabelFrame(main_frame, text="📋 Panel de Control", padding="10")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Pizarrón
        board_frame = ttk.Frame(top_frame)
        board_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(board_frame, text="📚 Tema de la clase:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        self.topic_entry = tk.Entry(board_frame, width=40, font=('Arial', 11))
        self.topic_entry.pack(side=tk.LEFT, padx=(10, 5))
        
        # Botones de control
        btn_frame = ttk.Frame(board_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="🎯 Generar Retroalimentación", 
                  command=self.generate_feedback).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="👥 Gestionar Estudiantes", 
                  command=self.open_student_manager).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📊 Estadísticas", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=2)
        
        # Frame central - Salón de clases
        classroom_frame = ttk.LabelFrame(main_frame, text="🏛️ Distribución del Salón", padding="10")
        classroom_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Pizarrón visual
        blackboard = tk.Frame(classroom_frame, bg='#2c3e50', height=60)
        blackboard.pack(fill=tk.X, pady=(0, 20))
        blackboard.pack_propagate(False)
        
        board_label = tk.Label(blackboard, text="PIZARRÓN", 
                              bg='#2c3e50', fg='white', font=('Arial', 16, 'bold'))
        board_label.pack(expand=True)
        
        # Grid de asientos
        seats_frame = ttk.Frame(classroom_frame)
        seats_frame.pack(expand=True)
        
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                seat_num = row * self.COLUMNS + col + 1
                btn = tk.Button(seats_frame, text=f"Asiento {seat_num}", 
                               width=12, height=3, font=('Arial', 9),
                               command=lambda s=seat_num: self.seat_clicked(s))
                btn.grid(row=row, column=col, padx=3, pady=3)
                self.seat_buttons.append(btn)
        
        # Frame inferior - Resultados
        results_frame = ttk.LabelFrame(main_frame, text="📝 Retroalimentación Personalizada", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12, 
                                                     font=('Arial', 10), wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Barra de estado
        self.status_bar = tk.Label(self.root, text="Listo - 0 estudiantes registrados", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#ecf0f1')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_seat_button(self, seat_number):
        """Actualiza la apariencia de un botón de asiento"""
        btn = self.seat_buttons[seat_number - 1]
        
        if seat_number in self.students:
            student = self.students[seat_number]
            btn.config(text=f"{student['name']}\n({student['matricula']})", 
                      bg='#27ae60', fg='white', font=('Arial', 8, 'bold'))
        else:
            btn.config(text=f"Asiento {seat_number}", 
                      bg='#bdc3c7', fg='black', font=('Arial', 9))
    
    def seat_clicked(self, seat_number):
        """Maneja el clic en un asiento"""
        if seat_number in self.students:
            self.show_student_info(seat_number)
        else:
            self.assign_student_to_seat(seat_number)
    
    def show_student_info(self, seat_number):
        """Muestra información del estudiante y opciones"""
        student = self.students[seat_number]
        
        info = f"👤 Estudiante: {student['name']}\n"
        info += f"🎫 Matrícula: {student['matricula']}\n"
        info += f"🧠 Personalidad: {student['personality']}\n"
        info += f"❤️ Gustos: {student['tastes']}\n"
        if student['extra_info']:
            info += f"ℹ️ Extra: {student['extra_info']}\n"
        
        choice = messagebox.askyesnocancel("Información del Estudiante",
                                          f"{info}\n¿Qué deseas hacer?\n\n"
                                          "Sí = Ver historial\n"
                                          "No = Quitar del asiento\n"
                                          "Cancelar = Cerrar")
        
        if choice is True:
            self.show_student_history(student['matricula'])
        elif choice is False:
            self.remove_student_from_seat(seat_number)
    
    def assign_student_to_seat(self, seat_number):
        """Asigna un estudiante a un asiento"""
        available_students = self.get_available_students()
        
        if not available_students:
            if messagebox.askyesno("Sin estudiantes", 
                                  "No hay estudiantes disponibles. ¿Deseas crear uno nuevo?"):
                self.create_new_student(seat_number)
            return
        
        # Crear ventana de selección
        self.select_student_window(available_students, seat_number)
    
    def get_available_students(self):
        """Obtiene estudiantes que no están asignados a asientos"""
        all_students = db.load_students()
        assigned_matriculas = {s['matricula'] for s in self.students.values()}
        return [s for s in all_students if s['matricula'] not in assigned_matriculas]
    
    def select_student_window(self, students, seat_number):
        """Ventana para seleccionar estudiante"""
        window = tk.Toplevel(self.root)
        window.title("Seleccionar Estudiante")
        window.geometry("500x400")
        window.transient(self.root)
        window.grab_set()
        
        tk.Label(window, text=f"Seleccionar estudiante para Asiento {seat_number}", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Lista de estudiantes
        frame = ttk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        listbox = tk.Listbox(frame, font=('Arial', 10))
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        for student in students:
            listbox.insert(tk.END, f"{student['name']} ({student['matricula']})")
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones
        btn_frame = ttk.Frame(window)
        btn_frame.pack(pady=10)
        
        def assign_selected():
            selection = listbox.curselection()
            if selection:
                student = students[selection[0]]
                self.students[seat_number] = student
                db.update_student_seat(student['matricula'], seat_number)
                self.update_seat_button(seat_number)
                self.update_status()
                window.destroy()
            else:
                messagebox.showwarning("Selección", "Por favor selecciona un estudiante")
        
        ttk.Button(btn_frame, text="Asignar", command=assign_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Crear Nuevo", 
                  command=lambda: [window.destroy(), self.create_new_student(seat_number)]).pack(side=tk.LEFT, padx=5)
        
    def create_new_student(self, seat_number=None):
        """Crea un nuevo estudiante"""
        window = tk.Toplevel(self.root)
        window.title("Crear Nuevo Estudiante")
        window.geometry("500x400")
        window.transient(self.root)
        window.grab_set()
        
        # Formulario
        ttk.Label(window, text="Crear Nuevo Estudiante", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = ttk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Campos
        fields = [
            ("Nombre:", "name"),
            ("Personalidad:", "personality"),
            ("Gustos:", "tastes"),
            ("Información extra:", "extra_info")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky='w', pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=i, column=1, sticky='we', padx=(10, 0), pady=5)
            entries[key] = entry
        
        frame.columnconfigure(1, weight=1)
        
        def save_student():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            
            if not data['name']:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            data['seat_number'] = seat_number
            matricula = db.add_student(data)
            
            if matricula:
                data['matricula'] = matricula
                if seat_number:
                    self.students[seat_number] = data
                    self.update_seat_button(seat_number)
                self.update_status()
                messagebox.showinfo("Éxito", f"Estudiante creado con matrícula: {matricula}")
                window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el estudiante")
        
        btn_frame = ttk.Frame(window)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Guardar", command=save_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=window.destroy).pack(side=tk.LEFT, padx=5)
    
    def remove_student_from_seat(self, seat_number):
        """Quita un estudiante del asiento"""
        student = self.students[seat_number]
        db.update_student_seat(student['matricula'], None)
        del self.students[seat_number]
        self.update_seat_button(seat_number)
        self.update_status()
        messagebox.showinfo("Éxito", f"Estudiante {student['name']} removido del asiento")
    
    def generate_feedback(self):
        """Genera retroalimentación para todos los estudiantes"""
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showerror("Error", "Por favor ingresa un tema en el pizarrón")
            return
        
        if not self.students:
            messagebox.showinfo("Sin estudiantes", "No hay estudiantes en el salón")
            return
        
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert(tk.END, f"🎯 RETROALIMENTACIÓN PERSONALIZADA PARA: '{topic}'\n")
        self.results_text.insert(tk.END, "="*80 + "\n\n")
        
        for seat_number, student in sorted(self.students.items()):
            self.results_text.insert(tk.END, f"👤 {student['name']} (Matrícula: {student['matricula']}) - Asiento {seat_number}\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n")
            
            # Generar retroalimentación con OpenAI
            feedback = ca.get_feedback_from_student(student, topic)
            self.results_text.insert(tk.END, feedback + "\n\n")
            
            # Guardar en historial
            db.save_feedback(student['matricula'], topic, feedback)
            
            self.results_text.see(tk.END)
            self.root.update()
    
    def show_student_history(self, matricula):
        """Muestra el historial de un estudiante"""
        history = db.get_feedback_history(matricula)
        student = db.get_student_by_matricula(matricula)
        
        window = tk.Toplevel(self.root)
        window.title(f"Historial - {student['name']}")
        window.geometry("700x500")
        window.transient(self.root)
        
        ttk.Label(window, text=f"📚 Historial de {student['name']} ({matricula})", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        text_widget = scrolledtext.ScrolledText(window, font=('Arial', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        if history:
            for item in history:
                text_widget.insert(tk.END, f"📅 {item['date']}\n")
                text_widget.insert(tk.END, f"📚 Tema: {item['topic']}\n")
                text_widget.insert(tk.END, f"💬 Retroalimentación:\n{item['feedback']}\n")
                text_widget.insert(tk.END, "-" * 70 + "\n\n")
        else:
            text_widget.insert(tk.END, "Sin historial de retroalimentación disponible.")
        
        ttk.Button(window, text="Cerrar", command=window.destroy).pack(pady=10)
    
    def open_student_manager(self):
        """Abre el gestor de estudiantes"""
        window = tk.Toplevel(self.root)
        window.title("Gestión de Estudiantes")
        window.geometry("800x600")
        window.transient(self.root)
        
        ttk.Label(window, text="👥 Gestión de Estudiantes", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Lista de todos los estudiantes
        frame = ttk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('Matrícula', 'Nombre', 'Personalidad', 'Asiento')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar datos
        all_students = db.load_students()
        for student in all_students:
            seat_info = f"Asiento {student['seat_number']}" if student['seat_number'] else "Sin asignar"
            tree.insert('', tk.END, values=(
                student['matricula'],
                student['name'],
                student['personality'][:30] + "..." if len(student['personality']) > 30 else student['personality'],
                seat_info
            ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones
        btn_frame = ttk.Frame(window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Crear Nuevo", 
                  command=lambda: [window.destroy(), self.create_new_student()]).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar Asientos", 
                  command=self.clear_all_seats).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cerrar", command=window.destroy).pack(side=tk.LEFT, padx=5)
    
    def clear_all_seats(self):
        """Limpia todos los asientos"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de querer limpiar todos los asientos?"):
            db.clear_all_seats()
            self.students.clear()
            for i in range(1, self.ROWS * self.COLUMNS + 1):
                self.update_seat_button(i)
            self.update_status()
            messagebox.showinfo("Éxito", "Todos los asientos han sido limpiados")
    
    def show_statistics(self):
        """Muestra estadísticas del sistema"""
        total_students = db.get_students_count()
        assigned_students = len(self.students)
        
        stats = f"📊 ESTADÍSTICAS DEL SISTEMA\n\n"
        stats += f"👥 Total de estudiantes registrados: {total_students}\n"
        stats += f"🪑 Estudiantes asignados a asientos: {assigned_students}\n"
        stats += f"🔢 Asientos disponibles: {self.ROWS * self.COLUMNS - assigned_students}\n"
        stats += f"📚 Capacidad total del salón: {self.ROWS * self.COLUMNS}\n"
        
        messagebox.showinfo("Estadísticas", stats)
    
    def load_students(self):
        """Carga estudiantes asignados a asientos"""
        all_students = db.load_students()
        for student in all_students:
            if student['seat_number']:
                self.students[student['seat_number']] = student
                self.update_seat_button(student['seat_number'])
        self.update_status()
    
    def update_status(self):
        """Actualiza la barra de estado"""
        total = db.get_students_count()
        assigned = len(self.students)
        self.status_bar.config(text=f"Total: {total} estudiantes | Asignados: {assigned} | Disponibles: {total - assigned}")


def main():
    root = tk.Tk()
    app = ClassroomApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
