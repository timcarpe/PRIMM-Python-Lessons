password = "open"
attempts = 0
guess = ""
while guess != password and attempts < 3:
    guess = input("Door code: ")
    attempts = attempts + 1
if guess == password:
    print("Door opened in", attempts, "tries.")
else:
    print("Door locked after", attempts, "tries.")
