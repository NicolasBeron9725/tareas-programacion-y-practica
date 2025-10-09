# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk # Necesitas importar ttk para usar ttk.Style()
import math
from functools import partial
import ttkbootstrap as ttkb # Cambiado a ttkb para evitar conflicto con ttk.Style
from ttkbootstrap.constants import *

# ----- Ventana -----
# Si 'superhero' no está disponible no rompe: podés cambiar el themename.
root = ttkb.Window(themename="superhero") # Usar ttkb.Window
root.title("Calculadora Científica Galáctica")
root.resizable(False, False)

# ----- Configuración de Estilos (Solución al error -font) -----
style = ttk.Style()
# Configuración global para la fuente de los botones
# El estilo se aplica al tema por defecto de TButton
style.configure("TButton", font=("Arial", 14, "bold")) 
# Configuración global para la fuente de la entrada (Entry)
style.configure("TEntry", font=("Arial", 22, "bold")) 

# ----- Variables y entrada -----
entry_var = tk.StringVar()
# Ya no pasamos el argumento 'font' aquí; se usa el estilo global "TEntry"
entry = ttkb.Entry( 
    root,
    textvariable=entry_var,
    justify="right"
)
entry.grid(row=0, column=0, columnspan=6, padx=15, pady=20, ipady=10, sticky="nsew")

# ----- Funciones -----
def press(value):
    entry_var.set(entry_var.get() + str(value))

def clear():
    entry_var.set("")

def backspace():
    entry_var.set(entry_var.get()[:-1])

def calculate():
    try:
        expression = entry_var.get().replace("^", "**")
        # Funciones y constantes permitidas (seguras)
        allowed_names = {k: getattr(math, k) for k in ("sqrt","log","log10","sin","cos","tan","factorial")}
        allowed_names.update({
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "pow": pow
        })
        # Ejecución segura de la expresión
        result = eval(expression, {"__builtins__": None}, allowed_names)
        entry_var.set(str(result))
    except Exception as e:
        messagebox.showerror("Error", f"Expresión inválida:\n{e}")

# ----- Botones -----
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3), ("sqrt", 1, 4), ("log", 1, 5),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3), ("sin", 2, 4), ("cos", 2, 5),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3), ("tan", 3, 4), ("^", 3, 5),
    ("0", 4, 0), (".", 4, 1), ("(", 4, 2), (")", 4, 3), ("C", 4, 4), ("<-", 4, 5),
    ("=", 5, 0), ("+", 5, 1)
]

color_map = {
    "numbers": "secondary",
    "operators": "info",
    "functions": "warning",
    "clear": "danger",
    "back": "dark",
    "equal": "success"
}

for (text, row, col) in buttons:
    if text == "=":
        action = calculate
        style = color_map["equal"]
    elif text == "C":
        action = clear
        style = color_map["clear"]
    elif text in ("<-",):
        action = backspace
        style = color_map["back"]
    elif text in ("sqrt", "log", "sin", "cos", "tan"):
        action = partial(press, f"{text}(")
        style = color_map["functions"]
    elif text in ("+", "-", "*", "/", "^"):
        action = partial(press, text)
        style = color_map["operators"]
    else:
        action = partial(press, text)
        style = color_map["numbers"]

    # Usamos ttkb.Button y eliminamos el argumento 'font'
    ttkb.Button(
        root,
        text=text,
        command=action,
        bootstyle=style,
        padding=10
    ).grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

for i in range(6):
    root.columnconfigure(i, weight=1)
for j in range(6):
    root.rowconfigure(j, weight=1)

root.mainloop()
