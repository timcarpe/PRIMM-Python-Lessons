import random
activities = ["jumps", "turns", "steps"]
for count in range(3):
    reps = random.randrange(2, 13, 2)
    activity = random.choice(activities)
    print("Training prompt:", reps, activity)
