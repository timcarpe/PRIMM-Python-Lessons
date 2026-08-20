roster = []
team_size = int(input("Number of names: "))
for count in range(team_size):
    name = input("Name: ")
    roster.append(name)
position = int(input("Valid replacement position: "))
replacement = input("Replacement name: ")
roster[position] = replacement
print("Final roster:")
for name in roster:
    print(name)
