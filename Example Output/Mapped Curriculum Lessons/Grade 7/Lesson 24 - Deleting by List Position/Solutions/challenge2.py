tasks = ["email", "design", "test", "publish"]
first_position = int(input("First position 0 to 3: "))
first_completed = tasks[first_position]
del tasks[first_position]
second_position = int(input("Second position 0 to 2: "))
second_completed = tasks[second_position]
del tasks[second_position]
print("Completed:", first_completed, second_completed)
print("Remaining:", tasks)
