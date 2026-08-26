kit = ["coat", "water", "torch"]
new_item = input("Item to insert: ")
kit.insert(1, new_item)
print("After insert:", kit)
old_item = input("Existing item to remove: ")
kit.remove(old_item)
print("After remove:", kit)
