def show_records(records):
    for record in records:
        print(record[0], record[1])
def find_score(records, target):
    for record in records:
        if record[0] == target:
            return record[1]
    return -1
results = [["ari", 7], ["bao", 9], ["cleo", 8]]
show_records(results)
target = input("Name: ")
score = find_score(results, target)
if score == -1:
    print("Name not found.")
else:
    print("Score:", score)
