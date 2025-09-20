def mas_repetido(lista):
    return max(set(lista), key=lista.count)

print(mas_repetido([1,2,3,2,4,2,5,3,3,3])) 
