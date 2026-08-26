def double(number):
    return number * 2
def triple(number):
    return number * 3
print("1: double\n2: triple")
choice = input("Choice: ")
value = int(input("Number: "))
if choice == "1":
    print("Result:", double(value))
else:
    print("Result:", triple(value))
