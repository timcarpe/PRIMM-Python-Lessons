supplies = ["pencil", "book", "tape"]
first = int(input("First position 0 to 2: "))
second = int(input("Second position 0 to 2: "))
temp = supplies[first]
supplies[first] = supplies[second]
supplies[second] = temp
print("Updated list:", supplies)
