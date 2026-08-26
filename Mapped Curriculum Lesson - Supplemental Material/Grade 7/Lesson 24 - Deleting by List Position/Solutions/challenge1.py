tasks = ["email", "design", "test", "publish"]
position = int(input("Completed position 0 to 3: "))
completed = tasks[position]
del tasks[position]

print("Completed:", completed)
print("Next:", tasks[0])
print("Remaining:", tasks)
