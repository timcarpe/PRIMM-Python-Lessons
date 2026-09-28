name = input("Player name: ")
total = int(input("Total score 0 to 30: "))
if total >= 24:
    print(name, "earned Gold")
elif total >= 15:
    print(name, "earned Silver")
else:
    print(name, "earned Bronze")
