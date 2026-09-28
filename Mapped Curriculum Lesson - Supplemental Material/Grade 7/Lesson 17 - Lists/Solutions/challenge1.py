item = input("Pack one item: ")
packing_list = ["water", "map"]
packing_list.append(item)
overnight = input("Is the trip overnight? ")
if overnight == "yes":
    packing_list.append("sleeping bag")
print("Packing list:", packing_list)
