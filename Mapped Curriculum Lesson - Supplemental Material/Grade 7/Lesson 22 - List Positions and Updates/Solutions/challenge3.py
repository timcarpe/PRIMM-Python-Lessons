places = ["Park", "Museum", "Station"]
position = int(input("Place position 0 to 2: "))
new_place = input("New place: ")
places[position] = new_place
print("First stop:", places[0])
print("Updated places:", places)
