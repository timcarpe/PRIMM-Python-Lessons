clubs = [["Art", 12], ["Chess", 18], ["Code", 15]]
row = int(input("Club row 0 to 2: "))
print("Before:", clubs[row])
new_name = input("New club name: ")
new_members = int(input("New member count: "))
clubs[row][0] = new_name
clubs[row][1] = new_members
print("After:", clubs[row])
