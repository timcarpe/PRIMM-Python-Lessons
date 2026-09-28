target = 7
attempts = 0
guess = 0
while guess != target and attempts < 3:
    guess = int(input("Guess 1 to 10: "))
    attempts = attempts + 1
    if guess < target:
        print("Too low")
    elif guess > target:
        print("Too high")
print("Finished in", attempts, "tries.")
