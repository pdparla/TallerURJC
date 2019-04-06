_author__ = 'HackMadrid'
# maths

# suma
print("suma 4 + 9")
suma = 4 + 9
print(suma)
print("--------\n")

# multiplicacion
print("producto 5 * 5")
mult = 5*5
print(mult)
print("--------\n")
breakpoint();
# area triangulo
print("area de un triangulo")
b=12
h=8
area = (b*h)/2
print(area)
print("--------\n")

# area rectangulo
print("area de un rectangulo")
def rect(ancho, largo):
	print(ancho*largo)
rect(ancho=6, largo =6)
print("--------\n")

# area de un cilindro
print("area de un cilindro")
import math
ra=int(input("ingresa radio\n"))
ha=int(input("ingresa altura\n"))
areal=2*math.pi*ra*(ra+ha)
print(str(areal))
print("--------\n")
