schedule = [["Talk", 1], ["Quiz", 2], ["Demo", 3]]
position = int(input("Insert position 0 to 3: "))
event = input("Event: ")
room = int(input("Room: "))
schedule.insert(position, [event, room])
delete_position = int(input("Delete position 0 to 3: "))
del schedule[delete_position]
for row in schedule:
    print(row[0], row[1])
