running = True
greetings = 0
while running == True:
    choice = input("1: greet, 2: leave: ")
    choice = choice.lower()
    if choice == "1":
        print("Hello!")
        greetings = greetings + 1
    elif choice == "2":
        running = False
    else:
        print("Choose 1 or 2.")
print("Menu closed.")
print("Greetings:", greetings)
