def double(number):
    return number * 2
def square(number):
    return number * number
def half(number):
    return number / 2
print("1: double\n2: square\n3: half")
choice = input("Choice: ")
value = int(input("Number: "))
if choice == "1":
    print("Result:", double(value))
elif choice == "2":
    print("Result:", square(value))
elif choice == "3":
    print("Result:", half(value))
else:
    print("Invalid choice.")
