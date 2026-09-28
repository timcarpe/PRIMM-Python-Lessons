survey = ["tea", "water", "tea", "juice"]
target = input("Drink to count: ")
count = 0
for drink in survey:
    if drink == target:
        count = count + 1
print(target, "appears", count, "times")
