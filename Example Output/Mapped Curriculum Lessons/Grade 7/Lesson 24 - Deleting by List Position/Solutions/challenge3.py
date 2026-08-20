queue = ["Ari", "Bao", "Cleo", "Dara"]
position = int(input("Cancel position 0 to 3: "))
cancelled = queue[position]
del queue[position]
print("Cancelled:", cancelled)
number = 0
for name in queue:
    print(number, name)
    number = number + 1
