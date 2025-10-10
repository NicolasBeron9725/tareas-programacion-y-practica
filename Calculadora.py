import ttkbootstrap as tb
from ttkbootstrap.constants import *
import math
from fractions import Fraction
from tkinter import messagebox, scrolledtext
import numpy as np

# Funciones seguras
SAFE_FUNCS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,
    'ln': math.log,
    'sqrt': math.sqrt,
    'abs': abs,
    'factorial': math.factorial,
    'pi': math.pi,
    'e': math.e,
    'pow': math.pow,
    'matmul': np.matmul,   # Multiplicación matricial
    'array': np.array      # Crear matrices
}


def nth_root(x, n):
    if x < 0 and n % 2 == 1:
        return -((-x) ** (1.0 / n))
    return x ** (1.0 / n)

SAFE_FUNCS['nthroot'] = nth_root


# -----------------------------
# Gauss-Jordan con pivoteo
# -----------------------------
def gauss_jordan(A, b):
    """Resuelve Ax = b usando Gauss-Jordan con pivoteo parcial"""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1,1)
    n = len(b)
    M = np.hstack([A, b])

    for i in range(n):
        max_row = np.argmax(abs(M[i:, i])) + i
        if i != max_row:
            M[[i, max_row]] = M[[max_row, i]]

        M[i] = M[i] / M[i, i]

        for j in range(n):
            if j != i:
                M[j] = M[j] - M[j, i] * M[i]

    return M[:, -1]


def gauss_jordan_inverse(A):
    """Calcula la inversa de A usando Gauss-Jordan con pivoteo parcial"""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    I = np.eye(n)
    M = np.hstack([A, I])

    for i in range(n):
        max_row = np.argmax(abs(M[i:, i])) + i
        if i != max_row:
            M[[i, max_row]] = M[[max_row, i]]

        M[i] = M[i] / M[i, i]

        for j in range(n):
            if j != i:
                M[j] = M[j] - M[j, i] * M[i]

    return M[:, n:]


SAFE_FUNCS['gaussjordan'] = gauss_jordan
SAFE_FUNCS['gaussinv'] = gauss_jordan_inverse


# -----------------------------
# Evaluación segura
# -----------------------------
def to_fraction(expr: str) -> str:
    import re
    def repl(m):
        a, b = m.group(1), m.group(2)
        return f'Fraction({a},{b})'
    pattern = re.compile(r'(?<![A-Za-z0-9_])(\d+)\s*/\s*(\d+)(?![A-Za-z0-9_])')
    return pattern.sub(repl, expr)


def safe_eval(expr: str):
    expr = expr.replace('^', '**')
    expr = expr.replace('÷', '/').replace('×', '*')
    expr = to_fraction(expr)
    allowed_names = dict(SAFE_FUNCS)
    allowed_names['Fraction'] = Fraction
    return eval(expr, {"__builtins__": {}}, allowed_names)


def format_result(value):
    if isinstance(value, Fraction):
        return f"{value}  ≈  {float(value)}"
    if isinstance(value, (int, float)):
        return f"{value:.10g}" if isinstance(value, float) else str(value)
    if isinstance(value, np.ndarray):
        return str(value)
    return str(value)


def explain_steps(expr: str, result):
    e = expr.replace('**', '^').strip()
    steps = []

    if 'matmul' in e:
        steps.append("Multiplicación de matrices:")
        steps.append(" - Se multiplica cada fila de la primera matriz por cada columna de la segunda.")
        steps.append(" - Cada elemento C[i,j] = suma(A[i,k]*B[k,j]).")
        steps.append(f"Resultado:\n{result}")
        return "\n".join(steps)

    if any(fn in e for fn in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']):
        steps.append("Funciones aplicadas:")
        if 'sin' in e or 'cos' in e or 'tan' in e:
            steps.append(" - Trigonométricas en radianes.")
        if 'log' in e:
            steps.append(" - log base 10.")
        if 'ln' in e:
            steps.append(" - log natural.")
        if 'sqrt' in e:
            steps.append(" - Raíz cuadrada equivale a potencia 1/2.")

    if 'nthroot' in e:
        steps.append("Raíz enésima:")
        steps.append(" - nthroot(x, n) aplica x^(1/n).")

    if '^' in e:
        steps.append("Potencias:")
        steps.append(" - a^b se evalúa como a elevado a b.")

    if '/' in e and 'Fraction' in to_fraction(e):
        steps.append("Fracciones exactas:")
        steps.append(" - a/b se interpreta como Fraction(a,b).")

    if any(op in e for op in ['+', '-', '*', '/']):
        steps.append("Orden de operaciones:")
        steps.append(" - Potencias/raíces → multiplicación/división → suma/resta.")
        if '(' in e or ')' in e:
            steps.append(" - Los paréntesis se resuelven primero.")

    steps.append(f"Resultado final: {format_result(result)}")
    return "\n".join(steps)


# -----------------------------
# Interfaz gráfica
# -----------------------------
class Calculadora(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Calculadora Científica Clásica con Notas")
        self.geometry("1100x650")

        # Variables de control
        self.auto_steps = tb.BooleanVar(value=True)
        self.auto_calc = tb.BooleanVar(value=True)

        # ---------------------------
        # Entrada y resultado
        # ---------------------------
        self.display = tb.Entry(self, font=("Consolas", 20))
        self.display.pack(fill=X, padx=10, pady=10)

        self.result_label = tb.Label(self, text="Resultado:", font=("Consolas", 16), bootstyle="info")
        self.result_label.pack(anchor="w", padx=10)

        frame_main = tb.Frame(self)
        frame_main.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo (botones)
        self.buttons_frame = tb.Frame(frame_main)
        self.buttons_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Panel derecho (notas)
        right_frame = tb.Frame(frame_main)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        tb.Label(right_frame, text="Área de notas y historial", font=("Consolas", 14, "bold")).pack(anchor="w")

        self.notes = scrolledtext.ScrolledText(right_frame, wrap="word", height=20, font=("Consolas", 11))
        self.notes.pack(fill=BOTH, expand=True, pady=5)

        tb.Checkbutton(right_frame, text="Modo paso a paso (explicación automática)", variable=self.auto_steps).pack(anchor="w", pady=3)
        tb.Checkbutton(right_frame, text="Modo cálculo automático (mostrar resultado al finalizar)", variable=self.auto_calc).pack(anchor="w")

        # ---------------------------
        # Creación de botones
        # ---------------------------
        botones = [
            ["sin", "cos", "tan", "log", "ln"],
            ["(", ")", "sqrt", "y√x", "x^y"],
            ["a/b", "abs", "factorial", "pi", "e"],
            ["7", "8", "9", "/", "*"],
            ["4", "5", "6", "-", "+"],
            ["1", "2", "3", "0", "."],
        ]

        for fila in botones:
            row = tb.Frame(self.buttons_frame)
            row.pack(expand=True, fill=BOTH)
            for b in fila:
                color = "primary" if b.isalpha() or b in ("pi", "e", "(", ")", "sqrt", "x^y", "y√x") else "light"
                tb.Button(row, text=b, bootstyle=color, width=8, command=lambda x=b: self.on_key(x)).pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)

        # Botones inferiores
        bottom = tb.Frame(self.buttons_frame)
        bottom.pack(expand=True, fill=BOTH)

        tb.Button(bottom, text="C", bootstyle="danger", command=self.clear).pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)
        tb.Button(bottom, text="←", bootstyle="secondary", command=self.backspace).pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)
        tb.Button(bottom, text="+/-", bootstyle="secondary", command=self.toggle_sign).pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)
        tb.Button(bottom, text="=", bootstyle="success", command=self.evaluate).pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)

        # Inicializar notas
        self.toggle_notes_mode()

    # -----------------------------
    # Funciones de la calculadora
    # -----------------------------
    def on_key(self, t):
        if t == "sqrt":
            self.display.insert("end", "sqrt(")
        elif t == "x^y":
            self.display.insert("end", "^")
        elif t == "y√x":
            self.display.insert("end", "nthroot(")
        elif t in ("sin", "cos", "tan", "log", "ln", "abs", "factorial"):
            self.display.insert("end", f"{t}(")
        elif t in ("pi", "e"):
            self.display.insert("end", t)
        else:
            self.display.insert("end", t)

    def clear(self):
        self.display.delete(0, "end")
        self.result_label.config(text="Resultado:")

    def backspace(self):
        current = self.display.get()
        if current:
            self.display.delete(len(current)-1, "end")

    def toggle_sign(self):
        expr = self.display.get()
        if expr:
            self.display.delete(0, "end")
            self.display.insert(0, f"-({expr})")

    def evaluate(self, force_steps=False):
        expr = self.display.get()
        try:
            result = safe_eval(expr)
            self.result_label.config(text=f"Resultado: {format_result(result)}")

            self.notes.config(state="normal")
            if force_steps or self.auto_steps.get():
                explanation = explain_steps(expr, result)
                self.notes.insert("end", f"> {expr}\n{explanation}\n{'-'*30}\n", "note")
            else:
                self.notes.insert("end", f"{expr} = {format_result(result)}\n", "note")
            self.notes.config(state="disabled")

            self.notes.see("end")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular:\n{e}")

    def toggle_notes_mode(self):
        if self.auto_steps.get():
            self.notes.config(state="disabled")
        else:
            self.notes.config(state="normal")


# -----------------------------
# Programa principal
# -----------------------------
if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()