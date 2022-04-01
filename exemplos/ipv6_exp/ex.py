a = [0,1,2,3,4,5]

print("Imprimindo quadrado da lista")
for x in a:
    print(x*x)

print("Imprimindo a lista menos o 3")
b = a
b.pop(3)
print(b)

print("Imprimindo a lista original")
print(a)
