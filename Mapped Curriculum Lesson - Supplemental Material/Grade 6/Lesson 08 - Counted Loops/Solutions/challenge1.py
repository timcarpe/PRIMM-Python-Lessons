number = int(input("Which times table? "))
lines = int(input("How many lines? "))
for count in range(1, lines + 1):
    print(number, "x", count, "=", number * count)
