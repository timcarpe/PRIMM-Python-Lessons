def show_names(records):
    for record in records:
        print(record[0])
def find_members(records, target):
    for record in records:
        if record[0] == target:
            return record[1]
    return -1
clubs = [["art", 12], ["chess", 18], ["code", 15]]
show_names(clubs)
name = input("Club to find: ").lower()
members = find_members(clubs, name)
print("Search result:", members)
