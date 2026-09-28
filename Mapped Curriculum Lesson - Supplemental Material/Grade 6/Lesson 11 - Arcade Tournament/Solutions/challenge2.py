name = input("Player name: ")
total = 0
for round_number in range(1, 4):
    print("Round", round_number)
    score = int(input("Score 0 to 10: "))
    total = total + score
print("Total:", total)
if total >= 24:
    print(name, "earned Gold")
elif total >= 15:
    print(name, "earned Silver")
else:
    print(name, "earned Bronze")
