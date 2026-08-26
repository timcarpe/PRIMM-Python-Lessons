has_card = input("Library card? yes/no: ")
if has_card == "yes":
    overdue = input("Overdue book? yes/no: ")
    if overdue == "yes":
        print("Return the overdue book first.")
    else:
        print("You may borrow a book.")
else:
    print("Apply for a library card.")
