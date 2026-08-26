target = 7
attempts = 0
guess = 0
while guess != target and attempts < 5:
    guess = int(input("Guess 1 to 10: "))
    attempts = attempts + 1
print("You used", attempts, "tries.")
