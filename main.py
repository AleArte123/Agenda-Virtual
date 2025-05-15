import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('agenda.db')
cursor = conn.cursor()

# Tabla de contactos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT
    )
''')

# Tabla de notas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        contenido TEXT
    )
''')

conn.commit()


def create_main_window():
    root = tk.Tk()
    root.title("Mi Agenda Digital")
    root.geometry("400x500")
    root.resizable(False, False)  # Evita que la ventana sea redimensionable

    # Título del programa
    title_label = tk.Label(root, text="Mi Agenda Digital",
                           font=("Harlow Solid Italic", 28, "bold"))
    title_label.pack(pady=5)

    # Etiquetas decorativas debajo del título
    labels_frame = tk.Frame(root)
    labels_frame.pack(pady=35)

    # Función para crear una etiqueta sobre un cuadrado de color
    def create_colored_label(frame, text, color):
        canvas = tk.Canvas(frame, width=80, height=40, highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=0)
        canvas.create_rectangle(0, 0, 80, 40, fill=color, outline=color)
        canvas.create_text(40, 20, text=text, fill="white",
                           font=("Rockwell", 11, "bold"))

    create_colored_label(labels_frame, "Ligera", "gold")
    create_colored_label(labels_frame, "Simple", "crimson")
    create_colored_label(labels_frame, "Útil", "salmon")

    # Creación del Notebook para las pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Pestaña de Contactos
    contacts_frame = ttk.Frame(notebook)
    notebook.add(contacts_frame, text="Contactos")

    # Etiquetas y campos de entrada para Contactos
    name_label = tk.Label(contacts_frame, text="Nombre:", font=("Arial", 12))
    name_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
    name_entry = tk.Entry(contacts_frame)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    phone_label = tk.Label(
        contacts_frame, text="Teléfono:", font=("Arial", 12))
    phone_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
    phone_entry = tk.Entry(contacts_frame)
    phone_entry.grid(row=1, column=1, padx=10, pady=5)

    email_label = tk.Label(
        contacts_frame, text="Correo Electrónico:", font=("Arial", 12))
    email_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
    email_entry = tk.Entry(contacts_frame)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    # Función para agregar contacto
    def add_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        if name == "" or phone == "":
            messagebox.showerror(
                "Error", "El nombre y teléfono son obligatorios.")
        else:
            cursor.execute("INSERT INTO contactos (nombre, telefono, correo) VALUES (?, ?, ?)",
                           (name, phone, email))
            conn.commit()
            messagebox.showinfo("Contacto agregado",
                                f"Se agregó a {name} correctamente.")
            # Limpiar los campos
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            load_contacts()  # Actualizar lista de contactos

    # Botón para agregar contacto
    add_contact_button = tk.Button(contacts_frame, text="Agregar Contacto", font=(
        "Arial", 12), bg="lightgreen", command=add_contact)
    add_contact_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Pestaña Ver Contactos
    view_contacts_frame = ttk.Frame(notebook)
    notebook.add(view_contacts_frame, text="Ver Contactos")

    # Lista de contactos
    contacts_listbox = tk.Listbox(view_contacts_frame, width=50, height=15)
    contacts_listbox.pack(pady=10)

    # Función para cargar contactos
    def load_contacts():
        contacts_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, nombre, telefono, correo FROM contactos")
        for row in cursor.fetchall():
            contact_info = f"{row[1]} - {row[2]} - {row[3]}"
            contacts_listbox.insert(tk.END, contact_info)

    # Función para eliminar contacto
    def delete_contact():
        selected = contacts_listbox.curselection()
        if selected:
            contact = contacts_listbox.get(selected[0])
            name = contact.split(" - ")[0]
            confirm = messagebox.askyesno(
                "Confirmar", f"¿Desea eliminar a {name}?")
            if confirm:
                cursor.execute(
                    "DELETE FROM contactos WHERE nombre = ?", (name,))
                conn.commit()
                messagebox.showinfo("Contacto eliminado",
                                    f"Se eliminó a {name}.")
                load_contacts()
        else:
            messagebox.showwarning(
                "Seleccionar contacto", "Por favor, selecciona un contacto.")

    # Función para editar contacto
    def edit_contact():
        selected = contacts_listbox.curselection()
        if selected:
            contact = contacts_listbox.get(selected[0])
            name = contact.split(" - ")[0]
            # Obtener datos del contacto
            cursor.execute(
                "SELECT id, nombre, telefono, correo FROM contactos WHERE nombre = ?", (name,))
            contact_data = cursor.fetchone()
            # Crear ventana de edición
            edit_window = tk.Toplevel()
            edit_window.title("Editar Contacto")
            edit_window.geometry("300x250")

            # Campos de edición
            tk.Label(edit_window, text="Nombre:", font=("Arial", 12)).grid(
                row=0, column=0, padx=10, pady=5, sticky='e')
            new_name_entry = tk.Entry(edit_window)
            new_name_entry.grid(row=0, column=1, padx=10, pady=5)
            new_name_entry.insert(0, contact_data[1])

            tk.Label(edit_window, text="Teléfono:", font=("Arial", 12)).grid(
                row=1, column=0, padx=10, pady=5, sticky='e')
            new_phone_entry = tk.Entry(edit_window)
            new_phone_entry.grid(row=1, column=1, padx=10, pady=5)
            new_phone_entry.insert(0, contact_data[2])

            tk.Label(edit_window, text="Correo Electrónico:", font=("Arial", 12)).grid(
                row=2, column=0, padx=10, pady=5, sticky='e')
            new_email_entry = tk.Entry(edit_window)
            new_email_entry.grid(row=2, column=1, padx=10, pady=5)
            new_email_entry.insert(0, contact_data[3])

            def save_changes():
                new_name = new_name_entry.get()
                new_phone = new_phone_entry.get()
                new_email = new_email_entry.get()
                if new_name == "" or new_phone == "":
                    messagebox.showerror(
                        "Error", "El nombre y teléfono son obligatorios.")
                else:
                    cursor.execute("UPDATE contactos SET nombre = ?, telefono = ?, correo = ? WHERE id = ?",
                                   (new_name, new_phone, new_email, contact_data[0]))
                    conn.commit()
                    messagebox.showinfo(
                        "Contacto actualizado", f"Se actualizó a {new_name} correctamente.")
                    edit_window.destroy()
                    load_contacts()

            tk.Button(edit_window, text="Guardar Cambios", bg="lightgreen",
                      command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

        else:
            messagebox.showwarning(
                "Seleccionar contacto", "Por favor, selecciona un contacto.")

    # Botones para eliminar y editar
    buttons_frame = tk.Frame(view_contacts_frame)
    buttons_frame.pack()

    delete_contact_button = tk.Button(
        buttons_frame, text="Eliminar Contacto", bg="salmon", command=delete_contact)
    delete_contact_button.pack(side=tk.LEFT, padx=10)

    edit_contact_button = tk.Button(
        buttons_frame, text="Editar Contacto", bg="lightblue", command=edit_contact)
    edit_contact_button.pack(side=tk.LEFT, padx=10)

    # Cargar contactos inicialmente
    load_contacts()

    # Pestaña de Notas
    notes_frame = ttk.Frame(notebook)
    notebook.add(notes_frame, text="Notas")

    # Etiquetas y campos de entrada para Notas
    title_label_notes = tk.Label(
        notes_frame, text="Título:", font=("Arial", 12))
    title_label_notes.grid(row=0, column=0, padx=10, pady=5, sticky='e')
    title_entry = tk.Entry(notes_frame)
    title_entry.grid(row=0, column=1, padx=10, pady=5)

    content_label = tk.Label(
        notes_frame, text="Contenido:", font=("Arial", 12))
    content_label.grid(row=1, column=0, padx=10, pady=5, sticky='ne')
    content_text = tk.Text(notes_frame, width=30, height=10)
    content_text.grid(row=1, column=1, padx=10, pady=5)

    # Función para agregar nota
    def add_note():
        titulo = title_entry.get()
        contenido = content_text.get("1.0", tk.END).strip()

        if titulo == "":
            messagebox.showerror("Error", "El título es obligatorio.")
        else:
            cursor.execute(
                "INSERT INTO notas (titulo, contenido) VALUES (?, ?)", (titulo, contenido))
            conn.commit()
            messagebox.showinfo(
                "Nota agregada", f"Se agregó la nota '{titulo}' correctamente.")
            # Limpiar los campos
            title_entry.delete(0, tk.END)
            content_text.delete("1.0", tk.END)
            load_notes()  # Actualizar lista de notas

    # Botón para agregar nota
    add_note_button = tk.Button(notes_frame, text="Agregar Nota", font=(
        "Arial", 12), bg="lightgreen", command=add_note)
    add_note_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Pestaña Ver Notas
    view_notes_frame = ttk.Frame(notebook)
    notebook.add(view_notes_frame, text="Ver Notas")

    # Lista de notas
    notes_listbox = tk.Listbox(view_notes_frame, width=50, height=15)
    notes_listbox.pack(pady=10)

    # Función para cargar notas
    def load_notes():
        notes_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, titulo, contenido FROM notas")
        for row in cursor.fetchall():
            note_info = f"{row[1]}"
            notes_listbox.insert(tk.END, note_info)

    # Función para eliminar nota
    def delete_note():
        selected = notes_listbox.curselection()
        if selected:
            note_title = notes_listbox.get(selected[0])
            confirm = messagebox.askyesno(
                "Confirmar", f"¿Desea eliminar la nota '{note_title}'?")
            if confirm:
                cursor.execute(
                    "DELETE FROM notas WHERE titulo = ?", (note_title,))
                conn.commit()
                messagebox.showinfo(
                    "Nota eliminada", f"Se eliminó la nota '{note_title}'.")
                load_notes()
        else:
            messagebox.showwarning(
                "Seleccionar nota", "Por favor, selecciona una nota.")

    # Función para editar nota
    def edit_note():
        selected = notes_listbox.curselection()
        if selected:
            note_title = notes_listbox.get(selected[0])
            # Obtener datos de la nota
            cursor.execute(
                "SELECT id, titulo, contenido FROM notas WHERE titulo = ?", (note_title,))
            note_data = cursor.fetchone()
            # Crear ventana de edición
            edit_window = tk.Toplevel()
            edit_window.title("Editar Nota")
            edit_window.geometry("300x300")

            # Campos de edición
            tk.Label(edit_window, text="Título:", font=("Arial", 12)).grid(
                row=0, column=0, padx=10, pady=5, sticky='e')
            new_title_entry = tk.Entry(edit_window)
            new_title_entry.grid(row=0, column=1, padx=10, pady=5)
            new_title_entry.insert(0, note_data[1])

            tk.Label(edit_window, text="Contenido:", font=("Arial", 12)).grid(
                row=1, column=0, padx=10, pady=5, sticky='ne')
            new_content_text = tk.Text(edit_window, width=25, height=10)
            new_content_text.grid(row=1, column=1, padx=10, pady=5)
            new_content_text.insert("1.0", note_data[2])

            def save_note_changes():
                new_title = new_title_entry.get()
                new_content = new_content_text.get("1.0", tk.END).strip()
                if new_title == "":
                    messagebox.showerror("Error", "El título es obligatorio.")
                else:
                    cursor.execute("UPDATE notas SET titulo = ?, contenido = ? WHERE id = ?",
                                   (new_title, new_content, note_data[0]))
                    conn.commit()
                    messagebox.showinfo(
                        "Nota actualizada", f"Se actualizó la nota '{new_title}' correctamente.")
                    edit_window.destroy()
                    load_notes()

            tk.Button(edit_window, text="Guardar Cambios", bg="lightgreen",
                      command=save_note_changes).grid(row=2, column=0, columnspan=2, pady=10)

        else:
            messagebox.showwarning(
                "Seleccionar nota", "Por favor, selecciona una nota.")

    # Botones para eliminar y editar notas
    notes_buttons_frame = tk.Frame(view_notes_frame)
    notes_buttons_frame.pack()

    edit_note_button = tk.Button(
        notes_buttons_frame, text="Editar Nota", bg="lightblue", command=edit_note)
    edit_note_button.pack(side=tk.LEFT, padx=10)

    delete_note_button = tk.Button(
        notes_buttons_frame, text="Eliminar Nota", bg="salmon", command=delete_note)
    delete_note_button.pack(side=tk.LEFT, padx=10)

    # Cargar notas inicialmente
    load_notes()

    root.mainloop()


create_main_window()

# Fin
