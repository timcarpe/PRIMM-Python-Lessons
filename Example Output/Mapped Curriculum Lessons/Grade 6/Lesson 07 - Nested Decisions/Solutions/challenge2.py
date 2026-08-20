raining = input("Is it raining? yes/no: ")
if raining == "yes":
    windy = input("Is it windy? yes/no: ")
    if windy == "yes":
        print("Wear a coat.")
    else:
        print("Take an umbrella.")
else:
    sunny = input("Is it sunny? yes/no: ")
    if sunny == "yes":
        print("Take sunglasses.")
    else:
        print("No weather gear needed.")
