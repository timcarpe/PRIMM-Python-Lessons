queue = ["Ari", "Bao", "Cleo", "Dara"]
served = queue[0]
del queue[0]
print("Served:", served)
position = int(input("Cancel position 0 to 2: "))
del queue[position]
print("Queue:", queue)
