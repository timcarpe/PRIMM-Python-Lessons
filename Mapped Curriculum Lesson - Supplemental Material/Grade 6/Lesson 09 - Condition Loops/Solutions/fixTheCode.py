target = 7
attempts = 0
guess = 0
while guess != target and attempts < 3:
    guess = int(input("Guess 1 to 10: "))
    attempts = attempts + "1"
print("Finished in", attempts, "tries.")
