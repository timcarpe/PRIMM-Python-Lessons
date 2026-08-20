running = True
while running == True:
    choice = input("1: greet, 2: leave, 3: help: ")
    if choice == "1":
        print("Hello!")
    elif choice == "2":
        running = False
    elif choice == "3":
        print("Help: choose a number.")
    else:
        print("Choose 1, 2 or 3.")
print("Menu closed.")
