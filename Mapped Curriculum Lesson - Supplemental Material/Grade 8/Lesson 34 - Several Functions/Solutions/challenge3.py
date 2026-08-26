def show_menu():
    print("1: area, 2: perimeter")
def area(length, width):
    return length * width
def perimeter(length, width):
    return 2 * length + 2 * width
show_menu()
choice = input("Choice: ")
length = float(input("Length: "))
width = float(input("Width: "))
if choice == "1":
    print("Area:", area(length, width))
elif choice == "2":
    print("Perimeter:", perimeter(length, width))
else:
    print("Invalid choice.")
