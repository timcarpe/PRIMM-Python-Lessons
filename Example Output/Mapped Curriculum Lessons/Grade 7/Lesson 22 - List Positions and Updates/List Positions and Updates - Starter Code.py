supplies = ["pencil", "book", "tape"]
position = int(input("Position 0 to 2: "))
print("Old item:", supplies[position])
replacement = input("Replacement item: ")
supplies[position] = replacement
print("Updated list:", supplies)
