menu = [["tea", 2], ["cake", 3], ["soup", 5]]
item = input("Item: ")
quantity = int(input("Quantity: "))
found = False
for row in menu:
    if row[0] == item:
        print("Cost:", row[1] * quantity)
        found = True
if found == False:
    print("Item not found.")
