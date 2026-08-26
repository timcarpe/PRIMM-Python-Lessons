def double(number):
    return number * 2
def square(number):
    return number * number
print("1: double\n2: square")
choice = input("Choice: ")
value = int(input("Number: "))
if choice == "1":
    print("Result:", double(value))
else:
    print("Result:", square(value))
