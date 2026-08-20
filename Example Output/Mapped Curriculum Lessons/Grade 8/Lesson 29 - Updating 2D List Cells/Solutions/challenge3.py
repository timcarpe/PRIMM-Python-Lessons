stock = [["Pens", 10], ["Books", 6], ["Tape", 4]]
row = int(input("Stock row 0 to 2: "))
delivery = int(input("Delivery amount: "))
stock[row][1] = stock[row][1] + delivery
print("Updated record:", stock[row])
for item in stock:
    print(item[0], item[1])
