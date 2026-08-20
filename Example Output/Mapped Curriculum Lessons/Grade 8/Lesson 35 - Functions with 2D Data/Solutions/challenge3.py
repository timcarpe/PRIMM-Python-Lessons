def show_records(records):
    for record in records:
        print(record[0], record[1])
def find_score(records, target):
    for record in records:
        if record[0] == target:
            return record[1]
    return -1
def highest_score(records):
    highest = records[0][1]
    for record in records:
        if record[1] > highest:
            highest = record[1]
    return highest
results = [["ari", 7], ["bao", 9], ["cleo", 8]]
show_records(results)
target = input("Name: ").lower()
score = find_score(results, target)
if score == -1:
    print("Name not found.")
else:
    print("Score:", score)
print("Highest score:", highest_score(results))
