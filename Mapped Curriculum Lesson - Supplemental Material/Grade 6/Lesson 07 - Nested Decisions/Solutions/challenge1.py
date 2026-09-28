raining = input("Is it raining? yes/no: ")
if raining == "yes":
    wind = input("Wind strong/light/none: ")
    if wind == "strong":
        print("Wear a coat.")
    elif wind == "light":
        print("Take an umbrella.")
    else:
        print("A hood will do.")
else:
    print("No rain gear needed.")
