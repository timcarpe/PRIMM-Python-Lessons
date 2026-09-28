def show_records(records):
    for record in records:
        print(record[0], record[1], record[2])
def find_members(records, target):
    for record in records:
        if record[0] == target:
            return record[1]
    return -1
clubs = [["art", 12, "R1"], ["chess", 18, "R2"], ["code", 15, "R3"]]
show_records(clubs)
target = input("Club to find: ")
target = target.lower()
members = find_members(clubs, target)
if members == -1:
    print("Club not found.")
else:
    print("Members:", members)
