running = True

while running == True:
    choice = input("1: greet, 0: leave: ")
    choice = choice.lower()
    if choice == "1":
        print("Hello!")
    elif choice == "0":
        running = False
    else:
        print("Choose 1 or 0.")

print("Menu closed.")
