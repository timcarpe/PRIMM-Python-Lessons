notes = []
note = input("Enter a note, or stop: ")
while note != "stop":
    notes.append(note)
    note = input("Enter a note, or stop: ")
print("Saved notes:")
for saved_note in notes:
    print(saved_note)
