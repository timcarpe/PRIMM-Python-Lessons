temperature = int(input("Enter the temperature: "))
if temperature >= 30:
    print("Hot")
elif temperature >= 20:
    print("Warm")
elif temperature < 0:
    print("Freezing")
else:
    print("Cool")
