notes = []
for count in range(3):
    note = input("Enter a note: ")
    notes.append(note)
print("Saved notes:")
number = 1
for note in notes:
    print(number, note)
    number = number + 1
