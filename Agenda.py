import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

agenda = []

def actualizar_lista():
    for i in tree.get_children():
        tree.delete(i)
    for contacto in agenda:
        tree.insert("", tk.END, values=(contacto["nombre"], contacto["telefono"], contacto["email"]))

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def agregar_contacto():
    nombre = entry_nombre.get().strip()
    telefono = entry_telefono.get().strip()
    email = entry_email.get().strip()

    if not nombre or not telefono or not email:
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
        return

    if not telefono.isdigit():
        messagebox.showwarning("Teléfono inválido", "El teléfono debe contener solo números")
        return

    if "@" not in email or "." not in email:
        messagebox.showwarning("Email inválido", "Ingrese un email válido")
        return

    for c in agenda:
        if c["nombre"].lower() == nombre.lower():
            messagebox.showwarning("Duplicado", "Ya existe un contacto con ese nombre")
            return

    agenda.append({"nombre": nombre, "telefono": telefono, "email": email})
    actualizar_lista()
    limpiar_campos()

def borrar_contacto():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Selección requerida", "Seleccione un contacto para borrar")
        return
    if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar este contacto?"):
        indice = tree.index(seleccion[0])
        agenda.pop(indice)
        actualizar_lista()

def cargar_contacto():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Selección requerida", "Seleccione un contacto para modificar")
        return
    indice = tree.index(seleccion[0])
    contacto = agenda[indice]
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, contacto["nombre"])
    entry_telefono.delete(0, tk.END)
    entry_telefono.insert(0, contacto["telefono"])
    entry_email.delete(0, tk.END)
    entry_email.insert(0, contacto["email"])
    btn_agregar.config(state=DISABLED)
    btn_guardar.config(state=NORMAL)

def guardar_modificacion():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Error", "No hay contacto seleccionado")
        return
    indice = tree.index(seleccion[0])
    nombre = entry_nombre.get().strip()
    telefono = entry_telefono.get().strip()
    email = entry_email.get().strip()

    if not nombre or not telefono or not email:
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
        return
    if not telefono.isdigit():
        messagebox.showwarning("Teléfono inválido", "El teléfono debe contener solo números")
        return
    if "@" not in email or "." not in email:
        messagebox.showwarning("Email inválido", "Ingrese un email válido")
        return

    agenda[indice] = {"nombre": nombre, "telefono": telefono, "email": email}
    actualizar_lista()
    limpiar_campos()
    btn_agregar.config(state=NORMAL)
    btn_guardar.config(state=DISABLED)

ventana = ttkb.Window(themename="flatly") 
ventana.title("Agenda Electrónica Profesional")
ventana.geometry("600x450")

frame_entrada = ttkb.Frame(ventana, padding=15)
frame_entrada.pack(padx=20, pady=10, fill=tk.X)

label_font = ("Comic Sans MS", 11, "bold")
entry_font = ("Comic Sans MS", 11)

ttkb.Label(frame_entrada, text="Nombre:", font=label_font).grid(row=0, column=0, pady=5, sticky="e")
entry_nombre = ttkb.Entry(frame_entrada, width=30, bootstyle="info", font=entry_font)
entry_nombre.grid(row=0, column=1, pady=5, padx=5)

ttkb.Label(frame_entrada, text="Teléfono:", font=label_font).grid(row=1, column=0, pady=5, sticky="e")
entry_telefono = ttkb.Entry(frame_entrada, width=30, bootstyle="info", font=entry_font)
entry_telefono.grid(row=1, column=1, pady=5, padx=5)

ttkb.Label(frame_entrada, text="Email:", font=label_font).grid(row=2, column=0, pady=5, sticky="e")
entry_email = ttkb.Entry(frame_entrada, width=30, bootstyle="info", font=entry_font)
entry_email.grid(row=2, column=1, pady=5, padx=5)

frame_botones = ttkb.Frame(ventana, padding=10)
frame_botones.pack(padx=20, pady=10, fill=tk.X)

btn_font = ("Comic Sans MS", 11, "bold")
btn_style = "primary-outline"

btn_agregar = ttkb.Button(frame_botones, text="Agregar", bootstyle=btn_style, width=12, command=agregar_contacto)
btn_agregar.grid(row=0, column=0, padx=5, pady=5)

btn_borrar = ttkb.Button(frame_botones, text="Borrar", bootstyle=btn_style, width=12, command=borrar_contacto)
btn_borrar.grid(row=0, column=1, padx=5, pady=5)

btn_modificar = ttkb.Button(frame_botones, text="Modificar", bootstyle=btn_style, width=12, command=cargar_contacto)
btn_modificar.grid(row=0, column=2, padx=5, pady=5)

btn_guardar = ttkb.Button(frame_botones, text="Guardar cambios", bootstyle=btn_style, width=15, command=guardar_modificacion, state=DISABLED)
btn_guardar.grid(row=0, column=3, padx=5, pady=5)

tree = ttkb.Treeview(ventana, columns=("Nombre","Teléfono","Email"), show="headings", height=10)
tree.heading("Nombre", text="Nombre")
tree.heading("Teléfono", text="Teléfono")
tree.heading("Email", text="Email")
tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Comic Sans MS", 11, "bold"))
style.configure("Treeview", font=("Comic Sans MS", 11))

ventana.mainloop()
