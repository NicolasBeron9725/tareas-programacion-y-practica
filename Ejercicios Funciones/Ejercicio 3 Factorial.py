def factorial(n):
    if n < 0:
        return "El número debe ser positivo"
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado

print(factorial(5))
