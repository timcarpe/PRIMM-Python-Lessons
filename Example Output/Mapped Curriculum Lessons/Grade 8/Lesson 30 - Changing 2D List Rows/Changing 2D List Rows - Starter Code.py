clubs = [["Art", 12], ["Chess", 18]]
new_club = ["Code", 15]
clubs.append(new_club)
clubs.insert(1, ["Music", 9])
del clubs[0]
for club in clubs:
    print(club[0], club[1])
