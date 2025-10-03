import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import random
import time
import math
import json
import os

# ----------------- CONFIGURACIÓN DEL JUEGO -----------------
TIEMPO_PREGUNTA = 20 # Segundos que dura el timer
NECESITAN_PARA_INSIGNIA = 3 # Aciertos necesarios en una categoría para ganar la insignia
SAVE_FILE = "preguntados_save.json"

# --- CATEGORÍAS Y TEMAS ---
PREGUNTAS = {
    "Redes": [
        {"pregunta": "¿Qué dispositivo conecta redes distintas?", "opciones": ["Switch", "Router", "Hub", "Firewall"], "respuesta": 1},
        {"pregunta": "¿Qué protocolo se usa para enviar correos?", "opciones": ["HTTP", "SMTP", "FTP", "IP"], "respuesta": 1},
        {"pregunta": "¿Qué significa LAN?", "opciones": ["Local Area Network", "Large Area Network", "Local Access Node", "Link Access Network"], "respuesta": 0},
        {"pregunta": "¿Qué dirección es privada en IPv4?", "opciones": ["192.168.1.1", "8.8.8.8", "23.45.67.89", "1.1.1.1"], "respuesta": 0},
        {"pregunta": "¿Qué puerto usa HTTP por defecto?", "opciones": ["80", "443", "22", "25"], "respuesta": 0},
        {"pregunta": "¿Qué protocolo resuelve nombres a IPs?", "opciones": ["DNS", "DHCP", "ARP", "ICMP"], "respuesta": 0},
        {"pregunta": "¿Qué es una máscara de subred?", "opciones": ["Divide red y host", "Tipo de cable", "Protocolo de cifrado", "Un router"], "respuesta": 0},
        {"pregunta": "¿Qué protocolo se usa para transferencia segura de archivos?", "opciones": ["SFTP", "Telnet", "HTTP", "SMTP"], "respuesta": 0},
        {"pregunta": "¿Qué dispositivo reduce dominio de colisión?", "opciones": ["Hub", "Switch", "Repeater", "Modem"], "respuesta": 1},
        {"pregunta": "¿Qué hace DHCP en una red?", "opciones": ["Asigna direcciones IP automáticamente", "Cifra paquetes", "Monitorea tráfico", "Resuelve nombres"], "respuesta": 0},
        {"pregunta": "¿Qué capa del modelo OSI gestiona el enrutamiento?", "opciones": ["Capa de Enlace", "Capa de Transporte", "Capa de Red", "Capa de Aplicación"], "respuesta": 2},
        {"pregunta": "¿Cuál es la función principal del protocolo ARP?", "opciones": ["Mapear direcciones IP a MAC", "Asignar direcciones IP dinámicamente", "Enviar correos electrónicos", "Establecer conexiones seguras"], "respuesta": 0},
    ],
    "IA": [
        {"pregunta": "¿Qué es aprendizaje supervisado?", "opciones": ["Entrenamiento sin datos", "Entrenamiento con etiquetas", "Entrenamiento aleatorio", "Entrenamiento automático"], "respuesta": 1},
        {"pregunta": "¿Qué técnica se usa para reducir dimensiones?", "opciones": ["PCA", "KNN", "SVM", "CNN"], "respuesta": 0},
        {"pregunta": "¿Qué es una red neuronal?", "opciones": ["Un algoritmo de sorting", "Un modelo inspirado en el cerebro", "Un protocolo de red", "Un lenguaje de programación"], "respuesta": 1},
        {"pregunta": "¿Qué mide la precisión en clasificación?", "opciones": ["Proporción de aciertos", "Velocidad del modelo", "Tamaño del dataset", "Número de features"], "respuesta": 0},
        {"pregunta": "¿Qué es overfitting?", "opciones": ["Modelo generaliza mal", "Modelo demasiado simple", "Optimización exitosa", "Arquitectura de red"], "respuesta": 0},
        {"pregunta": "¿Qué es un perceptrón?", "opciones": ["Neurona artificial", "Tipo de dataset", "Función de pérdida", "Librería de Python"], "respuesta": 0},
        {"pregunta": "¿Qué es un dataset de entrenamiento?", "opciones": ["Datos para entrenar", "Resultados finales", "Parámetros del modelo", "Arquitectura de red"], "respuesta": 0},
        {"pregunta": "¿Qué técnica evita overfitting?", "opciones": ["Regularización", "Aumento de datos", "Dropout", "Todas las anteriores"], "respuesta": 3},
        {"pregunta": "¿Qué es aprendizaje no supervisado?", "opciones": ["Entrenamiento sin etiquetas", "Entrenamiento con etiquetas", "Entrenamiento supervisado", "Entrenamiento paralelo"], "respuesta": 0},
        {"pregunta": "¿Qué hace una función de activación en una neurona?", "opciones": ["Introduce no linealidad", "Ordena datos", "Divide datasets", "Evalúa rendimiento"], "respuesta": 0},
        {"pregunta": "¿Qué métrica se calcula como (Verdaderos Positivos + Verdaderos Negativos) / Total?", "opciones": ["Precisión (Accuracy)", "Recall (Sensibilidad)", "F1-Score", "Curva ROC"], "respuesta": 0},
        {"pregunta": "¿Cuál es el propósito del 'backpropagation' en el entrenamiento de Redes Neuronales?", "opciones": ["Inferencia de datos", "Ajustar los pesos de la red", "Seleccionar la función de pérdida", "Inicializar los sesgos"], "respuesta": 1},
    ],
    "Programación": [
        {"pregunta": "¿Qué lenguaje se usa para estructura de páginas web?", "opciones": ["Python", "HTML", "C++", "Java"], "respuesta": 1},
        {"pregunta": "¿Qué estructura repite código?", "opciones": ["Condicional", "Bucle", "Clase", "Variable"], "respuesta": 1},
        {"pregunta": "¿Qué es una variable?", "opciones": ["Una función", "Un valor que puede cambiar", "Un tipo de dato fijo", "Un comentario"], "respuesta": 1},
        {"pregunta": "¿Qué significa OOP?", "opciones": ["Objetos y clases", "Ordenar operaciones", "Open Output Process", "Ninguna"], "respuesta": 0},
        {"pregunta": "¿Qué es un algoritmo?", "opciones": ["Conjunto de pasos", "Lenguaje", "Base de datos", "Interfaz gráfica"], "respuesta": 0},
        {"pregunta": "¿Qué operador asigna en Python?", "opciones": ["=", "==", ":", "->"], "respuesta": 0},
        {"pregunta": "¿Qué palabra define una función en Python?", "opciones": ["def", "func", "function", "lambda"], "respuesta": 0},
        {"pregunta": "¿Qué hace import en Python?", "opciones": ["Carga módulos", "Declara variables", "Ejecuta tests", "Compila código"], "respuesta": 0},
        {"pregunta": "¿Qué es una lista en Python?", "opciones": ["Colección ordenada", "Tipo de dato numérico", "Operador", "Función"], "respuesta": 0},
        {"pregunta": "¿Qué es un IDE?", "opciones": ["Entorno de desarrollo integrado", "Lenguaje de programación", "Servidor", "Protocolo"], "respuesta": 0},
        {"pregunta": "¿Qué principio de la POO describe la ocultación de los detalles de implementación?", "opciones": ["Herencia", "Polimorfismo", "Encapsulamiento", "Abstracción"], "respuesta": 2},
        {"pregunta": "¿Qué tipo de error ocurre cuando la sintaxis es correcta pero el programa no produce el resultado esperado?", "opciones": ["Error de Sintaxis", "Error Lógico", "Error de Compilación", "Error de Ejecución"], "respuesta": 1},
    ],
    "Ciberseguridad": [
        {"pregunta": "¿Cuál malware cifra archivos y pide rescate?", "opciones": ["Gusano", "Troyano", "Adware", "Ransomware"], "respuesta": 3},
        {"pregunta": "¿Qué significa VPN?", "opciones": ["Virtual Private Network", "Verified Protocol Node", "Variable Packet Network", "Virtual Packet Node"], "respuesta": 0},
        {"pregunta": "¿Qué es phishing?", "opciones": ["Tipo de firewall", "Ataque de ingeniería social", "Protocolo de red", "Antivirus"], "respuesta": 1},
        {"pregunta": "¿Qué mejora la seguridad de contraseñas?", "opciones": ["Usar contraseñas únicas", "Compartir contraseñas", "Usar 1234", "Guardar sin cifrar"], "respuesta": 0},
        {"pregunta": "¿Qué es autenticación multifactor?", "opciones": ["Varias pruebas de identidad", "Una contraseña larga", "Cifrado de disco", "Firewall activo"], "respuesta": 0},
        {"pregunta": "¿Qué es un firewall?", "opciones": ["Filtro de tráfico", "Antivirus", "Router", "Servidor web"], "respuesta": 0},
        {"pregunta": "¿Qué protocolo cifra web?", "opciones": ["TLS/SSL", "FTP", "HTTP", "SMTP"], "respuesta": 0},
        {"pregunta": "¿Qué es un exploit?", "opciones": ["Código que aprovecha vulnerabilidad", "Tipo de antivirus", "Configuración de red", "Protocolo"], "respuesta": 0},
        {"pregunta": "¿Qué es un ataque DDoS?", "opciones": ["Saturación de recursos", "Robo de contraseñas", "Cifrado de datos", "Instalación de malware"], "respuesta": 0},
        {"pregunta": "¿Qué práctica ayuda a la seguridad?", "opciones": ["Actualizaciones regulares", "Ignorar parches", "Compartir claves", "Usar software pirata"], "respuesta": 0},
        {"pregunta": "¿Qué tipo de cifrado utiliza la misma clave para cifrar y descifrar la información?", "opciones": ["Cifrado Simétrico", "Cifrado Asimétrico", "Hashing", "Esteganografía"], "respuesta": 0},
        {"pregunta": "¿Qué representa la 'C' en la Tríada CIA de la seguridad de la información?", "opciones": ["Confidencialidad", "Conexión", "Control", "Copia de Seguridad"], "respuesta": 0},
    ],
}

CATEGORIAS = list(PREGUNTAS.keys())
COLORES = {"Redes": "#ef4444", "IA": "#f59e0b", "Programación": "#06b6d4", "Ciberseguridad": "#10b981"}
ICONOS = {"Redes": "🔗", "IA": "🧠", "Programación": "👨‍💻", "Ciberseguridad": "🛡️"}
ICONO_SIZE_RULETA = 30 
ICONO_SIZE_INSIGNIA = 24 
ICONO_SIZE_INSIGNIA_BAR = 12 

# ----------------- APLICACIÓN PRINCIPAL -----------------

class PreguntadosFinal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Preguntados Tech - Final Mejorado")
        self.geometry("1150x760")
        self.resizable(False, False)

        # Estado del juego
        self.jugadores_individuales = []
        self.participantes = [] 
        self.es_modo_equipo = False
        self.puntajes = {}
        self.turno_idx = 0
        self.categoria_actual = None
        self.pregunta_actual = None
        self.indice_actual = None
        self.usadas = {c: set() for c in CATEGORIAS}
        self.timer_secs = TIEMPO_PREGUNTA
        self.timer_running = False
        self.timer_id = None # Para controlar la llamada after del timer
        self.correct_counts = {}
        self.insignias = {}
        
        # Variables de control de la ruleta (para animación fluida)
        self.ruleta_paso_actual = 0
        self.ruleta_pasos_totales = 70
        self.ruleta_giro_objetivo = 0
        self.ruleta_velocidad_inicial = 0
        self.girando_id = None # ID de la llamada after para la ruleta
        self.angulo = 0

        # UI config
        self.theme = "dark"
        self.ui_scale = 1.0
        self.base_fonts = {
            "title": ("Arial", 18, "bold"),
            "header": ("Arial", 14, "bold"),
            "question": ("Arial", 16),
            "option": ("Arial", 14),
            "small": ("Arial", 11),
            "ruleta_icon": ("Arial", ICONO_SIZE_RULETA)
        }

        # Creación de UI
        self.crear_menu()
        self.crear_izquierda()
        self.crear_derecha()
        self.pedir_config_inicial()
        self.aplicar_tema()
        
    # --- UI y TEMAS ---

    def crear_menu(self):
        menubar = tk.Menu(self)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Guardar partida", command=self.guardar_partida)
        game_menu.add_command(label="Cargar partida", command=self.cargar_partida)
        game_menu.add_separator()
        game_menu.add_command(label="Tema claro/oscuro", command=self.toggle_theme)
        game_menu.add_separator()
        game_menu.add_command(label="Salir", command=self.destroy)
        menubar.add_cascade(label="Juego", menu=game_menu)
        self.config(menu=menubar)

    def crear_izquierda(self):
        left = tk.Frame(self, width=400)
        left.pack(side="left", fill="y")
        left.config(bg="#0b1220")

        self.canvas = tk.Canvas(left, width=360, height=360, highlightthickness=0)
        self.canvas.pack(pady=12)
        self.centro = (180, 180)
        self.radio = 160
        self.dibujar_ruleta()
        self.canvas.create_polygon(175, 12, 185, 12, 180, 38, fill="#ffd23f", outline="black", tags="pointer")

        btn_frame = tk.Frame(left, bg=left["bg"])
        btn_frame.pack(pady=6)
        self.btn_girar = tk.Button(btn_frame, text="Girar Ruleta", command=self.girar_ruleta, width=12)
        self.btn_girar.grid(row=0, column=0, padx=6)
        self.btn_reset = tk.Button(btn_frame, text="Reiniciar juego", command=self.reiniciar_juego, width=12)
        self.btn_reset.grid(row=0, column=1, padx=6)

        score_wrap = tk.Frame(left, bg=left["bg"])
        score_wrap.pack(fill="both", expand=True, pady=8)
        canvas_scores = tk.Canvas(score_wrap, bg=left["bg"], highlightthickness=0, height=300)
        scrollbar = tk.Scrollbar(score_wrap, orient="vertical", command=canvas_scores.yview)
        self.scores_container = tk.Frame(canvas_scores, bg=left["bg"])
        self.scores_container.bind("<Configure>", lambda e: canvas_scores.configure(scrollregion=canvas_scores.bbox("all")))
        canvas_scores.create_window((0, 0), window=self.scores_container, anchor="nw")
        canvas_scores.configure(yscrollcommand=scrollbar.set)
        canvas_scores.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.player_widgets = {}

    def crear_derecha(self):
        right = tk.Frame(self, bg="#071827")
        right.pack(side="right", expand=True, fill="both")

        header = tk.Frame(right, bg=right["bg"])
        header.pack(fill="x", pady=10, padx=10)
        self.lbl_categoria = tk.Label(header, text="Categoría: —", font=self._font("header"), bg=header["bg"])
        self.lbl_categoria.pack(side="left")
        self.lbl_turno = tk.Label(header, text="Turno: -", font=self._font("header"), bg=header["bg"])
        self.lbl_turno.pack(side="left", padx=12)

        self.canvas_timer = tk.Canvas(header, width=80, height=80, bg=header["bg"], highlightthickness=0)
        self.canvas_timer.pack(side="right")
        self.canvas_timer.create_text(40, 40, text=f"{self.timer_secs}", fill="white", font=self._font("small"), tags="timer_text")

        self.lbl_big_cat = tk.Label(right, text="", font=self._font("title"), bg=right["bg"])
        self.lbl_big_cat.pack(padx=12, anchor="w")

        self.lbl_pregunta = tk.Label(right, text="Presioná 'Girar Ruleta' para iniciar", wraplength=700, justify="left", font=self._font("question"), bg=right["bg"])
        self.lbl_pregunta.pack(padx=12, pady=(6, 14), anchor="w")

        self.opcion_buttons = []
        for i in range(4):
            b = tk.Button(right, text=f"Opción {i + 1}", anchor="w", justify="left", width=90, height=2, font=self._font("option"), command=lambda idx=i: self.seleccionar_opcion(idx))
            b.pack(padx=12, pady=6)
            b.config(state="disabled")
            # Usar un color que contraste con el fondo oscuro y resalte al pasar el mouse
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg="#94a3b8"))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg="#f0f0f0" if self.theme == "light" else "#374151"))
            self.opcion_buttons.append(b)

        bottom = tk.Frame(right, bg=right["bg"])
        bottom.pack(fill="x", padx=12, pady=8)
        self.lbl_info = tk.Label(bottom, text="", font=self._font("small"), bg=bottom["bg"])
        self.lbl_info.pack(side="left")
        self.btn_siguiente = tk.Button(bottom, text="Continuar", command=self.siguiente, state="disabled")
        self.btn_siguiente.pack(side="right")
        
    def _font(self, key):
        f = self.base_fonts.get(key, ("Arial", 12))
        if len(f) == 3:
            return (f[0], max(8, int(f[1] * self.ui_scale)), f[2])
        return (f[0], max(8, int(f[1] * self.ui_scale)))

    def aplicar_tema(self):
        if self.theme == "dark":
            bg_main = "#071827"
            left_bg = "#0b1220"
            text_fg = "white"
            player_bg = "#1f2937"
            player_fg = "white"
            button_default_bg = "#374151"
        else:
            bg_main = "#f3f4f6"
            left_bg = "#e6eef5"
            text_fg = "#071827"
            player_bg = "#e5e7eb"
            player_fg = "#071827"
            button_default_bg = "#f0f0f0" # SystemButtonFace
        
        self.config(bg=bg_main)
        
        # Aplicar a frames
        self.winfo_children()[0].config(bg=left_bg) # left frame
        self.winfo_children()[1].config(bg=bg_main) # right frame

        for widget in [self.winfo_children()[1].winfo_children()[0], self.winfo_children()[1].winfo_children()[-1]]: # header y bottom
             widget.config(bg=bg_main)
        
        # Aplicar a labels en right
        for lbl in [self.lbl_categoria, self.lbl_turno, self.lbl_big_cat, self.lbl_pregunta, self.lbl_info]:
            lbl.config(bg=bg_main, fg=text_fg)
        
        # Aplicar a canvas y su texto
        self.canvas_timer.config(bg=bg_main)
        self.canvas_timer.itemconfig("timer_text", fill=text_fg)
        
        # Aplicar a botones de opción
        for b in self.opcion_buttons:
             b.config(bg=button_default_bg, fg=text_fg)
             b.bind("<Leave>", lambda e, btn=b: btn.config(bg=button_default_bg))

        # Reconstruir marcador para aplicar temas
        self.reconstruir_marcador()

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.aplicar_tema()

    # --- LÓGICA DE JUGADORES Y TURNOS ---

    def pedir_config_inicial(self):
        if os.path.exists(SAVE_FILE) and messagebox.askyesno("Cargar", "Encontré una partida guardada. Querés cargarla?"):
            try:
                self.cargar_partida()
                return
            except Exception:
                messagebox.showwarning("Carga fallida", "No se pudo cargar, inicia nueva.")
        self.pedir_jugadores()

    def pedir_jugadores(self):
        modo = simpledialog.askstring("Modo de Juego", "Elegí el modo:\n1. Individual (2 a 4 jugadores)\n2. Por Equipos (2 vs 2)", parent=self, initialvalue="1")
        if modo is None: return
        
        modo = modo.strip()
        
        if modo == "2":
            self.es_modo_equipo = True
            self.participantes = ["Equipo A", "Equipo B"]
            
            self.jugadores_individuales = []
            jug_A1 = simpledialog.askstring("Equipo A", "Nombre del Jugador 1 del Equipo A:", parent=self) or "A1"
            jug_A2 = simpledialog.askstring("Equipo A", "Nombre del Jugador 2 del Equipo A:", parent=self) or "A2"
            jug_B1 = simpledialog.askstring("Equipo B", "Nombre del Jugador 1 del Equipo B:", parent=self) or "B1"
            jug_B2 = simpledialog.askstring("Equipo B", "Nombre del Jugador 2 del Equipo B:", parent=self) or "B2"
            self.jugadores_individuales.extend([jug_A1, jug_A2, jug_B1, jug_B2])
            
            self.rotacion_turnos = [jug_A1, jug_B1, jug_A2, jug_B2]
            
        else:
            self.es_modo_equipo = False
            num = simpledialog.askinteger("Jugadores Individuales", "¿Cuántos jugadores? (2 a 4)", parent=self, minvalue=2, maxvalue=4)
            if not num: num = 2
                
            self.participantes = []
            self.jugadores_individuales = []
            for i in range(num):
                nombre = simpledialog.askstring(f"Jugador {i + 1}", f"Ingrese nombre del Jugador {i + 1}:", parent=self)
                if not nombre: nombre = f"Jugador {i + 1}"
                self.participantes.append(nombre)
                self.jugadores_individuales.append(nombre)
            self.rotacion_turnos = self.participantes
        
        self.puntajes = {p: 0 for p in self.participantes}
        self.correct_counts = {p: {c: 0 for c in CATEGORIAS} for p in self.participantes}
        self.insignias = {p: set() for p in self.participantes}
        self.usadas = {c: set() for c in CATEGORIAS}
        self.turno_idx = 0
        self.reconstruir_marcador()

    def get_participante_actual(self):
        if not self.participantes: return None
        if self.es_modo_equipo:
            nombre_persona = self.rotacion_turnos[self.turno_idx % len(self.rotacion_turnos)]
            if nombre_persona in self.jugadores_individuales[0:2]:
                return "Equipo A"
            else:
                return "Equipo B"
        else:
            return self.participantes[self.turno_idx % len(self.participantes)]

    def get_nombre_turno_label(self):
        if not self.rotacion_turnos: return "Turno: -"
        nombre_persona = self.rotacion_turnos[self.turno_idx % len(self.rotacion_turnos)]
        if self.es_modo_equipo:
            equipo = self.get_participante_actual()
            return f"Turno: {equipo} ({nombre_persona})"
        else:
            return f"Turno: {nombre_persona}"

    # --- Ruleta y Animación ---

    def dibujar_ruleta(self):
        self.canvas.delete("all", "pointer")
        num_categorias = len(CATEGORIAS)
        angulo_segmento = 360 / num_categorias
        
        for i, cat in enumerate(CATEGORIAS):
            start_angle = self.angulo + i * angulo_segmento
            end_angle = self.angulo + (i + 1) * angulo_segmento
            
            self.canvas.create_arc(self.centro[0] - self.radio, self.centro[1] - self.radio, 
                                   self.centro[0] + self.radio, self.centro[1] + self.radio, 
                                   start=start_angle, extent=angulo_segmento, fill=COLORES[cat], 
                                   outline="white", width=2, tags=cat)
            
            mid_angle = math.radians(start_angle + angulo_segmento / 2)
            icon_x = self.centro[0] + (self.radio * 0.7) * math.cos(mid_angle)
            icon_y = self.centro[1] - (self.radio * 0.7) * math.sin(mid_angle) 
            
            self.canvas.create_text(icon_x, icon_y, text=ICONOS[cat], 
                                    font=self._font("ruleta_icon"), fill="white", tags=f"icon_{cat}")
            
        self.canvas.create_oval(self.centro[0]-30, self.centro[1]-30, self.centro[0]+30, self.centro[1]+30, 
                                fill="#273347", outline="white", width=2, tags="center_circle")
        self.canvas.create_text(self.centro[0], self.centro[1], text="GO", fill="white", tags="center_text")
        self.canvas.create_polygon(175, 12, 185, 12, 180, 38, fill="#ffd23f", outline="black", tags="pointer")
        self.canvas.tag_raise("pointer")

    def girar_ruleta(self):
        if self.timer_running or self.girando_id is not None: return
        self.btn_girar.config(state="disabled")
        
        # Reiniciar variables de giro
        self.ruleta_paso_actual = 0
        self.ruleta_pasos_totales = 70 
        self.ruleta_giro_objetivo = random.randint(720, 1080) # 2 a 3 vueltas completas
        self.ruleta_velocidad_inicial = self.ruleta_giro_objetivo / self.ruleta_pasos_totales
        
        self.animar_giro()

    def animar_giro(self):
        if self.ruleta_paso_actual >= self.ruleta_pasos_totales:
            self.girando_id = None
            self.angulo %= 360
            self.dibujar_ruleta()
            self.determinar_categoria()
            return

        self.ruleta_paso_actual += 1
        
        fraccion_tiempo = self.ruleta_paso_actual / self.ruleta_pasos_totales
        
        # Curva de desaceleración (Deceleración rápida al final)
        velocidad_factor = 1.0 - math.pow(fraccion_tiempo, 4) 
        
        # Calcular el ángulo para este paso, añadiendo un pequeño factor base para asegurar el movimiento
        angulo_paso = self.ruleta_velocidad_inicial * (velocidad_factor * 0.95 + 0.05)
        
        self.angulo += angulo_paso
        self.dibujar_ruleta()
        
        # Programar el siguiente frame (40ms = 25 FPS)
        tiempo_siguiente_frame = 40 
        self.girando_id = self.after(tiempo_siguiente_frame, self.animar_giro)

    def determinar_categoria(self):
        num_categorias = len(CATEGORIAS)
        angulo_segmento = 360 / num_categorias
        angulo_puntero = 90 - self.angulo 
        if angulo_puntero < 0: angulo_puntero += 360
        indice_ruleta = int(angulo_puntero // angulo_segmento)
        categoria_elegida = CATEGORIAS[indice_ruleta % num_categorias]
        
        self.categoria_actual = categoria_elegida
        self.mostrar_pregunta()

    # --- Lógica de Juego y Rebote ---

    def mostrar_pregunta(self):
        preguntas_disponibles = [
            i for i in range(len(PREGUNTAS[self.categoria_actual])) 
            if i not in self.usadas[self.categoria_actual]
        ]
        if not preguntas_disponibles:
            self.lbl_pregunta.config(text=f"¡Categoría '{self.categoria_actual}' agotada! Girá de nuevo.")
            self.btn_girar.config(state="normal")
            self.lbl_categoria.config(text=f"Categoría: {ICONOS[self.categoria_actual]} {self.categoria_actual} (Agotada)", fg=COLORES[self.categoria_actual])
            self.lbl_big_cat.config(text=f"¡CATEGORÍA AGOTADA! 🥲")
            self.lbl_info.config(text="")
            self.timer_stop()
            for b in self.opcion_buttons: b.config(text="", state="disabled", bg="#f0f0f0" if self.theme == "light" else "#374151")
            return
            
        # Elegir una pregunta no usada. Usamos la primera disponible por simplicidad.
        self.indice_actual = preguntas_disponibles[0] 
        pregunta_data = PREGUNTAS[self.categoria_actual][self.indice_actual]
        self.pregunta_actual = pregunta_data
        
        self.lbl_categoria.config(text=f"Categoría: {ICONOS[self.categoria_actual]} {self.categoria_actual}", fg=COLORES[self.categoria_actual])
        self.lbl_big_cat.config(text=f"{ICONOS[self.categoria_actual]} {self.categoria_actual.upper()}")
        self.lbl_pregunta.config(text=f"[{self.indice_actual + 1}/{len(PREGUNTAS[self.categoria_actual])}] {pregunta_data['pregunta']}")
        
        for i in range(4):
            self.opcion_buttons[i].config(text=pregunta_data["opciones"][i], state="normal", bg="#f0f0f0" if self.theme == "light" else "#374151")
            
        self.timer_start()
        self.btn_siguiente.config(state="disabled")

    def seleccionar_opcion(self, indice_opcion):
        if not self.timer_running and indice_opcion != -1: return # Ignorar click si no hay timer
        self.timer_stop()
        
        respuesta_correcta = self.pregunta_actual["respuesta"]
        participante = self.get_participante_actual()
        acierto = False 

        if indice_opcion == respuesta_correcta:
            acierto = True
            self.puntajes[participante] += 1
            self.correct_counts[participante][self.categoria_actual] += 1
            self.lbl_info.config(text="¡Correcto! +1 punto. ¡Seguís jugando!", fg="#10b981")
            
            # ✅ CORREGIDO: Se usa self.opcion_buttons
            self.opcion_buttons[indice_opcion].config(bg="#a7f3d0") 
            
            if self.categoria_actual not in self.insignias[participante] and self.correct_counts[participante][self.categoria_actual] >= NECESITAN_PARA_INSIGNIA:
                self.insignias[participante].add(self.categoria_actual)
                messagebox.showinfo("¡Insignia Ganada!", f"¡{participante} ganó la insignia de {self.categoria_actual}!")
        else:
            if indice_opcion == -1:
                # Caso de tiempo agotado
                self.lbl_info.config(text="¡Tiempo Agotado! Pierdes el turno.", fg="#ef4444")
            else:
                # Caso de respuesta incorrecta
                self.lbl_info.config(text="Incorrecto. La respuesta era: ¡Pierdes el turno!", fg="#ef4444")
                self.opcion_buttons[indice_opcion].config(bg="#fecaca")
                
            self.opcion_buttons[respuesta_correcta].config(bg="#a7f3d0")
            
            # --- REBOTE: CAMBIO DE TURNO ---
            self.turno_idx += 1 

        self.usadas[self.categoria_actual].add(self.indice_actual)
        for b in self.opcion_buttons: b.config(state="disabled")
        self.reconstruir_marcador()
        self.btn_siguiente.config(state="normal")
        
        if acierto:
            self.btn_siguiente.config(text="Volver a Girar")
        else:
            self.btn_siguiente.config(text="Siguiente Turno")

        self.verificar_fin_juego()

    def siguiente(self):
        self.lbl_turno.config(text=self.get_nombre_turno_label())
        self.lbl_pregunta.config(text="Presioná 'Girar Ruleta' para la siguiente ronda.")
        self.lbl_categoria.config(text="Categoría: —")
        self.lbl_big_cat.config(text="")
        self.lbl_info.config(text="")
        self.btn_girar.config(state="normal")
        self.btn_siguiente.config(state="disabled")
        self.btn_siguiente.config(text="Continuar") 
        for b in self.opcion_buttons: b.config(text="", state="disabled", bg="#f0f0f0" if self.theme == "light" else "#374151")
        self.reconstruir_marcador()

    def verificar_fin_juego(self):
        participante = self.get_participante_actual()
        if len(self.insignias[participante]) == len(CATEGORIAS):
            messagebox.showinfo("¡VICTORIA!", f"¡{participante} ha ganado todas las insignias y el juego!")
            self.btn_girar.config(state="disabled")
            self.btn_siguiente.config(state="disabled")
            return True
        return False
        
    # --- Marcador, Timer, Guardar/Cargar ---

    def reconstruir_marcador(self):
        for w in self.scores_container.winfo_children():
            w.destroy()
            
        self.player_widgets.clear()
        current_player = self.get_participante_actual()
        
        for p in self.participantes:
            bg_player = "#1f2937" if self.theme == "dark" else "#e5e7eb"
            fg_player = "white" if self.theme == "dark" else "#071827"
            
            is_current = (p == current_player)
            if is_current:
                bg_player = "#4c1d95" 
                fg_player = "white"

            outer = tk.Frame(self.scores_container, pady=4, padx=8, bg=bg_player, bd=2, relief=tk.RAISED if is_current else tk.SOLID) 
            outer.pack(fill="x", padx=6, pady=4)
            
            label_frame = tk.Frame(outer, bg=bg_player)
            label_frame.pack(side="top", fill="x", padx=0, pady=(4, 0))
            
            lbl_name = tk.Label(label_frame, text=f"{p}: {self.puntajes[p]} pts", anchor="w", 
                                 bg=bg_player, fg=fg_player, font=self._font("header"))
            lbl_name.pack(side="left", padx=(0, 6)) 
            
            ins_frame = tk.Frame(label_frame, bg=bg_player)
            ins_frame.pack(side="left", fill="x", expand=True)
            
            insignia_widgets = {}

            for cat in CATEGORIAS:
                insignia_text = ICONOS[cat] if cat in self.insignias[p] else '⚪'
                insignia_fg = COLORES[cat] if cat in self.insignias[p] else "#6b7280"
                
                lbl_insignia = tk.Label(ins_frame, text=insignia_text, font=("Arial", ICONO_SIZE_INSIGNIA), 
                                         fg=insignia_fg, bg=bg_player)
                lbl_insignia.pack(side="left", padx=2)
                insignia_widgets[cat] = lbl_insignia

            prog_frame = tk.Frame(outer, bg=bg_player)
            prog_frame.pack(side="top", fill="x", padx=8, pady=(4, 8))

            prog_bars = {}
            for i, cat in enumerate(CATEGORIAS):
                bar_container = tk.Frame(prog_frame, bg=bg_player)
                bar_container.pack(side="left", padx=(4, 8)) 

                lbl_icon = tk.Label(bar_container, text=ICONOS[cat], font=("Arial", ICONO_SIZE_INSIGNIA_BAR), 
                                     bg=bg_player, fg=COLORES[cat])
                lbl_icon.pack(side="left")

                bar_width = 60 
                bar = tk.Frame(bar_container, width=bar_width, height=8, bg="#ccc") 
                bar.pack(side="left", padx=4)

                aciertos = self.correct_counts[p][cat]
                progreso = min(aciertos / NECESITAN_PARA_INSIGNIA, 1.0)
                
                fill_width = int(bar_width * progreso)
                fill = tk.Frame(bar, width=fill_width, height=8, bg=COLORES[cat])
                fill.pack(side="left")

                prog_bars[cat] = {"frame": bar_container, "label_icon": lbl_icon, "bar": bar, "fill": fill}

            self.player_widgets[p] = {
                "outer": outer,
                "label_frame": label_frame,
                "label_name": lbl_name,
                "ins_frame": ins_frame,
                "insignias": insignia_widgets,
                "prog_frame": prog_frame,
                "prog_bars": prog_bars
            }

        self.lbl_turno.config(text=self.get_nombre_turno_label())

    def timer_start(self):
        self.timer_stop()
        self.timer_secs = TIEMPO_PREGUNTA
        self.timer_running = True
        self.timer_update()

    def timer_stop(self):
        self.timer_running = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        if self.girando_id:
            self.after_cancel(self.girando_id)
            self.girando_id = None

    def timer_update(self):
        if not self.timer_running:
            return
            
        self.canvas_timer.delete("timer_text", "timer_arc")
        
        # 1. Dibujar el arco de progreso
        angle_start = 90
        angle_extent = -(360 * (self.timer_secs / TIEMPO_PREGUNTA))
        self.canvas_timer.create_arc(5, 5, 75, 75, start=angle_start, extent=angle_extent, 
                                     outline="#ff6f00", style=tk.ARC, width=4, tags="timer_arc")
        
        # 2. Dibujar el texto
        self.canvas_timer.create_text(40, 40, text=f"{self.timer_secs}", fill="white", 
                                      font=self._font("small"), tags="timer_text")
        
        # 3. Lógica de conteo
        if self.timer_secs > 0:
            self.timer_secs -= 1
            # Repetir cada segundo (1000ms)
            self.timer_id = self.after(1000, self.timer_update) 
        else:
            # 4. Tiempo agotado: llama a seleccionar_opcion con -1 (opción no seleccionada)
            self.seleccionar_opcion(-1) 

    def guardar_partida(self):
        try:
            data = {
                "participantes": self.participantes,
                "es_modo_equipo": self.es_modo_equipo,
                "jugadores_individuales": self.jugadores_individuales,
                "rotacion_turnos": self.rotacion_turnos,
                "puntajes": self.puntajes,
                "turno_idx": self.turno_idx,
                "usadas": {c: list(u) for c, u in self.usadas.items()}, # Convertir sets a listas
                "correct_counts": self.correct_counts,
                "insignias": {p: list(i) for p, i in self.insignias.items()} # Convertir sets a listas
            }
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo("Guardado", f"Partida guardada con éxito en {SAVE_FILE}")
        except Exception as e:
            messagebox.showerror("Error de Guardado", f"No se pudo guardar la partida: {e}")

    def cargar_partida(self):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
            
            self.participantes = data["participantes"]
            self.es_modo_equipo = data["es_modo_equipo"]
            self.jugadores_individuales = data["jugadores_individuales"]
            self.rotacion_turnos = data["rotacion_turnos"]
            self.puntajes = data["puntajes"]
            self.turno_idx = data["turno_idx"]
            
            # Convertir listas de vuelta a sets
            self.usadas = {c: set(u) for c, u in data["usadas"].items()} 
            self.correct_counts = data["correct_counts"]
            self.insignias = {p: set(i) for p, i in data["insignias"].items()}
            
            # Resetear estado de pregunta
            self.timer_stop()
            self.lbl_pregunta.config(text="Partida cargada. Presioná 'Girar Ruleta' para continuar.")
            self.lbl_categoria.config(text="Categoría: —")
            self.lbl_big_cat.config(text="")
            for b in self.opcion_buttons: b.config(text="", state="disabled", bg="#f0f0f0" if self.theme == "light" else "#374151")
            self.btn_girar.config(state="normal")
            self.btn_siguiente.config(state="disabled")

            self.reconstruir_marcador()
            messagebox.showinfo("Cargado", "Partida cargada con éxito.")

        except FileNotFoundError:
            messagebox.showerror("Error de Carga", f"Archivo {SAVE_FILE} no encontrado.")
            self.pedir_jugadores()
        except json.JSONDecodeError:
            messagebox.showerror("Error de Carga", "El archivo de guardado está corrupto.")
            self.pedir_jugadores()
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Ocurrió un error al cargar: {e}")
            self.pedir_jugadores()

    def reiniciar_juego(self):
        if messagebox.askyesno("Reiniciar", "¿Estás seguro de que querés reiniciar el juego? Se perderá el progreso actual."):
            self.timer_stop()
            self.pedir_jugadores()
            self.siguiente() # Limpiar la interfaz
            self.lbl_pregunta.config(text="Juego Reiniciado. Presioná 'Girar Ruleta'.")


if __name__ == "__main__":
    app = PreguntadosFinal()
    app.mainloop()