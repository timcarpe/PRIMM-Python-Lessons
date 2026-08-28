for round_number in range(1, 4):
    print("Warm-up round", round_number)
answer = ""
counter = 0
while answer != "done":
    answer = input("Type done to finish: ")
    counter = counter + 1
print("Answers entered:", counter)
