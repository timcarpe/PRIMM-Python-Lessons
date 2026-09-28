def show_records(records):
    for record in records:
        print(record[0], record[1], record[2])
def add_record(records):
    name = input("Club name: ")
    name = name.lower()
    members = int(input("Members: "))
    room = input("Room: ")
    records.append([name, members, room])
def update_members(records, target, new_members):
    for record in records:
        if record[0] == target:
            record[1] = new_members
            return True
    return False
clubs = [["art", 12, "R1"], ["chess", 18, "R2"], ["code", 15, "R3"]]
add_record(clubs)
target = input("Club to update: ")
target = target.lower()
new_members = int(input("New member count: "))
if update_members(clubs, target, new_members) == True:
    print("Club updated.")
else:
    print("Club not found.")
show_records(clubs)
