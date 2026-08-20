clubs = [["art", 12], ["chess", 18], ["code", 15]]
target = input("Club to update: ").lower()
found = False
for club in clubs:
    if club[0] == target:
        new_members = int(input("New members: "))
        club[1] = new_members
        print("Updated:", club)
        found = True
if found == False:
    print("Club not found.")
