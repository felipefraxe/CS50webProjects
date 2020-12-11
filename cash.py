from cs50 import get_float

while True:
    change = get_float("Change owned: $")
    if change > 0:
        break

coins = 0
change = round(change * 100)
while change > 0:
    if change >= 25:
        change -= 25
    elif change >= 10:
        change -= 10
    elif change >= 5:
        change -= 5
    else:
        change -= 1
    coins += 1
print(f"{coins}")