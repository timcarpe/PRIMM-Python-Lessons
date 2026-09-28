import random
minimum = int(input("Minimum: "))
maximum = int(input("Maximum: "))
target = random.randint(minimum, maximum)
guess = int(input("Your guess: "))
if guess == target:
    print("Correct")
else:
    print("The target was", target)
