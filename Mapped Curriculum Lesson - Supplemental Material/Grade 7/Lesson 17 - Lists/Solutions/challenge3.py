guests = []
guest = input("Guest name: ")
guests.append(guest)
guest = input("Guest name: ")
guests.append(guest)
guest = input("Guest name: ")
guests.append(guest)
plus_one = input("Is a plus-one coming? ")
if plus_one == "yes":
    guests.append("Plus one")
print("Guests:", guests)
