i = 1
while i <= 4:
    print(i, i ** 2)
    i += 1

print("\n")

for i in range(1, 10):
    if i == 3:
        print("Это тройка")
        break
    print(i)

prevN = 0
nextN = 1
while True:
    fibN = nextN + prevN
    print(fibN)
    prevN = nextN
    nextN = fibN
    if fibN > 100:
        break
    