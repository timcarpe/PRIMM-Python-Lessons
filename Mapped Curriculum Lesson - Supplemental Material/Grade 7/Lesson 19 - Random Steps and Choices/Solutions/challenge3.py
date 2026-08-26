import random
activities = ["jumps", "turns", "steps"]
count = random.randrange(2, 13, 2)
activity = random.choice(activities)
print("Training prompt:", count, activity)
