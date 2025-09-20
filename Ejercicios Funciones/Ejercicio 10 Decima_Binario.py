def decimal_a_binario(n):
    return bin(n).replace("0b", "")

def binario_a_decimal(b):
    return int(b, 2)

# Ejemplo
print(decimal_a_binario(10))  
print(binario_a_decimal("1010")) 
