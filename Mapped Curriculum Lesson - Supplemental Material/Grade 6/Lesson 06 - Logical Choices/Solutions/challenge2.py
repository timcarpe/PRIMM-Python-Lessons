age = int(input("Enter your age: "))
has_ticket = input("Do you have a ticket? ")
has_adult = input("Is an adult with you? ")
if (age >= 12 and has_ticket == "yes") or has_adult == "yes":
    print("You may enter.")
else:
    print("Please check the entry rules.")
