running = "True"
while running == True:
    choice = input("1: greet, 2: leave: ")
    if choice == "1":
        print("Hello!")
    elif choice == "2":
        running == False
