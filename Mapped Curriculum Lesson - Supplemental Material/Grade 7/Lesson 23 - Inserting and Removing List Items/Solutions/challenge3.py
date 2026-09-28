runners = ["Ari", "Bao", "Cleo", "Dara"]
position = int(input("Reserve position 0 to 4: "))
reserve = input("Reserve name: ")
runners.insert(position, reserve)
leaving = input("Runner to remove: ")
runners.remove(leaving)
print("Runners:", runners)
