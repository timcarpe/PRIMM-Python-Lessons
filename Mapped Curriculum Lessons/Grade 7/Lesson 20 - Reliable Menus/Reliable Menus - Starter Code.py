running = True
while running == True:
    choice = input("1: greet, 2: leave: ")
    choice = choice.lower()
    if choice == "1":
        print("Hello!")
    elif choice == "2":
        running = False
    else:
        print("Choose 1 or 2.")
print("Menu closed.")
