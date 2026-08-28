for exercise in range(1, 5):
    print("Exercise", exercise)
score = -1
ratings = 0
while score != 0:
    score = int(input("Effort score, or 0 to stop: "))
    if score != 0:
        ratings = ratings + 1
print("Scores entered:", ratings)
