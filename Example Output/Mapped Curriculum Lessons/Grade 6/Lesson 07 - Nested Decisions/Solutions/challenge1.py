raining = input("Is it raining? yes/no: ")
if raining == "yes":
    windy = input("Is it windy? yes/no: ")
    if windy == "yes":
        print("Wear a waterproof coat.")
    else:
        print("Take an umbrella.")
else:
    print("No rain gear needed.")
