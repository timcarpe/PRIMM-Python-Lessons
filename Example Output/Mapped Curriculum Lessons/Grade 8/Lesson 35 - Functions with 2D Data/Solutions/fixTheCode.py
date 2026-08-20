def find_members(records, target):
    for record in records:
        if record == target:
            return record[1]
        return -1
clubs = [["art", 12], ["chess", 18]]
print(find_members("chess"))
