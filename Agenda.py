import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import json
import os

# Nombre del archivo para guardar los datos
ARCHIVO_DATOS = "contactos_agenda.json"

class AgendaApp(ttkb.Window):
    """Aplicación de Agenda Electrónica implementada con ttkbootstrap y POO."""

    def __init__(self, themename="flatly"):
        # 1. Inicialización de la ventana y el estado
        super().__init__(themename=themename)
        self.title("Agenda Electrónica Profesional (Mejorada)")
        # Establece un tamaño base y permite redimensionar
        self.geometry("800x550") 
        self.resizable(True, True)
        
        # Lista que contendrá los diccionarios de contactos
        self.agenda = []
        # Variable para rastrear el índice del contacto que se está modificando (-1 significa modo Agregar)
        self.contacto_a_modificar_indice = -1

        # Cargar los datos al iniciar la aplicación
        self.cargar_datos()
        
        # 2. Configuración de la interfaz
        self.configurar_estilos()
        self.crear_widgets()
        self.configurar_layout()
        
        # 3. Inicializar la lista y los estados
        self.actualizar_lista()
        # Atajo: presionar ESC cancela el modo de modificación
        self.bind("<Escape>", lambda e: self.cancelar_modificacion())
        
        # Configurar acción al cerrar la ventana para guardar los datos
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configurar_estilos(self):
        """Configura estilos y fuentes más profesionales."""
        # Se usa una fuente moderna en lugar de Comic Sans MS
        self.font_label = ("Helvetica", 11, "bold")
        self.font_entry = ("Helvetica", 11)
        self.font_btn = ("Helvetica", 11, "bold")
        
        style = ttk.Style()
        
        # Configuración de estilos del Treeview para mejorar visualización y hacer las filas más altas
        style.configure("Treeview", rowheight=28, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        
        # CORRECCIÓN DEL ERROR: Configurar la fuente globalmente para los widgets de ttkb/ttk
        # Los widgets temáticos no aceptan 'font' como argumento directo, se debe usar style.configure.
        style.configure("TLabel", font=self.font_label)
        style.configure("TButton", font=self.font_btn)
        style.configure("TEntry", font=self.font_entry)


    def crear_widgets(self):
        """Crea todos los frames y elementos de la interfaz."""
        
        # --- Frame de Entrada (Datos del Contacto) ---
        self.frame_entrada = ttkb.Frame(self, padding=20)
        
        # Widgets de entrada
        # El argumento 'font' ha sido eliminado de ttkb.Label y ttkb.Entry
        ttkb.Label(self.frame_entrada, text="Nombre:").grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.entry_nombre = ttkb.Entry(self.frame_entrada, width=40, bootstyle="info")
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        ttkb.Label(self.frame_entrada, text="Teléfono:").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.entry_telefono = ttkb.Entry(self.frame_entrada, width=40, bootstyle="info")
        self.entry_telefono.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        ttkb.Label(self.frame_entrada, text="Email:").grid(row=2, column=0, pady=10, padx=10, sticky="e")
        self.entry_email = ttkb.Entry(self.frame_entrada, width=40, bootstyle="info")
        self.entry_email.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # --- Frame de Botones de Acción ---
        self.frame_botones = ttkb.Frame(self, padding=10)
        
        btn_style_primary = "primary"
        btn_style_danger = "danger-outline"
        
        # Se elimina el argumento 'font' de todos los botones
        # Este botón maneja tanto "Agregar" como "Guardar Modificación"
        self.btn_agregar = ttkb.Button(self.frame_botones, text="➕ Agregar Contacto", bootstyle=btn_style_primary, width=20, command=self.agregar_o_modificar_contacto)
        
        self.btn_borrar = ttkb.Button(self.frame_botones, text="🗑️ Borrar Seleccionado", bootstyle=btn_style_danger, width=20, command=self.borrar_contacto)
        
        self.btn_modificar = ttkb.Button(self.frame_botones, text="📝 Cargar para Modificar", bootstyle="warning-outline", width=25, command=self.cargar_contacto_para_modificar)
        
        self.btn_cancelar = ttkb.Button(self.frame_botones, text="❌ Cancelar Edición", bootstyle="secondary-outline", width=20, command=self.cancelar_modificacion, state=DISABLED)
        
        # --- Treeview (Lista de Contactos) ---
        # Se usa bootstyle="info" para aplicar el tema de ttkbootstrap
        self.tree = ttkb.Treeview(self, columns=("Nombre","Teléfono","Email"), show="headings", height=10, bootstyle="info")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        
        # Configurar anchos de columna para mejor visualización
        self.tree.column("Nombre", anchor=tk.W, width=150)
        self.tree.column("Teléfono", anchor=tk.CENTER, width=100)
        self.tree.column("Email", anchor=tk.W, width=200)

        # Scrollbar para el Treeview
        vsb = ttkb.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.vsb = vsb # Almacenar la scrollbar para el layout

    def configurar_layout(self):
        """Organiza los widgets usando pack y grid."""
        
        self.frame_entrada.pack(padx=30, pady=15, fill=tk.X)
        self.frame_botones.pack(padx=30, pady=5, fill=tk.X)
        
        # Layout del Treeview con Scrollbar (se usa side=LEFT/RIGHT para que ocupen todo el espacio)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 30), pady=(10, 30))
        self.tree.pack(padx=(30, 0), pady=(10, 30), fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Layout de los botones
        self.btn_agregar.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_borrar.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_modificar.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_cancelar.pack(side=tk.LEFT, padx=5, pady=5)

    def validar_campos(self, nombre, telefono, email, es_modificacion=False):
        """Valida los campos de entrada y muestra advertencias. Código reutilizable."""
        
        if not nombre or not telefono or not email:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return False

        if not telefono.isdigit():
            messagebox.showwarning("Teléfono inválido", "El teléfono debe contener solo números.")
            return False

        # Validación de formato de email simple (existe @ y .)
        if not ("@" in email and "." in email):
            messagebox.showwarning("Email inválido", "Ingrese un email válido (debe contener '@' y '.').")
            return False

        # Verificar duplicados (solo si no estamos modificando el mismo contacto)
        for i, contacto in enumerate(self.agenda):
            if contacto["nombre"].lower() == nombre.lower():
                # Si estamos modificando, ignoramos la coincidencia con el contacto actual
                if es_modificacion and i == self.contacto_a_modificar_indice:
                    continue
                
                messagebox.showwarning("Duplicado", f"Ya existe un contacto con el nombre '{nombre}'")
                return False
                
        return True

    def limpiar_campos(self):
        """Limpia todos los campos de entrada."""
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_nombre.focus_set()

    def actualizar_lista(self):
        """Refresca el contenido del Treeview con los datos de la agenda."""
        # Limpiar Treeview existente
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Llenar con los datos actualizados
        for contacto in self.agenda:
            self.tree.insert("", tk.END, values=(contacto["nombre"], contacto["telefono"], contacto["email"]))

    def agregar_o_modificar_contacto(self):
        """Función unificada para agregar o guardar modificaciones, basada en el estado interno."""
        
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        
        es_modificacion = self.contacto_a_modificar_indice != -1

        if not self.validar_campos(nombre, telefono, email, es_modificacion):
            return

        nuevo_contacto = {"nombre": nombre, "telefono": telefono, "email": email}

        if es_modificacion:
            # Lógica de Modificación
            self.agenda[self.contacto_a_modificar_indice] = nuevo_contacto
            messagebox.showinfo("Éxito", "Contacto modificado correctamente.")
            # Resetea el modo de modificación
            self.cancelar_modificacion(limpiar=True) 
        else:
            # Lógica de Agregar
            self.agenda.append(nuevo_contacto)
            messagebox.showinfo("Éxito", "Contacto agregado correctamente.")
            self.limpiar_campos()
            
        self.actualizar_lista()
        self.guardar_datos()

    def borrar_contacto(self):
        """Elimina el contacto seleccionado del Treeview y la agenda."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccione un contacto para borrar.")
            return
            
        if self.contacto_a_modificar_indice != -1:
            messagebox.showwarning("Modificación activa", "Por favor, cancele la edición actual antes de borrar un contacto.")
            return

        if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este contacto de forma permanente?"):
            indice = self.tree.index(seleccion[0])
            self.agenda.pop(indice)
            self.actualizar_lista()
            self.guardar_datos()

    def cargar_contacto_para_modificar(self):
        """Carga los datos del contacto seleccionado en los campos de entrada y habilita el modo de modificación."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccione un contacto para modificar.")
            return
            
        # Obtener el índice del contacto seleccionado en la lista 'agenda'
        self.contacto_a_modificar_indice = self.tree.index(seleccion[0])
        contacto = self.agenda[self.contacto_a_modificar_indice]
        
        # Limpiar e insertar datos
        self.limpiar_campos()
        self.entry_nombre.insert(0, contacto["nombre"])
        self.entry_telefono.insert(0, contacto["telefono"])
        self.entry_email.insert(0, contacto["email"])
        
        # Cambiar el estado de la UI a modo Modificación
        self.btn_agregar.config(text="💾 Guardar Modificación", bootstyle="success")
        self.btn_cancelar.config(state=NORMAL)
        self.btn_modificar.config(state=DISABLED)
        # Deshabilitar selección en la lista mientras se edita para evitar errores
        self.tree.config(selectmode="none") 

    def cancelar_modificacion(self, limpiar=True):
        """Cancela el modo de modificación, resetea el estado de la UI."""
        self.contacto_a_modificar_indice = -1
        
        if limpiar:
            self.limpiar_campos()
            
        # Restaurar estado de la UI a modo Agregar
            self.btn_agregar.config(text="➕ Agregar Contacto", bootstyle="primary")
        self.btn_cancelar.config(state=DISABLED)
        self.btn_modificar.config(state=NORMAL)
        self.tree.config(selectmode="browse") # Habilitar selección normal

    # --- Métodos de Persistencia de Datos ---
    
    def cargar_datos(self):
        """Carga los contactos desde el archivo JSON si existe."""
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.agenda = data
            except (IOError, json.JSONDecodeError):
                # En caso de error de lectura o JSON corrupto, inicializa la lista vacía
                self.agenda = []
        else:
            self.agenda = []

    def guardar_datos(self):
        """Guarda la lista de contactos en el archivo JSON."""
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                # Usa indent=4 para que el archivo JSON sea legible
                json.dump(self.agenda, f, indent=4)
        except IOError as e:
            messagebox.showerror("Error de Guardado", f"No se pudieron guardar los datos: {e}")

    def on_closing(self):
        """Función llamada al cerrar la ventana para guardar y salir."""
        self.guardar_datos()
        self.destroy()

if __name__ == "__main__":
    # Inicializa y corre la aplicación
    app = AgendaApp()
    app.mainloop()


