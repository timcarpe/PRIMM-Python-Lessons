supplies = ["pencil", "book", "tape"]
position = int(input("Position to replace 0 to 2: "))
replacement = input("Replacement item: ")
supplies[position] = replacement
check_position = int(input("Position to check 0 to 2: "))
print("Selected item:", supplies[check_position])
print("Updated list:", supplies)
