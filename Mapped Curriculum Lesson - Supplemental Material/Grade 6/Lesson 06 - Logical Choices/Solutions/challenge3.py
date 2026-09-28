age = int(input("Enter your age: "))
student = input("Are you a student? ")
if age < 16 or (student == "yes" and age <= 25):
    print("Discount price")
else:
    print("Full price")
