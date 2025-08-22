import math

cat1 = int(input("ingrese el cateto 1:"))
cat2 = int(input("ingrese el cateto 2:"))
hipotenusa = math.hypot(cat1, cat2)
print(f"La hipotenusa es: {hipotenusa}")