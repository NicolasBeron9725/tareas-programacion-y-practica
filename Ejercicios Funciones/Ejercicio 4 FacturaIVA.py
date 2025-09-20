def factura_total(cantidad, iva=21):
    return cantidad * (1 + iva / 100)

print(factura_total(100))
print(factura_total(100, 10))
