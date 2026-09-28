slices = int(input("How many slices are there? "))
first_eaten = int(input("Slices eaten by the first friend: "))
second_eaten = int(input("Slices eaten by the second friend: "))
slices_left = slices - first_eaten - second_eaten
print("Slices left:", slices_left)
