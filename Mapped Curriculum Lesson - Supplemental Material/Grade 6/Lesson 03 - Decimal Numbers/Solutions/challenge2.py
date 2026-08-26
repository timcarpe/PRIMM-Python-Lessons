distance = float(input("Enter kilometres: "))
travel_minutes = float(input("Enter travel minutes (not 0): "))
rest_minutes = float(input("Enter rest minutes: "))
speed = distance / travel_minutes
total_minutes = travel_minutes + rest_minutes
print("Kilometres per minute:", speed)
print("Total minutes:", total_minutes)
