import tkinter as tk
from tkinter import messagebox
import math
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def press(key):
    entry_var.set(entry_var.get() + str(key))

def clear():
    entry_var.set("")

def backspace():
    entry_var.set(entry_var.get()[:-1])

def calculate():
    try:
        expression = entry_var.get().replace("^", "**")
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        entry_var.set(str(result))
    except Exception:
        messagebox.showerror("Error", "Expresión inválida")


root = ttk.Window(themename="superhero") 
root.title("Calculadora Científica Galáctica")
root.resizable(False, False)

entry_var = tk.StringVar()

entry = ttk.Entry(
    root,
    textvariable=entry_var,
    font=("Orbitron", 22, "bold"), 
    bootstyle="dark",
    justify="right"
)
entry.grid(row=0, column=0, columnspan=6, padx=15, pady=20, ipady=10, sticky="nsew")

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3), ("sqrt", 1, 4), ("log", 1, 5),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3), ("sin", 2, 4), ("cos", 2, 5),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3), ("tan", 3, 4), ("^", 3, 5),
    ("0", 4, 0), (".", 4, 1), ("(", 4, 2), (")", 4, 3), ("C", 4, 4), ("⌫", 4, 5),
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
    elif text == "⌫":
        action = backspace
        style = color_map["back"]
    elif text in ("sqrt", "log", "sin", "cos", "tan"):
        action = lambda t=text: press(f"math.{t}(")
        style = color_map["functions"]
    elif text in ("+", "-", "*", "/", "^"):
        action = lambda t=text: press(t)
        style = color_map["operators"]
    else:
        action = lambda t=text: press(t)
        style = color_map["numbers"]

    ttk.Button(
        root,
        text=text,
        command=action,
        bootstyle=f"{style},rounded",
        width=12,
        padding=12,
        font=("Orbitron", 14, "bold")
    ).grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

for i in range(6):
    root.columnconfigure(i, weight=1)
for j in range(6):
    root.rowconfigure(j, weight=1)

root.mainloop()
