def show_menu():
    print("1: double")
    print("2: triple")
def double(number):
    return number * 2
def triple(number):
    return number * 3
show_menu()
choice = input("Choice: ")
value = int(input("Number: "))
if choice == "1":
    print("Result:", double(value))
else:
    print("Result:", triple(value))
