clubs = [["Art", 12], ["Chess", 18]]
name = input("New club: ")
members = int(input("Members: "))
new_club = [name, members]
clubs.append(new_club)
position = int(input("Delete row 0 to 2: "))
del clubs[position]
for club in clubs:
    print(club[0], club[1])
