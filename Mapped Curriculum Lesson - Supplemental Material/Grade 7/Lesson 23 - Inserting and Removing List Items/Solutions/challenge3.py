runners = ["Ari", "Bao", "Cleo", "Dara"]
position = int(input("Reserve position 0 to 4: "))
reserve = input("Reserve name: ")
runners.insert(position, reserve)
leaving = input("Existing name to remove: ")
runners.remove(leaving)
for runner in runners:
    print(runner)
