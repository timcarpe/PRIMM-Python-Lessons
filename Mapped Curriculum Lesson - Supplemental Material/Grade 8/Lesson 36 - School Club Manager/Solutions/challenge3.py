def show_records(records):
    for record in records:
        print(record[0], record[1], record[2])
def find_members(records, target):
    for record in records:
        if record[0] == target:
            return record[1]
    return -1
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
running = True
while running == True:
    choice = input("1: show, 2: search, 3: add, 4: update, 5: exit: ")
    if choice == "1":
        show_records(clubs)
    elif choice == "2":
        target = input("Club to find: ")
        target = target.lower()
        members = find_members(clubs, target)
        if members == -1:
            print("Club not found.")
        else:
            print("Members:", members)
    elif choice == "3":
        add_record(clubs)
    elif choice == "4":
        target = input("Club to update: ")
        target = target.lower()
        new_members = int(input("New member count: "))
        if update_members(clubs, target, new_members) == True:
            print("Club updated.")
        else:
            print("Club not found.")
    elif choice == "5":
        running = False
    else:
        print("Choose a valid option.")
print("Final record count:", len(clubs))
