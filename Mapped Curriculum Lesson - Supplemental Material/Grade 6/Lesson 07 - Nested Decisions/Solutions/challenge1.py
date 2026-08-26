raining = input("Is it raining? yes/no: ")

if raining == "yes":
    wind_strength = input("Wind strength strong/light: ")
    if wind_strength == "strong":
        print("Wear a coat.")
    else:
        print("Take an umbrella.")
else:
    print("No rain gear needed.")
