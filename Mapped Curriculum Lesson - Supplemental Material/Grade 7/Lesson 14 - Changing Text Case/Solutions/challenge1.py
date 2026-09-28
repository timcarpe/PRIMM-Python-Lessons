team = input("Team name: ")
team = team.lower()
typed_code = input("Team code: ")
code = typed_code.upper()
print("Team:", team)
if typed_code == code:
    print("Code format OK")
else:
    print("Code changed to", code)
