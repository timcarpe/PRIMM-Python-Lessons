password = "open"
attempts = 0
guess = ""
while guess != password and attempts < 3:
    guess = input("Door code: ")
    attempts = attempts + 1
if guess == password:
    print("Door opened. Attempts used:", attempts)
else:
    print("Door locked. Attempts used:", attempts)
