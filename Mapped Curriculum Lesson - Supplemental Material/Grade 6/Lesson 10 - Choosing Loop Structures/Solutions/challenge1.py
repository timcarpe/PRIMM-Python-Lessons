rounds = int(input("How many warm-up rounds? "))
for round_number in range(1, rounds + 1):
    print("Warm-up round", round_number)
answer = ""
while answer != "done":
    answer = input("Type done to finish: ")
print("Session complete.")
