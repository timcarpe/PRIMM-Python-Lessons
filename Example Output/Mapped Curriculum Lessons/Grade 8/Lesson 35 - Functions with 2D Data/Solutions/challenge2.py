def show_names(records):
    for record in records:
        print(record[0])
def total_members(records):
    total = 0
    for record in records:
        total = total + record[1]
    return total
clubs = [["art", 12], ["chess", 18], ["code", 15]]
show_names(clubs)
print("Total members:", total_members(clubs))
