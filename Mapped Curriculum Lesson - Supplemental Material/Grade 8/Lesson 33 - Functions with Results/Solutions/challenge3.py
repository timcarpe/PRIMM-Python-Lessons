def area(length, width):
    return length * width
length_1 = int(input("Room 1 length: "))
width_1 = int(input("Room 1 width: "))
length_2 = int(input("Room 2 length: "))
width_2 = int(input("Room 2 width: "))
total = area(length_1, width_1) + area(length_2, width_2)
print("Total area:", total)
