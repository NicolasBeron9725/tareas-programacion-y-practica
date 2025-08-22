import random

num = random.randint(1, 10)
intentos = 0

while True:
    intentos += 1
    adivina = int(input("Adivina el número (1-10): "))
    if adivina == num:
        print(f"¡Correcto! Lo adivinaste en {intentos} intentos.")
        break
    elif adivina < num:
        print("Demasiado bajo.")
    else:
        print("Demasiado alto.")
