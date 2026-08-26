def find_members(records, target):
    for record in records:
        if record[0] == target:
            return record[1]
    return -1

clubs = [["art", 12], ["chess", 18], ["code", 15]]
for record in clubs:
    print(record[0])

art_members = find_members(clubs, "art")
code_members = find_members(clubs, "code")

print("Art:", art_members)
print("Code:", code_members)
