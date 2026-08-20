for round_number in range(1, 4):
    print("Warm-up round", round_number)
answer = ""
attempts = 0
while answer != "done":
    answer = input("Type done to finish: ")
    attempts = attempts + 1
print("Answers entered:", attempts)
