heading = input("Poster heading: ")
instruction = input("Instruction: ")
total = len(heading) + len(instruction)
print(heading + "\n" + instruction)
print("Combined characters:", total)
if total > 20:
    print("Too long for the poster.")
