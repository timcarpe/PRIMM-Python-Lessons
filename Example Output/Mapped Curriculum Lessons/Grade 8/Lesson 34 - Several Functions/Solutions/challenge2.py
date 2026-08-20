def show_menu():
    print("1: double, 2: square, 3: half")
def double(number):
    return number * 2
def square(number):
    return number * number
def half(number):
    return number / 2
show_menu()
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
