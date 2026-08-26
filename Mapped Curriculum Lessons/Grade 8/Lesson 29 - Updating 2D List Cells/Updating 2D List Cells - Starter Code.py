clubs = [["Art", 12], ["Chess", 18], ["Code", 15]]
row = int(input("Club row 0 to 2: "))
new_members = int(input("New member count: "))
clubs[row][1] = new_members
print("Updated record:", clubs[row])
print("All records:", clubs)
