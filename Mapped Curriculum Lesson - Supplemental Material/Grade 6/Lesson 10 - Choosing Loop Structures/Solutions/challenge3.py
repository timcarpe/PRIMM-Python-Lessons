for station in range(1, 5):
    print("Exercise station", station)
rating = -1
ratings = 0
while rating != 0:
    rating = int(input("Effort rating, or 0 to stop: "))
    if rating != 0:
        ratings = ratings + 1
print("Ratings recorded:", ratings)
