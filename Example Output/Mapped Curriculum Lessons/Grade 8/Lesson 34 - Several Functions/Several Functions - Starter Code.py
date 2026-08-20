def show_menu():
    print("1: double")
    print("2: square")
def double(number):
    return number * 2
def square(number):
    return number * number
show_menu()
choice = input("Choice: ")
value = int(input("Number: "))
if choice == "1":
    print("Result:", double(value))
else:
    print("Result:", square(value))
