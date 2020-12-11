from cs50 import get_int

while True:
    height = get_int("Height(1-8): ")
    if 0 < height < 9:
        break
    
c = height - 1
for i in range(height):
    for j in range(c, 0, -1):
        print(" ", end="")
    print("#" * (i + 1))
    c -= 1