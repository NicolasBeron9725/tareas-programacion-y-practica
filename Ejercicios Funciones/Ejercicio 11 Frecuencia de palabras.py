def contar_palabras(texto):
    palabras = texto.split()
    freq = {}
    for p in palabras:
        freq[p] = freq.get(p, 0) + 1
    return freq

def mas_repetida(diccionario):
    return max(diccionario.items(), key=lambda x: x[1])

texto = "hola hola que tal hola que"
freq = contar_palabras(texto)
print(freq)             
print(mas_repetida(freq)) 
