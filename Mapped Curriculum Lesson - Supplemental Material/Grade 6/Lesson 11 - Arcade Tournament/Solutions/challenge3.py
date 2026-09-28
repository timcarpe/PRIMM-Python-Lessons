name = input("Player name: ")
total = 0
rounds = 0
again = "yes"
while again == "yes" and rounds < 5:
    rounds = rounds + 1
    score = int(input("Score 0 to 10: "))
    total = total + score
    again = input("Another round? yes/no: ")
print("Rounds played:", rounds)
print("Total:", total)
if total >= 24:
    print(name, "earned Gold")
elif total >= 15:
    print(name, "earned Silver")
else:
    print(name, "earned Bronze")
