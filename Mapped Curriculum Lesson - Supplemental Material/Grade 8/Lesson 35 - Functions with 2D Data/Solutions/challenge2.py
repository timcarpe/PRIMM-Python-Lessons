def total_members(records):
    total = 0
    for record in records:
        total = total + record[1]
    return total
clubs = [["art", 12], ["chess", 18], ["code", 15]]
for record in clubs:
    print(record[0])
print("Total members:", total_members(clubs))
