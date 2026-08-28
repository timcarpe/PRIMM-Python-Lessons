supplies = ["pencil", "book", "tape"]
position = int(input("Position 0 to 2: "))
print("Old item:", supplies[position])
replacement = input("Replacement item: ")
supplies[position] = replacement
print("New item:", supplies[position])
second_position = int(input("Second position 0 to 2: "))
second_replacement = input("Second replacement item: ")
supplies[second_position] = second_replacement
print("Updated list:", supplies)
