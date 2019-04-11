_author__ = 'HackMadrid'
# sucesion de fibonacci 

a=0
b=1
fib = []

print("Cuantas cifras de la secuencia de Fibonacci deseas?")
n = int(input())

i = 0
while i < n:
	fib.append(b)
	c = a + b
	a = b
	b = c
	i += 1

	print("n La secuencia es: %s" % (fib))