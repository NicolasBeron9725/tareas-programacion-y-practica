import gradio as gr
import io
import contextlib

# Diccionario completo con 30 ejemplos educativos
ejemplos = {
    "hola_mundo": ('print("Hola, mundo!")', "Imprime un saludo en pantalla."),
    "variables": ('nombre = "Ana"\nedad = 20\nprint("Soy", nombre, "y tengo", edad, "años")', "Uso de variables para guardar datos de texto y números."),
    "operaciones": ("a = 10\nb = 3\nprint(a+b, a-b, a*b, a/b, a**b, a%b)", "Suma, resta, multiplicación, división, potencia y módulo."),
    "if_else": ("x = 7\nif x > 5:\n    print('Mayor que 5')\nelse:\n    print('Menor o igual a 5')", "Condicional simple con if y else."),
    "if_elif": ("nota = 8\nif nota >= 9:\n    print('Excelente')\nelif nota >= 6:\n    print('Aprobado')\nelse:\n    print('Desaprobado')", "Condicional múltiple con if, elif y else."),
    "while": ("contador = 1\nwhile contador <= 5:\n    print(contador)\n    contador += 1", "Bucle while que cuenta del 1 al 5."),
    "for_range": ("for i in range(5):\n    print('Iteración', i)", "Bucle for usando range() para 5 iteraciones."),
    "lista": ("numeros = [1,2,3]\nnumeros.append(4)\nprint(numeros)", "Lista que almacena varios valores y permite añadir elementos."),
    "tupla": ("coordenada = (10, 20)\nprint(coordenada[0])", "Tupla: colección inmutable de datos."),
    "diccionario": ("persona = {'nombre':'Ana','edad':20}\nprint(persona['nombre'])", "Diccionario con claves y valores."),
    "set": ("colores = {'rojo','azul','rojo'}\nprint(colores)", "Set: colección de elementos únicos, elimina duplicados."),
    "funcion": ("def saludar(nombre):\n    return f'Hola {nombre}'\nprint(saludar('Ana'))", "Función con parámetro y valor de retorno."),
    "recursividad": ("def factorial(n):\n    if n==0: return 1\n    return n*factorial(n-1)\nprint(factorial(5))", "Función recursiva para calcular factorial."),
    "try_except": ("try:\n    print(10/0)\nexcept ZeroDivisionError:\n    print('No se puede dividir por cero')", "Manejo de errores con try/except."),
    "archivos": ("with open('archivo.txt','w') as f:\n    f.write('Hola mundo')\n\nwith open('archivo.txt') as f:\n    print(f.read())", "Escribir y leer un archivo de texto."),
    "math": ("import math\nprint(math.sqrt(16), math.pi)", "Uso del módulo math: raíz cuadrada y número pi."),
    "strings": ('texto = "Python"\nprint(texto.upper(), texto.lower(), texto.replace("P","J"))', "Métodos para manipular cadenas de texto."),
    "comprension": ("numeros = [x*2 for x in range(5)]\nprint(numeros)", "Lista por comprensión: genera una lista de valores en una sola línea."),
    "enumerate": ("frutas = ['manzana','pera']\nfor i, f in enumerate(frutas):\n    print(i, f)", "Recorrer lista con índices usando enumerate()."),
    "zip": ("nombres = ['Ana','Luis']\nedades = [20,25]\nfor n,e in zip(nombres,edades):\n    print(n,e)", "Recorrer varias listas al mismo tiempo con zip()."),
    "lambda": ("doble = lambda x: x*2\nprint(doble(5))", "Funciones anónimas con lambda."),
    "map_filter": ("nums = [1,2,3,4]\nprint(list(map(lambda x:x*2, nums)))\nprint(list(filter(lambda x:x%2==0, nums)))", "Uso de map() y filter() con listas."),
    "clase": ("class Persona:\n    def __init__(self,nombre):\n        self.nombre = nombre\n    def saludar(self):\n        print('Hola soy',self.nombre)\n\np=Persona('Ana')\np.saludar()", "Ejemplo de clase y objeto en Python."),
    "herencia": ("class Animal:\n    def hablar(self): print('Sonido')\nclass Perro(Animal):\n    def hablar(self): print('Guau')\n\np=Perro()\np.hablar()", "Ejemplo de herencia entre clases."),
    "modulos": ("# archivo util.py\ndef hola(): return 'Hola'\n\n# archivo principal\nimport util\nprint(util.hola())", "Ejemplo de cómo importar otro archivo (módulo) en Python."),
    "random": ("import random\nprint(random.randint(1,10))", "Genera un número entero aleatorio entre 1 y 10."),
    "datetime": ("from datetime import datetime\nprint(datetime.now())", "Obtener fecha y hora actual."),
    "matriz": ("matriz = [[1,2,3],[4,5,6]]\nfor fila in matriz:\n    print(fila)", "Lista de listas que representa una matriz."),
    "dicc_anidado": ("alumno = {'nombre':'Ana','notas':{'mate':9,'historia':7}}\nprint(alumno['notas']['mate'])", "Diccionario dentro de otro diccionario."),
    "break_continue": ("for i in range(5):\n    if i==2: continue\n    if i==4: break\n    print(i)", "Uso de break (salir del bucle) y continue (saltar iteración)."),
    "mini_calculadora": ("def sumar(a,b): return a+b\ndef restar(a,b): return a-b\ndef mult(a,b): return a*b\ndef div(a,b): return a/b if b!=0 else 'Error'\n\nprint(sumar(2,3))\nprint(div(10,0))", "Mini calculadora con funciones básicas."),
}

def ejecutar_codigo(codigo):
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(codigo, {})
        return buffer.getvalue()
    except Exception as e:
        return f"Error: {str(e)}"

def obtener_ejemplo(ejemplo):
    if ejemplo in ejemplos:
        return ejemplos[ejemplo][0], ejemplos[ejemplo][1]
    return "Ejemplo no encontrado", ""

with gr.Blocks() as demo:
    gr.Markdown("# HackerMachetero – Aprende Python Ejecutando Ejemplos")

    opcion = gr.Dropdown(choices=list(ejemplos.keys()), label="Selecciona un ejemplo")
    salida_codigo = gr.Code(language="python", label="Código de ejemplo")
    salida_explicacion = gr.Textbox(label="Explicación", interactive=False)

    boton = gr.Button("Ejecutar código")
    salida_ejecucion = gr.Textbox(label="Salida del programa", interactive=False)

    # Mostrar código + explicación al seleccionar un ejemplo
    opcion.change(obtener_ejemplo, inputs=opcion, outputs=[salida_codigo, salida_explicacion])

    # Ejecutar el código y mostrar salida
    boton.click(ejecutar_codigo, inputs=salida_codigo, outputs=salida_ejecucion)

# Lanzar la app
demo.launch()

