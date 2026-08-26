clubs = [["art", 12], ["chess", 18]]
target = "chess"
found = False
for club in clubs:
    if club[0] == target:
        print("Members:", club[1])
        found = True
if found == False:
    print("Club not found.")
