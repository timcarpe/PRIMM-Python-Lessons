import random
entrants = []
for count in range(3):
    name = input("Entrant name: ")
    name = name.strip()
    name = name.title()
    entrants.append(name)
winner = random.choice(entrants)
tokens = random.randint(1, 10)
print("Winner:", winner)
print("Bonus tokens:", tokens)
