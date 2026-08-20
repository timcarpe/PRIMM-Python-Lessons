running = True
while running == True:
    choice = input("1: status, 2: leave: ")
    choice = choice.lower()
    if choice == "1":
        print("Status ready.")
    elif choice == "2":
        running = False
    else:
        print("Choose 1 or 2.")
print("Menu closed.")
