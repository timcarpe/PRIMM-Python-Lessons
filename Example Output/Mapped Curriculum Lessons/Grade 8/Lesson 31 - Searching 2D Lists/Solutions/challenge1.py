clubs = [["art", 12], ["chess", 18], ["code", 15]]
target = "code"
found = False
for club in clubs:
    if club[0] == target:
        print("Members:", club[1])
        found = True
if found == False:
    print("Club not found.")
