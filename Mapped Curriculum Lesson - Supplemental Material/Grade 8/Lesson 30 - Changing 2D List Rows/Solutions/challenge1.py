clubs = [["Art", 12], ["Chess", 18]]
new_club = ["Code", 15]
clubs.append(new_club)
clubs.insert(1, ["Music", 9])
removed = clubs[0]
del clubs[0]
clubs.append(removed)
print("Moved to end:", removed[0])
for club in clubs:
    print(club[0], club[1])
