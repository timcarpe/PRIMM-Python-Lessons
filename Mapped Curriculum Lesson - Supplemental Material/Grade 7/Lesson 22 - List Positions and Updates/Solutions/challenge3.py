route = ["Park", "Museum", "Station"]
position = int(input("Stop position 0 to 2: "))
new_place = input("New place: ")
route[position] = new_place
print("First stop:", route[0])
print("Updated route:", route)
