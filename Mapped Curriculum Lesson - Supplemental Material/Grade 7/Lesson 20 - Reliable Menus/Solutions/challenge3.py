running = True
while running == True:
    choice = input("1: bus, 2: walk, 3: leave: ")
    if choice == "1":
        stop = input("Bus stop: ")
        print("Selected stop:", stop)
    elif choice == "2":
        print("Walking route selected.")
    elif choice == "3":
        running = False
    else:
        print("Choose 1, 2 or 3.")
print("Planner closed.")
