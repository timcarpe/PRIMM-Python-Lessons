total = int(input("Starting amount: "))
saving = int(input("Weekly saving: "))
for week in range(1, 5):
    total = total + saving
    print("Week", week, "total:", total)
