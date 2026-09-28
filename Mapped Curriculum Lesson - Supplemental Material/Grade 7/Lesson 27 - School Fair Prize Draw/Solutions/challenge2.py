import random
entrants = []
for count in range(3):
    name = input("Entrant name: ")
    name = name.strip()
    name = name.title()
    entrants.append(name)
prizes = ["Teddy bear", "Book token", "Water bottle"]
position = int(input("Position to replace 0 to 2: "))
new_name = input("New name: ")
new_name = new_name.strip()
new_name = new_name.title()
entrants[position] = new_name
leaving = input("Who is leaving? ")
leaving = leaving.strip()
leaving = leaving.title()
entrants.remove(leaving)
winner = random.choice(entrants)
prize = random.choice(prizes)
tokens = random.randint(1, 10)
print("Winner:", winner)
print("Prize:", prize)
print("Bonus tokens:", tokens)
print("Entrants:", entrants)
