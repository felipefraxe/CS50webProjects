from cs50 import get_int

while True:
    height = get_int("Height (1-8): ")
    if 0 < height < 9:
        break
cl = 1
cg = height - 1

for i in range(height):
    for j in range(cg):
        print(" ", end="")
    
    for k in range(cl):
        print("#", end="")
    
    print(" " * 2, end="")

    for l in range(cl):
        print("#", end="")
    cg -= 1
    cl += 1
    print()