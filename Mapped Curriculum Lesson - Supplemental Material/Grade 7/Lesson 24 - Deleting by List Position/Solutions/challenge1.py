tasks = ["email", "design", "test", "publish"]
position = int(input("Completed position 0 to 2: "))
completed = tasks[position]
del tasks[position]
print("Completed:", completed)
print("Moved up:", tasks[position])
print("Remaining:", tasks)
