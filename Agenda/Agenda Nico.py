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
        # Cambiamos el tema a 'cosmo' o 'lumen' para un look más corporativo/moderno
        super().__init__(themename="cosmo") 
        self.title("Sistema de Gestión de Contactos (Agenda Profesional)")
        self.geometry("850x650") # Tamaño ligeramente más grande para el nuevo layout
        self.minsize(650, 500) # Establece un tamaño mínimo
        
        self.agenda = []
        self.contacto_a_modificar_indice = -1

        self.cargar_datos()
        
        # 2. Configuración de la interfaz
        self.configurar_estilos()
        self.crear_widgets()
        # **CAMBIO CLAVE:** Usamos `grid` en el contenedor principal para un layout más controlado.
        self.configurar_layout()
        
        # 3. Inicializar la lista y los estados
        self.actualizar_lista()
        self.bind("<Escape>", lambda e: self.cancelar_modificacion())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configurar_estilos(self):
        """Configura estilos y fuentes más profesionales."""
        
        # Fuentes más limpias y consistentes
        self.font_title = ("Helvetica", 16, "bold")
        self.font_label = ("Helvetica", 10)
        self.font_entry = ("Helvetica", 10)
        self.font_btn = ("Helvetica", 10, "bold")
        
        style = ttk.Style()
        
        # Mejora de estilos generales de ttkbootstrap
        style.configure("TLabel", font=self.font_label)
        style.configure("TButton", font=self.font_btn, padding=8) # Más padding en botones
        style.configure("TEntry", font=self.font_entry, padding=5)

        # Configuración del Treeview para mejorar visualización
        style.configure("Treeview", rowheight=30, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        # Estilo para un encabezado principal
        style.configure("Title.TLabel", font=self.font_title, foreground=style.lookup("primary.TLabel", "foreground")) 


    def crear_widgets(self):
        """Crea todos los frames y elementos de la interfaz."""
        
        # --- Frame Principal (Panel de Control) ---
        # Se usará como contenedor principal para la entrada y botones
        self.frame_panel = ttkb.Frame(self, padding=20, borderwidth=2, relief="groove")
        
        # Título principal del panel
        ttkb.Label(self.frame_panel, text="Gestión de Contactos", style="Title.TLabel").pack(pady=(0, 15))
        
        # --- Frame de Entrada (Datos del Contacto) ---
        # Usamos un Frame con LabelFrame para agrupar visualmente los campos
        self.frame_entrada = ttkb.LabelFrame(self.frame_panel, text="Datos del Contacto", padding=15, bootstyle="info")
        self.frame_entrada.pack(pady=10, padx=10, fill=tk.X)
        
        # Widgets de entrada
        # Se usa grid dentro de frame_entrada para control preciso
        ttkb.Label(self.frame_entrada, text="Nombre:", bootstyle="info").grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.entry_nombre = ttkb.Entry(self.frame_entrada, width=35, bootstyle="info")
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        
        ttkb.Label(self.frame_entrada, text="Teléfono:", bootstyle="info").grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.entry_telefono = ttkb.Entry(self.frame_entrada, width=35, bootstyle="info")
        self.entry_telefono.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        ttkb.Label(self.frame_entrada, text="Email:", bootstyle="info").grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.entry_email = ttkb.Entry(self.frame_entrada, width=35, bootstyle="info")
        self.entry_email.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        
        # Centrar las columnas de entrada dentro del frame_entrada
        self.frame_entrada.grid_columnconfigure(0, weight=1)
        self.frame_entrada.grid_columnconfigure(1, weight=1)

        # --- Frame de Botones de Acción ---
        self.frame_botones = ttkb.Frame(self.frame_panel, padding=10)
        self.frame_botones.pack(pady=10, padx=10, fill=tk.X)
        
        # Botones de Acción (mantenemos los bootstyles profesionales)
        self.btn_agregar = ttkb.Button(self.frame_botones, text="➕ Agregar Contacto", bootstyle="primary", command=self.agregar_o_modificar_contacto)
        self.btn_borrar = ttkb.Button(self.frame_botones, text="🗑️ Borrar", bootstyle="danger-outline", command=self.borrar_contacto)
        self.btn_modificar = ttkb.Button(self.frame_botones, text="📝 Cargar para Editar", bootstyle="warning-outline", command=self.cargar_contacto_para_modificar)
        self.btn_cancelar = ttkb.Button(self.frame_botones, text="❌ Cancelar Edición (Esc)", bootstyle="secondary-outline", command=self.cancelar_modificacion, state=DISABLED)
        
        # Layout de los botones dentro de frame_botones (centrado y espaciado)
        self.btn_agregar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btn_borrar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.btn_modificar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.btn_cancelar.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_columnconfigure(1, weight=1)
        
        # --- Treeview (Lista de Contactos) ---
        self.tree = ttkb.Treeview(self, columns=("Nombre","Teléfono","Email"), show="headings", height=15, bootstyle="primary")
        self.tree.heading("Nombre", text="NOMBRE", anchor=tk.W)
        self.tree.heading("Teléfono", text="TELÉFONO", anchor=tk.CENTER)
        self.tree.heading("Email", text="CORREO ELECTRÓNICO", anchor=tk.W)
        
        # Configurar anchos y alineación de columna
        self.tree.column("Nombre", anchor=tk.W, width=200, stretch=True)
        self.tree.column("Teléfono", anchor=tk.CENTER, width=120, stretch=False)
        self.tree.column("Email", anchor=tk.W, width=300, stretch=True)

        # Scrollbar para el Treeview
        vsb = ttkb.Scrollbar(self, orient="vertical", command=self.tree.yview, bootstyle="primary-round")
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.vsb = vsb # Almacenar la scrollbar para el layout

    def configurar_layout(self):
        """Organiza los widgets principales usando grid."""
        
        # Configuración del grid principal de la ventana
        self.grid_rowconfigure(0, weight=1) # Fila del Treeview
        self.grid_rowconfigure(1, weight=0) # Fila del Panel de Control
        self.grid_columnconfigure(0, weight=1) # Columna del Treeview
        
        # Posicionar el Treeview (Lista) a la izquierda y que se expanda
        self.tree.grid(row=0, column=0, padx=(20, 0), pady=20, sticky="nsew")
        # Posicionar el Scrollbar junto al Treeview
        self.vsb.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ns")
        
        # Posicionar el Panel de Control (Entrada y Botones) abajo y que se expanda horizontalmente
        self.frame_panel.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

    # --- MÉTODOS DE LÓGICA (Mantienen la funcionalidad original y correcta) ---

    def validar_campos(self, nombre, telefono, email, es_modificacion=False):
        """Valida los campos de entrada y muestra advertencias."""
        
        if not nombre or not telefono or not email:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return False

        if not telefono.isdigit():
            messagebox.showwarning("Teléfono inválido", "El teléfono debe contener solo números.")
            return False

        if not ("@" in email and "." in email):
            messagebox.showwarning("Email inválido", "Ingrese un email válido (debe contener '@' y '.').")
            return False

        # Verificar duplicados
        for i, contacto in enumerate(self.agenda):
            if contacto["nombre"].lower() == nombre.lower():
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
        
        # Llenar con los datos actualizados, ordenados por nombre
        self.agenda.sort(key=lambda x: x['nombre'].lower())
        for contacto in self.agenda:
            self.tree.insert("", tk.END, values=(contacto["nombre"], contacto["telefono"], contacto["email"]))

    def agregar_o_modificar_contacto(self):
        """Función unificada para agregar o guardar modificaciones."""
        
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        
        es_modificacion = self.contacto_a_modificar_indice != -1

        if not self.validar_campos(nombre, telefono, email, es_modificacion):
            return

        nuevo_contacto = {"nombre": nombre, "telefono": telefono, "email": email}

        if es_modificacion:
            self.agenda[self.contacto_a_modificar_indice] = nuevo_contacto
            messagebox.showinfo("Éxito", "Contacto modificado correctamente.")
            self.cancelar_modificacion(limpiar=True) 
        else:
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
            # La agenda debe estar ordenada igual que el treeview para que el índice coincida
            # Como actualizamos_lista ordena, este índice es correcto.
            self.agenda.pop(indice) 
            self.actualizar_lista()
            self.guardar_datos()

    def cargar_contacto_para_modificar(self):
        """Carga los datos del contacto seleccionado en los campos de entrada y habilita el modo de modificación."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Seleccione un contacto para modificar.")
            return
            
        self.contacto_a_modificar_indice = self.tree.index(seleccion[0])
        contacto = self.agenda[self.contacto_a_modificar_indice]
        
        self.limpiar_campos()
        self.entry_nombre.insert(0, contacto["nombre"])
        self.entry_telefono.insert(0, contacto["telefono"])
        self.entry_email.insert(0, contacto["email"])
        
        # Cambiar el estado de la UI a modo Modificación
        self.btn_agregar.config(text="💾 Guardar Modificación", bootstyle="success")
        self.btn_cancelar.config(state=NORMAL)
        self.btn_modificar.config(state=DISABLED)
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
                self.agenda = []
        else:
            self.agenda = []

    def guardar_datos(self):
        """Guarda la lista de contactos en el archivo JSON."""
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(self.agenda, f, indent=4)
        except IOError as e:
            messagebox.showerror("Error de Guardado", f"No se pudieron guardar los datos: {e}")

    def on_closing(self):
        """Función llamada al cerrar la ventana para guardar y salir."""
        self.guardar_datos()
        self.destroy()

if __name__ == "__main__":
    # Inicializa y corre la aplicación con un tema corporativo
    app = AgendaApp()
    app.mainloop()