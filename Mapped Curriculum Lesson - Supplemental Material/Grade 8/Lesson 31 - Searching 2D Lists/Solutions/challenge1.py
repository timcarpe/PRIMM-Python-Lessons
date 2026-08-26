clubs = [["art", 12], ["chess", 18], ["code", 15]]
target = int(input("Member count to find: "))
found = False

for club in clubs:
    if club[1] == target:
        print("Club:", club[0])
        found = True

if found == False:
    print("Club not found.")
