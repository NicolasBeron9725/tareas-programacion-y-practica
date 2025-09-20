import math

def estadisticas(lista):
    n = len(lista)
    m = media(lista)
    var = sum((x - m)**2 for x in lista) / n
    return {
        "media": m,
        "varianza": var,
        "desviacion_tipica": math.sqrt(var)
    }

print(estadisticas([1, 2, 3, 4, 5]))
