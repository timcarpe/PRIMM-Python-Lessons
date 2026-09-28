import random
entrants = ["Ana", "Bao", "Cleo"]
prizes = ["Teddy bear", "Book token", "Water bottle"]
running = True
while running == True:
    choice = input("1: list, 2: add, 3: draw, 4: exit: ")
    if choice == "1":
        for entrant in entrants:
            print(entrant)
    elif choice == "2":
        name = input("New entrant: ")
        name = name.strip()
        name = name.title()
        entrants.append(name)
    elif choice == "3":
        print("Winner:", random.choice(entrants))
        print("Prize:", random.choice(prizes))
        print("Bonus tokens:", random.randint(1, 10))
    elif choice == "4":
        running = False
    else:
        print("Choose a valid option.")
print("Entrants remaining:", len(entrants))
