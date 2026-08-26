clubs = [["Art", 12], ["Chess", 18], ["Code", 15]]
row = int(input("Club row 0 to 2: "))
members_to_add = int(input("Members to add: "))

clubs[row][1] = clubs[row][1] + members_to_add

print("Updated record:", clubs[row])
print("All records:", clubs)
