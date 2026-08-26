number = int(input("Which times table? "))
start = int(input("Starting multiplier? "))
for count in range(start, start + 5):
    print(number, "x", count, "=", number * count)
